import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def plotLightcurve(obj_data, cyan_detlim = 19.3, orange_detlim = 18.7, showLimits = True):

	SMALL_SIZE = 14
	MEDIUM_SIZE = 18
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
	

	fig = plt.figure(figsize = (12,10))

	plt.errorbar(obj_data['mjd'], obj_data['c'], obj_data['cerr'], marker = 'o', ls = 'None', ms = 8, mfc = 'cyan', mec = 'black', mew = 0.75, ecolor = 'black', capsize = 5, capthick = 2, label = 'ATLAS c')
	plt.errorbar(obj_data['mjd'], obj_data['o'], obj_data['oerr'], marker = 'o', ls = 'None', ms = 8, mfc = 'orange', mec = 'black', mew = 0.75, ecolor = 'black', capsize = 5, capthick = 2, label = 'ATLAS o')

	if showLimits:
		plt.axhline(cyan_detlim, ls = '--', color = 'cyan')
		plt.axhline(orange_detlim, ls = '--', color = 'orange')

	plt.xlabel('MJD')
	plt.ylabel('Magnitude')

	plt.legend(loc = 'upper right', ncol = 1, frameon = False)

	plt.gca().invert_yaxis()
	plt.tight_layout()

	return fig

# ########################################################################################

def getAbsoluteLightcurve(obj_data, redshift = 0.00984, H0 = 70, c = 3e5):

	c_abs = obj_data['c'] - 5*np.log10(c * redshift * 1e6 / H0) + 5
	o_abs = obj_data['o'] - 5*np.log10(c * redshift * 1e6 / H0) + 5
	
	obj_data['c'] = pd.Series(c_abs, index = obj_data.index)
	obj_data['o'] = pd.Series(o_abs, index = obj_data.index)

	return obj_data
	
# ########################################################################################

def fitLightcurve(obj_data, spline_kind = 'linear'):

	obj_data = obj_data.dropna(axis = 0, how = 'any')

	interp_c = interp1d(obj_data['mjd'], obj_data['c'], kind = spline_kind)
	interp_o = interp1d(obj_data['mjd'], obj_data['o'], kind = spline_kind)

	return interp_c, interp_o

# ########################################################################################

def plotInterpolatedLightcurve(interp_data, colour):

	SMALL_SIZE = 14
	MEDIUM_SIZE = 18
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
	
	fig = plt.figure(figsize = (12,10))

	plt.plot(interp_data['mjd'], interp_data['interp_mag'], ls = '-', color = colour)

	plt.xlabel('Time, days')
	plt.ylabel('Magnitude')

	plt.gca().invert_yaxis()
	plt.tight_layout()

	return fig
	
# ########################################################################################

def inflateLightcurve(obj_data, redshift, c = 3e5, H0 = 70):
	
	dist_mod = 5*np.log10(c * redshift * 1e6 / H0) - 5
	
	obj_data_app = pd.DataFrame({'mjd': obj_data['mjd'], 'interp_mag': obj_data['interp_mag'] + dist_mod})
	
	return obj_data_app