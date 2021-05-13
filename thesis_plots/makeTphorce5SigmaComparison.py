import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def STRAIGHT_LINE(x, m, c):

	return m * x + c

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

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize = (20,20))

plot_colour = ['limegreen', 'lightcoral', 'khaki']
tphorce_file = ['../transients/AT2017gfo_tphorce.csv', 'NGC4993.csv', 'NGC4993_5arcsec.csv']

"""
Plot meta-data end
"""

for i in range(0, 3):

	tphorce_df = pd.read_csv(tphorce_file[i])

	MAG5SIG = np.array(tphorce_df['mag5sig'])
	duJy = np.array(tphorce_df['duJy'])

	ind1 = np.where(np.isfinite(duJy))
	MAG5SIG = MAG5SIG[ind1]
	duJy = duJy[ind1]

	derived_mag5sig = -2.5 * np.log10(5 * duJy) + 23.9

	ind2 = np.where(MAG5SIG >= 17.0)
	MAG5SIG = MAG5SIG[ind2]
	derived_mag5sig = derived_mag5sig[ind2]

	diff_mag5sig = derived_mag5sig - MAG5SIG

	ind3 = np.where(abs(diff_mag5sig) <= 0.5)
	MAG5SIG = MAG5SIG[ind3]
	diff_mag5sig = diff_mag5sig[ind3]

	# Scatter plot
	ax1.plot(MAG5SIG, diff_mag5sig, ls = 'None', marker = 'o', mfc = plot_colour[i], mec = 'black', ms = 6, zorder = 1000, alpha = 0.6)

	# Hisotgram
	if i == 0:
	
		ax2.hist(diff_mag5sig, color = plot_colour[i], edgecolor = 'black', bins = 40)

		ax2.set_xlabel('5$\sigma$ limit (derived from d$\mu$Jy) $-$ MAG5SIG')
		ax2.set_ylabel('Frequency')

		std_dev = np.std(diff_mag5sig)
		median = np.median(diff_mag5sig)
		mean = np.mean(diff_mag5sig)

		ax2.annotate('$\delta_x = %.2f$\n$\^x = %.2f$\n$\mu_x = %.2f$' %(std_dev, median, mean), xy = (0.1, 0.7), xycoords = 'axes fraction', fontsize = 'x-large')

	if i == 1:
	
		ax3.hist(diff_mag5sig, color = plot_colour[i], edgecolor = 'black', bins = 40)

		ax3.set_xlabel('5$\sigma$ limit (derived from d$\mu$Jy) $-$ MAG5SIG')
		ax3.set_ylabel('Frequency')

		std_dev = np.std(diff_mag5sig)
		median = np.median(diff_mag5sig)
		mean = np.mean(diff_mag5sig)

		ax3.annotate('$\delta_x = %.2f$\n$\^x = %.2f$\n$\mu_x = %.2f$' %(std_dev, median, mean), xy = (0.1, 0.7), xycoords = 'axes fraction', fontsize = 'x-large')

	if i == 2:
	
		ax4.hist(diff_mag5sig, color = plot_colour[i], edgecolor = 'black', bins = 40)

		ax4.set_xlabel('5$\sigma$ limit (derived from d$\mu$Jy) $-$ MAG5SIG')
		ax4.set_ylabel('Frequency')

		std_dev = np.std(diff_mag5sig)
		median = np.median(diff_mag5sig)
		mean = np.mean(diff_mag5sig)

		ax4.annotate('$\delta_x = %.2f$\n$\^x = %.2f$\n$\mu_x = %.2f$' %(std_dev, median, mean), xy = (0.1, 0.7), xycoords = 'axes fraction', fontsize = 'x-large')


ax1.axhline(0.0, linestyle = '--', color = 'black', linewidth = 0.8)

ax1.set_xlabel('MAG5SIG')
ax1.set_ylabel('5$\sigma$ limit (derived from d$\mu$Jy) $-$ MAG5SIG')

# Titles for plots:
ax2.set_title('At location of AT2017gfo')
ax3.set_title('At location of NGC4993')
ax4.set_title("Offset ~5'' from galaxy core")




plt.tight_layout()
plt.savefig('makeTphorce5SigmaComparison_grid.pdf')
plt.show()
