import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.gridspec as gridspec
import matplotlib.patheffects as pe
from matplotlib import cm

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

# gs = gridspec.GridSpec(1, 2)
fig, ax = plt.subplots(1, 1, figsize = (12,10))

colours = ['limegreen', 'grey', 'lightcoral', 'khaki']

"""
Plot meta-data end
"""

settings_file = 'settings.yaml'
population_file = 'population.csv'

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

results_directories_knnoext = np.array(['1e5_kn_to10Mpc_noext',
						    	        '1e5_kn_to20Mpc_noext',
								        '1e5_kn_to30Mpc_noext',
								        '1e5_kn_to40Mpc_noext',
								        '1e5_kn_to50Mpc_noext',
								        '1e5_kn_to60Mpc_noext',
								        '1e5_kn_to70Mpc_noext',
								        '1e5_kn_to80Mpc_noext',
								        '1e5_kn_to90Mpc_noext',
								        '1e5_kn_to100Mpc_noext'])


results_directories_list = [results_directories_kn, results_directories_knnoext]
distances_toplot = np.arange(10, 101, 10)

plot_titles = ['AT2017gfo-like w/ extinction', 'AT2017gfo-like w/o extinction']

for ii, item in enumerate(results_directories_list):

	insuff_det = []
	no_spat = []
	suff_det = []

	for jj in range(0, len(item)):

		results_directory_path = os.path.join('../results', item[jj])
		population_df = pd.read_csv(os.path.join(results_directory_path, population_file))
	
		reasons = population_df['reason'].value_counts().rename_axis('reason').reset_index(name = 'counts')
		reasons = reasons.sort_values(by = 'reason')
	
		insuff_det.append(int(reasons['counts'].where(reasons['reason'] == 'Insufficient detections').dropna()))
		no_spat.append(int(reasons['counts'].where(reasons['reason'] == 'No spatial coincidence').dropna()))
		suff_det.append(int(reasons['counts'].where(reasons['reason'] == 'Detected').dropna()))

	insuff_det = np.array(insuff_det) / 1e5
	no_spat = np.array(no_spat) / 1e5
	suff_det = np.array(suff_det) / 1e5
	
# 	print(insuff_det)
# 	print(suff_det)
# 	print(no_spat)

	total_abundance = insuff_det + no_spat + suff_det
	
# 	print(total_abundance)

	if plot_titles[ii] == 'AT2017gfo-like w/ extinction':
		
		ax.plot(distances_toplot, suff_det, marker = 'None', ls = '-', linewidth = 3, color = 'limegreen', label = 'Detected', path_effects = [pe.Stroke(linewidth = 4, foreground = 'black'), pe.Normal()])
		ax.plot(distances_toplot, insuff_det, marker = 'None', ls = '-', linewidth = 3, color = 'grey', label = 'Insufficient\ndetections', path_effects = [pe.Stroke(linewidth = 4, foreground = 'black'), pe.Normal()])
		ax.plot(distances_toplot, no_spat, marker = 'None', ls = '-', linewidth = 3, color = 'lightcoral', label = 'No coincident\nexposures', path_effects = [pe.Stroke(linewidth = 4, foreground = 'black'), pe.Normal()])
# 		ax.plot(distances_toplot, total_abundance, marker = 'None', ls = '-', linewidth = 3, color = 'royalblue', label = 'Total\nabundance')
		
	elif plot_titles[ii] == 'AT2017gfo-like w/o extinction':

		ax.plot(distances_toplot, suff_det, marker = 'None', ls = '--', linewidth = 3, color = 'limegreen', path_effects = [pe.Stroke(linewidth = 4, foreground = 'black'), pe.Normal()])
		ax.plot(distances_toplot, insuff_det, marker = 'None', ls = '--', linewidth = 3, color = 'grey', path_effects = [pe.Stroke(linewidth = 4, foreground = 'black'), pe.Normal()])
		ax.plot(distances_toplot, no_spat, marker = 'None', ls = '--', linewidth = 3, color = 'lightcoral', path_effects = [pe.Stroke(linewidth = 4, foreground = 'black'), pe.Normal()])
# 		ax.plot(distances_toplot, total_abundance, marker = 'None', ls = '--', linewidth = 3, color = 'royalblue', label = 'Total\nabundance')
	
	print(plot_titles[ii], np.median(no_spat)*100., np.mean(no_spat)*100.)
	
# 	ax.set_title(plot_titles[ii])

	ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
	ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))

	ax.set_xlabel('Distance, Mpc')
	ax.set_ylabel('Recovery abundance')


# print(no_spat)
# print(np.mean(no_spat))
# print(np.median(no_spat))


# axs[1,1].get_xaxis().set_visible(False)
# axs[1,1].get_yaxis().set_visible(False)
# plt.axis('off')



# ax = plt.subplot(gs[1,3])
# ax.plot([], [], marker = 'None', ls = '-', linewidth = 3, color = 'limegreen', label = 'Detected')
# ax.plot([], [], marker = 'None', ls = '-', linewidth = 3, color = 'grey', label = 'Insufficient\ndetections')
# ax.plot([], [], marker = 'None', ls = '-', linewidth = 3, color = 'lightcoral', label = 'No coincident\nexposures')
# ax.plot([], [], marker = 'None', ls = '-', linewidth = 3, color = 'royalblue', label = 'Total\nabundance')
# 
# plt.axis('off')
ax.legend(loc = 'upper center', frameon = False, ncol = 3, fontsize = 'medium')

ax.set_ylim([-0.01, 0.65])




plt.tight_layout()
plt.savefig('makeRecoveryReasonAbundancePlot_extinction.pdf')
plt.show()



