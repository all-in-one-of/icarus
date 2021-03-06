#!/usr/bin/python

# [Icarus] mayaOps.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# Benjamin Parry <ben.parry@gps-ldn.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Maya operations module.


import os
import shutil

import maya.cmds as mc
import maya.mel as mel

from shared import os_wrapper
from shared import recent_files


def applyTransforms(obj, objT, objR, objS):
	""" Apply transforms.
		(used by point cloud publish module)
	"""
	try:
		mc.xform(obj, s=objS, ws=True)
		mc.xform(obj, ro=objR, ws=True)
		mc.xform(obj, t=objT, ws=True)
		return -1
	except TypeError:
		return


def assetTag(obj, assetName):
	""" Add asset name tag as extra attribute.
	"""
	refTag = mc.listAttr(obj, st='icAsset')
	if not refTag:
		mc.addAttr(obj, ln='asset', dt='string')
	mc.setAttr('%s.icAsset' % obj, l=False)
	mc.setAttr('%s.icAsset' % obj, assetName, typ='string', l=True)


def assetExtTag(obj, assetExt):
	""" Add asset extension tag as extra attribute.
	"""
	refTag = mc.listAttr(obj, st='icAssetExt')
	if not refTag:
		mc.addAttr(obj, ln='assetExt', dt='string')
	mc.setAttr('%s.icAssetExt' % obj, l=False)
	mc.setAttr('%s.icAssetExt' % obj, assetExt, typ='string', l=True)


def assetTypeTag(obj, assetType):
	""" Add asset type tag as extra attribute.
	"""
	refTag = mc.listAttr(obj, st='icAssetType')
	if not refTag:
		mc.addAttr(obj, ln='icAssetType', dt='string')
	mc.setAttr('%s.icAssetType' % obj, l=False)
	mc.setAttr('%s.icAssetType' % obj, assetType, typ='string', l=True)


def assetRootDir(obj, assetRootDir):
	""" Add asset root dir as extra attribute.
	"""
	rootDir = mc.listAttr(obj, st='icAssetRootDir')
	if not rootDir:
		mc.addAttr(obj, ln='icAssetRootDir', dt='string')
	mc.setAttr('%s.icAssetRootDir' % obj, l=False)
	mc.setAttr('%s.icAssetRootDir' % obj, assetRootDir, typ='string', l=True)


#######################bakes camera anim###################
def cameraBake(objLs, assetPblName):
	#if camera with publish name exists renames to *_old to bypass maya conflict
	if mc.objExists(assetPblName):
		mc.rename(assetPblName, '%s_old' % assetPblName)
	originalcamLs = [objLs[0]]
	originalcamShape = mc.listRelatives(originalcamLs[0], s=True, pa=True)
	newcamLs = mc.duplicate(originalcamLs[0], n=assetPblName, rc=True)
	newcam = assetPblName
	#placing new camera under world root
	if mc.listRelatives(assetPblName, p=True) != None:
		mc.parent(newcam, w=True)
	newcamShape = mc.listRelatives(newcam, s=True)
	minFrame = int(mc.playbackOptions(min=True, q=True))
	maxFrame = int(mc.playbackOptions(max=True, q=True))
	#unlocking new camera attr
	attrLs = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.fl']
	lockAttr([newcam], attrLs, lock=False, children=False)
	#deleting any existent constraints
	for newcamNode in newcamLs:
		if 'Constraint' in newcamNode:
			mc.delete(newcamNode)
	#creating parent constraint for new camera
	if mc.objExists('renderCamera_bake_parentCstrt'):
		mc.delete('renderCamera_bake_parentCstrt')
	mc.parentConstraint(originalcamLs[0], newcam, mo=False, n='renderCamera_bake_parentCstrt')
	#connecting bakable attributes
	attrBakeLs = ['.focalLength']
	for attrBake in attrBakeLs:
		mc.connectAttr(originalcamShape[0] + attrBake, newcamShape[0] + attrBake, f=True)
	#baking camera in world space
	mc.bakeResults(newcam, hi='both', s=True, dic=True, sm=True, time=(minFrame, maxFrame))
	#applying euler filter
	if mc.objExists(newcam + '_rotateX'):
		mc.filterCurve( newcam + '_rotateX')
	if mc.objExists(newcam + '_rotateY'):
		mc.filterCurve( newcam + '_rotateY')
	if mc.objExists(newcam + '_rotateZ'):
		mc.filterCurve( newcam + '_rotateZ')	
	mc.delete('renderCamera_bake_parentCstrt')
	return newcamLs

###################camera node check######################
def cameraNodeCheck(obj):
	try:
		objSh = mc.listRelatives(obj, s=True, pa=True)[0]
		if mc.nodeType(objSh) == 'camera':
			return 1
		else:
			return
	except (TypeError, RuntimeError):
		return

#######checks if ICSet contains icAssetRoot attr##########
def chkIcAssetRootAttr(obj):
	if not chkIcDataSet(obj):
		return 
	try:
		mc.getAttr('%s.icAssetRootDir' % obj)
		return 1
	except ValueError:
		return 

##########checks if obj is a icarus data set##############
def chkIcDataSet(obj=None):
	if not obj:
		try:
			obj = mc.ls(sl=True)[0]
		except:
			pass
	if obj:
		if mc.nodeType(obj) == 'ICSet':
			return obj
	return

###########adds asset requirement tag as extra attr#######
def compatibleTag(obj, compatibleTag):
	comptTag = mc.listAttr(obj, st='icAssetCompatibility')
	if not comptTag:
		mc.addAttr(obj, ln='icAssetCompatibility', dt='string')
	mc.setAttr('%s.icAssetCompatibility' % obj, l=False)
	mc.setAttr('%s.icAssetCompatibility' % obj, compatibleTag, typ='string', l=True)

