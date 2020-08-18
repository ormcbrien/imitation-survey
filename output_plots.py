import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def calculateDetectionEfficiency(all_settings):

	results_directory = all_settings['results_directory']

	results_df = pd.read_csv(os.path.join(os.getcwd(), 'results', results_directory, 'population.csv'))

	detected = results_df['detected']
	detected_count = detected.value_counts().rename_axis('detected').reset_index(name = 'frequency')

	detected_count['recovery'] = detected_count['frequency'] / detected_count['frequency'].sum()
	
	detected_count = detected_count.sort_values(by = 'detected')
	
	detected_count.to_csv('results/' + results_directory + '/efficiency.csv', index = False)

# ========================================================================================

def makeRedshiftDistribution(all_settings):

	results_directory = all_settings['results_directory']
	lower_redshift_limit = all_settings['lower_redshift_limit']
	upper_redshift_limit = all_settings['upper_redshift_limit']
	num_redshift_bins = all_settings['num_redshift_bins']

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
	
	results_file = os.path.join(os.getcwd(), 'results', results_directory, 'population.csv')
	results_df = pd.read_csv(results_file)

	bin_edges = np.linspace(lower_redshift_limit, upper_redshift_limit, num_redshift_bins + 1)

	# for i, bin_edge in enumerate(bin_edges):
	# 	bin_edges[i] = np.format_float_positional(bin_edge, precision = 3)
	# 
	# print(bin_edges)

	plt.hist(results_df['redshift'], bins = bin_edges, color = 'blue', edgecolor = 'black', alpha = 0.75, align = 'mid')
	plt.xticks(bin_edges, rotation = 45.)

	plt.xlim([lower_redshift_limit, upper_redshift_limit])

	plt.xlabel('Redshift, $z$')
	plt.ylabel('Number of transients')

	plt.tight_layout()
	plt.savefig('results/' + results_directory + '/redshiftDistribution.pdf')
	plt.close()

# ========================================================================================

def makeCoordinateDistributionMap(all_settings):
	
	results_directory = all_settings['results_directory']
	lower_declination_limit = all_settings['lower_declination_limit']
	upper_declination_limit = all_settings['upper_declination_limit']

	"""
	Plot meta-data
	"""

	SMALL_SIZE = 15
	MEDIUM_SIZE = 20
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

	fig = plt.figure(figsize = (12, 8))
	ax = fig.add_subplot(111, projection = 'mollweide')
	ax.grid(True)


	"""
	Plot meta-data end
	"""

	results_file = os.path.join(os.getcwd(), 'results', results_directory, 'population.csv')
	results_df = pd.read_csv(results_file)

	ra = np.array(results_df['ra'])
	dec = np.array(results_df['dec'])
	detected = np.array(results_df['detected'])
	reason = np.array(results_df['reason'])
	
	ind_detected = np.where(reason == 'Detected')
	ind_spatial = np.where(reason == 'No spatial coincidence')
	ind_temporal = np.where(reason == 'No temporal coincidence')
	ind_nondetected = np.where(reason == 'Insufficient detections')

	# Fixing plot axes for sky projection
	origin = 0

	RA = np.remainder(ra + 360 - origin, 360)
	ind = RA > 180
	RA[ind] -= 360
	RA = -RA

	xtick_labels = np.array([150, 120, 90, 60, 30, 0, 330, 300, 270, 240, 210])
	xtick_labels = np.remainder(xtick_labels + 360 - origin, 360)

	ytick_labels = np.array([-75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75])
	# That's better

	ax.axhline(lower_declination_limit * np.pi/180., ls = '--', color = 'red')
	ax.axhline(upper_declination_limit * np.pi/180., ls = '--', color = 'red')


