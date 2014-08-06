#!/usr/bin/python
#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:setLog
#copyright	:Gramercy Park Studios


import os, sys

#reading from user log file	
def read(entry=-1):
	uHome = '/Users/%s' % os.environ['USERNAME']
	try:
		logFile = open('%s/.setlog' % uHome , 'r')
		entryLs = logFile.read().split('\n')
		entryLs = entryLs[entry].split(',')
		logFile.close()
		if len(entryLs) == 2:
			return entryLs
	except IOError:
		return
		


#writing to user log file. allows max of 5 entries
def write(newEntry):
	uHome = '/Users/%s' % os.environ['USERNAME']
	try:
		logFile = open('%s/.setlog' % uHome , 'r+')
		#limiting entry list
		entryLs = logFile.read().split('\n')
		if len(entryLs) >= 2:
			entryLs = [entryLs[-1], newEntry]
			logFile.close()
			logFile = open('%s/.setlog' % uHome , 'w')
		else:
			entryLs = [newEntry]
	except IOError:
		logFile = open('%s/.setlog' % uHome , 'w')
		entryLs = [newEntry]
		
	#writing entries
	for entry in entryLs:
		logFile.write('\n%s' % entry)
	logFile.close()

