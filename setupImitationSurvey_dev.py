import imitationSurvey as imsu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
Stages of setting up imitation survey:

1. Generate absolute magnitude lightcurve of AT2017gfo in ATLAS-c and ATLAS-o
2. Interpolate lightcurve via spline/polynomial fitting

"""

"""
STAGE 1 = Generate absolute magnitude lightcurve
"""

obj_data = pd.read_csv('kilonova_data/app_AT2017gfo_co.csv')
# print(obj_data)

# fig_app = imsu.plotLightcurve(obj_data)
# plt.show(fig_app)

obj_data_abs = imsu.getAbsoluteLightcurve(obj_data)
obj_data_abs.to_csv('kilonova_data/abs_AT2017gfo_co.csv')
# print(obj_data_abs)

# fig_abs = imsu.plotLightcurve(obj_data_abs, showLimits = False)
# plt.show(fig_abs)

"""
STAGE 2 = Fit spline/polynomial to lightcurve to interpolate
"""

interp_c, interp_o = imsu.fitLightcurve(obj_data_abs, spline_kind = 'cubic')

obj_data_abs_trunc = obj_data.dropna(axis = 0, how = 'any')
interp_mjd = np.linspace(np.nanmin(obj_data_abs_trunc['mjd']), np.nanmax(obj_data_abs_trunc['mjd']), 100)

mag_interp_c = interp_c(interp_mjd)
mag_interp_o = interp_o(interp_mjd)

# plt.plot(interp_mjd, mag_interp_c, ls = '-', color = 'cyan')
# plt.plot(interp_mjd, mag_interp_o, ls = '-', color = 'orange')
# plt.show()

pd.DataFrame({'mjd': interp_mjd - np.nanmin(interp_mjd), 'interp_mag': mag_interp_c}).to_csv('kilonova_data/interpolated_lc_cyan.csv')
pd.DataFrame({'mjd': interp_mjd - np.nanmin(interp_mjd), 'interp_mag': mag_interp_o}).to_csv('kilonova_data/interpolated_lc_orange.csv')


