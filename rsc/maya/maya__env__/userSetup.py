#!/usr/bin/python

# [GPS] userSetup.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2017 Gramercy Park Studios
#
# Commands to execute at Maya startup.


import os
import sys

sys.path.append(os.path.join(os.environ['IC_BASEDIR'], 'core', 'ui'))
import env__init__
env__init__.appendSysPaths()

import maya.cmds as mc
os.environ['IC_ENV'] = 'MAYA'
import mayaOps
import osOps
import verbose


# Deploy custom tool shelves
shelfResources = os.path.join(os.environ['IC_BASEDIR'], 'rsc', 'maya', 'shelves')
mayaShelvesDir = os.path.join(mc.about(preferences=True), 'prefs', 'shelves')

try:
	osOps.copyDirContents(shelfResources, mayaShelvesDir)
	verbose.gpsToolDeploy('OK')
except:
	verbose.gpsToolDeploy('Failed')


# List of plugins to load by default
ma_pluginLs = ['AbcExport', 
               'AbcImport', 
               'fbxmaya', 
               'objExport', 
               'OpenEXRLoader', 
               'tiffFloatReader']

for ma_plugin in ma_pluginLs:
	mc.loadPlugin(ma_plugin, qt=True)