######################creates lod system###################
def createLodSystem(objLs):
	lodsMasterGrp = objLs[0]
	attrLs = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz']
	lodsMasterGrp = mc.group(n='%s_lodsTmpMasterGRP' % objLs[0], em=True)
	#lodC
	lodC = generateLods(objLs, lodLvl='lodC', reduceIter=4)
	mc.parent(lodC, lodsMasterGrp)
	lockAttr([lodC], attrLs)
	#renameHrq(lodC, 'lodC')
	#lodB
	lodB = generateLods(objLs, lodLvl='lodB', reduceIter=2)
	mc.parent(lodB, lodsMasterGrp)
	lockAttr([lodB], attrLs)
	#renameHrq(lodB, 'lodB')
	#lodA
	lodA = mc.rename(objLs[0], '%s_lodA' % objLs[0])
	mc.parent(lodA, lodsMasterGrp)
	#lodsMaster			
	lodsMasterGrp = mc.rename(lodsMasterGrp, objLs[0])
	#creating lods visibility switch
	if not mc.objExists('%s.lod' % lodsMasterGrp):
		createVisibilitySwitch(lodsMasterGrp, [lodA, lodB, lodC])
	#deleting history
	deleteHist(objLs)
	return lodsMasterGrp

##################creates set for selection################
def createSet(setName, rm=False):
	if mc.objExists(setName):
		if rm:
			mc.lockNode(setName, lock=False)
			mc.rename(setName, '%s_' % setName)
		else:
			return
	newSet = mc.sets(n=setName)
	return newSet

###################connects lods visibility##################
def createVisibilitySwitch(masterGrp, slaveGrpLs):
	mc.select(masterGrp, r=True)
	mc.addAttr(ln="lod", at="enum", en="lodA:lodB:lodC:")
	lodAGrp, lodBGrp, lodCGrp = slaveGrpLs
	lodACndt = mc.shadingNode('condition', asUtility=True)
	lodBCndt = mc.shadingNode('condition', asUtility=True)
	lodCCndt = mc.shadingNode('condition', asUtility=True)
	cndtNodeLs = [lodACndt, lodBCndt, lodCCndt]
	cndtSecondTerm = 0
	for cndtNode in cndtNodeLs:
   		mc.setAttr('%s.colorIfTrueR' % cndtNode, 1)
   		mc.setAttr('%s.colorIfFalseR' % cndtNode, 0)
   		mc.setAttr('%s.secondTerm' % cndtNode, cndtSecondTerm)
   		cndtSecondTerm += 1
	mc.connectAttr('%s.lod' % masterGrp, '%s.firstTerm' % lodACndt)
	mc.connectAttr('%s.outColorR' % lodACndt, '%s.visibility' % lodAGrp)
	mc.connectAttr('%s.lod' % masterGrp, '%s.firstTerm' % lodBCndt)
	mc.connectAttr('%s.outColorR' % lodBCndt, '%s.visibility' % lodBGrp)
	mc.connectAttr('%s.lod' % masterGrp, '%s.firstTerm' % lodCCndt)
	mc.connectAttr('%s.outColorR' % lodCCndt, '%s.visibility' % lodCGrp)


#################decimates obj mesh###########################
def decimate(objLs, iterations=1):
	for obj in objLs:
		mc.select(obj, r=True)
		for i in range(0, iterations):
			mc.polyReduce(ver=1, trm=0, p=25, top=True, kqw=1, shp=0.5)

##################deletes channels############################
def deleteChannels(objLs, hierarchy=False):
	if hierarchy:
		for obj in objLs:
			mc.delete(obj, c=True, hi='None', cp=True, s=True)
	else:
		mc.delete(objLs[0], c=True, hi='None', cp=True, s=True)

##################deletes animation###########################
def deleteAnimation(objLs):
	try:
		objConn = mc.listConnections(allObj)
		for conn in objConn:
			connType = mc.nodeType(conn)
			if connType.startswith('animCurve'):
				mc.delete(conn)
	except TypeError:
		pass

#############deletes full or partial history##################
def deleteHist(objLs, partial=False):
	for obj in objLs:
		if partial:
			mc.bakePartialHistory(ppt=True )
		else:
			mc.delete(ch=True, c=True, e=True, cn=True)

###########deletes icSets connected to selection##############			
def deleteICDataSet(objLs):
	for obj in objLs:
		if mc.objExists('%s.icARefTag' % obj):
			mc.setAttr('%s.icARefTag' % obj, l=False)
			mc.deleteAttr('%s.icARefTag' % obj)
		objSetLs = mc.listSets(o=obj)
		if objSetLs:
			for objSet in objSetLs:
				if mc.nodeType(objSet) == 'ICSet':
					mc.setAttr('%s.overrideComponentDisplay' % objSet, l=False)
					mc.setAttr('%s.overrideComponentDisplay' % objSet, 0)
					mc.delete(objSet)
					break

#############deletes imgPlane from camera#####################
def deleteIM(objLs):
	objLsShape = mc.listRelatives(objLs[0], s=True)
	connectionsLs = mc.listConnections(objLsShape[0])
	imPlane = ''
	#getting imgPlane
	if connectionsLs != None:
		for connection in connectionsLs:
			if mc.nodeType(connection) == 'imagePlane':
				imPlane = connection
	if imPlane != '':
		mc.delete(imPlane)

########################exports all#######################
def exportAll(pathToPblAsset, fileType):
	mc.file(pathToPblAsset, typ=fileType, f=True, ea=True)

##############exports animation curves via atom###########
def exportAnimation(pathToPblAsset, pblDir, objLs):
	mayaAppPath = os.path.split(os.environ['IC_MAYA_EXECUTABLE'])[0]
	#plugin = os.path.join(mayaAppPath, 'plug-ins/atomImportExport.bundle')
	mc.loadPlugin('atomImportExport', qt=True)
	startFr = mc.playbackOptions(min=True, q=True)
	endFr = mc.playbackOptions(max=True, q=True)
	mc.select(objLs[0], r=True)
	mc.file(pathToPblAsset,
	typ='atomExport',
	op="precision=8;statics=1;baked=0;sdk=1;constraint=1;animLayers=1;selected=childrenToo;whichRange=2;range=%s:%s;hierarchy=none;controlPoints=0;useChannelBox=1;options=keys;copyKeyCmd=-animation objects -time >%s:%s> -float >%s:%s> -option keys -hierarchy none -controlPoints 0" % (startFr, endFr, startFr, endFr, startFr, endFr),
	es=True,
	f=True)

