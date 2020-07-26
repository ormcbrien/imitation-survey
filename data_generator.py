import numpy as np
import matplotlib.pyplot as plt
import random

def getShellWeights(lower_redshift_limit, upper_redshift_limit, num_redshift_bins):

	num_shells = num_redshift_bins - 1
	redshift_distribution = np.linspace(lower_redshift_limit, upper_redshift_limit, num_redshift_bins)
	c = 2.99792458e5 # Speed of light in km/s
	H_0 = 70.0		 # Hubble constant (km/s/Mpc)
	
	volume_distribution = (4./3.) * np.pi * (c * redshift_distribution / H_0)**3	
	shell_volume_distribution = np.empty(num_shells)
	
	for i in range(1, len(volume_distribution)):
	
		shell_volume_distribution[i-1] = volume_distribution[i] - volume_distribution[i-1]
	
	shell_weights = shell_volume_distribution / np.nanmax(volume_distribution)
	
# 	for i in range(1, len(redshift_distribution)):
# 		print('z = %f to %f has weight %f' %(redshift_distribution[i-1], redshift_distribution[i], shell_weights[i-1]))
		
	return shell_weights, redshift_distribution
	
# ========================================================================================

def getBandWeights(lower_declination_limit, upper_declination_limit, declination_band_width):

	declination_distribution = np.arange(lower_declination_limit, upper_declination_limit, declination_band_width)
	
	band_midpoints = np.empty(len(declination_distribution) - 1)
	
	for i in range(1, len(declination_distribution)):
	
		band_midpoints[i-1] = declination_distribution[i-1] + (declination_distribution[i] - declination_distribution[i-1]) / 2.0
	
	band_weights = np.cos(band_midpoints * np.pi / 180.)
	
# 	for i in range(1, len(declination_distribution)):
# 		print('Dec = %f to %f has midpoint %f and weight %f' %(declination_distribution[i-1], declination_distribution[i], band_midpoints[i-1], band_weights[i-1]))
		
	return band_weights, declination_distribution
	
# ========================================================================================

def getRedshiftBounds(shell_weights, redshift_distribution):

    weights_sum = shell_weights.sum()
    # standardization:
    np.multiply(shell_weights, 1. / weights_sum, shell_weights)
    shell_weights_cumulative_sum = shell_weights.cumsum()
    
    x = random.random()
    
    for i in range(len(shell_weights_cumulative_sum)):
        
        if x < shell_weights_cumulative_sum[i]:
            
            return redshift_distribution[i], redshift_distribution[i+1]

# ========================================================================================

def getDeclinationBounds(band_weights, declination_distribution):

    weights_sum = band_weights.sum()
    # standardization:
    np.multiply(band_weights, 1. / weights_sum, band_weights)
    band_weights_cumulative_sum = band_weights.cumsum()
    
    x = random.random()
    
    for i in range(len(band_weights_cumulative_sum)):
        
        if x < band_weights_cumulative_sum[i]:
            
            return declination_distribution[i], declination_distribution[i+1]

# ========================================================================================

def filterAtlasDataFrameByExplosionEpoch(full_ATLAS_df, kn, lower_fit_time_limit, upper_fit_time_limit):

	lower_expl_epoch_bound = kn.expl_epoch + lower_fit_time_limit
	upper_expl_epoch_bound = kn.expl_epoch + upper_fit_time_limit
	
	partial_ATLAS_df = full_ATLAS_df.query('MJDOBS >= %f & MJDOBS <= %f' %(lower_expl_epoch_bound, upper_expl_epoch_bound))

	return partial_ATLAS_df
	
# ========================================================================================
	
def filterAtlasDataFrameByCoords(partial_ATLAS_df, kn, plot_mode = False):

	ATLAS_chip_halfwidth = 5.46 / 2. # degrees
	ATLAS_chip_fullwidth = ATLAS_chip_halfwidth * 2.
	
	max_allowed_ra = 360.
	min_allowed_ra = 0.

	upper_kn_ra_bound = kn.ra + (ATLAS_chip_fullwidth * np.cos(kn.dec*np.pi/180.)) / 2.
	lower_kn_ra_bound = kn.ra - (ATLAS_chip_fullwidth * np.cos(kn.dec*np.pi/180.)) / 2.
	upper_kn_ra_bound_unc = kn.ra + (ATLAS_chip_fullwidth) / 2.
	lower_kn_ra_bound_unc = kn.ra - (ATLAS_chip_fullwidth) / 2.
	upper_kn_dec_bound = kn.dec + ATLAS_chip_halfwidth
	lower_kn_dec_bound = kn.dec - ATLAS_chip_halfwidth
	
