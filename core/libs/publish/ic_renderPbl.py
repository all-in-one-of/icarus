#!/usr/bin/python

# [Icarus] ic_renderPbl.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# Render publishing module.


import os, sys, traceback
import pblChk, pblOptsPrc, vCtrl, pDialog, osOps, icPblData, verbose, djvOps, inProgress


def publish(renderDic, pblTo, mainLayer, streamPbl, pblNotes):

	job = os.environ['JOB']
	assetType = 'render'
	prefix = ''
	convention = ''
	suffix = ''
	subsetName = os.environ['SHOT']
	assetExt = ''
	assetPblName = '%s%s%s' % (prefix, convention, suffix)
	assetName = assetPblName 

	# Process asset publish options
	assetPblName, assetDir, pblDir = pblOptsPrc.prc(pblTo, subsetName, assetType, prefix, convention, suffix)
	renderRootPblDir = pblDir

	# Version control
	currentVersion = vCtrl.version(pblDir, current=True)
	version = vCtrl.version(pblDir)

	# Checks if no main layer was set and cancels publish if publishing first version
	if version == 'v001':
		if not mainLayer:
			verbose.noMainLayer()
			return

	# Confirmation dialog
	dialogMsg = ''
	dialogTitle = 'Publishing Render'
	if not streamPbl:
		dialogMsg += "Warning:\n\nPublish won't be streamed.\nLayers from previous renders will not be ported.\n\n\n"
	if not mainLayer:
		dialogMsg += 'Warning:\n\nNo main layer was set.\nThe main render layer will be ported from the previous publish.\n\nContinue?\n\n\n'
	dialogMsg += 'Render:\t%s\n\nVersion:\t%s\n\nNotes:\t%s' % (assetPblName, version, pblNotes)
	dialog = pDialog.dialog()
	if not dialog.dialogWindow(dialogMsg, dialogTitle):
		return

	try:
		verbose.pblFeed(begin=True)
		pblResult = 'SUCCESS'

		# Create publish directories
		pblDir = osOps.createDir(os.path.join(pblDir, version))

		# Create in-progress tmp file
		inProgress.start(pblDir)

		# File operations
		if not mainLayer:
			streamPbl = True
		elif version == 'v001':
			streamPbl = True
		# Streaming publish. Hard linking previous version and removing previous icarus data files
		if streamPbl:
			if version != 'v001':
				# Get all layers in current publish
				currentPblLayerLs = os.listdir(os.path.join(renderRootPblDir, currentVersion))
				for currentPblLayer in currentPblLayerLs:
					# Create respective layer folder in new version
					if os.path.isdir(os.path.join(renderRootPblDir, currentVersion, currentPblLayer)):
						osOps.createDir(os.path.join(pblDir, currentPblLayer))
						# Get all files in current layer
						currentLayerFileLs = sorted(os.listdir(os.path.join(renderRootPblDir, currentVersion, currentPblLayer)))
						# Hard linking files to new version
						for currentLayerFile in currentLayerFileLs:
							verbose.pblFeed(msg='Processing %s' % currentLayerFile)
							osOps.hardLink(os.path.join(renderRootPblDir, currentVersion, currentPblLayer, currentLayerFile), os.path.join(pblDir, currentPblLayer))

		# Process all new layers and passes
		for key in renderDic.keys():
			srcLayerDir = os.path.expandvars(renderDic[key]) # expand environment variables in render path
			dirContents = sorted(os.listdir(srcLayerDir))
			for file_ in dirContents:
				verbose.pblFeed(msg='Processing %s' % file_)
				if key == mainLayer:
					osOps.createDir(os.path.join(pblDir, 'main'))
					#if os.path.isfile(os.path.join(srcLayerDir, file_)):
					#	prcFile = pblOptsPrc.renderName_prc(key, 'main', file_)
					#	if prcFile:
					#		osOps.hardLink(os.path.join(srcLayerDir, file_), os.path.join(pblDir, 'main', prcFile))
					osOps.hardLink(os.path.join(srcLayerDir, file_), os.path.join(pblDir, key))
				else:
					destLayerDir = os.path.join(pblDir, key)
					if not os.path.isdir(destLayerDir):
						osOps.createDir(destLayerDir)
					osOps.hardLink(os.path.join(srcLayerDir, file_), destLayerDir)

		# Create publish snapshot from main layer new version
		mainLayerDir = os.path.join(pblDir, 'main')
		mainLayerFileLs = sorted(os.listdir(mainLayerDir))
		mainLayerPaddingLs = []
		snapShot = False
		#print mainLayerFileLs
		for mainLayerFile in mainLayerFileLs:
			#if '_main.' in mainLayerFile:
			if '_main' in mainLayerFile: # use regex for better matching
				snapShot = True
				mainLayerBody, mainLayerPadding, mainLayerExtension = pblOptsPrc.render_split(mainLayerFile)
				mainLayerPaddingLs.append(mainLayerPadding)

		if snapShot:
			verbose.pblSaveSnapshot()
			startFrame = min(mainLayerPaddingLs)
			endFrame = max(mainLayerPaddingLs)
			midFrame = int((int(startFrame) + int(endFrame))/2)
			inFile = os.path.join(mainLayerDir, mainLayerBody)
			outFile = os.path.join(pblDir, 'preview')
			djvOps.prcImg(inFile, outFile, midFrame,  midFrame, mainLayerExtension, resize=(512,288), outExt='jpg')
			#djvOps.prcQt(inFile, pblDir, startFrame, endFrame, mainLayerExtension, resize=(256,144))

		# Store asset metadata in file
		assetPblName += '_%s' % version
		#src = renderDic['main']
		src = None
		icPblData.writeData(pblDir, assetPblName, assetName, assetType, assetExt, version, pblNotes, src)

		# Delete in-progress tmp file
		inProgress.end(pblDir)

		verbose.pblFeed(end=True)

	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		pathToPblAsset = ''
		osOps.recurseRemove(pblDir)
		pblResult = pblChk.success(pathToPblAsset)
		pblResult += verbose.pblRollback()

	# Show publish result dialog
	dialogTitle = "Publish Report"
	dialogMsg = "Render:\t%s\n\nVersion:\t%s\n\n\n%s" % (assetPblName, version, pblResult)
	dialog = pDialog.dialog()
	dialog.dialogWindow(dialogMsg, dialogTitle, conf=True)