#####################export geo types#####################
def exportGeo(objLs, geoType, pathToPblAsset):
	mayaAppPath = os.path.split(os.environ['IC_MAYA_EXECUTABLE'])[0]
	if geoType == 'abc':
		plugin = 'AbcExport'
		mc.loadPlugin(plugin, qt=True)
		minFrame = int(mc.playbackOptions(min=True, q=True))
		maxFrame = int(mc.playbackOptions(max=True, q=True))
		#minFrame = int(os.environ['IC_STARTFRAME'])
		#maxFrame = int(os.environ['IC_ENDFRAME'])
		abcJob = '-fr %s %s -s 1 -uv -ws -ef -rt %s -f %s' % (minFrame, maxFrame, objLs[0], pathToPblAsset)
		mc.AbcExport(j=abcJob)
		return
	if geoType == 'vrmesh':
		objLs[0] = pathToPblAsset.split('/')[-1]
		pathToPblAsset = pathToPblAsset.split('/')[:-1]
		pathToPblAsset = '/'.join(pathToPblAsset)
		mel.eval('''vrayCreateProxy -exportType 1 -previewFaces 75000 -dir "%s" -fname "%s" -animOn -animType 1 
		-velocityOn -velocityIntervalStart -0.5 -velocityIntervalEnd 0.5;''' % (pathToPblAsset, objLs[0])) # Changed velocity values to default, was 0 & 0.05
		return
	if geoType == 'sd':
		plugin = os.path.join(os.environ['IC_BASEDIR'], 'rsc', 'maya', 'plugins', 'realflow.bundle')
		mc.loadPlugin(plugin, qt=True)
		mc.realflow(exportSD=True, selected=True, usePlaybackRange=True, deformation=True, file=pathToPblAsset)
		return
	if geoType == 'obj':
		fileType = 'OBJexport'
		fileExtension = '.obj'
		plugin = 'objExport'
		fileOptions = 'groups=1;ptgroups=1;materials=0;smoothing=1;normals=1'
	elif geoType == 'fbx':
		fileType = 'FBX export'
		fileExtension = '.fbx'
		plugin = 'fbxmaya'
		fileOptions = 'v=0'
	mc.loadPlugin(plugin, qt=True)
	mc.select(objLs[0])
	mc.file(pathToPblAsset,
	op=fileOptions, 
	typ=fileType, 
	force=True, 
	es=True)

#################exports locators as nulls#################
def exportNulls(objSel, objLs, pathToPblAsset):
	nullLs = []
	nullCount = 1
	nullGrp =  mc.group(n='nullGrp_tmp', em=True)
	minFrame = int(mc.playbackOptions(min=True, q=True))
	maxFrame = int(mc.playbackOptions(max=True, q=True))
	for obj in objLs:
		if mc.nodeType(mc.listRelatives(obj, s=True)) == 'locator':
			null = mc.duplicate(obj, n='null_%s' % nullCount, ic=True)
			mc.parent(null, nullGrp)
			mc.bakeResults(null, hi='both', sm=True, s=True, dic=True, time=(minFrame, maxFrame))
			nullCount += 1
	mc.rename(objSel, '%s_tmp' % objSel)
	nullGrp = mc.rename(nullGrp, objSel)
	mc.select(nullGrp, r=True)
	mc.file(pathToPblAsset, typ='mayaAscii', es=True, f=True)
	mc.delete(nullGrp)	
	mc.rename('%s_tmp' % objSel, objSel)

##################exports selection#######################
def exportSelection(pathToPblAsset, fileType):
	mc.file(pathToPblAsset, typ=fileType, es=True, f=True)

####################freezes transforms####################
def freezeTrnsf(objLs):
	for obj in objLs:
		mc.select(obj, r=True)
		mc.makeIdentity(apply=True, t=True, r=True, s=True)

###########generates  a lower level of detail#############
def generateLods(objLs, lodLvl, reduceIter):
	mc.select(objLs[0])
	objLod = mc.duplicate(n='%s_%s' % (objLs[0], lodLvl), rr=True, rc=True)[0]
	allObjLs = mc.listRelatives(objLod, ad=True, typ='transform')
	for obj in allObjLs:
		try:
			mc.listRelatives(obj, s=True)[0]
			mc.select(obj, r=True)
			mel.eval('polyCleanupArgList 3 { "0","1","1","0","0","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","1","0" }')
			for i in range(0, reduceIter):
				mc.polyReduce(ver=1, trm=0, p=25, top=True, kqw=1, shp=0.5)
			mc.select(obj, r=True)
			mc.delete(ch=True, c=True, e=True, cn=True)
		except:
			pass
	return objLod

###############gets all attributes in an ICSet############
def getICSetAttrs(ICSet):
	icSetAttrDic = {}
	attrLs = ['icAsset', 'icAssetRootDir', 'icRefTag', 'icAssetType', 'icVersion', 'icAssetExt', 'icAssetCompatibility', 'Notes']
	for attr in attrLs:
		attrFullPath = '%s.%s' % (ICSet, attr)
		if mc.objExists(attrFullPath):
			icSetAttrDic[attr] = (mc.getAttr(attrFullPath))
	return icSetAttrDic


def getScene():
	""" Returns filename and path of currently open scene.
		Deprecated: superseded by scenemanager.get_current_name()
		Still in use by publishing modules
	"""
	sceneName = mc.file(q=True, sceneName=True)
	return sceneName
	# if sceneName:
	# 	return sceneName
	# else:
	# 	return 'untitled scene'


