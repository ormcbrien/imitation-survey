import imitationSurvey as imsu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
Stages of setting up imitation survey:

1. Generate absolute magnitude lightcurve of AT2017gfo in ATLAS-c and ATLAS-o
2. Interpolate lightcurve via spline/polynomial fitting

"""

print('')
print('# Setting up imitation survey')
print('#')
print('# Stage 1 - Generating absolute magnitude kilonova lightcurve')

"""
STAGE 1 = Generate absolute magnitude lightcurve
"""

print('\nReading kilonova data file')
obj_data = pd.read_csv('kilonova_data/app_AT2017gfo_co.csv')

print('\nMaking apparent magnitude plot')
fig_app = imsu.plotLightcurve(obj_data)
plt.show(fig_app)

print('\nConverting magnitudes to absolute space and outputting to file')
obj_data_abs = imsu.getAbsoluteLightcurve(obj_data)
obj_data_abs.to_csv('kilonova_data/abs_AT2017gfo_co.csv', index = False)
# print(obj_data_abs)

print('\nMaking absolute magnitude plot')
fig_abs = imsu.plotLightcurve(obj_data_abs, showLimits = False)
plt.show(fig_abs)

"""
STAGE 2 = Fit spline/polynomial to lightcurve to interpolate
"""

print('')
print('# Setting up imitation survey')
print('#')
print('# Stage 2 - Interpolate absolute lighcurve and extrapolate to higher temporal resolution')

print('\nSpline fitting lightcurves')
interp_c, interp_o = imsu.fitLightcurve(obj_data_abs, spline_kind = 'cubic')

obj_data_abs_trunc = obj_data.dropna(axis = 0, how = 'any')
interp_mjd = np.arange(np.nanmin(obj_data_abs_trunc['mjd']), np.nanmax(obj_data_abs_trunc['mjd']), 1, dtype = int)

print('\nSeparating c and o band data')
mag_interp_c = interp_c(interp_mjd)
mag_interp_o = interp_o(interp_mjd)

# plt.plot(interp_mjd, mag_interp_c, ls = '-', color = 'cyan')
# plt.plot(interp_mjd, mag_interp_o, ls = '-', color = 'orange')
# plt.show()

print('\nOutputting c and o interpolated lightcurves to separate files')
pd.DataFrame({'mjd': interp_mjd - np.nanmin(interp_mjd), 'interp_mag': mag_interp_c}).to_csv('kilonova_data/interpolated_lc_cyan.csv', index = False)
pd.DataFrame({'mjd': interp_mjd - np.nanmin(interp_mjd), 'interp_mag': mag_interp_o}).to_csv('kilonova_data/interpolated_lc_orange.csv', index = False)


print('')
print('# Setting up imitation survey')
print('#')
print('# Tasks completed')
print('# Please run generateImitationSurvey.py next')