# 	if plot_mode:
# 
# 		SMALL_SIZE = 15
# 		MEDIUM_SIZE = 20
# 		BIGGER_SIZE = 25
# 
# 		plt.rc('font', size=SMALL_SIZE)          	# controls default text sizes
# 		plt.rc('axes', titlesize=BIGGER_SIZE)     	# fontsize of the axes title
# 		plt.rc('axes', labelsize=MEDIUM_SIZE)    	# fontsize of the x and y labels
# 		plt.rc('xtick', labelsize=SMALL_SIZE)    	# fontsize of the tick labels
# 		plt.rc('ytick', labelsize=SMALL_SIZE)    	# fontsize of the tick labels
# 		plt.rc('legend', fontsize=MEDIUM_SIZE)    	# legend fontsize
# 		plt.rc('figure', titlesize=BIGGER_SIZE)  	# fontsize of the figure title
# 
# 		plt.rcParams["font.family"] = "serif"
# 		plt.rcParams['mathtext.fontset'] = 'dejavuserif'
# 	
# 		fig = plt.figure(figsize = (12, 10))
# 		ax = fig.add_subplot(111)
# 	
# 		ra_array = np.array([lower_kn_ra_bound, upper_kn_ra_bound, upper_kn_ra_bound, lower_kn_ra_bound, lower_kn_ra_bound])
# 		ra_array_unc = np.array([lower_kn_ra_bound_unc, upper_kn_ra_bound_unc, upper_kn_ra_bound_unc, lower_kn_ra_bound_unc, lower_kn_ra_bound_unc])
# 		dec_array = np.array([lower_kn_dec_bound, lower_kn_dec_bound, upper_kn_dec_bound, upper_kn_dec_bound, lower_kn_dec_bound])
# 	
# 		ax.plot(kn.ra, kn.dec, ls = 'None', marker = 'o', mfc = 'red', mec = 'black', ms = 10)
# 		ax.plot(ra_array_unc, dec_array, ls = '--', marker = 'None', color = 'red', label = 'normal')
# 		ax.plot(ra_array, dec_array, ls = '--', marker = 'None', color = 'blue', label = 'corrected')
# 	
# 		plt.xlabel('RA, degrees')
# 		plt.ylabel('Dec, degrees')
# 		plt.legend(loc = 'upper center', frameon = False, ncol = 2, bbox_to_anchor = (0.50, 1.15))
# 		plt.show(fig)
	
	# Filter RA first as it wraps (360 --> 0 degrees)
	if upper_kn_ra_bound > max_allowed_ra:
	
		partial_ATLAS_df = partial_ATLAS_df.query('RA >= %f | RA <= %f' %(lower_kn_ra_bound, (upper_kn_ra_bound - max_allowed_ra)) )
	
	elif lower_kn_ra_bound < min_allowed_ra:
	
		partial_ATLAS_df = partial_ATLAS_df.query('RA >= %f | RA <= %f' %((lower_kn_ra_bound + max_allowed_ra), (upper_kn_ra_bound - max_allowed_ra)) )
	
	else:

		partial_ATLAS_df = partial_ATLAS_df.query('RA >= %f & RA <= %f' %(lower_kn_ra_bound, upper_kn_ra_bound) )
	
	# Now filter by DEC
	partial_ATLAS_df = partial_ATLAS_df.query('DEC >= %f & DEC <= %f' %(lower_kn_dec_bound, upper_kn_dec_bound) )
	
# 	partial_ATLAS_df = partial_ATLAS_df.query('RA >= %f & RA <= %f & DEC >= %f & DEC <= %f' %(lower_kn_ra_bound, upper_kn_ra_bound, lower_kn_dec_bound, upper_kn_dec_bound))

	return partial_ATLAS_df

# ========================================================================================

def fitKilonovaLightcurve(kilonova_df, lower_fit_time_limit, upper_fit_time_limit, polynomial_degree, plot_mode = False, save_results = False, results_directory = 'test'):

	kilonova_df_cyan = kilonova_df.query('c.notnull()', engine = 'python')
	kilonova_df_orange = kilonova_df.query('o.notnull()', engine = 'python')
	
# 	print(kilonova_df_cyan)
# 	print(kilonova_df_orange)

	phase_c = kilonova_df_cyan['phase']
	c_lc = kilonova_df_cyan['c']
	c_err = kilonova_df_cyan['cerr']
	phase_o = kilonova_df_orange['phase']
	o_lc = kilonova_df_orange['o']
	o_err = kilonova_df_orange['oerr']
	
	p_c = np.poly1d(np.polyfit(phase_c, c_lc, polynomial_degree))
	p_o = np.poly1d(np.polyfit(phase_o, o_lc, polynomial_degree))

	if plot_mode:

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
		
		plt.errorbar(phase_c, c_lc, c_err, ls = 'None', marker = 'o', ms = 8, mfc = 'cyan', mec = 'black', ecolor = 'black', capsize = 5)
		plt.errorbar(phase_o, o_lc, o_err, ls = 'None', marker = 'o', ms = 8, mfc = 'orange', mec = 'black', ecolor = 'black', capsize = 5)
	
		time_array = np.arange(lower_fit_time_limit, upper_fit_time_limit, 0.1)
	
		plt.plot(time_array, p_c(time_array), ls = '-', color = 'green', marker = '|', mfc = 'green', mec = 'green', ms = 10)
		plt.plot(time_array, p_o(time_array), ls = '-', color = 'red', marker = '|', mfc = 'red', mec = 'red', ms = 10)

		plt.title('Polynomial fit, $k = %d$' %polynomial_degree)
		plt.xlabel('Phase, days')
		plt.ylabel('Magnitude')
		plt.gca().invert_yaxis()
		plt.tight_layout()
		
		if save_results:
			plt.savefig('results/' + results_directory + '/polynomial_k_%d.pdf' %polynomial_degree)
			plt.close()
		else:
			plt.show()
			plt.close()
	
	return p_c, p_o












