import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import imitationSurvey as imsu
import random
import os

"""
Stages of generating imitation survey:

1. Read interpolated lightcurve data and inflate to random redshift
2. Define survey duration, observational limitations and recover 'detection' days from cadence
3. 

"""

"""
STAGE 1 = 'Inflate' interpolated lightcurves to random redshift
"""

interpolated_c = pd.read_csv('kilonova_data/interpolated_lc_cyan.csv')
interpolated_o = pd.read_csv('kilonova_data/interpolated_lc_orange.csv')

fig_interp_c = imsu.plotInterpolatedLightcurve(interpolated_c, colour = 'cyan')
fig_interp_o = imsu.plotInterpolatedLightcurve(interpolated_o, colour = 'orange')

# plt.show(fig_interp_c)
# plt.show(fig_interp_o)

# redshift = random.uniform(0.0, 0.014)
redshift = [random.uniform(0.0, 0.014) for i in range(0,100)]
# print(redshift)

if not os.path.exists('kilonova_data/inflated_lc_cyan'):
	os.mkdir('kilonova_data/inflated_lc_cyan')
	
if not os.path.exists('kilonova_data/inflated_lc_orange'):
	os.mkdir('kilonova_data/inflated_lc_orange')

for i in range(0, len(redshift)):

	inflated_lc_c = imsu.inflateLightcurve(interpolated_c, redshift[i])
	inflated_lc_o = imsu.inflateLightcurve(interpolated_o, redshift[i])

	inflated_lc_c.to_csv('kilonova_data/inflated_lc_cyan/kilonova_%d.csv' %i)
	inflated_lc_o.to_csv('kilonova_data/inflated_lc_orange/kilonova_%d.csv' %i)

# fig_interp_c_inflate = imsu.plotInterpolatedLightcurve(inflated_lc_c, colour = 'cyan')
# fig_interp_o_inflate = imsu.plotInterpolatedLightcurve(inflated_lc_o, colour = 'orange')
# plt.show(fig_interp_c_inflate)
# plt.show(fig_interp_o_inflate)

"""
STAGE 2 = Recover detection days for duration survey is run
"""

survey_duration = 365 # days
cadence = 2 # days

survey_timeline = np.arange(0, survey_duration, cadence)




