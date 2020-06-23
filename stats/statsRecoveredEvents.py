import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import yaml

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

with open('../imsu_config.yaml') as f:
	config_settings = yaml.load(f)

"""
Universe stats
	- Histograms of redshift and explosion epoch distributions
"""

number_of_kilonovae = config_settings['number_of_kilonovae']

recovered_events_c = sorted(glob.glob('../survey/recovered_detections_cyan/*'))
recovered_events_o = sorted(glob.glob('../survey/recovered_detections_orange/*'))

print('')
print('Number of kilonovae simulated:\t%d' %number_of_kilonovae)
print('Events recovered in cyan:\t%d' %len(recovered_events_c))
print('Events recovered in orange:\t%d' %len(recovered_events_o))

recovery_rate_c = (len(recovered_events_c) / number_of_kilonovae)*100.
recovery_rate_o = (len(recovered_events_o) / number_of_kilonovae)*100.

print('')
print('Recovery rate in cyan:\t%.1f%%' %recovery_rate_c)
print('Recovery rate in orange:\t%.1f%%' %recovery_rate_o)

events_c = []
events_o = []

for event in recovered_events_c:
	events_c.append(int(event.strip('../survey/recovered_detections_cyan/recovered_lc_c_')))

for event in recovered_events_o:
	events_o.append(int(event.strip('../survey/recovered_detections_orange/recovered_lc_o_')))

# print(events_c)
# print(events_o)

event_overlap = np.intersect1d(events_c, events_o, return_indices = False)
# print(event_overlap)

print('')
print('Number of events recovered in both cyan and orange:\t%d' %len(event_overlap))





