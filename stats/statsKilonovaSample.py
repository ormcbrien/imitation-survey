import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

kn_sample_data = pd.read_csv('../survey/kn_sample_data.csv')

fig, ax1 = plt.subplots(figsize = (12, 10))
ax2 = ax1.twiny()

ax1.hist(kn_sample_data['redshift'], color = 'red', edgecolor = 'black', bins = 20, alpha = 0.5, label = 'Redshift')
ax2.hist(kn_sample_data['expl_epoch'], color = 'blue', edgecolor = 'black', bins = 20, alpha = 0.5, label = 'Explosion Epoch')

ax1.set_xlabel('Redshift')
ax2.set_xlabel('Explosion epoch, days')
ax1.set_ylabel('Frequency')

ax1.set_xlim([config_settings['lower_redshift'], config_settings['upper_redshift']])
ax2.set_xlim([0, config_settings['survey_duration']])

ax1.legend(frameon = False, loc = 'upper right')
ax2.legend(frameon = False, loc = 'upper left')

plt.tight_layout()
plt.show()
