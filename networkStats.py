import pandas as pd
import csv
from optparse import OptionParser
import matplotlib.pyplot as plt
import numpy as np
import netinfo


''' This is the valid one 04/03/2018'''


global stats
stats = {}

def getNormalCondStats(runs):
	files = []
	Veh_inserted = {}
	Veh_running = {}
	Veh_waiting = {}
	Veh_teleported = {}
	meanTimeLoss = {}
	for i in range(1, int(runs) + 1):
		file = 'Normal/log' + str(i) + '.xml'
		files.append(file)
	tag = 'nc'
	for file in files:
		print "reading", file,"..."
		with open(file, 'r') as f:
			lines = f.readlines()
			f.close()
		for i in range(len(lines)):
			if 'Inserted' in lines[i]:
				if len(lines[i].split(' ')) > 3:
					tmp = lines[i].split(' ')[2]	
				else:
					tmp = lines[i].split(' ')[2][:-1]
				if not Veh_inserted.has_key(tag):
					Veh_inserted[tag] = [int(tmp)]
				else:
					Veh_inserted[tag].append(int(tmp))
			elif 'Running' in lines[i]:
				tmp = lines[i].split(' ')[2][:-1]
				if not Veh_running.has_key(tag):
					Veh_running[tag] = [int(tmp)]
				else:
					Veh_running[tag].append(int(tmp))
			elif 'Vehicles:' in lines[i]:
				tmp = lines[i+3].split(' ')[2][:-1]
				if not Veh_waiting.has_key(tag):
					Veh_waiting[tag] = [int(tmp)]
				else:
					Veh_waiting[tag].append(int(tmp))
			elif 'Teleports' in lines[i]:
				tmp = lines[i].split(' ')[1]
				if not Veh_teleported.has_key(tag):
					Veh_teleported[tag] = [int(tmp)]
				else:
					Veh_teleported[tag].append(int(tmp))
			elif 'TimeLoss' in lines[i]:
				tmp = lines[i].split(' ')[2][:-1]
				if not meanTimeLoss.has_key(tag):
					meanTimeLoss[tag] = [float(tmp)]
				else:
					meanTimeLoss[tag].append(float(tmp))
	print 'All files read'
	stats = [int(round(np.mean(Veh_inserted[tag]), 0)), int(round(np.mean(Veh_running[tag]), 0)), int(round(np.mean(Veh_waiting[tag]), 0)), int(round(np.mean(Veh_teleported[tag]), 0)), np.mean(meanTimeLoss[tag])]
	normalStats_df = pd.DataFrame(data=stats, index=['Veh_inserted', 'Veh_running', 'Veh_waiting', 'Veh_teleported', 'meanTimeLoss'])
	print normalStats_df
	normalStats_df.to_csv('Normal/networkStatsNC.csv')
	

