import os
import yaml
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import PercentFormatter
from matplotlib import cm

"""
Plot meta-data
"""
SMALL_SIZE = 40
MEDIUM_SIZE = 45
BIGGER_SIZE = 50

plt.rc('font', size=SMALL_SIZE)          	# controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     	# fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    	# fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    	# fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    	# fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)    	# legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  	# fontsize of the figure title

plt.rcParams["font.family"] = "serif"
plt.rcParams['mathtext.fontset'] = 'dejavuserif'

fig = plt.figure(figsize = (35,55))

"""
Plot meta-data end
"""

settings_file = 'settings.yaml'
population_file = 'population.csv'

# results_directories = np.array(['1e5_kn_to10Mpc',
# 								'1e5_kn_to20Mpc',
# 								'1e5_kn_to30Mpc',
# 								'1e5_kn_to40Mpc',
# 								'1e5_kn_to50Mpc',
# 								'1e5_kn_to60Mpc',
# 								'1e5_kn_to70Mpc',
# 								'1e5_kn_to80Mpc',
# 								'1e5_kn_to90Mpc',
# 								'1e5_kn_to100Mpc',
# 								'1e5_kn_to110Mpc',
# 								'1e5_kn_to120Mpc',
# 								'1e5_kn_to130Mpc',
# 								'1e5_kn_to140Mpc',
# 								'1e5_kn_to150Mpc'])

results_directories = np.array(['1e5_kn_to10Mpc',
								'1e5_kn_to20Mpc',
								'1e5_kn_to30Mpc',
								'1e5_kn_to40Mpc',
								'1e5_kn_to50Mpc',
								'1e5_kn_to60Mpc',
								'1e5_kn_to70Mpc',
								'1e5_kn_to80Mpc',
								'1e5_kn_to90Mpc',
								'1e5_kn_to100Mpc'])

plot_title_dict = {'1e5_kn_to10Mpc': '10$\,$Mpc',
					'1e5_kn_to20Mpc': '20$\,$Mpc',
					'1e5_kn_to30Mpc': '30$\,$Mpc',
					'1e5_kn_to40Mpc': '40$\,$Mpc',
					'1e5_kn_to50Mpc': '50$\,$Mpc',
					'1e5_kn_to60Mpc': '60$\,$Mpc',
					'1e5_kn_to70Mpc': '70$\,$Mpc',
					'1e5_kn_to80Mpc': '80$\,$Mpc',
					'1e5_kn_to90Mpc': '90$\,$Mpc',
					'1e5_kn_to100Mpc': '100$\,$Mpc'}

nplots = len(results_directories)
# ncolumns = int(np.floor(np.sqrt(nplots)))
ncolumns = 1

# Compute nrows required

nrows = nplots // ncolumns 
nrows += nplots % ncolumns

# Create a Position index

nposition = range(1, nplots + 1)

cm_subsection = np.linspace(0.0, 1.0, nplots)
colours = [cm.viridis(x) for x in cm_subsection]

for i in range(0, nplots):
	print(i, nplots, plot_title_dict[results_directories[i]])
	
	results_directory_path = os.path.join('../results', results_directories[i])
	population_df = pd.read_csv(os.path.join(results_directory_path, population_file))
	
	with open(os.path.join(results_directory_path, settings_file), 'r') as stream:
		all_settings = yaml.safe_load(stream)
	
	lower_redshift_limit = all_settings['lower_redshift_limit']
	upper_redshift_limit = all_settings['upper_redshift_limit']
	num_redshift_bins = all_settings['num_redshift_bins']
	
	redshift_bins = np.linspace(lower_redshift_limit, upper_redshift_limit, num_redshift_bins)
	
	ax = fig.add_subplot(nrows, ncolumns, nposition[i])
# 	ax_full = ax.twinx()
	
	recovered_redshifts_df = population_df.query('detected == %s' %(True))
	
# 	ax.hist(population_df['redshift'], bins = redshift_bins, color = colours[i], edgecolor = 'black', alpha = 0.5)
	ax.hist([recovered_redshifts_df['redshift'], population_df['redshift']], bins = redshift_bins, color = ['limegreen', 'royalblue'], edgecolor = 'black', alpha = 0.50, log = False, stacked = True, weights = [np.ones( len(recovered_redshifts_df['redshift']) ) / len (recovered_redshifts_df['redshift']), np.ones(len(population_df['redshift'])) / len(population_df['redshift'])])
# 	ax_full.hist(population_df['redshift'], bins = redshift_bins, color = 'royalblue', edgecolor = 'black', alpha = 0.40, label = 'Generated', density = True)
# 	ax.hist(population_df['redshift'], bins = redshift_bins, color = 'royalblue', edgecolor = 'black', alpha = 0.40, label = 'Generated', stacked = True, log = True)
		
	ax.set_xlim([lower_redshift_limit, upper_redshift_limit])
	ax.set_xticks(redshift_bins)
	ax.set_xticklabels(['%.4f' %val for val in redshift_bins], rotation = 335.)


# 	ax.set_ylim([0, 25000])
	ax.yaxis.set_major_locator(plt.MaxNLocator(4))
# 	ax_full.yaxis.set_major_locator(plt.MaxNLocator(5))

	ax.set_ylabel('% of\nevents')

	if i >= 9:
		ax.set_xlabel('Redshift, $z$')

	ax.annotate(plot_title_dict[results_directories[i]], xy = (0.03, 0.65), xycoords = 'axes fraction', fontsize = 'xx-large')

	ax.yaxis.set_major_formatter(PercentFormatter(1))


fig.tight_layout()

plt.savefig('makeHistogramOfRecoveredRedshifts_thin.pdf')
# plt.show()



