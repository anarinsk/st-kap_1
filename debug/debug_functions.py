# %% Testing 광역 수준 
dft1 = gen_filtered_df(df_lv1, 20)
#dft1 = dft1.loc[dft1['광역']=="서울"]
dft2 = gen_mean_col(dft1) 

draw_step_selected(dft2, selected=["서울", "세종"]) 
draw_corr(dft2)
# %% Testing 시군구1 수준 
dft1 = gen_filtered_df(df_lv2, 20)
dft1 = dft1.loc[dft1['광역']=="서울"]
dft2 = gen_mean_col(dft1) 

draw_step_selected(dft2, selected=["은평구", "광진구"]) 
draw_corr(dft2)
# %%
