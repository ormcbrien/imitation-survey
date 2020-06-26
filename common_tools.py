import random

class Kilonova():

	def __init__(self, redshift = None, ra = None, dec = None, expl_epoch = None):
		
		self.redshift = redshift
		self.ra = ra
		self.dec = dec
		self.expl_epoch = expl_epoch
	
	def setExplosionEpoch(self, survey_begin, survey_end):

		self.expl_epoch = random.uniform(survey_begin, survey_end)
		
	def setCoords(self):
	
		self.ra = random.uniform(0.0, 360.0)
		self.dec = random.uniform(-90.0, 90.0)
		
	def setRedshift(self, lower_redshift_bound, upper_redshift_bound):
	
		self.redshift = random.uniform(lower_redshift_bound, upper_redshift_bound)
		
	def info(self):
	
		print('z   = %f' %self.redshift)
		print('t_0 = MJD %f' %self.expl_epoch)
		print('RA  = %f degrees' %self.ra)
		print('Dec = %f degrees' %self.dec)

def readSurveyParameters():

	import yaml
	
	with open('settings.yaml', 'r') as stream:
		all_settings = yaml.safe_load(stream)
	
	survey_begin = all_settings['survey_begin']
	survey_end = all_settings['survey_end']
	lower_redshift_limit = all_settings['lower_redshift_limit']
	upper_redshift_limit = all_settings['upper_redshift_limit']
	num_redshift_bins = all_settings['num_redshift_bins']
	ATLAS_data_file = all_settings['ATLAS_data_file']


	survey_parameters = (all_settings,
							survey_begin,
							survey_end,
							lower_redshift_limit,
							upper_redshift_limit,
							num_redshift_bins,
							ATLAS_data_file)

	return survey_parameters

if __name__ == '__main__':
	main()