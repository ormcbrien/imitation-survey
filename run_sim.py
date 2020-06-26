import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import common_tools as ct
import data_generator as dg
from common_tools import Kilonova

def main():

	(all_settings,
	survey_begin,
	survey_end,
	lower_redshift_limit,
	upper_redshift_limit,
	num_redshift_bins,
	ATLAS_data_file) = ct.readSurveyParameters()
	
	full_ATLAS_df = pd.read_csv(ATLAS_data_file, sep = '\s+')
	
	shell_weights, redshift_distribution = dg.getShellWeights(lower_redshift_limit, upper_redshift_limit, num_redshift_bins)

# Main loop needs to begin here
	
	kn = Kilonova()
	kn.setExplosionEpoch(survey_begin, survey_end)
	kn.setCoords()
	lower_redshift_bound, upper_redshift_bound = dg.getRedshiftBounds(shell_weights, redshift_distribution)
	kn.setRedshift(lower_redshift_bound, upper_redshift_bound)
	kn.info()
	
	partial_ATLAS_df = dg.filterAtlasDataFrameByExplosionEpoch(full_ATLAS_df, kn)
# 	print(partial_ATLAS_df.sort_values(by = ['RA']))
	
	partial_ATLAS_df = dg.filterAtlasDataFrameByCoords(partial_ATLAS_df, kn)
	print(partial_ATLAS_df)
	
	
	
	return None



if __name__ == '__main__':
	main()