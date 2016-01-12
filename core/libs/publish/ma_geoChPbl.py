#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:ma_geoChPbl
#copyright	:Gramercy Park Studios


#geo Cache publish module
import os, sys, traceback
import maya.cmds as mc
import mayaOps, pblChk, pblOptsPrc, vCtrl, pDialog, osOps, icPblData, verbose, inProgress
	
def publish(pblTo, slShot, geoChType, pblNotes, mail, approved):
	
	#gets selection
	objLs = mc.ls(sl=True)
	
	#checks item count
	if not pblChk.itemCount(objLs):
		return

	#defining main variables
	assetType = 'ma_geoCache'
	subsetName = geoChType
	prefix = ''
	convention = objLs[0] 
	suffix = '_%s_geoCache' % geoChType
	if geoChType == 'vrmesh':
		fileType = 'vrmesh'
		extension = 'vrmesh'
	elif geoChType == 'realflow':
		fileType = 'sd'
		extension = 'sd'
	else:
		fileType = 'abc'
		extension = 'abc'
		
	#sanitizes selection charatcers
	cleanObj = osOps.sanitize(convention)
	if cleanObj != convention:
		verbose.illegalCharacters(convention)
		return
		
	#gets all dependants	
	allObjLs = mc.listRelatives(convention, ad=True, f=True, typ='transform')
	if allObjLs:
		allObjLs.append(convention)
	else:
		allObjLs = [convention]
		
	#check if asset to publish is a set
	if mc.nodeType(convention) == 'objectSet':
		verbose.noSetsPbl()
		return
	
	#check if asset to publish is an icSet
	if mayaOps.chkIcDataSet(convention):
		verbose.noICSetsPbl()
		return

	#check if asset to publish is referenced
	for allObj in allObjLs: 
		if mc.referenceQuery(allObj, inr=True):
			verbose.noRefPbl()
			return
		
	#processing asset publish options
	mayaOps.deleteICDataSet(allObjLs)
	assetPblName, assetDir, pblDir = pblOptsPrc.prc(pblTo, subsetName, assetType, prefix, convention, suffix)
	
	#determining approved publish directory
	#determining publish env var for relative directory
	if pblTo != os.environ['JOBPUBLISHDIR']:
		assetPblName += '_%s' % slShot
	
	#version control	
	version = '%s' % vCtrl.version(pblDir)
	if approved:
		version += '_apv'
		
	#confirmation dialog
	dialogTitle = 'Publishing'
	dialogMsg = 'Asset:\t%s\n\nVersion:\t%s\n\nSubset:\t%s\n\nNotes:\t%s' % (assetPblName, version, subsetName, pblNotes)
	dialog = pDialog.dialog()
	if not dialog.dialogWindow(dialogMsg, dialogTitle):
		return

	#publishing
	try:	
		verbose.pblFeed(begin=True)
		
		#creating publish directories
		pblDir = osOps.createDir(os.path.join(pblDir, version))

		#creating in progress tmp file
		inProgress.start(pblDir)

		#ic publish data file
		icPblData.writeData(pblDir, assetPblName, convention, assetType, extension, version, pblNotes)
	
		#maya operations
		mayaOps.snapShot(pblDir)

		#file operations
		pathToPblAsset = os.path.join(pblDir, '%s.%s' % (assetPblName, extension))
		verbose.pblFeed(msg=assetPblName)
		mayaOps.exportGeo(objLs, fileType, pathToPblAsset)

		#deleting in progress tmp file
		inProgress.end(pblDir)
		
		#published asset check
		pblResult = pblChk.success(pathToPblAsset)
		
		verbose.pblFeed(end=True)

	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		pathToPblAsset = ''
		osOps.recurseRemove(pblDir)
		pblResult = pblChk.success(pathToPblAsset)
		pblResult += verbose.pblRollback()

	#publish result dialog
	dialogTitle = 'Publish Report'
	dialogMsg = 'Asset:\t%s\n\nVersion:\t%s\n\nSubset:\t%s\n\n\n%s' % (assetPblName, version, subsetName, pblResult)
	dialog = pDialog.dialog()
	dialog.dialogWindow(dialogMsg, dialogTitle, conf=True)
	

	
