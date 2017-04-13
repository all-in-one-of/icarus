#!/usr/bin/python

# [Icarus] verbose.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2017 Gramercy Park Studios
#
# This module processes verbosity printing.


import os


statusBar = None

# Define some ANSI colour codes
# class bcolors:
# 	HEADER = '\033[95m'
# 	OKBLUE = '\033[94m'
# 	OKGREEN = '\033[92m'
# 	WARNING = '\033[93m'
# 	FAIL = '\033[91m'
# 	ENDC = '\033[0m'
# 	BOLD = '\033[1m'
# 	UNDERLINE = '\033[4m'


def message(message):
	print_(message, 3)

def warning(message):
	#print_(bcolors.WARNING + "Warning: " + message + bcolors.ENDC, 2)
	print_("Warning: " + message, 2)

def error(message):
	#print_(bcolors.FAIL + "ERROR: " + message + bcolors.ENDC, 1)
	print_("ERROR: " + message, 1)


def print_(message, verbosityLevel=3, status=True, log=False):
	""" Print the message to the console.
		If 'status' is True, the message will be shown on the main UI status bar.
		If 'log' is True, the message will be written to a logfile (not yet implemented).

		Verbosity Levels:
		0 - Nothing is output
		1 - Errors and messages requiring user action
		2 - Errors and warning messages
		3 - Info message (default)
		4 - Detailed info messages
	"""
	global statusBar

	try:
		verbositySetting = int(os.environ['IC_VERBOSITY'])
	except KeyError:
		verbositySetting = 3

	# Print message to the console
	if verbosityLevel <= verbositySetting:
		print(message)

	# Print message to the status bar
	if verbosityLevel <= 3 and status and statusBar is not None:
		timeout = 1800 + max(2400, len(message)*60)
		statusBar.showMessage(message, timeout)


def registerStatusBar(statusBarObj):
	""" Register a QStatusBar object with this module so that messages can be printed to the appropriate UI status bar.
	"""
	global statusBar
	statusBar = statusBarObj


def pluralise(noun, count=None):
	""" Pluralise nouns.
		if 'count' variable is given, return singular if count is 1, otherwise return plural form.
		In the name of simplicity, this function is far from exhaustive.
	"""
	if count is not None:
		if count == 1:
			return noun

	import re

	if re.search('[^fhms][ei]x$', noun):
		return re.sub('[ei]x$', 'ices', noun)
	elif re.search('[sxz]$', noun):
		return re.sub('$', 'es', noun)
	elif re.search('[^aeioudgkprt]h$', noun):
		return re.sub('$', 'es', noun)
	elif re.search('[^aeiou]y$', noun):
		return re.sub('y$', 'ies', noun)
	elif re.search('ies$', noun):
		return noun
	else:
		return noun + 's'


# Messages follow in alphabetical order...
def appPaths_noApp(app):
	warning("Application '%s' does not exist." %app)

def appPaths_noVersion(app, ver):
	warning("Application '%s' has no '%s' version." %(app, ver))

def appPaths_enterVersion():
	print_("Please enter a version.", 1)

def appPaths_guessPathFailed(os):
	warning("Failed to guess %s path." %os)

def animRequires(asset):
	print_( 'Requires %s' % asset, 1 )

def assetConflict():
	print_( 'Asset already exists in scene.', 2 )

def assetUpdateMatch():
	print_( 'Assets do not match. Update cancelled.', 2 )

def chkDirSize():
	print_( 'Comparing directory sizes...', 3 )

def concurrentPublish():
	return 'Another publish for the same asset is currently under progress. Please check your settings or try again later.'

def dailyFail():
	return 'Could not verify dailies files.'

def gpsPreview_uiValues():
	print_( 'Not all GPS Preview UI values could be read.', 2 )

def gpsToolDeploy(status):
	print_( 'Deploying GPS tools... %s' % status, 3 )

def icarusLaunch(icarusVersion, icarusLocation=""):
	print_( 'GRAMERCY PARK STUDIOS - ICARUS %s' % icarusVersion, 0 )
	print_( '[Running from "%s"]' % icarusLocation, 4 )
	print_( '\n', 0 )

def ignored(asset):
	print_( '%s ignored' % asset, 2 )

def illegalCharacters(string=''):
	print_( '"%s" contains illegal characters.' % string, 1 )

def integersInput(input):
	print_( '%s input must be integers.' % input, 1 )

