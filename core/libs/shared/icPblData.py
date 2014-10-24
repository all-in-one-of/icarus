#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:icPblData
#copyright	:Gramercy Park Studios


#icarus publish data module
import os, time, verbose

def writeData(pblDir, assetPblName, assetName, assetType, assetExt, version, pblNotes, requires=None, compatible=None):
	pblTime = time.ctime()
	userName = os.environ['USERNAME']
	publishTime = time.ctime()
	pblNotes += '\n\n%s %s' % (userName, pblTime)
	icDataFile = open('%s/icData.py' % pblDir, 'w')
	icDataFile.write("assetPblName = '%s'\nasset = '%s'\nassetType = '%s'\nassetExt = '%s'\nversion = '%s'\nrequires = '%s'\ncompatible = '%s'\nnotes = '''%s'''" % (assetPblName, assetName, assetType, assetExt, version, requires, compatible, pblNotes))
	icDataFile.close()
	

	