# 	ax.scatter(np.radians(RA[ind_temporal]), np.radians(dec[ind_temporal]), s = 50, marker = 'o', c = 'lightgreen', edgecolors = 'black', linewidths = 1.0, alpha = 0.75, label = 'No temporal coincidence')
# 	ax.scatter(np.radians(RA[ind_spatial]), np.radians(dec[ind_spatial]), s = 50, marker = 'o', c = 'khaki', edgecolors = 'black', linewidths = 1.0, alpha = 0.75, label = 'No spatial coincidence')
# 	ax.scatter(np.radians(RA[ind_nondetected]), np.radians(dec[ind_nondetected]), s = 50, marker = 'o', c = 'lightgrey', edgecolors = 'black', linewidths = 1.0, alpha = 0.75, label = 'Insufficient detections')
# 	ax.scatter(np.radians(RA[ind_detected]), np.radians(dec[ind_detected]), s = 50, marker = 'o', c = 'red', edgecolors = 'black', linewidths = 1.0, alpha = 0.85, label = 'Detected')
	
	ax.scatter(np.radians(RA[ind_temporal]), np.radians(dec[ind_temporal]), s = 50, marker = '.', c = 'khaki', edgecolors = 'black', linewidths = 0.5, alpha = 1.0, label = 'No temporal coincidence')
	ax.scatter(np.radians(RA[ind_spatial]), np.radians(dec[ind_spatial]), s = 50, marker = '.', c = 'lightcoral', edgecolors = 'black', linewidths = 0.5, alpha = 1.0, label = 'No spatial coincidence')
	ax.scatter(np.radians(RA[ind_nondetected]), np.radians(dec[ind_nondetected]), s = 50, marker = '.', c = 'lightgrey', edgecolors = 'black', linewidths = 0.5, alpha = 1.0, label = 'Insufficient detections')
	ax.scatter(np.radians(RA[ind_detected]), np.radians(dec[ind_detected]), s = 50, marker = '.', c = 'limegreen', edgecolors = 'black', linewidths = 0.5, alpha = 1.0, label = 'Detected')
	
# 	ax.legend(loc = 'upper center', frameon = False, ncol = 2)

# 	ax.set_xlabel('Right ascension', **{'fontname': 'serif'}, fontsize = 20)
# 	ax.set_ylabel('Declination', **{'fontname': 'serif'}, fontsize = 20)

	ax.set_xlabel('Right ascension')
	ax.set_ylabel('Declination')


	ax.set_xticklabels(map(lambda x: '' + np.str(x) + '$^\circ$', xtick_labels))
	ax.set_yticklabels(map(lambda x: '' + np.str(x) + '$^\circ$', ytick_labels))
	# ax.set_xticklabels(tick_labels)

	fig.tight_layout()
	plt.legend(bbox_to_anchor = (0.875, 1.0), bbox_transform = plt.gcf().transFigure, ncol = 2, frameon = False)
	
	plt.savefig('results/' + results_directory + '/coordinateDistributionMap.pdf')
	plt.close()

# ========================================================================================

def showSurveyTimeline(all_settings, full_QC_df, QC_columns):
	
	survey_begin = all_settings['survey_begin']
	survey_end = all_settings['survey_end']
	results_directory = all_settings['results_directory']
	
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
	
	full_QC_df_cyan = full_QC_df.query('%s == "c"' %QC_columns['qc_filters'])
	full_QC_df_orange = full_QC_df.query('%s == "o"' %QC_columns['qc_filters'])
	
	plt.plot(full_QC_df_cyan[QC_columns['qc_time']], full_QC_df_cyan[QC_columns['qc_limits']], ls = 'None', marker = 'v', mfc = 'cyan', mec = None, ms = 5, alpha = 0.15)
	plt.plot(full_QC_df_orange[QC_columns['qc_time']], full_QC_df_orange[QC_columns['qc_limits']], ls = 'None', marker = 'v', mfc = 'orange', mec = None, ms = 5, alpha = 0.15)
	
	plt.axvline(survey_begin, ls = '--', color = 'red')
	plt.axvline(survey_end, ls = '--', color = 'red')
	
	plt.xlabel('MJD')
	plt.ylabel('5$\sigma$ limiting magnitude')
	
	plt.gca().invert_yaxis()
	plt.tight_layout()
	plt.savefig('results/' + results_directory + '/showSurveyTimeline.png')
	
	
	
	
	
	
	