def getTransforms(obj):
	""" Gets selected obj worldspace transforms.
	"""
	try:
		objSLs = mc.xform(obj, q=True, s=True, ws=True)
		objRLs = mc.xform(obj, q=True, ro=True, ws=True)
		objTLs = mc.xform(obj, q=True, t=True, ws=True)
		for i in range(len(objSLs)):
			objSLs[i] = round(objSLs[i], 3)
		for i in range(len(objRLs)):
			objRLs[i] = round(objRLs[i], 3)
		for i in range(len(objTLs)):
			objTLs[i] = round(objTLs[i], 3)
		return objTLs, objRLs, objSLs
	except:
		return


#groups manual lods in model and creates visibility switch#
def groupManualLods(objLs, lodA, lodB, lodC):
	lodsMasterGrp = objLs[0]
	if not lodA:
		return
	else:
		lodA = mc.rename(lodA, '%s_lodA' % objLs[0])
	if not lodB:
		lodB = mc.group(n='%s_lodB' % objLs[0], em=True)
		mc.parent(lodB, objLs[0])
	if not lodC:
		lodC = mc.group(n='%s_lodC' % objLs[0], em=True)
		mc.parent(lodC, objLs[0])
	#creating lods visibility switch
	if not mc.objExists('%s.lod' % lodsMasterGrp):
		createVisibilitySwitch(lodsMasterGrp, [lodA, lodB, lodC])
	#deleting history
	deleteHist(objLs)
	return lodsMasterGrp


def icDataSet(obj, assetData, update=None, drawOverrides=True, addElements=True):
	""" Create Icarus data set node.
		TODO: Clean up draw overrides node creation
	"""
	mc.loadPlugin('gps_ICSet', qt=True)

	# Store current selection
	currentSlLs = mc.ls(sl=True)

	if update:
		dataSet = update

	else:
		# Clear current selection and select all nodes gathered in objLs
		mc.select(cl=True)
		if mc.objExists(obj):
			mc.select(obj)

		# Create set with selection
		dataSet = mc.createNode('ICSet', n='ICSet_'+assetData.get_attr('asset', 'assetPblName'))
		if addElements:
			mc.sets(obj, forceElement=dataSet, edit=True)
		if drawOverrides:
			# Set default component display
			mc.setAttr(dataSet+'.overrideComponentDisplay', 1)
			mc.setAttr(dataSet+'.icAssetDisplay', 2)
			# Create condition nodes for component display overrides
#			condition1 = mc.createNode('condition', n=dataSet+'_condition1')
#			mc.setAttr(condition1+'.colorIfTrueR', 1)
#			mc.setAttr(condition1+'.colorIfTrueG', 0)
#			mc.setAttr(condition1+'.colorIfTrueB', 0)
#			mc.setAttr(condition1+'.colorIfFalseR', 0)
#			mc.setAttr(condition1+'.colorIfFalseG', 0)
#			mc.setAttr(condition1+'.colorIfFalseB', 0)
#			condition2 = mc.createNode('condition', n=dataSet+'_condition2')
#			mc.setAttr(condition2+'.secondTerm', 1)
#			mc.setAttr(condition2+'.colorIfTrueR', 0)
#			mc.setAttr(condition2+'.colorIfTrueG', 0)
#			mc.setAttr(condition2+'.colorIfTrueB', 0)
#			mc.setAttr(condition2+'.colorIfFalseR', 1)
#			mc.setAttr(condition2+'.colorIfFalseG', 0)
#			mc.setAttr(condition2+'.colorIfFalseB', 0)
#			# Connect conditions to the dataSet
#			mc.connectAttr(dataSet+'.icAssetDisplay', condition1+'.firstTerm', f=True)
#			mc.connectAttr(condition1+'.outColorR', obj+'.overrideLevelOfDetail', f=True)
#			mc.connectAttr(dataSet+'.icAssetDisplay', condition2+'.firstTerm', f=True)
#			mc.connectAttr(condition2+'.outColorR', obj+'.overrideShading', f=True)
			mc.connectAttr(dataSet+'.overrideComponentDisplay', obj+'.drawOverride.overrideEnabled', f=True)
			mc.connectAttr(dataSet+'.overrideComponentColor', obj+'.drawOverride.overrideColor', f=True)
# 			expString = """switch (%s.icAssetDisplay) {
# 	case 0:
# 		%s.overrideShading = 0;
# 		%s.overrideLevelOfDetail = 1;
# 		break;
# 	case 1:
# 		%s.overrideShading = 0;
# 		%s.overrideLevelOfDetail = 0;
# 		break;
# 	case 2:
# 		%s.overrideShading = 1;
# 		%s.overrideLevelOfDetail = 0;
# 		break;
# }
# """ % (dataSet, obj, obj, obj, obj, obj, obj)
# 			exp = mc.expression(alwaysEvaluate=False, string=expString, name=dataSet+'_exp')

	# Add asset metadata to set
	assetTag(dataSet, assetData.get_attr('asset', 'asset'))
	referenceTag(dataSet, assetData.get_attr('asset', 'assetPblName'))
	assetTypeTag(dataSet, assetData.get_attr('asset', 'assetType'))
	versionTag(dataSet, assetData.get_attr('asset', 'version'))
	assetExtTag(dataSet, assetData.get_attr('asset', 'assetExt'))
	notesTag(dataSet, assetData.get_attr('asset', 'notes'))

	try:
		assetRootDir(dataSet, assetData.get_attr('asset', 'assetRootDir'))
	except AttributeError:
		pass
	try:
		compatibleTag(dataSet, assetData.get_attr('asset', 'compatible'))
	except (AttributeError, RuntimeError):
		pass

	# Clear gather selection and restore original selection
	mc.select(cl=True)
	if currentSlLs:
		for currentSl in currentSlLs:
			mc.select(currentSl, add=True)

	return dataSet


