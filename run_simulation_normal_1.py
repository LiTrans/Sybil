# -*- coding: utf-8 -*-

import subprocess
from optparse import OptionParser
import os
import time
import sys

#Batch that runs the simulation many times 
# python run_simulation_normal_1.py -r 50

options = OptionParser()
options.add_option("-r", "--runs", help = "number of runs", dest="runs")
(opt,arg) = options.parse_args()

path1 = 'C:\Users\Administrateur.BALZAC14\Documents\Montreal Centre-Ville_ATTAQUE_SYBIL'


for i in range(1, int(opt.runs )+ 1):
	subprocess.Popen(['python', 'sumo_server_montreal_normal_1.py', '-r', str(i)])
	sys.stdout.flush()
	time.sleep(900)
	
	

	

