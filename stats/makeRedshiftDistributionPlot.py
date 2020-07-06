import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yaml

with open('../settings.yaml', 'r') as stream:
	all_settings = yaml.safe_load(stream)

lower_redshift_limit = all_settings['lower_redshift_limit']
upper_redshift_limit = all_settings['upper_redshift_limit']
num_bins = all_settings['num_redshift_bins'] - 1

"""
Plot meta-data
"""

SMALL_SIZE = 15
MEDIUM_SIZE = 20
BIGGER_SIZE = 25

plt.figure(figsize = (12,10))

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
Plot meta-data end
"""

results_file = 'results_2020-07-06_14-56-21.csv'
results_df = pd.read_csv(results_file)

# print(results_df)

plt.hist(results_df['redshift'], bins = num_bins, color = 'blue', edgecolor = 'black', alpha = 0.75)

plt.xlabel('Redshift, $z$')
plt.ylabel('Frequency')

plt.show()