########################imports referenced nodes#################
def importRefs(objLs):
	for obj in objLs: 
		if mc.referenceQuery(obj, inr=True):
			refFile = mc.referenceQuery(obj, f=True)
			mc.file(refFile, ir=True)

#################locks object attributes#####################
def lockAttr(objLs, attrLs, lock=True, children=True):
	for obj in objLs:
		if children:
			try:
				allObjLs = mc.listRelatives(obj, ad=True, typ='transform')
				allObjLs.append(obj)
			except:
				allObjLs = [obj]
		else:
			allObjLs = [obj]
		for allObj in allObjLs:
			for attr in attrLs:
				if lock:
					mc.setAttr(allObj + attr, lock=True)
				else:
					mc.setAttr(allObj + attr, lock=False)

###########################locks node########################
def lockNode(objLs, lock=True):
	for obj in objLs:
		if lock:
			mc.lockNode(obj, lock=True)
		else:
			mc.lockNode(obj, lock=False)

############checks if lods already exist in model############
def lodSystemCheck(objLs):
	lodA, lodB, lodC = None, None, None
	for child in mc.listRelatives(objLs[0], c=True):
		if 'loda' in child.lower():
			lodA = child
		elif 'lodb' in child.lower():
			lodB = child
		elif 'lodc' in child.lower():
			lodC = child
		else:
			return
	return lodA, lodB, lodC


# def newScene():
# 	""" Create a new scene.
# 		Deprecated: superseded by scenemanager.file_new()
# 	"""
# 	mc.NewScene()
# 	update()


###################node type check########################
def nodetypeCheck(obj):
	nodeType_ = mc.nodeType(obj)
	return nodeType_

###############adds publish notes as custom attr##########
def notesTag(obj, pblNotes):
	if pblNotes is None:
		pblNotes = ""
	notesAttr = mc.listAttr(obj, st='Notes')
	if not notesAttr:
		mc.addAttr(obj, ln='Notes', dt='string')
	mc.setAttr('%s.Notes' % obj, l=False)
	mc.setAttr('%s.Notes' % obj, pblNotes, typ='string', l=True)


def openScene(filePath, extension=None, dialog=True, updateRecentFiles=True):
	""" Open a saved scene.
		Deprecated: superseded by scenemanager.file_open()
		Still in use by publishing modules
	"""
	if mel.eval('saveChanges("")'):
		if dialog:
			openFolder = mc.fileDialog2(ds=2, fm=1, ff=extension, dir=filePath, cap='[GPS] Open', okc='Open')
			if openFolder == None:
				return
		else:
			openFolder = [filePath]
		filename = mc.file(openFolder[0], open=True, force=True, ignoreVersion=True)
		if updateRecentFiles:
			recent_files.recents.put(filename)


######parent constraints two identical hierarchies########
def parentCnstrHrq(obj1, obj2):
	hrq1 = mc.listRelatives(obj1, ad=True, typ='transform')
	hrq2 = mc.listRelatives(obj2, ad=True, typ='transform')
	for i in range(0, len(hrq1)):
		mc.parentConstraint(hrq1[i], hrq2[i])


def redirectScene(sceneFile):
	""" Redirect scene name and path.
		Deprecated: superseded by scenemanager.set_current_name()
		Still in use by publishing modules
	"""
	mc.file(rename=sceneFile)


#####relinks cacheNode path and retrieves controlled geo######
def relinkCache(cacheLs, cachePath, asset, version):
	originalcachePath = mc.getAttr(cacheLs[0]+'.cachePath')
	if os.path.isdir(originalcachePath) == True:
		cacheFile_ls = os.listdir(originalcachePath)
		if len(cacheFile_ls) > 1:
			for cacheFile in cacheFile_ls:
				filePath = os.path.join(originalcachePath, cacheFile)
				shutil.copy(filePath, cachePath)
			mc.setAttr(cacheLs[0]+'.cachePath', cachePath, type='string')
			mc.rename(cacheLs[0], asset  + '_%s' % version)

###############relinks camera imagePlane####################
def relinkImPlate(objLs, texturePath):
	objLsShape = mc.listRelatives(objLs[0], s=True)
	connectionsLs = mc.listConnections(objLsShape[0])
	imPath = ''
	#getting imgPlane path
	if connectionsLs != None:
		for connection in connectionsLs:
			if mc.nodeType(connection) == 'imagePlane':
				imPlane = connection
				imPath = mc.getAttr(imPlane + '.imageName')
	#copying img seq to publish path
	if imPath != '' :
		imPath = imPath.split('/')
		del imPath[-1]
		imPath = '/'.join(imPath)
		if os.path.isdir(imPath) == True:
			imFilesLs = os.listdir(imPath); imFilesLs.sort()
			for imFile in imFilesLs:
				copyFile = imPath + '/%s' % imFile
				imFile = imFile
				shutil.copy(copyFile, texturePath)
			mc.setAttr(imPlane + '.imageName', texturePath + '/%s' % imFile, type='string')

###################adds reference tag as extra attr#######
def referenceTag(obj, assetPblName):
	refTag = mc.listAttr(obj, st='icRefTag')
	if not refTag:
		mc.addAttr(obj, ln='icRefTag', dt='string')
	mc.setAttr('%s.icRefTag' % obj, l=False)
	mc.setAttr('%s.icRefTag' % obj, assetPblName, typ='string', l=True)