def getAttacksStats(runs, attack, random):
	print runs, type(runs), attack, type(attack), random, type(random)
	files = []
	filesDict = {}
	Veh_inserted = {}
	Veh_running = {}
	Veh_waiting = {}
	Veh_teleported = {}
	Veh_arrived = {}
	#Veh_arrivedList = []
	meanTimeLoss = {}
	tags = []
	groups = [0, 5, 10, 20, 50]
	
	if attack == 1:
		folder = '2'
	else:
		folder = '3'
	
	for g in groups:
		files=[]
		for r in range(1, int(runs) + 1):
			if int(g) == 0:
				file = 'Normal/log' + str(r) + '.xml'
				tag = 'Normal'
			else:
				if random == True: 
					file = 'Attack' + folder +  '/log_a' + folder + '_g' + str(g)+ '_r' + str(r) + '.xml'
					tag = 'g' + str(g) + 'a' + str(attack) + 'r'
					outputFile = 'networkStats_attaque' + str(attack) + '_aleatoire.csv'
				else:
					file = 'Attack' + folder +  '/log_a' + folder + 'tg_g' + str(g)+ '_r' + str(r) + '.xml'
					tag = 'g' + str(g) + 'a' + str(attack) + 't'
					outputFile = 'networkStats_attaque' + str(attack) + '_cible.csv'
				#print tag
			files.append(file)
			if not tag in tags:
				tags.append(tag)
			#print tags
			if not filesDict.has_key(tag):
				filesDict[tag] = files
		
	print 'Reading filesDict'
		
	for tag in tags:
		Veh_arrivedList = []
		print tag
		files = filesDict.get(tag)
		for file in files:
			#print "reading", file,"..."
			with open(file, 'r') as f:
				lines = f.readlines()
				f.close()
			for i in range(len(lines)):
				if 'Inserted' in lines[i]:
					if len(lines[i].split(' ')) > 3:
						tmp = lines[i].split(' ')[2]	
					else:
						tmp = lines[i].split(' ')[2][:-1]
					if not Veh_inserted.has_key(tag):
						Veh_inserted[tag] = [int(tmp)]
					else:
						Veh_inserted[tag].append(int(tmp))
				elif 'Running' in lines[i]:
					tmp = lines[i].split(' ')[2][:-1]
					if not Veh_running.has_key(tag):
						Veh_running[tag] = [int(tmp)]
					else:
						Veh_running[tag].append(int(tmp))
				elif 'Vehicles' in lines[i]:
					tmp = lines[i+3].split(' ')[2][:-1]
					if not Veh_waiting.has_key(tag):
						Veh_waiting[tag] = [int(tmp)]
					else:
						Veh_waiting[tag].append(int(tmp))
				elif 'Teleports' in lines[i]:
					tmp = lines[i].split(' ')[1]
					if not Veh_teleported.has_key(tag):
						Veh_teleported[tag] = [int(tmp)]
					else:
						Veh_teleported[tag].append(int(tmp))
				elif 'TimeLoss' in lines[i]:
					tmp = lines[i].split(' ')[2][:-1]
					if not meanTimeLoss.has_key(tag):
						meanTimeLoss[tag] = [float(tmp)]
					else:
						meanTimeLoss[tag].append(float(tmp))
		for i in range(len(Veh_running[tag])):	
			Veh_arrivedList.append(Veh_inserted.get(tag)[i] - Veh_running.get(tag)[i])
		Veh_arrived[tag] = Veh_arrivedList
		
				
		stats[tag] = [int(round(np.mean(Veh_inserted[tag]), 0)), int(round(np.mean(Veh_arrived[tag]), 0)), int(round(np.mean(Veh_running[tag]), 0)), int(round(np.mean(Veh_waiting[tag]), 0)), int(round(np.mean(Veh_teleported[tag]), 0)), np.mean(meanTimeLoss[tag])]
		
	print 'All files read'
	#print stats
	
	labels = ['Veh_inserted', 'Veh_arrived', 'Veh_running', 'Veh_waiting', 'Veh_teleported',  'meanTimeLoss']
	attacksStats_df = pd.DataFrame(data=stats, index=labels)
	#print attacksStats_df
	attacksStats_df.to_csv(outputFile)
	return stats
	
	
