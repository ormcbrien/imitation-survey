import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime
from progress.bar import Bar

import common_tools as ct
import data_generator as dg
import survey as sv
import output_plots as op
from common_tools import Kilonova

def main():

	(all_settings,
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
	results_directory) = ct.readSurveyParameters()
	
	if save_results:
		filewrite = ct.prepareResultsDirectory(save_results, results_directory)
	
	kilonova_df = pd.read_csv(kilonova_data_file)
	p_c, p_o = dg.fitKilonovaLightcurve(kilonova_df, lower_fit_time_limit, upper_fit_time_limit, polynomial_degree, plot_mode, save_results, results_directory)
	
	full_ATLAS_df = pd.read_csv(ATLAS_data_file, sep = '\s+')
	
	shell_weights, redshift_distribution = dg.getShellWeights(lower_redshift_limit, upper_redshift_limit, num_redshift_bins)
	band_weights, declination_distribution = dg.getBandWeights(lower_declination_limit, upper_declination_limit, declination_band_width)
	
	bar = Bar('Running simulation', max = sample_size)

	for i in range(0, sample_size):
# 		print('\n### KILONOVA %d' %i)
	
		kn = Kilonova()
		kn.setIterationNumber(i)
		kn.setExplosionEpoch(survey_begin, survey_end)
		
		lower_redshift_bound, upper_redshift_bound = dg.getRedshiftBounds(shell_weights, redshift_distribution)
		kn.setRedshift(lower_redshift_bound, upper_redshift_bound)
		
		lower_declination_bound, upper_declination_bound = dg.getDeclinationBounds(band_weights, declination_distribution)
		kn.setCoords(lower_declination_bound, upper_declination_bound)
# 		kn.info()
	
		partial_ATLAS_df = dg.filterAtlasDataFrameByExplosionEpoch(full_ATLAS_df, kn, lower_fit_time_limit, upper_fit_time_limit)
	
		if partial_ATLAS_df.empty and save_results == False:
			bar.next()
			continue
		elif partial_ATLAS_df.empty and save_results == True:
			kn.saveKilonova(filewrite, reason = 'No temporal coincidence')
			bar.next()
			continue

		partial_ATLAS_df = dg.filterAtlasDataFrameByCoords(partial_ATLAS_df, kn, plot_mode)
# 		print(partial_ATLAS_df)

		if partial_ATLAS_df.empty and save_results == False:
			bar.next()
			continue
		elif partial_ATLAS_df.empty and save_results == True:
			kn.saveKilonova(filewrite, reason = 'No spatial coincidence')
			bar.next()
			continue
		
		kn.generateLightcurve(p_c, p_o, partial_ATLAS_df, do_extinction)
# 		kn.showLightcurve()
	
		recovered_df = sv.recoverDetections(kn, partial_ATLAS_df, plot_mode, save_results, results_directory)
		
		count_df = sv.countDetections(recovered_df)
		
		kn.setDetectionStatus(count_df)

		if save_results and kn.detected:
			kn.saveKilonova(filewrite, reason = 'Detected')
		elif save_results and not kn.detected:
			kn.saveKilonova(filewrite, reason = 'Insufficient detections')
		
		bar.next()

	bar.finish()
	
	if save_results:	
		filewrite.close()		
	
		op.calculateDetectionEfficiency(all_settings)
		op.makeRedshiftDistribution(all_settings)
		op.makeCoordinateDistributionMap(all_settings)
		op.showSurveyTimeline(all_settings, full_ATLAS_df)
	
	
	return None



if __name__ == '__main__':
	main()