def updateTextures(txPath, txObjLs=None, updateMaya=True, copy=True):
	"""
    Handles copying and updating texture file node paths for incoming txObjLs
    :param txPath: The directory of the new texture file path.
    :param txObjLs: A list of objects.
    :param updateMaya: Updated the file paths in the current scene.
    :param copy: Makes a copy of the textures to the directory txPath
    :return:
        If updateMaya=True: A dictionary of all modified texture 
        file nodes{texture File Node: file path before modification}
        If updateMaya=False: None
    """
	# txFullPath, txRelPath = txPaths
	currentPaths = {}
	if not txObjLs:
		fileNode = mc.itemFilter(byType='file')
		fileNodeLs = mc.lsThroughFilter(fileNode)
	else:
		txObjLsHist = mc.listHistory(txObjLs, f=True)
		txObjLsHist = list(set(txObjLsHist))
		txObjLsShd = mc.listHistory(txObjLsHist)
		txObjLsShd = list(set(txObjLsShd))
		fileNodeLs = mc.ls(txObjLsShd, type='file')
		fileNodeLs = list(set(fileNodeLs))
	if fileNodeLs:
		fileNodeLs = list(set(fileNodeLs))
		for fileNode in fileNodeLs:
			if not mc.getAttr('%s.useFrameExtension' % fileNode):
				filePath = mc.getAttr(fileNode + '.fileTextureName')
				#getting full path from mayaAttributes
				oldFilePath = filePath
				filePath = os.path.expandvars(filePath)
				if os.path.isfile(filePath):
					fileName = filePath.split('/')[-1]
					if copy:
						shutil.copy(filePath, txPath)
					if updateMaya:
						currentPaths[fileNode] = oldFilePath
						#vray does not support relative path env vars in texures. Until this changes full path is written
						#mc.setAttr(fileNode + '.fileTextureName', os.path.join(txRelPath, fileName), type='string')
						mc.setAttr(fileNode + '.fileTextureName', os.path.join(txPath, fileName), type='string')
						
	if updateMaya:
		return currentPaths
	else:
		return


def relinkTextures(txDict):
	"""
	Changes the path directory of the incoming txFileNodes
	:param txDict: A dict of txFileNode Keys and path values
	"""
	for txFileNode, path in txDict.items():
		mc.setAttr(txFileNode + '.fileTextureName', path, type='string')

####################removes drawing overrides##################
#returns 0, if it does not override anything, 1 if objects cvould not be overriden because of display layers, 2 otherwise
def removeDrawOverride(objLs=None, icSet=False, hierarchy=True, shapes=True, overrideLayers=False):
	result = 2
	if icSet:
		hierarchy=True
		shapes=True
		#checks if selection is an icSet
		if not objLs or mc.nodeType(objLs[0]) != 'ICSet':
			result = 0
			return result
		else:
			objLs = mc.sets(objLs[0], q=True)
			if not objLs:
				result = 0
				return result
	else:
		if not objLs:
			result = 0
			return result

	if hierarchy:
		allObjLs = mc.listRelatives(objLs[0], ad=True, f=True, typ='transform')
		if allObjLs:
			allObjLs.append(objLs[0])
		else:
			allObjLs = list(objLs)
	else:
		allObjLs = list(objLs)

	#Removing asset connected to icSet from allObjLs
	if icSet:
		try:
			allObjLs.remove(objLs[0])
		except ValueError:
			pass

	#Overriding display in allObjLs
	for allObjs in allObjLs:
		#overriding transforms
		displayLayer = mc.listConnections(allObjs, type="displayLayer")
		if not overrideLayers and displayLayer:
			result = 1
			continue
		else:
			mc.editDisplayLayerMembers("defaultLayer", allObjs, noRecurse=True)
		mc.setAttr('%s.overrideEnabled' % allObjs, l=False)
		connectedAttr = mc.listConnections('%s.overrideEnabled' % allObjs, p=True)
		if connectedAttr:
		  mc.disconnectAttr(connectedAttr[0], '%s.overrideEnabled' % allObjs)
		mc.setAttr('%s.overrideEnabled' % allObjs, 0)
		#overriding shapes
		if shapes:
			objSh = mc.listRelatives(allObjs, s=True, f=True)
			if objSh:
				mc.setAttr('%s.overrideEnabled' % objSh[0], l=False)
				connectedShAttr = mc.listConnections('%s.overrideEnabled' % objSh[0], p=True)
				if connectedShAttr:
					mc.disconnectAttr(connectedShAttr[0], '%s.overrideEnabled' % objSh[0])
				mc.setAttr('%s.overrideEnabled' % objSh[0], 0)

	#lastly overriding shape of ICSet connected object
	if shapes:
		objSh = mc.listRelatives(objLs[0], s=True, f=True)
		if objSh:
			mc.setAttr('%s.overrideEnabled' % objSh[0], l=False)
			connectedShAttr = mc.listConnections('%s.overrideEnabled' % objSh[0], p=True)
			if connectedShAttr:
				mc.disconnectAttr(connectedShAttr[0], '%s.overrideEnabled' % objSh[0])
			mc.setAttr('%s.overrideEnabled' % objSh[0], 0)
	return result

####################renames paired hierarchy###################
def renameHrq(hrq, suffix):
	hrq = mc.listRelatives(hrq, ad=True, typ='transform')
	for i in range(0, len(hrq)):
		mc.rename(hrq[i], '%s_%s' % (hrq[i], suffix))

####################renames objects in list####################
def renameObj(objLs, newName, oldName=False):
	renamedObjLs = []
	for obj in objLs:
		if oldName:
			newName = obj.replace(oldName, newName)
		objRenamed = mc.rename(obj, newName)
		newName = ''
		renamedObjLs.append(objRenamed)
	return renamedObjLs


def saveFile(fileType, updateRecentFiles=True):
	""" Save Maya scene.
		Deprecated: superseded by scenemanager.file_save_as()
		Still in use by publishing modules
	"""
	if fileType == 'ma':
		fileType = 'mayaAscii'
	elif fileType == 'mb':
		fileType = 'mayaBinary'
	filename = mc.file(options='v=0', force=True, save=True, type=fileType)
	if updateRecentFiles:
		recent_files.recents.put(filename)
	os_wrapper.setPermissions(filename)
	print "\nScene saved: %s" %filename, # print confirmation - the trailing comma make the message visible in Maya's command line output field


