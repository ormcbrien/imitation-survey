import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import imitationSurvey as imsu
import random
import os
import yaml

with open('imsu_config.yaml') as f:
	config_settings = yaml.load(f)

"""
Stages of generating imitation survey:

1. Read interpolated lightcurve data and inflate to random redshift
2. Define survey duration, observational limitations and recover 'detection' days from cadence
3. 

"""

print('')
print('# Generating imitation survey')
print('#')
print('# Stage 1 - Distribute kilonova sample across given redshift range')


"""
STAGE 1 = 'Inflate' interpolated lightcurves to random redshift
"""

print('\nReading c and o interpolated lightcurves')
interpolated_c = pd.read_csv('kilonova_data/interpolated_lc_cyan.csv')
interpolated_o = pd.read_csv('kilonova_data/interpolated_lc_orange.csv')

# fig_interp_c = imsu.plotInterpolatedLightcurve(interpolated_c, colour = 'cyan')
# fig_interp_o = imsu.plotInterpolatedLightcurve(interpolated_o, colour = 'orange')

print('\nSampling redshift range to distribute events across')
redshift = [random.uniform(config_settings['lower_redshift'], config_settings['upper_redshift']) for i in range(0, config_settings['number_of_kilonovae'])]
# print(redshift)

print('\nCreating directory for inflated lightcurves in c')
if not os.path.exists('kilonova_data/inflated_lc_cyan'):
	os.mkdir('kilonova_data/inflated_lc_cyan')

print('\nCreating directory for inflated lightcurves in o')
if not os.path.exists('kilonova_data/inflated_lc_orange'):
	os.mkdir('kilonova_data/inflated_lc_orange')

print('\nInflating lightcurves to given redshift and saving in created directories')
for i in range(0, config_settings['number_of_kilonovae']):

	inflated_lc_c = imsu.inflateLightcurve(interpolated_c, redshift[i])
	inflated_lc_o = imsu.inflateLightcurve(interpolated_o, redshift[i])
	
	if i < 10:
	
		inflated_lc_c.to_csv('kilonova_data/inflated_lc_cyan/kilonova_0000%d.csv' %i, index = False)
		inflated_lc_o.to_csv('kilonova_data/inflated_lc_orange/kilonova_0000%d.csv' %i, index = False)

	elif i >= 10 and i < 100:
	
		inflated_lc_c.to_csv('kilonova_data/inflated_lc_cyan/kilonova_000%d.csv' %i, index = False)
		inflated_lc_o.to_csv('kilonova_data/inflated_lc_orange/kilonova_000%d.csv' %i, index = False)

	elif i >= 100 and i < 1000:
	
		inflated_lc_c.to_csv('kilonova_data/inflated_lc_cyan/kilonova_00%d.csv' %i, index = False)
		inflated_lc_o.to_csv('kilonova_data/inflated_lc_orange/kilonova_00%d.csv' %i, index = False)

	elif i >= 1000 and i < 10000:
	
		inflated_lc_c.to_csv('kilonova_data/inflated_lc_cyan/kilonova_0%d.csv' %i, index = False)
		inflated_lc_o.to_csv('kilonova_data/inflated_lc_orange/kilonova_0%d.csv' %i, index = False)

print('\nCreating directory to keep survey paramter information')
if not os.path.exists('survey'):
	os.mkdir('survey')

print('\nGenerating kilonova sample meta-data (kilonova number and associated redshift and explosion epoch relative to survey timeline)')
kn_number_count = np.array([i for i in range(0, config_settings['number_of_kilonovae'])])
expl_epochs = random.sample(range(config_settings['archive_start'], config_settings['archive_end']), config_settings['number_of_kilonovae'])

pd.DataFrame({'kn_number': kn_number_count, 'redshift': redshift, 'expl_epoch': expl_epochs}).to_csv('archive_survey/kn_sample_data.csv', index = False)

# """
# STAGE 2 = Recover detection days for duration survey is run
# """
# 
# print('')
# print('# Generating imitation survey')
# print('#')
# print('# Stage 2 - Generate survey timeline and determine observational losses')
# 
# 
# survey_duration = config_settings['survey_duration'] # days
# cadence = config_settings['survey_cadence'] # days
# print('\nSetting survey duration to %f days with cadence %f days' %(survey_duration, cadence))
# survey_timeline = np.arange(0, survey_duration, cadence)
# 
# weather_loss = config_settings['weather_loss']
# tech_loss = config_settings['tech_loss']
# 
# total_fractional_loss = weather_loss + tech_loss
# print('\nSetting loss factors as %f per cent for weather loss and %f per cent for technical issues' %(weather_loss*100, tech_loss*100))
# 
# print('\nConstructing illustration to show losses out of total survey timeline...')
# plt.figure(figsize = (16,6))
# plt.plot(survey_timeline, np.zeros(len(survey_timeline)), marker = 'o', ls = 'None', color = 'black', label = 'total')
# 
# 
# # LOSS MECHANISMS
# # - weather
# # - technical difficulties
# # - moon
# # - solar conjunction
# 
# print('\nRemoving epochs due to fractional loss (i.e. weather and technical faults)')
# survey_timeline = imsu.getFractionalLoss(survey_timeline, fraction_loss = total_fractional_loss)
# plt.plot(survey_timeline, np.zeros(len(survey_timeline))+1, marker = 'o', ls = 'None', color = 'blue', label = 'fractional')
# 
# print('\nRemoving epochs based on proximity to the moon')
# survey_timeline = imsu.getMoonLoss(survey_timeline, moon_window = config_settings['moon_window'])
# plt.plot(survey_timeline, np.zeros(len(survey_timeline))+2, marker = 'o', ls = 'None', color = 'grey', label = 'moon')
# 
# print('\nLoss plot output...')
# plt.legend(frameon = False, loc = 'upper center', ncol = 3)
# plt.yticks([])
# plt.ylim([-0.1, 2.2])
# plt.show()
# 
# if not os.path.exists('survey'):
# 	os.mkdir('survey')
# 
# print('\nOutputting survey timeline')
# pd.DataFrame({'survey_timeline': survey_timeline}).to_csv('survey/survey_timeline.csv', index = False)

print('')
print('# Generating imitation survey')
print('#')
print('# Tasks complete')
print('# Please run generateUniverse.py next')
print('')

