import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Plot meta-data
"""

SMALL_SIZE = 15
MEDIUM_SIZE = 20
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

fig = plt.figure(figsize = (12, 5))
ax = fig.add_subplot(111, projection = 'mollweide')
ax.grid(True)


"""
Plot meta-data end
"""

QC_file = '../QC/QC_all_data_kws_57308_59024_20200624_merged_daves_moving_object_database_data.dat'
QC_df = pd.read_csv(QC_file, sep = '\s+')

ra = np.array(QC_df['RA'])
dec = np.array(QC_df['DEC'])

# Fixing plot axes for sky projection
origin = 0

RA = np.remainder(ra + 360 - origin, 360)
ind = RA > 180
RA[ind] -= 360
RA = -RA

RA = RA * np.pi / 180.
dec = dec * np.pi / 180.

xtick_labels = np.array([150, 120, 90, 60, 30, 0, 330, 300, 270, 240, 210])
xtick_labels = np.remainder(xtick_labels + 360 - origin, 360)

ytick_labels = np.array([-75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75])

ax.set_xlabel('Right ascension')
ax.set_ylabel('Declination')

ax.set_xticklabels(map(lambda x: '' + np.str(x) + '$^\circ$', xtick_labels))
ax.set_yticklabels(map(lambda x: '' + np.str(x) + '$^\circ$', ytick_labels))
# That's better

hb = ax.hexbin(RA, dec, cmap = plt.cm.viridis, gridsize = 30, bins = None, vmin = 0, vmax = 2500)
cb = fig.colorbar(hb, ax = ax)

fig.tight_layout()
plt.savefig('make2DHistogramOfPointings.pdf')
plt.show()