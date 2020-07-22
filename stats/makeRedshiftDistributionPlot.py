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

plt.figure(figsize = (20,10))

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

results_file = '../results/results_2020-07-22_13-25-37.csv'
results_df = pd.read_csv(results_file)

# print(results_df)

bin_edges = np.linspace(lower_redshift_limit, upper_redshift_limit, num_bins + 1)

# for i, bin_edge in enumerate(bin_edges):
# 	bin_edges[i] = np.format_float_positional(bin_edge, precision = 3)
# 
# print(bin_edges)

plt.hist(results_df['redshift'], bins = bin_edges, color = 'blue', edgecolor = 'black', alpha = 0.75, align = 'mid')
plt.xticks(bin_edges, rotation = 45.)

plt.xlim([lower_redshift_limit, upper_redshift_limit])

plt.xlabel('Redshift, $z$')
plt.ylabel('Number of kilonovae')

plt.show()



