import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import yaml
from scipy.optimize import curve_fit

def POWER_LAW(x, A, gamma):
	
	return A * x ** gamma

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

fig, ax1 = plt.subplots(1, 1, figsize = (12,10))
ax2 = ax1.twinx()

"""
Plot meta-data end
"""

c = 2.99792458e5 # Speed of light in km/s
H_0 = 70.0		 # Hubble constant (km/s/Mpc)

number_of_events = 2.3
settings_file = 'settings.yaml'
efficiency_file = 'efficiency.csv'

### KILONOVAE STUFF FIRST

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

upper_redshifts = np.empty_like(results_directories)
durations_in_days = np.empty_like(results_directories)
efficiencies = np.empty_like(results_directories)

for i in range(0, len(results_directories)):
	
	results_directory_path = os.path.join('../results', results_directories[i])
	efficiency_df = pd.read_csv(os.path.join(results_directory_path, efficiency_file))
	
	try:
		efficiencies[i] = efficiency_df['recovery'].where(efficiency_df['detected'] == True)[1]
	except:
		efficiencies[i] = 0.0
	
	with open(os.path.join(results_directory_path, settings_file), 'r') as stream:
		all_settings = yaml.safe_load(stream)
	
	upper_redshifts[i] = all_settings['upper_redshift_limit']
	durations_in_days[i] = all_settings['survey_end'] - all_settings['survey_begin']

upper_redshifts = upper_redshifts.astype(float)
durations_in_days = durations_in_days.astype(float)
efficiencies = efficiencies.astype(float)

durations_in_years = durations_in_days / 365.

distances_in_Mpc = c * upper_redshifts / H_0

lower_declination_limit = all_settings['lower_declination_limit']
upper_declination_limit = all_settings['upper_declination_limit']

lower_declination_limit_in_rad_for_integration = np.radians(90. - abs(lower_declination_limit))
upper_declination_limit_in_rad_for_integration = np.radians(90. - abs(upper_declination_limit))

lower_vol_segment = np.pi * (np.cos(lower_declination_limit_in_rad_for_integration) - np.cos(lower_declination_limit_in_rad_for_integration)**3 / 3.)
upper_vol_segment = np.pi * (np.cos(upper_declination_limit_in_rad_for_integration) - np.cos(upper_declination_limit_in_rad_for_integration)**3 / 3.)
whole_vol_segment = (4. / 3.) * np.pi
correction_ratio = (lower_vol_segment + upper_vol_segment) / whole_vol_segment

volumes_in_Gpc = (4./3.) * np.pi * (distances_in_Mpc * 1.e-3)**3 * correction_ratio

rate_of_occurence = number_of_events / (efficiencies * volumes_in_Gpc * durations_in_years)

ax1.semilogy(distances_in_Mpc, rate_of_occurence, marker = 'o', ls = '--', color = 'limegreen', mfc = 'limegreen', mec = 'black', ms = 8, label = 'AT2017gfo-like')
ax1.set_xlabel('Distance, Mpc')
ax1.set_ylabel('Volumetric rate, $\mathrm{Gpc^{-3}\,yr^{-1}}$')


### AT2018KZR next

results_directories = np.array(['1e5_18kzr_to10Mpc',
								'1e5_18kzr_to20Mpc',
								'1e5_18kzr_to30Mpc',
								'1e5_18kzr_to40Mpc',
								'1e5_18kzr_to50Mpc',
								'1e5_18kzr_to60Mpc',
								'1e5_18kzr_to70Mpc',
								'1e5_18kzr_to80Mpc',
								'1e5_18kzr_to90Mpc',
								'1e5_18kzr_to100Mpc'])

efficiencies = np.empty_like(results_directories)

for i in range(0, len(results_directories)):
	
	results_directory_path = os.path.join('../results', results_directories[i])
	efficiency_df = pd.read_csv(os.path.join(results_directory_path, efficiency_file))
	
	try:
		efficiencies[i] = efficiency_df['recovery'].where(efficiency_df['detected'] == True)[1]
	except:
		efficiencies[i] = 0.0
	
efficiencies = efficiencies.astype(float)

rate_of_occurence = number_of_events / (efficiencies * volumes_in_Gpc * durations_in_years)

ax1.semilogy(distances_in_Mpc, rate_of_occurence, marker = 'o', ls = '--', color = 'lightcoral', mfc = 'lightcoral', mec = 'black', ms = 8, label = 'AT2018kzr-like')




### MODEL TYPE Ia LAST

results_directories = np.array(['1e5_hsiao_to10Mpc',
								'1e5_hsiao_to20Mpc',
								'1e5_hsiao_to30Mpc',
								'1e5_hsiao_to40Mpc',
								'1e5_hsiao_to50Mpc',
								'1e5_hsiao_to60Mpc',
								'1e5_hsiao_to70Mpc',
								'1e5_hsiao_to80Mpc',
								'1e5_hsiao_to90Mpc',
								'1e5_hsiao_to100Mpc'])

efficiencies = np.empty_like(results_directories)

for i in range(0, len(results_directories)):
	
	results_directory_path = os.path.join('../results', results_directories[i])
	efficiency_df = pd.read_csv(os.path.join(results_directory_path, efficiency_file))
	
	try:
		efficiencies[i] = efficiency_df['recovery'].where(efficiency_df['detected'] == True)[1]
	except:
		efficiencies[i] = 0.0
	
efficiencies = efficiencies.astype(float)

rate_of_occurence = 160 / (efficiencies * volumes_in_Gpc * durations_in_years)

# ax1.semilogy(distances_in_Mpc, rate_of_occurence, marker = 'o', ls = '--', color = 'lightcoral', mfc = 'lightcoral', mec = 'black', ms = 8, label = 'Model Type Ia')

for i in range(0, len(distances_in_Mpc)):
	print('%.2f' %rate_of_occurence[i])

### ==== Rest of the plot stuff now ===

ax1.set_xticks([10, 20, 30, 50, 40, 60, 70 ,80, 90, 100])
ax1.set_xticklabels([10, 20, 30, 50, 40, 60, 70 ,80, 90, 100])

# ax1.set_ylim([-0.01, 0.61])
# ax2.set_ylim([0.6e3, 1.5e6])


ax2.semilogy(distances_in_Mpc, volumes_in_Gpc, marker = 'o', ls = '-', color = 'black', mfc = 'white', mec = 'black', ms = 8, label = 'Volume')
ax2.set_ylabel('Volume, $\mathrm{Gpc^{3}}$')

# lines2 = ln3 + ln4
# labels2 = [line.get_label() for line in lines2]

ax1.legend(loc = 'upper center', frameon = False, ncol = 1)

# ax3.set_xticks([10, 30, 50, 70, 90, 110, 130, 150])
# ax3.set_xticklabels([10, 30, 50, 70, 90, 110, 130, 150])


fig.tight_layout()
fig.savefig('makeRateOverVolumePlot.pdf')
plt.show()
