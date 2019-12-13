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

if not os.path.exists('survey'):
	os.mkdir('survey')
	
kn_number_count = np.array([i for i in range(0, 100)])
expl_epochs = random.sample(range(0, 365), 100)

pd.DataFrame({'kn_number': kn_number_count, 'redshift': redshift, 'expl_epoch': expl_epochs}).to_csv('survey/kn_sample_data.csv')

"""
STAGE 2 = Recover detection days for duration survey is run
"""

survey_duration = 365 # days
cadence = 2 # days

weather_loss = 0.3
tech_loss = 0.12

total_fractional_loss = weather_loss + tech_loss

survey_timeline = np.arange(0, survey_duration, cadence)

plt.figure(figsize = (16,6))
plt.plot(survey_timeline, np.zeros(len(survey_timeline)), marker = 'o', ls = 'None', color = 'black', label = 'total')


# LOSS MECHANISMS
# - weather
# - technical difficulties
# - moon
# - solar conjunction

survey_timeline = imsu.getFractionalLoss(survey_timeline, fraction_loss = total_fractional_loss)
plt.plot(survey_timeline, np.zeros(len(survey_timeline))+1, marker = 'o', ls = 'None', color = 'blue', label = 'fractional')

survey_timeline = imsu.getMoonLoss(survey_timeline, moon_window = 4)
plt.plot(survey_timeline, np.zeros(len(survey_timeline))+2, marker = 'o', ls = 'None', color = 'grey', label = 'moon')


plt.legend(frameon = False, loc = 'center right')
plt.show()

if not os.path.exists('survey'):
	os.mkdir('survey')

# print(survey_timeline)
pd.DataFrame({'survey_timeline': survey_timeline}).to_csv('survey/survey_timeline.csv')
