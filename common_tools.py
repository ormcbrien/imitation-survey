import os
import shutil
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import astropy.units as u
from astropy.coordinates import SkyCoord
from dustmaps.config import config
import dustmaps.sfd
from dustmaps.sfd import SFDQuery

def abs2app(abs_mag, redshift):

	c = 2.99792458e5 # Speed of light in km/s
	H_0 = 70.0		 # Hubble constant (km/s/Mpc)

	app_mag = 5*np.log10(1.e6 * (c * redshift / H_0)) - 5 + abs_mag

	return app_mag


class Kilonova():

	def __init__(self, iteration = None, redshift = None, ra = None, dec = None, expl_epoch = None, timeline_c = None, timeline_o = None, mag_c = None, mag_o = None, extinction_c = 0.0, extinction_o = 0.0, detected = False, detection_count = 0, reason = 'None'):
		
		self.iteration = iteration
		self.redshift = redshift
		self.ra = ra
		self.dec = dec
		self.expl_epoch = expl_epoch
		self.timeline_c = timeline_c
		self.timeline_o = timeline_o
		self.mag_c = mag_c
		self.mag_o = mag_o
		self.extinction_c = extinction_c
		self.extinction_o = extinction_o
		self.detected = detected
		self.detection_count = detection_count
		self.reason = reason
	
	def setIterationNumber(self, iteration):
		
		self.iteration = iteration
	
	def setExplosionEpoch(self, survey_begin, survey_end):

		self.expl_epoch = random.uniform(survey_begin, survey_end)
		
	def setCoords(self, lower_declination_bound, upper_declination_bound):
	
		self.ra = random.uniform(0.0, 360.0)
		self.dec = random.uniform(lower_declination_bound, upper_declination_bound)
		
	def setRedshift(self, lower_redshift_bound, upper_redshift_bound):
	
		self.redshift = random.uniform(lower_redshift_bound, upper_redshift_bound)
		
	def generateLightcurve(self, p_c, p_o, partial_ATLAS_df, do_extinction = False):

		cyan_partial_ATLAS_df = partial_ATLAS_df.query('FILTER == "c"')
		orange_partial_ATLAS_df = partial_ATLAS_df.query('FILTER == "o"')

		phase_c = cyan_partial_ATLAS_df['MJDOBS'] - self.expl_epoch
		phase_o = orange_partial_ATLAS_df['MJDOBS'] - self.expl_epoch
	
		mag_c = abs2app(p_c(phase_c), self.redshift)
		mag_o = abs2app(p_o(phase_o), self.redshift)
		
		if do_extinction:
		
			dustmaps_path = os.path.dirname(os.path.abspath(dustmaps.__file__))
