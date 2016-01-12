#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:ma_shdPbl
#copyright	:Gramercy Park Studios


#shader publish module
import os, sys, traceback
import maya.cmds as mc
import mayaOps, pblChk, pblOptsPrc, vCtrl, pDialog, osOps, icPblData, verbose, inProgress
	
def publish(pblTo, slShot, subsetName, textures, pblNotes, mail, approved):
	
	#gets selection
	objLs = mc.ls(sl=True)
	
	#checks item count
	if not pblChk.itemCount(objLs):
		return
		
	#defining main variables
	assetType = 'ma_shader'
	prefix = ''
	convention = objLs[0]
	suffix = '_shader'
	fileType = 'mayaBinary'
	extension = 'mb'
	
	#sanitizes selection charatcers
	cleanObj = osOps.sanitize(convention)
	if cleanObj != convention:
		verbose.illegalCharacters(convention)
		return
		
	#checking if selection is a valid shader
	if mayaOps.nodetypeCheck(convention) != 'shadingEngine':
		verbose.shaderSupport()
		return

	#check if asset to publish is referenced
	if mc.referenceQuery(convention, inr=True):
		verbose.noRefPbl()
		return
			
	#processing asset publish options
	assetPblName, assetDir, pblDir = pblOptsPrc.prc(pblTo, subsetName, assetType, prefix, convention, suffix)
	
	#adding shot name to assetPblName if asset is being publish to a shot
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
		if textures:
			osOps.createDir(os.path.join(pblDir, 'tx'))

		#creating in progress tmp file
		inProgress.start(pblDir)
		
		#ic publish data file
		icPblData.writeData(pblDir, assetPblName, convention, assetType, extension, version, pblNotes)
	
		#maya operations
		mayaOps.deleteICDataSet(objLs)
		if textures:
			#copying textures to pbl direcotry
			txFullPath = os.path.join(pblDir, 'tx')
			txRelPath = txFullPath.replace(os.path.expandvars('$JOBPATH'), '$JOBPATH')
			txPaths = (txFullPath, txRelPath)
			mayaOps.relinkTexture(txPaths, txObjLs=objLs, updateMaya=True)

		#file operations
		pathToPblAsset = os.path.join(pblDir, '%s.%s' % (assetPblName, extension))
		verbose.pblFeed(msg=assetPblName)
		mayaOps.exportSelection(pathToPblAsset, fileType)

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
	
	
