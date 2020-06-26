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

def filterAtlasDataFrameByExplosionEpoch(full_ATLAS_df, Kilonova):

	lower_expl_epoch_bound = Kilonova.expl_epoch - 2.0
	upper_expl_epoch_bound = Kilonova.expl_epoch + 15.0
	
	partial_ATLAS_df = full_ATLAS_df.query('MJDOBS >= %f & MJDOBS <= %f' %(lower_expl_epoch_bound, upper_expl_epoch_bound))

	return partial_ATLAS_df
	
def filterAtlasDataFrameByCoords(partial_ATLAS_df, Kilonova):

	ATLAS_chip_halfwidth = 5.4 # degrees
	
	max_allowed_ra = 360.
	min_allowed_ra = 0.
# 	max_allowed_dec = 90.
# 	min_allowed_dec = -90.

	upper_kn_ra_bound = Kilonova.ra + ATLAS_chip_halfwidth
	lower_kn_ra_bound = Kilonova.ra - ATLAS_chip_halfwidth
	upper_kn_dec_bound = Kilonova.dec + ATLAS_chip_halfwidth
	lower_kn_dec_bound = Kilonova.dec - ATLAS_chip_halfwidth
	
	# Filter RA first as it wraps (360 --> 0 degrees)
	if upper_kn_ra_bound > max_allowed_ra:
	
		partial_ATLAS_df = partial_ATLAS_df.query('RA >= %f | RA <= %f' %(lower_kn_ra_bound, upper_kn_ra_bound - max_allowed_ra))
	
	elif lower_kn_ra_bound < min_allowed_ra:
	
		partial_ATLAS_df = partial_ATLAS_df.query('RA >= %f | RA <= %f' %(lower_kn_ra_bound + max_allowed_ra, upper_kn_ra_bound - max_allowed_ra))
	
	else:

		partial_ATLAS_df = partial_ATLAS_df.query('RA >= %f & RA <= %f' %(lower_kn_ra_bound, upper_kn_ra_bound))
	
	# Now filter by DEC
	partial_ATLAS_df = partial_ATLAS_df.query('DEC >= %f & DEC <= %f' %(lower_kn_dec_bound, upper_kn_dec_bound))
	
# 	partial_ATLAS_df = partial_ATLAS_df.query('RA >= %f & RA <= %f & DEC >= %f & DEC <= %f' %(lower_kn_ra_bound, upper_kn_ra_bound, lower_kn_dec_bound, upper_kn_dec_bound))

	return partial_ATLAS_df



