# def saveFileAs(filePath, extension, updateRecentFiles=True):
# 	""" Save Maya scene as.
# 		Deprecated: superseded by scenemanager.file_save_dialog()
# 	"""
# 	saveFolder = mc.fileDialog2(ds=2, fm=0, ff=extension, dir=filePath, cap='[GPS] Save As', okc='Save')
# 	if saveFolder == None:
# 		return
# 	else:
# 		mc.file(rename=saveFolder[0])

# 		fileType = os.path.splitext(saveFolder[0])[1][1:] # get the extension without a leading dot
# 		saveFile(fileType, updateRecentFiles)


def snapShot(output_folder, isolate=True, fit=False):
	""" Generate viewport snapshot.
	"""
	# Get current selection, frame and panel
	currentSel = mc.ls(sl=True)
	currentFrame = mc.currentTime(q=True)
	currentPanel = mc.playblast(ae=True)

	# Isolate the current object
	if isolate:
		mc.isolateSelect(currentPanel, state=1)
		mc.isolateSelect(currentPanel, addSelected=True)

	# Frame view to selection
	if fit:
		mc.viewFit(fitFactor=1)

	# Store current selection and deselect all
	mc.select(cl=True)

	# Generate playblast
	mc.playblast(completeFilename=os.path.join(output_folder, 'preview.jpg'), 
	#mc.playblast(filename=os.path.join(output_folder, 'preview'), 
				 frame=(currentFrame), 
				 framePadding=4, 
				 rawFrameNumbers=True, 
				 width=512, 
				 height=288, 
				 percent=100, 
				 format='image', 
				 compression='jpg', 
				 quality=90, 
				 viewer=False, 
				 offScreen=True, 
				 clearCache=True, 
				 showOrnaments=False)

	# Turn off isolate selection
	if isolate:
		mc.isolateSelect(currentPanel, state=0) 

	# Reset view
	if fit:
		mc.viewSet(previousView=True)

	# Reselect original selection
	for sel in currentSel:
		mc.select(sel, add=True)


def submitRender():
	""" Launch Render Submitter window.
	"""
	frameRange = "%s-%s" %(int(mc.getAttr('defaultRenderGlobals.startFrame')), int(mc.getAttr('defaultRenderGlobals.endFrame')))

	from tools.renderQueue import render_submit
	render_submit.run_maya(frameRange=frameRange)

	# from tools.renderQueue import render_submit
	# try:
	# 	renderSubmitUI.display()
	# except (AttributeError, UnboundLocalError):
	# 	renderSubmitUI = render_submit.renderSubmitUI(parent=render_submit._maya_main_window())
	# 	renderSubmitUI.display(frameRange=frameRange)


def submitRenderLayer():
	""" Launch Render Submitter window for the current render layer.
	"""
	frameRange = "%s-%s" %(int(mc.getAttr('defaultRenderGlobals.startFrame')), int(mc.getAttr('defaultRenderGlobals.endFrame')))
	currentLayer = mc.editRenderLayerGlobals(query=True, currentRenderLayer=True)

	from tools.renderQueue import render_submit
	# render_submit.run_maya(frameRange=frameRange, flags='-rl %s' %currentLayer)
	render_submit.run_maya(frameRange=frameRange, layers=currentLayer)
	# renderSubmitDialog = render_submit.renderSubmitDialog()
	# renderSubmitDialog.display(frameRange=frameRange, flags='-rl %s' %currentLayer)


# def update():
# 	""" Automatically set some defaults from the shot settings.
# 		Deprecated: superseded by scenemanager.set_defaults()
# 		Remove?
# 	"""
# 	unit = os.getenv('IC_LINEAR_UNIT', 'cm')
# 	angle = os.getenv('IC_ANGULAR_UNIT', 'deg')
# 	timeFormat = os.getenv('IC_TIME_UNIT', 'pal')
# 	startFrame = int(os.getenv('IC_STARTFRAME', '1001'))
# 	endFrame = int(os.getenv('IC_ENDFRAME', '1100'))
# 	inFrame = int(os.getenv('IC_INFRAME', startFrame))
# 	outFrame = int(os.getenv('IC_OUTFRAME', endFrame))
# 	psExecutable = os.getenv('IC_PS_EXECUTABLE', '')
# 	djvExecutable = os.getenv('IC_DJV_EXECUTABLE', '')

# 	# Setting defaults for Maya startup
# 	#mc.currentUnit(l=unit, a=angle, t=timeFormat)
# 	try:
# 		mc.currentUnit(l=unit)
# 		mc.optionVar(sv=('workingUnitLinear', unit))
# 		mc.optionVar(sv=('workingUnitLinearDefault', unit))
# 		# mc.optionVar(sv=('workingUnitLinearHold', unit))
# 	except RuntimeError:
# 		mc.warning("Unable to set linear unit.")
# 	try:
# 		mc.currentUnit(a=angle)
# 		mc.optionVar(sv=('workingUnitAngular', angle))
# 		mc.optionVar(sv=('workingUnitAngularDefault', angle))
# 		# mc.optionVar(sv=('workingUnitAngularHold', angle))
# 	except RuntimeError:
# 		mc.warning("Unable to set angular unit.")
# 	try:
# 		mc.currentUnit(t=timeFormat)
# 		mc.optionVar(sv=('workingUnitTime', timeFormat))
# 		mc.optionVar(sv=('workingUnitTimeDefault', timeFormat))
# 		# mc.optionVar(sv=('workingUnitTimeHold', timeFormat))
# 	except RuntimeError:
# 		mc.warning('Unable to set time unit.')

# 	mc.optionVar(fv=('playbackMinRangeDefault', startFrame))
# 	mc.optionVar(fv=('playbackMinDefault', inFrame))
# 	mc.optionVar(fv=('playbackMaxRangeDefault', endFrame))
# 	mc.optionVar(fv=('playbackMaxDefault', outFrame))

# 	mc.optionVar(sv=('upAxisDirection', 'y'))

# 	mc.optionVar(sv=('EditImageDir', psExecutable))
# 	mc.optionVar(sv=('PhotoshopDir', psExecutable))

