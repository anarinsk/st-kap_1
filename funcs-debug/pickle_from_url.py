
# %% import 
import numpy as np 
import pandas as pd 
import os
import pickle 


# %%
#%% to write pickle, use orthodox method 
import pickle
filehandler = open(b"gwang_2.pkl","wb")
pickle.dump(tdf2,filehandler)
filehandler.close()

#%% to check 
import pickle
file = open("gwang_2.pkl",'rb')
tdf3 = pickle.load(file)

#%%
from urllib.request import urlopen

#url = "https://github.com/anarinsk/st-kap_1/blob/master/sigun_2.pkl?raw=true"
url = "https://github.com/anarinsk/st-kap_1/blob/master/gwang_2.pkl?raw=true"
url2 = urlopen(url)
tdf3 = pickle.load(url2)
tdf3
# %%