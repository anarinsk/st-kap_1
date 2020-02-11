#%%
df_lv1

#%%
def gen_mean_col(df):
    if "시군구1" in df.columns: 
        grouped = ['광역', '월']
    else: 
        grouped = ['월']
    
    dff0 = df.groupby(grouped).apply( lambda x: sum((x['20대이하']+x['30대'])/x['합계']))
    dff0 = pd.DataFrame(dff0, columns=['평균 청년 구매율']).reset_index()
    dff1 = pd.merge(df, dff0, how='left', on=grouped)   
 
    return dff1

df1 = gen_mean_col(df_lv2)
df1

# %%