# 			print(dustmaps_path)

			if not os.path.exists(os.path.join(dustmaps_path, "DustMaps/")):
				config["data_dir"] = "{pathToSource}/DustMaps/".format(pathToSource = dustmaps_path)
				#Downloading dustmap for galactic extinction from Schlafly & Finkbeiner (SFD; 2011)
				dustmaps.sfd.fetch()
			else:
				config["data_dir"] = "{pathToSource}/DustMaps/".format(pathToSource = dustmaps_path)
			
			#Setting the extraction query for the SFD Dustmap
			coords = SkyCoord(self.ra * u.deg, self.dec * u.deg, frame = 'icrs')
			extinction_map = SFDQuery()
			ebv = extinction_map(coords)
		
			A_g = ebv * 3.172
			A_r = ebv * 2.271
			A_i = ebv * 1.682

			A_c = (A_g + A_r) / 2.
			A_o = (A_r + A_i) / 2.
		
		else:
		
			A_c = 0.0
			A_o = 0.0
		
		self.timeline_c = phase_c + self.expl_epoch
		self.timeline_o = phase_o + self.expl_epoch
		self.mag_c = mag_c + A_c
		self.mag_o = mag_o + A_o
		self.extinction_c = A_c
		self.extinction_o = A_o
		
	def setDetectionStatus(self, count_df):
	
		if (count_df['detection_count'] >= 3).any():
			self.detected = True
		
		self.detection_count = count_df['detection_count'].sum()
		

	def saveKilonova(self, filewrite, reason):
	
		filewrite.write('%d,%f,%f,%f,%f,%f,%f,%s,%d,%s\n' %(self.iteration, self.redshift, self.ra, self.dec, self.expl_epoch, self.extinction_c, self.extinction_o, self.detected, self.detection_count, reason))
	
	def info(self):
	
		print('z   = %f' %self.redshift)
		print('t_0 = MJD %f' %self.expl_epoch)
		print('RA  = %f degrees' %self.ra)
		print('Dec = %f degrees' %self.dec)
	
	def showLightcurve(self):
		
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
		
		plt.plot(self.timeline_c, self.mag_c, marker = 'o', ms = 8, mfc = 'cyan', mec = 'black', ls = '--', color = 'cyan')
		plt.plot(self.timeline_o, self.mag_o, marker = 'o', ms = 8, mfc = 'orange', mec = 'black', ls = '--', color = 'orange')
	
		plt.gca().invert_yaxis()
		plt.xlabel('MJD')
		plt.ylabel('Magnitude')
		plt.title('MJD %f, $z = %f$' %(self.expl_epoch, self.redshift))
		plt.show()

# ========================================================================================

def readSurveyParameters():

	import yaml
	
	with open('settings.yaml', 'r') as stream:
		all_settings = yaml.safe_load(stream)
	
	survey_begin = all_settings['survey_begin']
	survey_end = all_settings['survey_end']
	lower_declination_limit = all_settings['lower_declination_limit']
	upper_declination_limit = all_settings['upper_declination_limit']
	declination_band_width = all_settings['declination_band_width']
	lower_redshift_limit = all_settings['lower_redshift_limit']
	upper_redshift_limit = all_settings['upper_redshift_limit']
	num_redshift_bins = all_settings['num_redshift_bins']
	sample_size = all_settings['sample_size']
	ATLAS_data_file = all_settings['ATLAS_data_file']
	kilonova_data_file = all_settings['kilonova_data_file']
	lower_fit_time_limit = all_settings['lower_fit_time_limit']
	upper_fit_time_limit = all_settings['upper_fit_time_limit']
	polynomial_degree = all_settings['polynomial_degree']
	do_extinction = all_settings['do_extinction']
	plot_mode = all_settings['plot_mode']
	save_results = all_settings['save_results']
	results_directory = all_settings['results_directory']


	survey_parameters = (all_settings,
							survey_begin,
							survey_end,
							lower_declination_limit,
							upper_declination_limit,
							declination_band_width,
							lower_redshift_limit,
							upper_redshift_limit,
							num_redshift_bins,
							sample_size,
							ATLAS_data_file,
							kilonova_data_file,
							lower_fit_time_limit,
							upper_fit_time_limit,
							polynomial_degree,
							do_extinction,
							plot_mode,
							save_results,
							results_directory)

	return survey_parameters

# ========================================================================================

def prepareResultsDirectory(save_results, results_directory):

	if not os.path.exists('results'):
		os.mkdir('results')
		
	abs_results_directory = os.path.join(os.getcwd(), 'results', results_directory)
	shutil.rmtree(abs_results_directory)
	os.mkdir(abs_results_directory)
	
	os.mkdir(os.path.join(abs_results_directory, 'plots'))
# 	os.mkdir(os.path.join(abs_results_directory, 'weights'))
	
	filewrite = open(os.path.join(abs_results_directory, 'population.csv'), 'a')
	filewrite.write('number,redshift,ra,dec,expl_epoch,extinction_c,extinction_o,detected,detection_count,reason\n')
	
	os.system('cp settings.yaml %s' %abs_results_directory)
	
	return filewrite
	

if __name__ == '__main__':
	main()