def plotAttacksStats(runs):
	Veh_inserted = {}
	Veh_running = {}
	Veh_waiting = {}
	Veh_arrived = {}
	Veh_teleported = {}
	stats = {}
	case1 = []
	case2 = []
	case3 = []
	case4 = []
	
	attacks = [1, 2]
	random = [True, False]
	groupes = [5, 10, 20, 50]
	#attacksTags = ['a1r', 'a1t', 'a2r', 'a2t']
	
	for attack in attacks:
		for mode in random:
			stats = getAttacksStats(runs, attack, mode)
	
	labels = ['Veh_inserted', 'Veh_arrived', 'Veh_running', 'Veh_waiting', 'Veh_teleported', 'meanTimeLoss']
	
	statsAttacks_df = pd.DataFrame(data=stats, index=labels)
	stats2 = statsAttacks_df.T
	#print stats2
	#statsAttacks_df.plot(kind='bar', grid=True)
	
	
	
	#print statsAttacks_df
	#statsAttacks_df.to_csv('globalStatsAttacks.csv')
	#statsAttacks_df.plot(kind='bar', grid=True)
	# plt.xticks(rotation=15)
	# ax = plt.subplot(111)
	# box = ax.get_position()
	# Shrink current axis by 20%
	# box = ax.get_position()
	# ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
	# Put a legend to the right of the current axis
	#ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	
	# # Shrink current axis's height by 10% on the bottom
	# box = ax.get_position()
	# ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
	# # Put a legend below current axis
	# ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)
	#plt.show()

	#df = df[['pos', 'new id']]
			
	a1r = statsAttacks_df[['Normal', 'g5a1r', 'g10a1r', 'g20a1r', 'g50a1r']]
	a1t = statsAttacks_df[['Normal', 'g5a1t', 'g10a1t', 'g20a1t', 'g50a1t']]
	a2r = statsAttacks_df[['Normal', 'g5a2r', 'g10a2r', 'g20a2r', 'g50a2r']]
	a2t = statsAttacks_df[['Normal', 'g5a2t', 'g10a2t', 'g20a2t', 'g50a2t']]
	

	Veh_inserted['a1r'] = a1r.loc['Veh_inserted'].tolist()
	Veh_arrived['a1r'] = a1r.loc['Veh_arrived'].tolist()
	Veh_running['a1r'] = a1r.loc['Veh_running'].tolist()
	Veh_waiting['a1r'] = a1r.loc['Veh_waiting'].tolist()
	Veh_teleported['a1r'] = a1r.loc['Veh_teleported'].tolist()
	
	Veh_inserted['a1t'] = a1t.loc['Veh_inserted'].tolist()
	Veh_arrived['a1t'] = a1t.loc['Veh_arrived'].tolist()
	Veh_running['a1t'] = a1t.loc['Veh_running'].tolist()
	Veh_waiting['a1t'] = a1t.loc['Veh_waiting'].tolist()
	Veh_teleported['a1t'] = a1r.loc['Veh_teleported'].tolist()
	
	Veh_inserted['a2r'] = a2r.loc['Veh_inserted'].tolist()
	Veh_arrived['a2r'] = a2r.loc['Veh_arrived'].tolist()
	Veh_running['a2r'] = a2r.loc['Veh_running'].tolist()
	Veh_waiting['a2r'] = a2r.loc['Veh_waiting'].tolist()
	Veh_teleported['a2r'] = a2r.loc['Veh_teleported'].tolist()
	
	Veh_inserted['a2t'] = a2t.loc['Veh_inserted'].tolist()
	Veh_arrived['a2t'] = a2t.loc['Veh_arrived'].tolist()
	Veh_running['a2t'] = a2t.loc['Veh_running'].tolist()
	Veh_waiting['a2t'] = a2t.loc['Veh_waiting'].tolist()
	Veh_teleported['a2t'] = a2t.loc['Veh_teleported'].tolist()
	
	
	vi_df = pd.DataFrame(data=Veh_inserted, index=[0, 5, 10, 20, 50])
	va_df = pd.DataFrame(data=Veh_arrived, index=[0, 5, 10, 20, 50])
	vr_df = pd.DataFrame(data=Veh_running, index=[0, 5, 10, 20, 50])
	vw_df = pd.DataFrame(data=Veh_waiting, index=[0, 5, 10, 20, 50])
	vt_df = pd.DataFrame(data=Veh_teleported, index=[0, 5, 10, 20, 50])
	
	
	vi_df.plot(kind='bar', grid=True)
	plt.title('voitures inserees vs attaques')
	plt.xlabel('nombre de feux de circulation attaques')
	plt.ylabel('nombre de voitures')
	plt.xticks(rotation=0)
	ax = plt.subplot(111)
	box = ax.get_position()
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	
	va_df.plot(kind='bar', grid=True)
	plt.title('trips completes vs attaques')
	plt.xlabel('nombre de feux de circulation attaques')
	plt.ylabel('nombre de voitures')
	plt.xticks(rotation=0)
	ax = plt.subplot(111)
	box = ax.get_position()
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	
	vr_df.plot(kind='bar', grid=True)
	plt.title('voitures pour arriver a destination vs attaques')
	plt.xlabel('nombre de feux de circulation attaques')
	plt.ylabel('nombre de voitures')
	plt.xticks(rotation=0)
	ax = plt.subplot(111)
	box = ax.get_position()
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	
	vw_df.plot(kind='bar', grid=True)
	plt.title('voitures non inserees vs attaques')
	plt.xlabel('nombre de feux de circulation attaques')
	plt.ylabel('nombre de voitures')
	plt.xticks(rotation=0)
	ax = plt.subplot(111)
	box = ax.get_position()
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	
	vt_df.plot(kind='bar', grid=True)
	plt.title('voitures teleportees vs attaques')
	plt.xlabel('nombre de feux de circulation attaques')
	plt.ylabel('nombre de voitures')
	plt.xticks(rotation=0)
	ax = plt.subplot(111)
	box = ax.get_position()
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	
	
	plt.show()	
			
			
			
			
			
			
			
			
			
			
			
			
