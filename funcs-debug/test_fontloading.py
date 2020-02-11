
#%%
import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np

#%%
fm.get_fontconfig_fonts()
font_location = './NanumBarunGothicLight.ttf' 
font_name = fm.FontProperties(fname=font_location).get_name()
matplotlib.rc('font', family=font_name)
#%%

#%%
t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2*np.pi*t)
plt.plot(t, s)

plt.xlabel('time (s)')
plt.ylabel('voltage (mV)')
plt.title('한글을 테스트하자! About as simple as it gets, folks')
plt.grid(True)
plt.savefig("test.png")
plt.show()


#%%
import os
print (os.getcwd())

# %%
