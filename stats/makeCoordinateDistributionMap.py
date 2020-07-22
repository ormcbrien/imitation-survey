import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yaml

with open('../settings.yaml', 'r') as stream:
	all_settings = yaml.safe_load(stream)


"""
Plot meta-data
"""

SMALL_SIZE = 15
MEDIUM_SIZE = 20
BIGGER_SIZE = 25

fig = plt.figure(figsize = (12, 10))
ax = fig.add_subplot(111, projection = 'aitoff')
ax.grid(True)

plt.rc('font', size=SMALL_SIZE)          	# controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     	# fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    	# fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    	# fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    	# fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)    	# legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  	# fontsize of the figure title

plt.rcParams["font.family"] = "serif"
plt.rcParams['mathtext.fontset'] = 'dejavuserif'

"""
Plot meta-data end
"""

results_file = '../results/results_2020-07-22_13-25-37.csv'
results_df = pd.read_csv(results_file)

ra = results_df['ra']
dec = results_df['dec']
detected = results_df['detected']

origin = 0

RA = np.remainder(ra + 360 - origin, 360)
ind = RA > 180
RA[ind] -= 360
RA = -RA

xtick_labels = np.array([150, 120, 90, 60, 30, 0, 330, 300, 270, 240, 210])
xtick_labels = np.remainder(xtick_labels + 360 - origin, 360)

ytick_labels = np.array([-75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75])

ax.scatter(np.radians(RA), np.radians(dec), s = 50, marker = 'o', c = 'green', edgecolors = 'black')
ax.scatter(np.radians(RA[detected]), np.radians(dec[detected]), s = 80, marker = 'o', c = 'None', edgecolors = 'red')

ax.set_xlabel('Right Ascension', **{'fontname': 'serif'}, fontsize = 20)
ax.set_ylabel('Declination', **{'fontname': 'serif'}, fontsize = 20)

ax.set_xticklabels(map(lambda x: '' + np.str(x) + '$^\circ$', xtick_labels))
ax.set_yticklabels(map(lambda x: '' + np.str(x) + '$^\circ$', ytick_labels))
# ax.set_xticklabels(tick_labels)

plt.show()



