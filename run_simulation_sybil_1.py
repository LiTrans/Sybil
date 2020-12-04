# -*- coding: utf-8 -*-

import subprocess
from optparse import OptionParser
import os
import time
import sys

#Batch that runs the simulation many times 
# python run_simulation_sybil_1.py -r 50 
# Dedant il y a sumo_server_montreal_sybil_1.py OU sumo_server_montreal_sybil_1_A_1.py


options = OptionParser()
options.add_option("-r", "--runs", help = "number of runs", dest="runs")
(opt,arg) = options.parse_args()

path1 = 'C:\Users\Administrateur.BALZAC14\Documents\Montreal Centre-Ville_ATTAQUE_SYBIL'


for i in range(1, int(opt.runs )+ 1):
	subprocess.Popen(['python', 'sumo_server_montreal_sybil_1_A_2.py', '-r', str(i)])
	sys.stdout.flush()
	time.sleep(900)
	
	

	

