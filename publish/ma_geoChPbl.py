#!/usr/bin/python

# [Icarus] ma_geoChPbl.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Publish an asset of the type ma_geoCache.


import os
import sys
import traceback

import maya.cmds as mc

from . import pblChk
from . import pblOptsPrc
from . import inProgress
from rsc.maya.scripts import mayaOps
from shared import icPblData
from shared import os_wrapper
from shared import pDialog
from shared import vCtrl
from shared import verbose


def publish(pblTo, slShot, subtype, pblNotes):

	# Get selection
	objLs = mc.ls(sl=True)

	# Check item count
	if not pblChk.itemCount(objLs):
		return

	# Define main variables
	assetType = 'ma_geoCache'
	subsetName = subtype
	prefix = ''
	convention = objLs[0]
	suffix = '_%s_geoCache' % subtype
	if subtype == 'vrmesh':
		fileType = 'vrmesh'
		extension = 'vrmesh'
	elif subtype == 'realflow':
		fileType = 'sd'
		extension = 'sd'
	else:
		fileType = 'abc'
		extension = 'abc'

	# Check for illegal characters
	cleanObj = os_wrapper.sanitize(convention)
	if cleanObj != convention:
		verbose.illegalCharacters(convention)
		return

	# Get all dependents
	allObjLs = mc.listRelatives(convention, ad=True, f=True, typ='transform')
	if allObjLs:
		allObjLs.append(convention)
	else:
		allObjLs = [convention]

	# Check if asset to publish is a set
	if mc.nodeType(convention) == 'objectSet':
		verbose.noSetsPbl()
		return

	# Check if asset to publish is an icSet
	if mayaOps.chkIcDataSet(convention):
		verbose.noICSetsPbl()
		return

	# Check if asset to publish is referenced
	for allObj in allObjLs:
		if mc.referenceQuery(allObj, inr=True):
			verbose.noRefPbl()
			return

	# Process asset publish options
	assetPblName, assetDir, pblDir = pblOptsPrc.prc(pblTo, subsetName, assetType, prefix, convention, suffix)

	# Add shot name to assetPblName if asset is being publish to a shot
	# Determining publish env var for relative directory
	if pblTo != os.environ['IC_JOBPUBLISHDIR']:
		assetPblName += '_%s' % slShot

	# Version control
	version = '%s' % vCtrl.version(pblDir)
#	if approved:
#		version += '_apv'

	# Confirmation dialog
	dialogTitle = 'Publishing %s' % convention
	dialogMsg = 'Asset:\t%s\n\nVersion:\t%s\n\nSubset:\t%s\n\nNotes:\t%s' % (assetPblName, version, subsetName, pblNotes)
	dialog = pDialog.dialog()
	if not dialog.display(dialogMsg, dialogTitle):
		return

	# Publishing
	try:
		verbose.pblFeed(begin=True)

		# Create publish directories
		pblDir = os_wrapper.createDir(os.path.join(pblDir, version))

		# Create in-progress tmp file
		inProgress.start(pblDir)

		# Store asset metadata in file
		src = mayaOps.getScene()
		icPblData.writeData(pblDir, assetPblName, convention, assetType, extension, version, pblNotes, src)

		# Maya operations
		mayaOps.deleteICDataSet(allObjLs)

		# Take snapshot
		mayaOps.snapShot(pblDir, isolate=True, fit=True)

		# File operations
		pathToPblAsset = os.path.join(pblDir, '%s.%s' % (assetPblName, extension))
		verbose.pblFeed(msg=assetPblName)
		mayaOps.exportGeo(objLs, fileType, pathToPblAsset)

		# Delete in-progress tmp file
		inProgress.end(pblDir)

		# Published asset check
		pblResult = pblChk.success(pathToPblAsset)

		verbose.pblFeed(end=True)

	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		pathToPblAsset = ''
		os_wrapper.recurseRemove(pblDir)
		pblResult = pblChk.success(pathToPblAsset)
		pblResult += verbose.pblRollback()

	# Show publish result dialog
	dialogTitle = 'Publish Report'
	dialogMsg = 'Asset:\t%s\n\nVersion:\t%s\n\nSubset:\t%s\n\n\n%s' % (assetPblName, version, subsetName, pblResult)
	dialog = pDialog.dialog()
	dialog.display(dialogMsg, dialogTitle, conf=True)

