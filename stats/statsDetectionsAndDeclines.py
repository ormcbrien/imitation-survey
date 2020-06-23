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
Measure how many events were recovered on more than one epoch
"""

recovered_events_c = sorted(glob.glob('../survey/recovered_detections_cyan/*'))
recovered_events_o = sorted(glob.glob('../survey/recovered_detections_orange/*'))

number_of_detections_c = []

for f in recovered_events_c:
	
	recovered_lc_c = pd.read_csv(f)
	number_of_detections_c.append(len(recovered_lc_c['mjd_overlap']))

number_of_detections_o = []

for f in recovered_events_o:
	
	recovered_lc_o = pd.read_csv(f)
	number_of_detections_o.append(len(recovered_lc_o['mjd_overlap']))

plt.figure(figsize = (12,10))

nbins_c = len( list( set( number_of_detections_c) ) )
nbins_o = len( list( set( number_of_detections_o) ) )

plt.hist(number_of_detections_c, color = '#00ffff', edgecolor = 'black', bins = nbins_c, alpha = 0.75, label = '%s events' %(str(len(number_of_detections_c))))
plt.hist(number_of_detections_o, color = '#f97306', edgecolor = 'black', bins = nbins_o, alpha = 0.75, label = '%s events' %(str(len(number_of_detections_o))))

plt.legend(frameon = False, loc = 'upper right')

plt.xlabel('Number of detections per event')
plt.ylabel('Number of events recovered')

plt.tight_layout()
plt.show()
