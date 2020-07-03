import pandas as pd
import numpy as np

def app2abs(mag, filter):

	d = 40.
	
	A_g = 0.407
	A_r = 0.282
	A_i = 0.209
	
	if filter == 'g':
		A = A_g
	elif filter == 'r':
		A = A_r
	elif filter == 'i':
		A = A_i
	elif filter == 'c':
		A = (A_g + A_r) / 2.
	elif filter == 'o':
		A = (A_r + A_i) / 2.
	
	return mag - 5*np.log10(d) - 25 - A

df = pd.read_csv('app_AT2017gfo.csv')
print(df)

df_out = pd.DataFrame({'phase': df['phase'],
					   'g': app2abs(df['g'], 'g'), 
					   'gerr': df['gerr'], 
					   'r': app2abs(df['r'], 'r'), 
					   'rerr': df['rerr'], 
					   'i': app2abs(df['i'], 'i'), 
					   'ierr': df['ierr'], 
					   'c': app2abs(df['c'], 'c'), 
					   'cerr': df['cerr'], 
					   'o': app2abs(df['o'], 'o'), 
					   'oerr': df['oerr']})

print(df_out)

df_out.to_csv('abs_AT2017gfo.csv', index = False)
