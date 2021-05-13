import numpy as np
import matplotlib.pyplot as plt

"""
Plot meta-data
"""
SMALL_SIZE = 20
MEDIUM_SIZE = 25
BIGGER_SIZE = 30

plt.rc('font', size=SMALL_SIZE)          	# controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     	# fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    	# fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    	# fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    	# fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)    	# legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  	# fontsize of the figure title

plt.rcParams["font.family"] = "serif"
plt.rcParams['mathtext.fontset'] = 'dejavuserif'

fig, ax = plt.subplots(1, 1, figsize = (12,10))

"""
Plot meta-data end
"""

groups = ['LIGO O1',
		  'LIGO O2',
		  'LIGO O3a',
		  'ATLAS',
		  'ZTF',
		  'DLT40',
		  'DES',
		  'PTF',
		  'Fong et al. 2015',
		  'Della Valle et al. 2018',
		  'Coward et al. 2012',
		  'Jin et al. 2018',
		  'Dichiara et al. 2020',
		  'Chruslinksa et al. 2018',
		  'Kalogera et al. 2004',
		  'Kim et al. 2015',
		  'Pol et al. 2020']

rates_lower = {'LIGO O1': 0.,
			   'LIGO O2': 320.,
			   'LIGO O3a': 80.,
			   'ATLAS': 0.,
			   'ZTF': 0.,
			   'DLT40': 0.,
			   'DES': 0.,
			   'Fong et al. 2015': 90.,
			   'Della Valle et al. 2018': 71.,
			   'PTF': 0.,
			   'Coward et al. 2012': 630.,
			   'Jin et al. 2018': 452.,
			   'Dichiara et al. 2020': 60.,
			   'Chruslinksa et al. 2018': 300.,
			   'Kalogera et al. 2004': 169.,
			   'Kim et al. 2015': 70.,
			   'Pol et al. 2020': 260.}

rates_upper = {'LIGO O1': 12600.,
			   'LIGO O2': 4740.,
			   'LIGO O3a': 810.,
			   'ATLAS': 1520.,
			   'ZTF': 1775.,
			   'DLT40': 9.9e4,
			   'DES': 2.4e4,
			   'Fong et al. 2015': 1850.,
			   'Della Valle et al. 2018': 1162.,
			   'PTF': 800.,
			   'Coward et al. 2012': 1800.,
			   'Jin et al. 2018': 2541.,
			   'Dichiara et al. 2020': 360.,
			   'Chruslinksa et al. 2018': 1200.,
			   'Kalogera et al. 2004': 2921.,
			   'Kim et al. 2015': 70.,
			   'Pol et al. 2020': 610.}

# Colour key:
# 
# Optical      = royalblue
# GW           = limegreen
# GRB          = lightcoral
# Pop. synth   = grey
# Galactic DNS = gold

colours = {'LIGO O1': 'royalblue',
		   'LIGO O2': 'royalblue',
		   'LIGO O3a': 'royalblue',
		   'ATLAS': 'limegreen',
		   'ZTF': 'limegreen',
		   'DLT40': 'limegreen',
		   'DES': 'limegreen',
		   'PTF': 'limegreen',
		   'Fong et al. 2015': 'lightcoral',
		   'Della Valle et al. 2018': 'lightcoral',
		   'Coward et al. 2012': 'lightcoral',
		   'Jin et al. 2018': 'lightcoral',
		   'Dichiara et al. 2020': 'lightcoral',
		   'Chruslinksa et al. 2018': 'grey',
		   'Kalogera et al. 2004': 'gold',
		   'Kim et al. 2015': 'gold',
		   'Pol et al. 2020': 'gold'}

for group in groups:
	ax.barh([group], width = rates_upper[group], left = rates_lower[group], facecolor = colours[group], edgecolor = 'black')

ax.axvspan(0., 0., facecolor = 'royalblue', edgecolor = 'black', label = 'GW')
ax.axvspan(0., 0., facecolor = 'limegreen', edgecolor = 'black', label = 'Optical')
ax.axvspan(0., 0., facecolor = 'lightcoral', edgecolor = 'black', label = 'sGRB')
ax.axvspan(0., 0., facecolor = 'grey', edgecolor = 'black', label = 'Pop. synthesis')
ax.axvspan(0., 0., facecolor = 'gold', edgecolor = 'black', label = 'Galactic DNS')

the_legend = ax.legend(loc = 'upper right', frameon = True, ncol = 1)
the_legend.get_frame().set_edgecolor('black')

ax.set_xlim([1e1, 2e6])

ax.set_xscale('log')

ax.set_xlabel('Rate, $\mathrm{Gpc^{-3}\,yr^{-1}}$')

plt.yticks(rotation = 45.)
# ax.set_ylabel('Group')

fig.tight_layout()
plt.savefig('makeRateEstimateComparisonPlot.pdf')
plt.show()