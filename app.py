#%%
# Basic 
import streamlit as st
import numpy as np
import pandas as pd
import os
# matplot related 
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.style
import matplotlib as mpl
import itertools
import copy
import random 

# Assign plotting style 
mpl.style.use('seaborn-pastel')
plt.rcParams["font.family"] = 'NanumBarunGothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10.
plt.rcParams['xtick.labelsize'] = 10.
plt.rcParams['ytick.labelsize'] = 10.
plt.rcParams['axes.labelsize'] = 13.
mpl.rcParams['figure.dpi'] = 300.
#plt.gcf().canvas.renderer.dpi = 300.

#%% Functions to use 
## %% Misc. funcs
here = "work"
def gen_dir(terminal, where=here):
    if where == "work": 
        base_dir = 'D:/'
    else:
        base_dir = 'C:/Users/anari/'
    
    github_dir = 'github/adp-kap_1/'
    return os.path.join(base_dir, github_dir, terminal)
## %% Load, Pivot, Massage
@st.cache
def loading_pkl_df(depth):
    depth2 = depth + '.pkl'
    df = pd.read_pickle(gen_dir(depth2))
    if depth == '광역': 
        df1 = df.stack(level=['광역']).reset_index()
    else:
        df1 = df.stack(level=['광역','시군구1']).reset_index()
    df1.drop(columns = ['index'], inplace=True)
    df1.rename(columns={'level_0': '월'}, inplace=True)
    return df1 
# %%
df_lv1 = loading_pkl_df('광역')
df_lv2 = loading_pkl_df('시군구1')


## %% Funcions 
def append_total(df, list_name): 
    list1 = df[list_name].unique().tolist()
    list2 = ["전체"]
    list2.extend(list1)
    return list2
## %% Post-processing
def pick_depth(df): 
    if "시군구1" in df.columns: 
        return "시군구1" 
    else: 
        return "광역"

def gen_mean_col(df):
    
    grouped = ['월']
    
    dff0 = df.groupby(grouped).apply( lambda x: (sum(x['20대이하'])+sum(x['30대']))/sum(x['합계']))
    dff0 = pd.DataFrame(dff0, columns=['평균 청년 구매율']).reset_index()
    dff1 = pd.merge(df, dff0, how='left', on=grouped)   
 
    return dff1

def gen_filtered_df(df, total_limit=20): 
    my_filter1 = (df['청년 구매율'].notna()) & (df['합계'] >= total_limit) 
    #df.loc[my_filter1]
    return df.loc[my_filter1]

##%% Visualization by locals
## Funcs

def draw_step(data, var_y, var_x="월", 
              alpha=0.15, linestyle="-", marker="o", 
              color="in data"):
    #fig, ax = plt.subplots(figsize=(10, 6))
    data.reset_index(inplace=True)
    
    if color == "in data":
        color = data['color'][0]    
    else:
        color = color 
    
    plt.step(data[var_x], data[var_y], where='mid', 
             linestyle=linestyle, linewidth=2.5, 
             color=color, alpha=alpha)     
    plt.plot(data[var_x], data[var_y], 
             lw=0 , marker=marker,
             color=color, alpha=alpha)   

def color_assign(df, selected, depth):
    color = plt.rcParams['axes.prop_cycle'].by_key()['color']
    df = df.assign(color='gray')    
    for q in range(len(selected)):
        df.loc[df[depth] == selected[q],'color'] = color[q]
    return df

## %%
def draw_grouped_step(
                df, 
                depth, 
                selected_region="no",
                figsize=(9,6)):

    fig, ax = plt.subplots(figsize=figsize)
    
    if selected_region == "no":
        selected = random.sample(list(df[depth].unique()),1)
    else: 
        selected = selected_region

    df = color_assign(df, selected, depth)
   
    for metro, group_data in df.groupby(depth):
        group_data = group_data.reset_index()
        draw_step(group_data, '청년 구매율')

    for metro, group_data in df.groupby(depth):
        group_data = group_data.reset_index()
        draw_step(group_data, '평균 청년 구매율', 
                  color="black", 
                  linestyle="--", alpha=0.1, marker=" ")

    for metro, group_data in df[df[depth].isin(selected)].groupby(depth):
        group_data = group_data.reset_index()
        draw_step(group_data, '청년 구매율', alpha=1)
    
    plt.xticks(np.arange(0,12, step=1))
    xlabels = [str(x+1)+'월' for x in range(0,12)]
    ax.set_xticklabels(xlabels)
    plt.ylabel('청년 구매율')
    
    dft=df.loc[df['월']==11][[depth,'청년 구매율']]
    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    ax2.set_yticks(dft['청년 구매율'])
    ax2.set_yticklabels(dft[depth], alpha=0.2)

    dft=df.loc[df['월']==11][[depth,'청년 구매율','color']]
    dft=dft[dft[depth].isin(selected)]
    
    for color, data in dft.groupby(['color']): 
        ax2 = ax.twinx()
        ax2.set_ylim(ax.get_ylim())
        ax2.set_yticks(data['청년 구매율'])
        ax2.set_yticklabels(data[depth], alpha=1, color="black", size=12)

    return plt.show() 
#plt.savefig(gen_dir('광역\youthrate.png', where='work'), dpi=300)
## %%
def draw_corr(df): 
    # corr
    my_depth = pick_depth(dft1)
    df_cor = df.groupby([my_depth])[['청년 구매율', '합계']].corr(method='kendall')
    df_cor = df_cor.loc[df_cor['합계'] != 1]['합계'].reset_index()[[my_depth, '합계']]
    df_cor.columns = [my_depth, '상관계수']
    df_cor = df_cor.sort_values(['상관계수'], ascending=True)

    fig, ax = plt.subplots(figsize=(9, 7))
    ax.barh(df_cor[my_depth], df_cor['상관계수'], align='center')
    ax.legend([r'Kendall $\tau$'])

## %%
def draw_step_selected(df, selected):   
    my_depth = pick_depth(df)
    return draw_grouped_step(df, depth=my_depth, selected_region=selected)    

# %%
st.title('남한 지역별 부동산 구매자 분석')
st.markdown("- 감정원 아파트 구매자 자료에 기반한다.")

option_1 = st.sidebar.selectbox(
    '광역 지역', append_total(df_lv1, "광역")
     )

df2 = df_lv2.loc[df_lv2['광역']==option_1]

option_2 = st.sidebar.selectbox(
    '시군구 level1', append_total(df2, "시군구1")
     )
#%%

if (option_1 == "전체") & (option_2 == "전체"): 
    st.subheader("기다리시게")


if (option_1 != "전체") & (option_2 == "전체"): 
    dft1 = gen_filtered_df(df_lv1, 20)
    dft2 = gen_mean_col(dft1) 
    draw_step_selected(dft2, selected=[option_1]) 
    st.subheader("월별 청년 구매비율 변화 (광역 기준)")
    st.pyplot()
    st.subheader("구매량과 청년 구매비율 (광역 기준)")
    draw_corr(dft2)
    st.pyplot()


if (option_1 != "전체") & (option_2 != "전체"): 
    dft1 = gen_filtered_df(df_lv2, 20)
    dft1 = dft1.loc[dft1['광역']==option_1]
    dft2 = gen_mean_col(dft1) 
    st.subheader("월별 청년 구매비율 변화")
    draw_step_selected(dft2, selected=[option_2]) 
    st.pyplot()
    st.subheader(st.markdown("Kendall $\tau$"))
    draw_corr(dft2)
    st.pyplot()
