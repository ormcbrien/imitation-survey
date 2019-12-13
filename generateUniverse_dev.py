import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import imitationSurvey as imsu
import random
import os
import glob

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

"""
STAGE 0 = See the generated universe
"""

plt.figure(figsize = (16, 8))

survey_duration = 365

kilonova_files_c = sorted(glob.glob('kilonova_data/inflated_lc_cyan/*.csv'))
kilonova_files_o = sorted(glob.glob('kilonova_data/inflated_lc_orange/*.csv'))

kn_sample_data = pd.read_csv('survey/kn_sample_data.csv')
redshifts = kn_sample_data['redshift']
expl_epochs = kn_sample_data['expl_epoch']

for i in range(0, len(kilonova_files_c)):
	
	kilonova_data_c = pd.read_csv(kilonova_files_c[i])
	kilonova_data_o = pd.read_csv(kilonova_files_o[i])
	
	plt.plot(kilonova_data_c['mjd'] + expl_epochs[i], kilonova_data_c['interp_mag'], ls = '-', color = 'cyan', marker = 'None')
	plt.plot(kilonova_data_o['mjd'] + expl_epochs[i], kilonova_data_o['interp_mag'], ls = '-', color = 'orange', marker = 'None')

survey_timeline = pd.read_csv('survey/survey_timeline.csv')

for i in range(0, len(survey_timeline['survey_timeline'])):
	
	plt.axvline(survey_timeline['survey_timeline'][i], ls = '-', color = 'grey', alpha = 0.6)

plt.axhline(18.7, ls = '--', color = 'orange')
plt.axhline(19.3, ls = '--', color = 'cyan')

plt.xlabel('Time, days')
plt.ylabel('Apparent magnitude')

plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

"""
STAGE 1 = Choose sensitivity function
"""

doObservationFunc = 1

if doObservationFunc == 1:
	
	sens_func = pd.read_csv('atlas/limit_function_MLO.csv')
	print(sens_func)
	
elif doObservationFunc == 0:

	sens_func = pd.read_csv('survey/survey_timeline.csv')
	o_limit = np.full(len(sens_func['survey_timeline']), 18.7)
	c_limit = np.full(len(sens_func['survey_timeline']), 19.3)
	
	sens_func['c_limit'] = c_limit
	sens_func['o_limit'] = o_limit
	print(sens_func)	


"""
STAGE 2 = Recover detections
"""