def itemSel():
	print_( 'Please select one item.', 1 )

def launchApp(application):
	print_( 'Launching %s...' % application, 3 )

def launchAppNotFound(application):
	print_( 'ERROR: Unable to launch %s - the executable could not be found.' % application, 2 )

def launchAppNotSet(application):
	print_( 'ERROR: Unable to launch %s - executable path not set. Please set the correct location from the job settings window.' % application, 2 )

def jobSet(job, shot):
	print_( 'Shot set: Now working on %s - %s' % (job, shot), 3 )

def lightLinkError(lightRelinkResult):
	print_( 'Light link error: The following objects could not be relinked.\n%s' % lightRelinkResult, 1 )

def locatorsOnly():
	print_( 'Only locators can be published as nulls.', 2 )

def lodARequired():
	raise('lodA level required.')

def nameConflict(assetName):
	print_( 'Asset with name "%s" already exists in scene. Existing asset has been renamed.' % assetName, 2 )

def noAsset():
	print_( 'Could not find any compatible assets.', 1 )

def noDir():
	print_( 'Could not find the specified directory.', 1 )

def noDirContents():
	print_( 'The specified directory is empty.', 2 )

def noEnv():
	print_( 'Could not launch Icarus - No environment could be found.', 1 )

def noFile():
	print_( 'Could not find the specified file.', 1 )

def noGetTranforms():
	print_( 'Could not get object transforms.', 1 )

def noHrox(hroxFile):
	print_( '%s - File could not be found.' % hroxFile, 1 )

def noICSetsPbl():
	print_( 'ICSets cannot be selected for publishing', 1 )

def noJob(job):
	error( 'The job path "%s" does not exist. The job may have been archived, moved or deleted.' % job)

def noMainLayer():
	print_( 'Please set a main layer.', 1 )

def noNotes():
	print_( 'No notes found.', 2 )

def noPermissionsSet():
	print_( 'Warning: Permissions could not be set.', 2 )

def noReference():
	print_( 'The specified node is not a reference.', 1 )

def noRefPbl():
	print_( 'Cannot publish referenced assets.', 1 )

def noRefTag():
	print_( 'No reference tag found.', 1 )

def noRendersPbl():
	print_( 'No renders have been published.', 1 )

def noSel():
	print_( 'Nothing selected.', 2 )

def noSeq(dir):
	print_( "'%s': No sequence or bad sequence format.\nSequences must be in the format [<filename>.<padding>.<extension>]" % dir, 2 )

def noSetsPbl():
	print_( 'Sets cannot be selected for publishing.', 1 )

def noShot(shot):
	warning( 'No valid shots found in job path "%s".' % shot)

def notCamera():
	print_( 'The current selection is not a camera.', 2 )

def noVersion():
	print_( 'No versioning detected.', 1 )

def notVersionManagerCompatible(icSet):
	print_( 'The selected ICSet is not compatible with Version Manager.', 1 )

def pblFeed(msg=None, begin=None, end=None):
	if msg:
		print_( msg, 3 )
		return
	if begin:
		print_( 'Publishing...', 3 )
		return
	if end:
		print_( 'Done.', 3 )
		return

def pblRollback():
	msg = 'Current publish has been rolled back. No changes made.\nCheck console output for details.'
	print_( msg, 1 )
	return msg

def pblAssetReq():
	print_( 'Animation can only be published from published assets.', 1 )

def pblSaveSnapshot():
	print_( 'Saving snapshot...', 3 )

def pointCloudParticle():
	print_( 'pointCloud publishing requires a particle or nParticle object.', 1 )

def processing(asset=None):
	print_( 'processing: %s...' % asset, 3 )

def recentFiles_notWritten():
	print_( 'Warning: unable to write recent files configuration file.', 2 )

def redFields():
	print_( 'All fields in red are mandatory', 1 )

def renderElements(layer=None, pass_=None, versionHeader=False):
	if versionHeader:
		print_( '\n\nRENDER PUBLISH INFO: %s\n--\n[<layer>_<pass>]\n--' % versionHeader, 3 )
		return
	else:
		print_( '[%s_%s]' % (layer, pass_), 3 )

def shaderLinkError(shaderRelinkResult):
	print_( 'Shader link error: The following objects could not be relinked.\n%s' % shaderRelinkResult, 1 )

def shaderSupport():
	print_( 'The specified node is not a shading group.', 2 )

