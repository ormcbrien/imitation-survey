import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import imitationSurvey as imsu
import random
import os
import glob
import yaml

with open('imsu_config.yaml') as f:
	config_settings = yaml.load(f)

SMALL_SIZE = 14
MEDIUM_SIZE = 18
BIGGER_SIZE = 25

plt.rc('font', size=SMALL_SIZE)          	# controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     	# fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    	# fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    	# fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    	# fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)    	# legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  	# fontsize of the figure title

plt.rcParams["font.family"] = "serif"
plt.rcParams['mathtext.fontset'] = 'dejavuserif'

"""
Stages of generating Universe for survey:

0. See the generated universe, including all kilonova lightcurves, the epochs of ATLAS 
1. Choose appropriate sensitivity function - observed, simulated
2. Recover kilonova detections during regular survey

"""

print('')
print('# Generating simulated universe')
print('#')
print('# Stage 0 - Display simulated universe, including kilonova sample across explosion epochs')

"""
STAGE 0 = See the generated universe
"""

plt.figure(figsize = (16, 8))

survey_duration = config_settings['survey_duration']

print('\nRead kilonova lightcurve directories')
kilonova_files_c = sorted(glob.glob('kilonova_data/inflated_lc_cyan/*.csv'))
kilonova_files_o = sorted(glob.glob('kilonova_data/inflated_lc_orange/*.csv'))

print('\nRead kilonova sample data file')
kn_sample_data = pd.read_csv('survey/kn_sample_data.csv')
redshifts = kn_sample_data['redshift']
expl_epochs = kn_sample_data['expl_epoch']

print('\nPlot kilonova lightcurve data')
for i in range(0, len(kilonova_files_c)):
	
	kilonova_data_c = pd.read_csv(kilonova_files_c[i])
	kilonova_data_o = pd.read_csv(kilonova_files_o[i])
	
	plt.plot(kilonova_data_c['mjd'] + expl_epochs[i], np.array(kilonova_data_c['interp_mag']), ls = '-', color = 'cyan', marker = 'None', label = None)
	plt.plot(kilonova_data_o['mjd'] + expl_epochs[i], np.array(kilonova_data_o['interp_mag']), ls = '-', color = 'orange', marker = 'None', label = None)

plt.plot([],[], ls = '-', color = 'cyan', marker = 'None', label = 'cyan lightcurves')
plt.plot([],[], ls = '-', color = 'orange', marker = 'None', label = 'orange lightcurves')

print('\nRead survey timeline')
survey_timeline = pd.read_csv('survey/survey_timeline.csv')

for i in range(0, len(survey_timeline['survey_timeline'])):
	
	plt.axvline(survey_timeline['survey_timeline'][i], ls = '-', color = 'grey', alpha = 0.6)

plt.plot([],[], ls = '-', color = 'grey', alpha = 0.6, label = 'survey timeline')

plt.xlabel('Time, days')
plt.ylabel('Apparent magnitude')

"""
STAGE 1 = Choose sensitivity function
"""

print('')
print('# Generating simulated universe')
print('#')
print('# Stage 1 - Add sensitivity function to plot')


print('\nUsing flat limit for both filters as sensitivty function')
sens_func = pd.read_csv('survey/survey_timeline.csv')
o_limit = np.full(len(sens_func['survey_timeline']), 18.7)
c_limit = np.full(len(sens_func['survey_timeline']), 19.3)

sens_func['c_limit'] = c_limit
sens_func['o_limit'] = o_limit

plt.axhline(19.3, ls = '--', color = 'cyan', label = 'cyan detection limit')
plt.axhline(18.7, ls = '--', color = 'orange', label = 'orange detection limit')

plt.gca().invert_yaxis()
plt.legend(frameon = False)
plt.tight_layout()
plt.show()

"""
STAGE 2 = Recover detections
"""
print('')
print('# Generating simulated universe')
print('#')
print('# Stage 2 - Recover detections based on survey timeline and sensitivity function')

# print(sens_func)

fig = plt.figure(figsize = (12,10))

print('\nIsolating survey timeline dates and sensitivty functions')
survey_timeline = np.array(sens_func['survey_timeline'])
# print(survey_timeline)
c_limit = np.array(sens_func['c_limit'])
o_limit = np.array(sens_func['o_limit'])

print('\nIdentifying overlap in kilonova lightcurve dates, and identify which of those are above detection limit')

if not os.path.exists('survey/recovered_detections_cyan'):
	os.mkdir('survey/recovered_detections_cyan')
	
if not os.path.exists('survey/recovered_detections_orange'):
	os.mkdir('survey/recovered_detections_orange')

for i in range(0, len(kilonova_files_c)):

	kilonova_data_c = pd.read_csv(kilonova_files_c[i])
	kilonova_data_o = pd.read_csv(kilonova_files_o[i])

	kilonova_data_c['mjd'] = kilonova_data_c['mjd'] + expl_epochs[i]
	kilonova_data_o['mjd'] = kilonova_data_o['mjd'] + expl_epochs[i]

	kilonova_mjd = np.array(kilonova_data_c['mjd'])
	kilonova_mag_c = np.array(kilonova_data_c['interp_mag'])
	kilonova_mag_o = np.array(kilonova_data_o['interp_mag'])

	mjd_overlap = np.intersect1d(survey_timeline, kilonova_mjd, return_indices = True)
	ind_mjd_overlap = mjd_overlap[2]
	mjd_overlap_keep = mjd_overlap[0]

	recovered_mags_c = kilonova_mag_c[ind_mjd_overlap]
	recovered_mags_o = kilonova_mag_o[ind_mjd_overlap]

	ind_c = np.where(recovered_mags_c <= c_limit[ind_mjd_overlap])
	ind_o = np.where(recovered_mags_o <= o_limit[ind_mjd_overlap])

	recovered_mags_c = recovered_mags_c[ind_c]
	recovered_mags_o = recovered_mags_o[ind_o]

	if len(recovered_mags_c) > 0:
		
		df_out = pd.DataFrame({'mjd_overlap': mjd_overlap_keep[ind_c], 'recovered_mag': recovered_mags_c}).to_csv('survey/recovered_detections_cyan/recovered_lc_c_%d.csv' %i, index = False)

		plt.plot(mjd_overlap_keep[ind_c], recovered_mags_c, marker = 'o', color = 'cyan', ls = '-', ms = 8, mfc = 'cyan', mec = 'black', mew = 0.75)
		
	elif len(recovered_mags_o) > 0:
	
		df_out = pd.DataFrame({'mjd_overlap': mjd_overlap_keep[ind_o], 'recovered_mag': recovered_mags_o}).to_csv('survey/recovered_detections_orange/recovered_lc_o_%d.csv' %i, index = False)
		
		plt.plot(mjd_overlap_keep[ind_o], recovered_mags_o, marker = 'o', color = 'orange', ls = '-', ms = 8, mfc = 'orange', mec = 'black', mew = 0.75)
	
	else:
	
		pass

print('\nRecovered detections have been output to files')

plt.xlabel('Survey timeline, days')
plt.ylabel('Apparent magnitude')

plt.tight_layout()
plt.gca().invert_yaxis()
plt.show()