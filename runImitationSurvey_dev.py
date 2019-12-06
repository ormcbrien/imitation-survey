import imitationSurvey as imsu
import pandas as pd
import matplotlib.pyplot as plt

"""
Stages of imitation survey:

1. Generate absolute magnitude lightcurve of AT2017gfo in ATLAS-c and ATLAS-o
2. 

"""

"""
STAGE 1 = Generate absolute magnitude lightcurve
"""

obj_data = pd.read_csv('kilonova_data/AT2017gfo_co.txt')
# print(obj_data)

fig_app = imsu.plotLightcurve(obj_data)
plt.show(fig_app)

obj_data_abs = imsu.getAbsoluteLightcurve(obj_data)
print(obj_data_abs)

fig_abs = imsu.plotLightcurve(obj_data_abs, showLimits = False)
plt.show(fig_abs)