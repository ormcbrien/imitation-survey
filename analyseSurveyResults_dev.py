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
Identify overlap between recovered cyan and orange detections
"""

recovered_events_c = np.array(sorted(glob.glob('survey/recovered_detections_cyan/*')))
recovered_events_o = np.array(sorted(glob.glob('survey/recovered_detections_orange/*')))

original_events_c = np.array(sorted(glob.glob('kilonova_data/inflated_lc_cyan/*')))
original_events_o = np.array(sorted(glob.glob('kilonova_data/inflated_lc_orange/*')))

# for i in range(0, len(recovered_events_c)):
# 	print(recovered_events_c[i], recovered_events_o[i])

events_c = []
events_o = []

for event in recovered_events_c:
	events_c.append(int(event.replace('survey/recovered_detections_cyan/recovered_lc_c_', '').replace('.csv', '')))

for event in recovered_events_o:
	events_o.append(int(event.replace('survey/recovered_detections_orange/recovered_lc_o_', '').replace('.csv', '')))

events_c = np.array(events_c)
events_o = np.array(events_o)

event_overlap, ind_c, ind_o = np.intersect1d(events_c, events_o, return_indices = True)

overlap_events_c = recovered_events_c[ind_c]
overlap_events_o = recovered_events_o[ind_o]


for i in range(0, len(overlap_events_c)):

	plt.figure(figsize = (16,10))

	cyan_data = pd.read_csv(overlap_events_c[i])
	orange_data = pd.read_csv(overlap_events_o[i])
	
	event_mjd_cyan = cyan_data['mjd_overlap']
	event_mjd_orange = orange_data['mjd_overlap']
	
	overlap_mjd, ind_mjd_c, ind_mjd_o = np.intersect1d(event_mjd_cyan, event_mjd_orange, return_indices = True)
	
	overlap_lc_c = cyan_data['recovered_mag'][ind_mjd_c]
	overlap_lc_o = orange_data['recovered_mag'][ind_mjd_o]
	
	plt.plot(event_mjd_cyan, cyan_data['recovered_mag'], ls = 'None', mfc = 'cyan', mec = 'black', marker = 'o', ms = 6)
	plt.plot(event_mjd_orange, orange_data['recovered_mag'], ls = 'None', mfc = 'orange', mec = 'black', marker = 'o', ms = 6)
	
	plt.plot(event_mjd_cyan[ind_mjd_c], overlap_lc_c, ls = 'None', mfc = 'None', mec = 'cyan', marker = 'o', ms = 16)
	plt.plot(event_mjd_orange[ind_mjd_o], overlap_lc_o, ls = 'None', mfc = 'None', mec = 'orange', marker = 'o', ms = 16)
	
	plt.title(overlap_events_c[i] + '\n' + overlap_events_o[i])
	plt.xlabel('Survey timeline, days')
	plt.ylabel('Recovered magnitudes')
	
	plt.gca().invert_yaxis()
	plt.tight_layout()
	plt.show()



