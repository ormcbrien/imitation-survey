import glob
import os
import sys

if not os.path.exists('results'):
	sys.exit('\nNo results directory to clear. Quitting.\n')
else:
	dir_contents = glob.glob('results/*.csv')
	
	print('\nFiles to be deleted...\n')
	
	for i, f in enumerate(dir_contents):
		print(i, f)
	
	print('\nDeleting.\n')
	
	for f in dir_contents:
		os.remove(f)
	
	
	
	
		