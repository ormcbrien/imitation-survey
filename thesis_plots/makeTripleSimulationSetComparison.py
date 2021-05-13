import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import yaml
from scipy.optimize import curve_fit

def EXPONENTIAL(x, A, beta):
	
	return A * np.exp(-beta * x)

def LINEAR(x, m, c):

	return m * x + c
	
"""
Plot meta-data
"""
SMALL_SIZE = 20
MEDIUM_SIZE = 25
BIGGER_SIZE = 30

plt.rc('font', size=SMALL_SIZE)          	# controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     	# fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    	# fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    	# fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    	# fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)    	# legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  	# fontsize of the figure title

plt.rcParams["font.family"] = "serif"
plt.rcParams['mathtext.fontset'] = 'dejavuserif'

fig, ax = plt.subplots(1, 1, figsize = (12,10))


"""
Plot meta-data end
"""

settings_file = 'settings.yaml'
efficiency_file = 'efficiency.csv'

results_directories_kn = np.array(['1e5_kn_to10Mpc',
						    	   '1e5_kn_to20Mpc',
								   '1e5_kn_to30Mpc',
								   '1e5_kn_to40Mpc',
								   '1e5_kn_to50Mpc',
								   '1e5_kn_to60Mpc',
								   '1e5_kn_to70Mpc',
								   '1e5_kn_to80Mpc',
								   '1e5_kn_to90Mpc',
								   '1e5_kn_to100Mpc'])

results_directories_18kzr = np.array(['1e5_18kzr_to10Mpc',
						    	      '1e5_18kzr_to20Mpc',
								      '1e5_18kzr_to30Mpc',
								      '1e5_18kzr_to40Mpc',
								      '1e5_18kzr_to50Mpc',
								      '1e5_18kzr_to60Mpc',
								      '1e5_18kzr_to70Mpc',
								      '1e5_18kzr_to80Mpc',
								      '1e5_18kzr_to90Mpc',
								      '1e5_18kzr_to100Mpc'])

results_directories_ia = np.array(['1e5_hsiao_to10Mpc',
						    	   '1e5_hsiao_to20Mpc',
								   '1e5_hsiao_to30Mpc',
								   '1e5_hsiao_to40Mpc',
								   '1e5_hsiao_to50Mpc',
								   '1e5_hsiao_to60Mpc',
								   '1e5_hsiao_to70Mpc',
								   '1e5_hsiao_to80Mpc',
								   '1e5_hsiao_to90Mpc',
								   '1e5_hsiao_to100Mpc'])
				
distances = np.arange(10, 101, 10)
distances_toplot = np.arange(8, 104, 1)
marker_face_colours = ['limegreen', 'lightcoral', 'gold']
# annotation_colours = ['lightgreen', 'lightyellow', 'pink']
the_labels = ['AT2017gfo', 'AT2018kzr', 'Type Ia model']

results_directories_list = [results_directories_kn, results_directories_18kzr, results_directories_ia]

for ii, item in enumerate(results_directories_list):

# 	print('###', item)
	efficiencies = np.empty_like(item, dtype = float).astype(float)

	for jj in range(0, len(item)):

		results_directory_path = os.path.join('../results', item[jj])
		efficiency_df = pd.read_csv(os.path.join(results_directory_path, efficiency_file))

		try:
			efficiencies[jj] = efficiency_df['recovery'].where(efficiency_df['detected'] == True)[1]
		except:
			efficiencies[jj] = 0.0

# 	for val in efficiencies:
# 		print('%.5f' %val)

	if ii == 0:

		popt, pcov = curve_fit(EXPONENTIAL, distances, efficiencies)
		perr = np.sqrt( np.diag( pcov ) )
		print(popt, perr)
		
		ax.plot(distances_toplot, EXPONENTIAL(distances_toplot, *popt), ls = '--', color = marker_face_colours[ii], linewidth = 2)
		ax.annotate(r'$\varepsilon = %.3f \mathrm{e}^{-%.3f d}$' %(popt[0], popt[1]), xy = (distances[5], efficiencies[5] + 0.04), xycoords = 'data', fontsize = 'large', bbox = dict(facecolor = 'none', edgecolor = marker_face_colours[ii], linewidth = 2))

	elif ii != 0:
	
		popt, pcov = curve_fit(LINEAR, distances, efficiencies)
		perr = np.sqrt( np.diag( pcov ) )
		print(popt, perr)
	
		ax.plot(distances_toplot, LINEAR(distances_toplot, *popt), ls = '--', color = marker_face_colours[ii], linewidth = 2)
		ax.annotate(r'$\varepsilon = %.3f d + %.3f$' %(popt[0], popt[1]), xy = (distances[5], efficiencies[5] + 0.04), xycoords = 'data', fontsize = 'large', bbox = dict(facecolor = 'none', edgecolor = marker_face_colours[ii], linewidth = 2))
	
	else:
	
		sys.exit('No fitting!')
	
	ax.plot(distances, efficiencies, ls = 'None', marker = 'o', ms = 8, mfc = marker_face_colours[ii], mec = 'black', label = the_labels[ii])

ax.set_xlabel('Distance, Mpc')
ax.set_ylabel('Efficiency')

ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))

ax.set_ylim([0.0, 1.0])

plt.legend(loc = 'lower left', ncol = 1, frameon = False)

plt.tight_layout()
plt.savefig('makeTripleSimulationSetComparison.pdf')
plt.show()
