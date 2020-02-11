# %% import & basic params 
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

# Global Parameters 

here = "home"
# %% Misc. funcs
def gen_dir(terminal, where=here):
    if where == "work": 
        base_dir = 'D:/'
    else:
        base_dir = 'C:/Users/anari/'
    
    github_dir = 'github/adp-kap_1/'
    return os.path.join(base_dir, github_dir, terminal)
## %% Load, Pivot, Massage
def loading_group_df(depth):
    depth2 = depth + '.pkl'
    df = pd.read_pickle(gen_dir(depth2))
    if depth == '광역': 
        df1 = df.stack(level=['광역']).reset_index()
    else:
        df1 = df.stack(level=['광역','시군구1']).reset_index()
    df1.drop(columns = ['index'], inplace=True)
    df1.rename(columns={'level_0': '월'}, inplace=True)
    return df1 
#
## %%
df_lv1 = loading_group_df('광역')
df_lv2 = loading_group_df('시군구1')
# %%


# %%
## Visualization by locals
## Funcs

def gen_filtered_df(gwangyuk, df, total_limit=20): 
    
    my_filter1 = (df['청년 구매율'].notna()) & (df['합계'] >= total_limit) 
    df = df.loc[my_filter1 & (df['광역'].isin(gwangyuk))]
    return df 

def draw_step(data, var_y, var_x="월", alpha=0.15):
    #fig, ax = plt.subplots(figsize=(10, 6))
    data.reset_index(inplace=True)
    color = data['color'][0]    
    plt.step(data[var_x], data[var_y], where='mid', 
             linewidth=2.5, color=color, alpha=alpha)     
    plt.plot(data[var_x], data[var_y], lw=0 , color=color, marker = 'o', alpha=alpha)   

def color_assign(df, selected, depth):
    color = plt.rcParams['axes.prop_cycle'].by_key()['color']
    df = df.assign(color='gray')
    for q in range(len(selected)):
        df.loc[df[depth] == selected[q],'color'] = color[q]
    return df

def touch_fig(df):
#    
    plt.xticks(np.arange(0,12, step=1))
    xlabels = [str(x+1)+'월' for x in range(0,12)]
    ax.set_xticklabels(xlabels)
    plt.ylabel('청년 구매율')
    
    dft=df.loc[df['월']==11][['시군구1','청년 구매율']]
    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    ax2.set_yticks(dft['청년 구매율'])
    ax2.set_yticklabels(dft['시군구1'], alpha=0.2)

    dft=df.loc[df['월']==11][['시군구1','청년 구매율']]
    dft=dft[dft['시군구1'].isin(selected)]
    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    ax2.set_yticks(dft['청년 구매율'])
    ax2.set_yticklabels(dft['시군구1'], alpha=1)
#%%

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

    dft=df.loc[df['월']==11][[depth,'청년 구매율']]
    dft=dft[dft[depth].isin(selected)]
    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    ax2.set_yticks(dft['청년 구매율'])
    ax2.set_yticklabels(dft[depth], alpha=1)

    return plt.show() 
#plt.savefig(gen_dir('광역\youthrate.png', where='work'), dpi=300)
# %%
def draw_corr(df, my_gwangyuk=["서울"]): 
    # %% Custom filters 
    my_filter1 = (df['청년 구매율'].notna())  
    my_filter2 = my_filter1 & (df1['광역'].isin(my_gwangyuk)) 
    df = df.loc[my_filter2]
    # corr
    df_cor = df.groupby(['시군구1'])[['청년 구매율', '합계']].corr(method='kendall')
    df_cor.reset_index(inplace=True)
    df_cor = df_cor.loc[(df_cor['합계'].notna())]
    df_cor = df_cor[df_cor['level_1'] == "청년 구매율"][['시군구1', '합계']]
    df_cor.columns = ['시군구', '상관계수']
    df_cor.sort_values(['상관계수'], ascending=False)
    df2 = df_cor.sort_values(['상관계수'])

    fig, ax = plt.subplots(figsize=(9, 7))
    ax.barh(df2['시군구'], df2['상관계수'], align='center')
    ax.legend([r'Kendall $\tau$'])

# %%
draw_corr(df1, ["광주"])
# %%
def draw_step_wrapper(df, gwangyuk, sigungu):
   
    if sigungu=="ALL":
        return draw_grouped_step(df, depth=gwangyuk)
    else: 
        df = df.loc[df['광역']==gwangyuk]
        return draw_grouped_step(df, depth=sigungu)
    return df 
    #return draw_step(df, depth='시군구1')

# %%
dft = df_lv2.loc[df_lv2['광역']=='서울']
draw_grouped_step(dft, '시군구1')
# %%
dft = df_lv1
draw_grouped_step(dft, '광역') 

#%%
def tmpfunc(df, depth):
    df.drop(columns=[depth, '청년 구매율'], inplace=True)
    df1 = df.sum(axis = 0)    
    df1['청년 구매율'] = (df1['20대이하']+df1['30대']) / df1['합계']
    df1[depth] = "평균"
    return df1

dft2 = dft.groupby(['월']).apply(tmpfunc, depth='광역')
test = pd.DataFrame(dft2[['광역', '청년 구매율']]).reset_index()
test
# %%
