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

''' This script runs the simulation in normal conditions. '''

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
	#junction '386' is of interest to our adaptive traffic control lets subscribe to it
	junction_ID = '386'
	traci.junction.subscribeContext(junction_ID, tc.CMD_GET_VEHICLE_VARIABLE, 42)
	while ct < 32400000:
		traci.simulationStep()
		ct = simulation.getCurrentTime()
		p=traci.junction.getContextSubscriptionResults(junction_ID)
		if p is not None:
			temp=list(p)
			for x in temp:
				if vehicle_list.count(x)==0:
					vehicle_list.append(x)
		outputVehicle = "Normal_1/vehicles_around_junction" + junction_ID + str(opt.run) +".txt"
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
	
	outputFile = "Normal_1/tripInfo" + str(opt.run) + ".xml"
	logFile = "Normal_1/log" + str(opt.run) + ".xml"
	print 'RANWA IS IN THE HOUSE'
	
	seed = random.randint(1000, 10000)
    
	# Starting Traci
	traci.start(['sumo-gui', "-c", "montreal.sumo.cfg", "-a", "montreal.additional.xml",  "--step-length", "0.1"])
	# to generate the tripInfo files in Normal scenario for run number in the option
	#traci.start(['sumo', "-c", "montreal.sumo.cfg", "--step-length", "0.1", "--seed", str(seed), "--tripinfo-output", outputFile, '--duration-log.statistics', 'True', '--collision.action', 'warn', '--log', logFile])
	run()
    