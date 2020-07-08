import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def recoverDetections(kn, partial_ATLAS_df, plot_mode = False):
	
	cyan_partial_ATLAS_df = partial_ATLAS_df.query('FILTER == "c"')
	orange_partial_ATLAS_df = partial_ATLAS_df.query('FILTER == "o"')
	
	cyan_overlap = cyan_partial_ATLAS_df['MAG5SIG'].ge(other = kn.mag_c)
	orange_overlap = orange_partial_ATLAS_df['MAG5SIG'].ge(other = kn.mag_o)
	
# 	for alpha, bravo in zip(kn.timeline_c[cyan_overlap], kn.mag_c[cyan_overlap]):
# 		print(alpha, bravo)
# 	
# 	for alpha, bravo in zip(kn.timeline_o[orange_overlap], kn.mag_o[orange_overlap]):
# 		print(alpha, bravo)

	recovered_timeline_cyan, recovered_mag_cyan = kn.timeline_c[cyan_overlap], kn.mag_c[cyan_overlap]
	recovered_timeline_orange, recovered_mag_orange = kn.timeline_o[orange_overlap], kn.mag_o[orange_overlap]
	
	
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
	
		plt.plot(cyan_partial_ATLAS_df['MJDOBS'], cyan_partial_ATLAS_df['MAG5SIG'], ls = 'None', marker = 'v', mfc = 'cyan', mec = 'black', ms = 8)
		plt.plot(orange_partial_ATLAS_df['MJDOBS'], orange_partial_ATLAS_df['MAG5SIG'], ls = 'None', marker = 'v', mfc = 'orange', mec = 'black', ms = 8)
	
		plt.plot(kn.timeline_c, kn.mag_c, ls = 'None', marker = 'o', mfc = 'cyan', mec = 'black', ms = 8)
		plt.plot(kn.timeline_o, kn.mag_o, ls = 'None', marker = 'o', mfc = 'orange', mec = 'black', ms = 8)
	
		plt.plot(recovered_timeline_cyan, recovered_mag_cyan, ls = 'None', marker = 'o', mfc = 'None', mec = 'green', ms = 12)
		plt.plot(recovered_timeline_orange, recovered_mag_orange, ls = 'None', marker = 'o', mfc = 'None', mec = 'red', ms = 12)
	
		plt.xlabel('MJD')
		plt.ylabel('Magnitude')
		plt.title('MJD %f, $z = %f$' %(kn.expl_epoch, kn.redshift))
		plt.gca().invert_yaxis()
		plt.show()

	recovered_cyan_df = pd.DataFrame({'recovered_timeline': recovered_timeline_cyan, 'recovered_mag': recovered_mag_cyan, 'recovered_filter': np.full_like(recovered_mag_cyan, 'c', dtype = str)})
	recovered_orange_df = pd.DataFrame({'recovered_timeline': recovered_timeline_orange, 'recovered_mag': recovered_mag_orange, 'recovered_filter': np.full_like(recovered_mag_orange, 'o', dtype = str)})

	recovered_df = pd.concat([recovered_cyan_df, recovered_orange_df])
	
# 	print(recovered_cyan_df)
# 	print(recovered_orange_df)
	print(recovered_df)

	return recovered_df

# ========================================================================================

def countDetections(recovered_df):
	
	timeline = recovered_df['recovered_timeline']
	timeline_floor = np.floor(timeline)
	
	unique_days = np.array( list( set( list( np.floor(timeline) ) ) ) )
	unique_days_count = np.empty_like(unique_days, dtype = int)
	
	for i, unique_day in enumerate(unique_days):
	
		nightly_detection_count = 0
	
		for j, timeline_floor_day in enumerate(timeline_floor):
		
			if unique_day == timeline_floor_day:
				
				nightly_detection_count += 1
			
		unique_days_count[i] = nightly_detection_count

	count_df = pd.DataFrame({'nights': unique_days, 'detection_count': unique_days_count})
	count_df = count_df.sort_values(by = 'nights')
	print(count_df)
	
	return count_df







