### IDEX Raw Pressure Data By Module

import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
import seaborn as sns
import pandas as pd
import pdb
import glob
import os

station = raw_input("Enter station name: ")
run_name = raw_input("Please enter run name: ")
print "select 'y' to graph 2-10 or 'n' to graph a single cycle"
multiple = raw_input("Graph cycles 2-10? y/n: ")

###########################
### Graph Cycles 2 - 10 ###
###########################
if multiple == 'y':
	cycles = ['02','03','04','05','06','07','08','09','10']
	m = glob.glob('rigdata/{}/{}_cycle02/upload_to_s3/IDEXcsvs/IDEX*.csv'.format(station,run_name))
	modules = []
	for i in range(len(m)):
		temp = m[i].split("/")[-1]
		modules.append(temp)
		#print modules
	for i in range(len(modules)):
		for j in range(len(cycles)):
			if os.path.exists('rigdata/{}/{}_cycle{}/upload_to_s3/IDEXcsvs/{}'.format(station,run_name,cycles[j],modules[i])) == True:
				DF = pd.read_csv('rigdata/{}/{}_cycle{}/upload_to_s3/IDEXcsvs/{}'.format(station,run_name,cycles[j],modules[i]))
				data = DF['pressure']
				plt.plot(data,'k--', alpha=0.5)
				z = 1
				if j ==1:
					n = DF['flownumber'].iloc[-1]
					color=iter(cm.rainbow(np.linspace(0,1,n)))
					while z <= DF['flownumber'].iloc[-1]:
						a = DF[DF.flownumber == z].iloc[0].name
						c = next(color)
						plt.axvline(x=a, label=DF[DF.flownumber == z]['pump_type'].iloc[0], c=c)
						z = z+1
			else:
				if i == 0:
					print "Run",cycles[j],"does not exist"
					pass
				else:
					pass
		plt.legend()
		plt.title(modules[i].split("/")[-1])
		plt.ylabel('Absolute Pressure (psi)')
		plt.xlabel('time (seconds*10^-1)')
		plt.show()


################################
### Graphing just 1 selected ###
################################
elif multiple == 'n':
	cycle_num = raw_input("Enter cycle number: ")

	#for i in range(len(cycles)):
	modules = glob.glob('rigdata/{}/{}_cycle{}/upload_to_s3/IDEXcsvs/IDEX*.csv'.format(station,run_name,cycle_num))
	for i in range(len(modules)):
		DF = pd.read_csv(modules[i])
		data = DF['pressure']
		plt.plot(data,'k--', alpha=0.5)
		z = 1
		n = DF['flownumber'].iloc[-1]
		color=iter(cm.rainbow(np.linspace(0,1,n)))
		while z <= DF['flownumber'].iloc[-1]:
			a = DF[DF.flownumber == z].iloc[0].name
			#print a
			c = next(color)
			plt.axvline(x=a, label=DF[DF.flownumber == z]['pump_type'].iloc[0], c=c)
			z = z+1
		plt.legend()
		plt.title(modules[i].split("/")[-1])
		plt.ylabel('Absolute Pressure (psi)')
		plt.xlabel('time (seconds*10^-1)')
		plt.show()

################################
### They put the wrong input ###
################################
else: 
	print "bad input!"

