import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import sncosmo
import pandas as pd

def app2abs(mag, z):
	
	c = 3.e5
	H0 = 70.
	
	Mag = mag - 5 * (np.log10(c*z/H0) + 5)
	
	return Mag

"""
Plot meta-data
"""

SMALL_SIZE = 20
MEDIUM_SIZE = 25
BIGGER_SIZE = 30

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

"""
Plot meta-data end
"""

cyan_flt = np.loadtxt('/Users/omcbrien/PhD/ATLAS/transient_science/filters/btucker_compilation/ATLAS/ATLAS_c.dat')
oran_flt = np.loadtxt('/Users/omcbrien/PhD/ATLAS/transient_science/filters/btucker_compilation/ATLAS/ATLAS_o.dat')

band_c = sncosmo.Bandpass(cyan_flt[:,0], cyan_flt[:,1], name = 'atlasc')
band_o = sncosmo.Bandpass(oran_flt[:,0], oran_flt[:,1], name = 'atlaso')

nobs = 70
t0 = 0.
duration = 120.
z = 0.6

t_obs = np.linspace(t0 - 20., t0 + duration, nobs)

model1 = sncosmo.Model(source='hsiao')
# model1.update({'z': z, 't0': t0, 'x0': 1.e-5, 'x1': 0.1, 'c': -0.1})
model1.update({'z': z, 't0': t0})
model1.set_source_peakabsmag(-19.0, band_c, 'ab')
# print(model1.parameters)

mag_c = model1.bandmag(band_c, 'ab', t_obs)
mag_o = model1.bandmag(band_o, 'ab', t_obs)
# print(mag_c)

Mag_c = app2abs(mag_c, z)
Mag_o = app2abs(mag_o, z)


plt.plot(t_obs, Mag_c, ls = '-', color = 'cyan', label = 'ATLAS $c$', linewidth = 3, path_effects = [pe.Stroke(linewidth = 4, foreground = 'black'), pe.Normal()])
plt.plot(t_obs, Mag_o, ls = '-', color = 'orange', label = 'ATLAS $o$', linewidth = 3, path_effects = [pe.Stroke(linewidth = 4, foreground = 'black'), pe.Normal()])

plt.legend(ncol = 1, loc = 'upper right', frameon = False)

plt.xlabel('Phase, days')
plt.ylabel('Magnitude')

plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('generateTypeIaLightcurve.pdf')
plt.show()

df = pd.DataFrame({'phase': t_obs, 'c': Mag_c, 'cerr': np.full_like(Mag_c, 0.3), 'o': Mag_o, 'oerr': np.full_like(Mag_o, 0.3)})
df.to_csv('../transients/abs_templateIa-hsiao.csv')

# lcs = sncosmo.realize_lcs(obs, model1, [params])
# print(type(lcs))
# print(lcs[0]['flux'])








