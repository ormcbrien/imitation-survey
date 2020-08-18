import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import time
from datetime import datetime
from progress.bar import Bar

import common_tools as ct
import data_generator as dg
import survey as sv
import output_plots as op
from common_tools import Transient

def main():

	# READ SETTINGS FILE
	begin_time = time.time()

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
	QC_file,
	QC_columns,
	chipwidth,
	transient_data_file,
	lower_fit_time_limit,
	upper_fit_time_limit,
	polynomial_degree,
	do_extinction,
	plot_mode,
	save_results,
	results_directory,
	flavour_mode) = ct.readSurveyParameters()
	
	
	if save_results:
		filewrite = ct.prepareResultsDirectory(save_results, results_directory)
	
	settings_time = time.time()
	
	# FIT TEMPLATE LIGHTCURVE	
	transient_df = pd.read_csv(transient_data_file)
	p_c, p_o = dg.fitTransientLightcurve(transient_df, lower_fit_time_limit, upper_fit_time_limit, polynomial_degree, save_results, results_directory)
	
	template_time = time.time()
	
	# READ QC FILE CONTENTS	
	full_QC_df = pd.read_csv(QC_file, sep = '\s+', usecols = QC_columns.values())
	
	qc_time = time.time()
	
	# CALCULATE SHELL AND BAND WEIGHTS
	shell_weights, redshift_distribution = dg.getShellWeights(lower_redshift_limit, upper_redshift_limit, num_redshift_bins)
	band_weights, declination_distribution = dg.getBandWeights(lower_declination_limit, upper_declination_limit, declination_band_width)
	
	weights_time = time.time()

	# CREATE PROGRESS BAR AND RUN SIMULATION
	
	if flavour_mode:
		bar = Bar('%s' %ct.getFlavourText(), max = sample_size)
	elif not flavour_mode:
		bar = Bar('Running simulation...', max = sample_size)

	for i in range(0, sample_size):
	
		transient = Transient()
		transient.setIterationNumber(i)
		transient.setExplosionEpoch(survey_begin, survey_end)
		
		lower_redshift_bound, upper_redshift_bound = dg.getRedshiftBounds(shell_weights, redshift_distribution)
		transient.setRedshift(lower_redshift_bound, upper_redshift_bound)
		
		lower_declination_bound, upper_declination_bound = dg.getDeclinationBounds(band_weights, declination_distribution)
		transient.setCoords(lower_declination_bound, upper_declination_bound)
	
		partial_QC_df = dg.filterQualityControlDataFrameByExplosionEpoch(full_QC_df, QC_columns, transient, lower_fit_time_limit, upper_fit_time_limit)
	
		if partial_QC_df.empty and save_results == False:
			bar.next()
			continue
		elif partial_QC_df.empty and save_results == True:
			transient.saveTransient(filewrite, reason = 'No temporal coincidence')
			bar.next()
			continue

		partial_QC_df = dg.filterQualityControlDataFrameByCoords(partial_QC_df, QC_columns, transient, chipwidth, plot_mode)

		if partial_QC_df.empty and save_results == False:
			bar.next()
			continue
		elif partial_QC_df.empty and save_results == True:
			transient.saveTransient(filewrite, reason = 'No spatial coincidence')
			bar.next()
			continue
		
		transient.generateLightcurve(p_c, p_o, partial_QC_df, QC_columns, do_extinction)
	
		recovered_df = sv.recoverDetections(transient, partial_QC_df, QC_columns, plot_mode, save_results, results_directory)
		
		count_df = sv.countDetections(recovered_df)
		
		transient.setDetectionStatus(count_df)

		if save_results and transient.detected:
			transient.saveTransient(filewrite, reason = 'Detected')
		elif save_results and not transient.detected:
			transient.saveTransient(filewrite, reason = 'Insufficient detections')
		
		bar.next()

	bar.finish()
	
	simulation_time = time.time()
	
	print('Settings read in %.2f s' %(settings_time - begin_time))
	print('Template lightcurve fit in %.2f s' %(template_time - settings_time))
	print('QC file read in %.2f s' %(qc_time - template_time))
	print('Weights calculated in %.2f s' %(weights_time - qc_time))
	print('Simulation ran in %.2f s' %(simulation_time - weights_time))
	
	# SAVE RESULTS AND MAKE FINAL PLOTS
	
	if save_results:	
		filewrite.close()		
	
		op.calculateDetectionEfficiency(all_settings)
		op.makeRedshiftDistribution(all_settings)
		op.makeCoordinateDistributionMap(all_settings)
		op.showSurveyTimeline(all_settings, full_QC_df, QC_columns)
	
		save_time = time.time()
		
		print('Results plots produced in %.2f s' %(save_time - simulation_time))
		
	return None



if __name__ == '__main__':
	main()