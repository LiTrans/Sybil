import os
import sys
import socket
import optparse
import subprocess
import random
import select
import struct
import binascii
import time
import threading
from traci import trafficlights, simulation, edge, junction
import traci.constants as tc
from datetime import datetime
from optparse import OptionParser

''' This script runs the simulation in a sybil attack on three junctions'''

# to import python modules from the $SUMO_HOME/tools directory
try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary
except ImportError:
    sys.exit("please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

import traci

def run():
	global ct
	ct = 0
	edgesList = []
	vehicle_list = []
	#junctions '386', '428' and '376' are of interest to our adaptive traffic control lets subscribe to them
	junction_ID_1 = '386'
	junction_ID_2 = '428'
	junction_ID_3 = '376'
	traci.junction.subscribeContext(junction_ID_1, tc.CMD_GET_VEHICLE_VARIABLE, 42)
	traci.junction.subscribeContext(junction_ID_2, tc.CMD_GET_VEHICLE_VARIABLE, 42)
	traci.junction.subscribeContext(junction_ID_3, tc.CMD_GET_VEHICLE_VARIABLE, 42)
	#les 3 routes que g cree pour les vehicules sybils
	traci.route.add(routeID="r1",edges=["-479572754#1","-479572754#0", "-456316923"])
	traci.route.add(routeID="r2",edges=["-300627772#1","-479572754#1", "-479572754#0"])
	traci.route.add(routeID="r3",edges=["-361607072","361607071", "479572754#0"])
	
	#A chaque 100 secondes, je genere 6 vehicules sybiles dont les identifiants commencent par 10000000 et a partir de 28000s
	d=28000
	z=0
	for i in range(40):
		v1="10000000" + str(z)
		v2="10000000" + str(z+1)
		v3="10000000" + str(z+2)
		v4="10000000" + str(z+3)
		v5="10000000" + str(z+4)
		v6="10000000" + str(z+5)
		v7="10000000" + str(z+6)
		v8="10000000" + str(z+7)
		v9="10000000" + str(z+8)
		v10="10000000" + str(z+9)
		v11="10000000" + str(z+10)
		v12="10000000" + str(z+11)
		v13="10000000" + str(z+12)
		v14="10000000" + str(z+13)
		v15="10000000" + str(z+14)
		v16="10000000" + str(z+15)
		v17="10000000" + str(z+16)
		v18="10000000" + str(z+17)
		traci.vehicle.add(str(v1),"r1",depart=d, pos=0)
		traci.vehicle.add(str(v2),"r1",depart=d, pos=0)
		traci.vehicle.add(str(v3),"r1",depart=d, pos=0)
		traci.vehicle.add(str(v4),"r1",depart=d, pos=0)
		traci.vehicle.add(str(v5),"r1",depart=d, pos=0)
		traci.vehicle.add(str(v6),"r1",depart=d, pos=0)
		traci.vehicle.add(str(v7),"r2",depart=d, pos=0)
		traci.vehicle.add(str(v8),"r2",depart=d, pos=0)
		traci.vehicle.add(str(v9),"r2",depart=d, pos=0)
		traci.vehicle.add(str(v10),"r2",depart=d, pos=0)
		traci.vehicle.add(str(v11),"r2",depart=d, pos=0)
		traci.vehicle.add(str(v12),"r2",depart=d, pos=0)
		traci.vehicle.add(str(v13),"r3",depart=d, pos=0)
		traci.vehicle.add(str(v14),"r3",depart=d, pos=0)
		traci.vehicle.add(str(v15),"r3",depart=d, pos=0)
		traci.vehicle.add(str(v16),"r3",depart=d, pos=0)
		traci.vehicle.add(str(v17),"r3",depart=d, pos=0)
		traci.vehicle.add(str(v18),"r3",depart=d, pos=0)
		traci.vehicle.setColor(str(v1),(250,0,0,0))
		traci.vehicle.setColor(str(v2),(250,0,0,0))
		traci.vehicle.setColor(str(v3),(250,0,0,0))
		traci.vehicle.setColor(str(v4),(250,0,0,0))
		traci.vehicle.setColor(str(v5),(250,0,0,0))
		traci.vehicle.setColor(str(v6),(250,0,0,0))
		traci.vehicle.setColor(str(v7),(0,250,0,0))
		traci.vehicle.setColor(str(v8),(0,250,0,0))
		traci.vehicle.setColor(str(v9),(0,250,0,0))
		traci.vehicle.setColor(str(v10),(0,250,0,0))
		traci.vehicle.setColor(str(v11),(0,250,0,0))
		traci.vehicle.setColor(str(v12),(0,250,0,0))
		traci.vehicle.setColor(str(v13),(0,0,250,0))
		traci.vehicle.setColor(str(v14),(0,0,250,0))
		traci.vehicle.setColor(str(v15),(0,0,250,0))
		traci.vehicle.setColor(str(v16),(0,0,250,0))
		traci.vehicle.setColor(str(v17),(0,0,250,0))
		traci.vehicle.setColor(str(v18),(0,0,250,0))
		d=d+100
		z=z+18
		
	while ct < 32400000:
		traci.simulationStep()
		ct = simulation.getCurrentTime()
		#Insertion de vehicules sybiles
		p=traci.junction.getContextSubscriptionResults(junction_ID_1)
		if p is not None:
			temp=list(p)
			for x in temp:
				#g des vehicules sybiles que je ne veux pas coller a ma liste
				if ((vehicle_list.count(x)==0) & (int(x)<10000000)):
					vehicle_list.append(x)
		q=traci.junction.getContextSubscriptionResults(junction_ID_2)
		if q is not None:
			temp=list(q)
			for x in temp:
				#g des vehicules sybiles que je ne veux pas coller a ma liste
				if ((vehicle_list.count(x)==0) & (int(x)<1000000)):
					vehicle_list.append(x)
		r=traci.junction.getContextSubscriptionResults(junction_ID_3)
		if r is not None:
			temp=list(r)
			for x in temp:
				#g des vehicules sybiles que je ne veux pas coller a ma liste
				if ((vehicle_list.count(x)==0) & (int(x)<1000000)):
					vehicle_list.append(x)
	outputVehicle = "Sybil_3_A_2/vehicles_around_junction" + junction_ID_1 + junction_ID_2 + junction_ID_3+ str(opt.run) +".txt"
	with open(outputVehicle,'w') as out:
		for y in vehicle_list:
			out.write(y + '\n')
	out.close()	
	traci.close()
	sys.stdout.flush()

	
def send_time(ct):
	print sys.stderr, 'Sending time to server'
	date = datetime.now()
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('127.0.0.1', 8000)
	sock.connect(server_address)
	print sys.stderr, 'Starting communication with server', server_address, 'at %s' % date
	t = struct.pack('>B I', 0, ct)
	sock.sendall(t)
	r = sock.recv(24)
	if r:
		if r == 'Time received':
			print 'Valid time reception confirmation received'
		else:
			print 'Invalid time reception confirmation received'
	else:
		print 'No time reception confirmation received'
	print 'Closing connection with server at %s' % date
	sock.close()
	
def send(tlsID, tlsState):
	print sys.stderr, 'Sending tlsState to server'
	date = datetime.now()
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('127.0.0.1', 8000)
	sock.connect(server_address)
	print sys.stderr, 'Starting communication with server', server_address, 'at %s' % date
	request = struct.pack('>2B H', 0, 1, tlsID)	# 0 = client = SUMO / 1 = mode = write
	sock.sendall(request)
	r = sock.recv(24)
	if r:
		if r == 'Waiting for data':
			print 'Request for tlsState received'
			sock.sendall(tlsState)
			print 'tlsState sent from SUMO for %s : %s' % (tlsID, tlsState)
			r = sock.recv(24)
			format = '>B H %is' % len(tlsState)
			data = struct.unpack(format, r) 	# data = (0, tlsID, tlsState)
			if data[0] == 0 and data[1] == tlsID and data[2] == tlsState:
				print 'Valid tlsState confirmation received'
			else:
				print 'Invalid tlsState confirmation received'
		else:
			print 'Invalid request confirmation received'
	else:
		print 'Not response from server'   
	print 'Closing connection with server at %s' % date
	sock.close()
	
def get_tlsState(tlsID, tlsState):
    print 'Getting tlsState' 
    date = datetime.now()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 8000)
    sock.connect(server_address)
    print sys.stderr, 'Starting communication with server', server_address, 'at %s' % date
    request = struct.pack('>2B H', 0, 0, tlsID)	# 0 = client = SUMO / 0 = mode = read
    sock.sendall(request)
    r = sock.recv(24)	
    if r:
        if r == '0':
            print 'No tlsState for %s received' % tlsID
            tlsState = None
        else:
            print 'tlsState for %s received' % tlsID
            format = '>B H %is' % len(tlsState)
            data = struct.unpack(format, r)		# data = (0, tlsID, tlsState)
            print 'Data received = ', data
            if data[0] == 0 and data[1] == tlsID and len(data[2]) == len(tlsState):
                print 'Valid tlsState value received'
                tlsID = data[1]
                tlsState = data[2]
            else:
                print 'Invalid tlsState value received'
    else:
        print 'Not response from server'
    print 'Closing connection with server at %s' % date
    sock.close()
    return tlsState


if __name__ == "__main__":
       
	options = OptionParser()
	options.add_option("-r", "--run", help = "run id", dest="run", default = 1)
	(opt,arg) = options.parse_args()
	
	outputFile = "Sybil_3_A_2/tripInfo" + str(opt.run) + ".xml"
	logFile = "Sybil_3_A_2/log" + str(opt.run) + ".xml"
	print 'Sybil IS IN THE HOUSE'
	
	seed = random.randint(1000, 10000)
    
	# Starting Traci
	#traci.start(['sumo-gui', "-c", "montreal3_A_2.sumo.cfg", "-a", "montreal.additional.xml",  "--step-length", "0.1"])
	#to generate the tripInfo files in Sybil scenario for run number in the option for 3 junctions
	traci.start(['sumo', "-c", "montreal3_A_2.sumo.cfg", "--step-length", "0.1", "--seed", str(seed), "--tripinfo-output", outputFile, '--duration-log.statistics', 'True', '--collision.action', 'warn', '--log', logFile])
	run()
    