# 	mc.optionVar(sv=('PlayblastCmdAvi', djvExecutable))
# 	mc.optionVar(sv=('PlayblastCmdQuicktime', djvExecutable))
# 	mc.optionVar(sv=('ViewImageDir', djvExecutable))
# 	mc.optionVar(sv=('ViewSequenceDir', djvExecutable))

# 	mc.playbackOptions(animationStartTime=startFrame, 
# 	                   minTime=inFrame, 
# 	                   maxTime=outFrame, 
# 	                   animationEndTime=endFrame, 
# 	                   playbackSpeed=0, 
# 	                   maxPlaybackSpeed=1)


###################updates ic set version#################
def updateIcDataSetVersion(version, ICSet=None):
	if not ICSet:
		ICSet = mc.ls(sl=True)
	if not ICSet or mc.nodeType(ICSet)!= 'ICSet':
		return
	else:
		return

###################adds version tag as extra attr#########
def versionTag(obj, version):
	vTag = mc.listAttr(obj, st='icVersion')
	if not vTag:
		mc.addAttr(obj, ln='icVersion', dt='string')
	mc.setAttr('%s.icVersion' % obj, l=False)
	mc.setAttr('%s.icVersion' % obj, version, typ='string', l=True)

#########################.nk camera export####################
def nkCameraExport(objLs, pblDir, assetPblName, version):
	pathtoPblAsset = os.path.join(pblDir, '%s.nk' % assetPblName)
	objlsShape = mc.listRelatives(objLs[0], s=True)
	minFrame = int(mc.playbackOptions(min=True, q=True))
	maxFrame = int(mc.playbackOptions(max=True, q=True))
	mc.currentTime(minFrame)
	currentFrame = mc.currentTime(q=True)
	nkFile = open(pathtoPblAsset, 'w')
	nkFile.write('Camera {\n selectable false\n rot_order XYZ\n')
	#translation 
	#tx
	nkFile.write(' translate {{curve x%s' % minFrame)
	while currentFrame <= maxFrame:
	    tx = str(mc.getAttr(objLs[0] + '.tx', t=currentFrame))
	    nkFile.write(' ' + tx)
	    currentFrame += 1
	nkFile.write('} ')
	#ty
	mc.currentTime(minFrame)
	currentFrame = mc.currentTime(q=True)
	nkFile.write('{curve x%s' % minFrame)
	while currentFrame <= maxFrame:
	    ty = str(mc.getAttr(objLs[0] + '.ty', t=currentFrame))
	    nkFile.write(' ' + ty)
	    currentFrame += 1
	nkFile.write('} ')
	#tz
	mc.currentTime(minFrame)
	currentFrame = mc.currentTime(q=True)
	nkFile.write('{curve x%s' % minFrame)
	while currentFrame <= maxFrame:
	    tz = str(mc.getAttr(objLs[0] + '.tz', t=currentFrame))
	    nkFile.write(' ' + tz)
	    currentFrame += 1
	nkFile.write('}}\n')
	#rotation
	#rx
	mc.currentTime(minFrame)
	currentFrame = mc.currentTime(q=True)
	nkFile.write(' rotate {{curve x%s' % minFrame)
	while currentFrame <= maxFrame:
	    rx = str(mc.getAttr(objLs[0] + '.rx', t=currentFrame))
	    nkFile.write(' ' + rx)
	    currentFrame += 1
	nkFile.write('} ')
	#ry
	mc.currentTime(minFrame)
	currentFrame = mc.currentTime(q=True)
	nkFile.write('{curve x%s' % minFrame)
	while currentFrame <= maxFrame:
	    ry = str(mc.getAttr(objLs[0] + '.ry', t=currentFrame))
	    nkFile.write(' ' + ry)
	    currentFrame += 1
	nkFile.write('} ')
	#rz
	mc.currentTime(minFrame)
	currentFrame = mc.currentTime(q=True)
	nkFile.write('{curve x%s' % minFrame)
	while currentFrame <= maxFrame:
	    rz = str(mc.getAttr(objLs[0] + '.rz', t=currentFrame))
	    nkFile.write(' ' + rz)
	    currentFrame += 1
	nkFile.write('}}\n')
	#focal lenght
	mc.currentTime(minFrame)
	currentFrame = mc.currentTime(q=True)
	nkFile.write(' focal {{curve x%s' % minFrame)
	while currentFrame <= maxFrame:
	    fl = str(mc.getAttr(objlsShape[0] + '.fl', t=currentFrame))
	    nkFile.write(' ' + fl)
	    currentFrame += 1
	nkFile.write('}}\n')
	#horizontal and vertical apertures
	haperture = mc.getAttr(objlsShape[0] + '.horizontalFilmAperture')
	vaperture = mc.getAttr(objlsShape[0] + '.verticalFilmAperture')
	#maya's camera aperture settings are in inches and nuke mm. This needs to be converted.
	#converting aperture for inches to milimeters
	haperture = haperture * 25.4
	vaperture = vaperture * 25.4
	nkFile.write(' haperture %s' % haperture + '\n vaperture %s' % vaperture )
	#camera scale
	nkFile.write('\n win_scale {1 1}\n')
	#camera name and label
	nkFile.write(' name %s\n }' % assetPblName)
	nkFile.close()


def nkFileNodeExport(objLs, nodeType, fileName, pblDir, visiblePblDir, assetPblName, version):
	""" Export Nuke node from Maya.
	"""
	pathtoPblAsset = os.path.join(pblDir, '%s.nk' % assetPblName)
	filePath = os.path.join(visiblePblDir, 'tx', fileName)

	# Make file path relative
	filePath = os_wrapper.relativePath(filePath, 'IC_SHOTPUBLISHDIR', tokenFormat='nuke')

	nkFile = open(pathtoPblAsset, 'w')
	nkFile.write('''Read {
	inputs 0
	file "%s"
	cacheLocal always
	name %s
	selected true
	cached true\n}''' % (filePath, assetPblName))
	nkFile.close()
	return

