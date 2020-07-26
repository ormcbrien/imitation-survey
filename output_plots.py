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
	plt.ylabel('Number of kilonovae')

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

	fig = plt.figure(figsize = (12, 8))
	ax = fig.add_subplot(111, projection = 'mollweide')
	ax.grid(True)

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

	ra = results_df['ra']
	dec = results_df['dec']
	detected = results_df['detected']

	origin = 0

	RA = np.remainder(ra + 360 - origin, 360)
	ind = RA > 180
	RA[ind] -= 360
	RA = -RA

	xtick_labels = np.array([150, 120, 90, 60, 30, 0, 330, 300, 270, 240, 210])
	xtick_labels = np.remainder(xtick_labels + 360 - origin, 360)

	ytick_labels = np.array([-75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75])

	ax.scatter(np.radians(RA[~detected]), np.radians(dec[~detected]), s = 50, marker = 'o', c = 'lightgrey', edgecolors = 'grey')
	ax.scatter(np.radians(RA[detected]), np.radians(dec[detected]), s = 50, marker = 'o', c = 'red', edgecolors = 'black')

	ax.set_xlabel('Right ascension', **{'fontname': 'serif'}, fontsize = 20)
	ax.set_ylabel('Declination', **{'fontname': 'serif'}, fontsize = 20)

	ax.set_xticklabels(map(lambda x: '' + np.str(x) + '$^\circ$', xtick_labels))
	ax.set_yticklabels(map(lambda x: '' + np.str(x) + '$^\circ$', ytick_labels))
	# ax.set_xticklabels(tick_labels)

	ax.axhline(lower_declination_limit*np.pi/180., ls = '-', color = 'red')
	ax.axhline(upper_declination_limit*np.pi/180., ls = '-', color = 'red')

	plt.tight_layout()
	plt.savefig('results/' + results_directory + '/coordinateDistributionMap.pdf')
	plt.close()

# ========================================================================================

def showSurveyTimeline(all_settings, full_ATLAS_df):
	
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
	
	full_ATLAS_df_cyan = full_ATLAS_df.query('FILTER == "c"')
	full_ATLAS_df_orange = full_ATLAS_df.query('FILTER == "o"')
	
	plt.plot(full_ATLAS_df_cyan['MJDOBS'], full_ATLAS_df_cyan['MAG5SIG'], ls = 'None', marker = 'v', mfc = 'cyan', mec = None, ms = 5, alpha = 0.15)
	plt.plot(full_ATLAS_df_orange['MJDOBS'], full_ATLAS_df_orange['MAG5SIG'], ls = 'None', marker = 'v', mfc = 'orange', mec = None, ms = 5, alpha = 0.15)
	
	plt.axvline(survey_begin, ls = '-', color = 'red')
	plt.axvline(survey_end, ls = '-', color = 'red')
	
	plt.xlabel('MJD')
	plt.ylabel('5$\sigma$ limiting magnitude')
	
	plt.gca().invert_yaxis()
	plt.tight_layout()
	plt.savefig('results/' + results_directory + '/showSurveyTimeline.png')
	
	
	
	
	
	
	