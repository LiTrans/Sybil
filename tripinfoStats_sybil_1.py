import pandas as pd
import csv
from optparse import OptionParser
import matplotlib.pyplot as plt
import numpy as np


''' This is the valid one Sybil_1_A_1 ou Sybil_1  '''

'''This script reads the content of the tripInfo files generated during the sybil 1 junction conditions simulations and builds the chart mean mean time loss vs simulation runs
	The input must be the number of files to read (default=50)'''

def tripsStats(runs):		
	meanTlPerRun = []		
	meanTimeLoss = []
	meanTlPerRunValues = []
	files = []
	#Junction that we are studying
	junction_ID = '386'
	
	
	for i in range(1, int(runs) + 1):
		file = 'Sybil_1_A_1/tripInfo' + str(i) + '.csv'              ##################
		files.append(file)
	i=1
	for file in files:
		print "reading", file,"..."
		#Lire les vehicules affectes dans la zone
		inputVehicle = "Sybil_1_A_1/vehicles_around_junction" + junction_ID + str(i)+ ".txt"   #################
		file_Vehicle = open(inputVehicle, 'r') 
		vehicle_list_chaine=file_Vehicle.read() 
		file_Vehicle.close()
		vehicle_list=vehicle_list_chaine.split()
		#Lire les tripInfo
		df = pd.read_csv(file)
		trips = df[df['tripinfo_arrival']>29000]
		vehicle_list_tl = []
		good_trips = []
				
		for x in vehicle_list:
			ligne_df=trips.loc[trips['tripinfo_id'] == int(x)]
			# print 
			# trips.index[i]
			solution = ligne_df['tripinfo_timeLoss']
			if len(solution)!=0:
				s=solution.item()
				vehicle_list_tl.append(s)
		#c le temps perdu juste sur la jonction en question
		meanTlPerRun.append(sum(vehicle_list_tl)/len(vehicle_list_tl))
		#meanTlPerRun.append(trips['tripinfo_timeLoss'].mean()) #C le temps perdu pour tout les vehicules de la simulation
		i=i+1
	print "...reading done"
		
	for n in range(len(meanTlPerRun)):
		meanTlPerRunValues.append(meanTlPerRun[n])
		meanTimeLoss.append(np.mean(meanTlPerRunValues))
	
	x = range(1,len(meanTlPerRun)+1)
	
	legend_list =["Mean trip time loss per simulation", "Average of the mean trip time loss"]
		
	y = meanTlPerRun
	plt.plot(x, y, 'ro', label='Mean trip time loss per simulation')
	y = meanTimeLoss
	plt.plot(x, y, 'b-', label='Average of the mean trip time loss')
	ax = plt.subplot(111)
	box = ax.get_position()
	# Shrink current axis by 20%
	#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
	# Put a legend to the right of the current axis
	#ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	# Put a legend below current axis
	#ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=False, shadow=False, ncol=5)
	# Put a legend above the graphic
	ax.legend(loc='upper left', bbox_to_anchor=(0.5, 1.15), fancybox=False, shadow=False, ncol=1)
	
	
	#plt.legend(legend_list, loc='upper right')
	#box = ax.get_position()
	# Shrink current axis by 20%
	# Put a legend to the right of the current axis
	#plt.title('mean trip timeLoss vs runs')
	plt.ylabel('Time (s)')
	plt.xlabel('Number of simulation')
	plt.grid(axis='both')
	plt.savefig("moyenne_Temps_perdu_Sybil_1.svg")
	plt.show()
	
	

if __name__ == "__main__":
	
	options = OptionParser()
	options.add_option("-r", "--run", help = "number of runs", dest="run", default = 1)
	(opt,arg) = options.parse_args()
	
	tripsStats(opt.run)