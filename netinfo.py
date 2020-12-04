#!/usr/bin/env python
# coding: utf-8 

from xml.dom.minidom import parse
import xml.dom.minidom
from optparse import OptionParser
from xml.etree import ElementTree as ET
import sys
import pandas as pd
import unicodedata

def getTlLogic(tlID, netfile):
	'''Returns timing plan parameters for the specified traffic light from the SUMO net file '''
	tree = ET.parse(netfile)
	root = tree.getroot()
	for child in root:
		if child.tag == 'tlLogic':
			tlLogic = []
			if child.get('id') == tlID:
				tlLogic.append(child.get('id'))
				tlLogic.append(child.get('offset'))
				phases = 0
				for phase in child.iter('phase'):
					tlLogic.append(phase.get('duration'))
					tlLogic.append(phase.get('state'))
					phases +=1
				tlLogic.insert(2, phases)
				return tlLogic

def getTlList(netfile):
	'''Returns a list of the traffic lights in the network
		The input must be the SUMO net file '''
	with open('skipList.txt', 'r') as f:
		tmp = f.readline()
		skipList = eval(tmp)
		f.close()
	tlList = []
	tree = ET.parse(netfile)
	root = tree.getroot()
	for child in root:
		if child.tag == 'tlLogic' and not child.get('id') in skipList:
			tlList.append(child.get('id'))
	return tlList
				
def saveTlTiming(netfile):
	tlList = getTlList(netfile)
	timingDict = {}
	for tl in tlList:
		tlLogic = getTlLogic(tl, netfile)
		for n in range(int(tlLogic[2])):
			if not timingDict.has_key(tl):
				timingDict[tl] = tlLogic[2*n+3]
			else:				
				timingDict[tl] = timingDict.get(tl) + ',' + tlLogic[2*n+3]
	with open('tl_timings.txt', 'w') as out:
		for tl in tlList:
			out.write('{} {}'.format(tl, timingDict[tl]) + '\n')
		out.close()
		
def getTlLocDict(netfile):
	'''Returns a dictionnary containing the traffic lights ID and its corresponding location in the network
		The input must be the SUMO net file'''
	import unicodedata
	location ={}
	names = {}
	tlList = getTlList(netfile)
	tree = ET.parse(netfile)
	root = tree.getroot()
	for tlID in tlList:
		for child in root:
			if child.tag == 'edge':
				if child.get('from') == tlID or child.get('to') == tlID:
					name = child.get('name')
					if type(name) is unicode:
						name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
					if not location.has_key(tlID):
						location[tlID] = name
						names[tlID] = [name]
					else:
						if not name in names.get(tlID):
							location[tlID] = location.get(tlID) + '/' + name
							names[tlID].append(name)
	
	with open('tlsID_location.txt', 'w') as f:
		for tlID in tlList:
			f.write('{} {}'.format(tlID, location.get(tlID) + '\n'))
	f.close()
	return location

def getTlsOnStreet(street, netfile):
	'''Returns a list containing the ID of the traffic lights on a given street
		The input must be the SUMO net file and the name of the given street must match the name in the net file'''
	tlList = []
	junctions = []
	if type(street) is unicode:
		street = unicodedata.normalize('NFKD', street).encode('ascii', 'ignore')
	tree = ET.parse(netfile)
	root = tree.getroot()
	for child in root:
		if child.tag == 'edge':
			name = child.get('name')
			if type(name) is unicode:
				name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
			if street == name:
				if not child.get('from') in junctions:
					junctions.append(child.get('from'))
				else:
					if not child.get('to') in junctions:
						junctions.append(child.get('to'))
		if child.tag == 'junction':
			for j in junctions:
				if child.get('id') == j and child.get('type') == 'traffic_light':
					if not j in tlList:
						tlList.append(j)
	return tlList

def getTLStreetDict(netfile):
	'''Returns a dictionnary containing the traffic lights in each street of the network
		The input must be the SUMO net file'''
	stDict = {}
	jctDict = {}
	junctions = []
	tree = ET.parse(netfile)
	root = tree.getroot()
	for child in root:
		if child.tag == 'edge' and child.get('function') != 'internal':
			name = child.get('name')
			if type(name) is unicode:
				name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
			if not jctDict.has_key(name):
				jctDict[name] = [child.get('from'), child.get('to')]
			else:
				if not child.get('from') in jctDict[name]:
					jctDict[name].append(child.get('from'))
				if not child.get('to') in jctDict[name]:
					jctDict[name].append(child.get('to'))
		if child.tag == 'junction':
			for name in jctDict.keys():
				for jct in jctDict[name]:
					if child.get('id') == jct and child.get('type') == 'traffic_light':
						if not stDict.has_key(name):
							stDict[name] = [child.get('id')]
						else:
							stDict[name].append(child.get('id'))	
	with open('traffic_lights_per_street.txt', 'w') as f:
		for name in stDict.keys():
			f.write('{} : '.format(name) + ' '.join(stDict[name]) +'\n')
		f.close()		
						
						
						
						
						
						
						
						
						
						
						
						
						
						