#!/usr/bin/python
#support	:Mike Bonnington - mike.bonnington@gps-ldn.com
#title		:userPrefs
#copyright	:Gramercy Park Studios


from ConfigParser import SafeConfigParser
import os


config = SafeConfigParser()
configFile = os.path.join(os.environ['ICUSERPREFS'], 'userPrefs.ini')


def read():
	"""Read config file - create it if it doesn't exist"""

	if os.path.exists(configFile):
		config.read(configFile)

	else:
		create()


def write():
	"""Write config file to disk"""

	with open(configFile, 'w') as f:
		config.write(f)


def create():
	"""Create config file if it doesn't exist and populate with with defaults"""

	userPrefsDir = os.environ['ICUSERPREFS']

	if not os.path.exists(userPrefsDir):
		os.system('mkdir -p %s' % userPrefsDir)
		os.system('chmod -R 775 %s' % userPrefsDir)

	config.add_section('main')
	config.set('main', 'lastjob', '')
	config.set('main', 'numrecentfiles', '10')
	config.set('main', 'minimiseonlaunch', 'True')

	config.add_section('gpspreview')
	config.set('gpspreview', 'offscreen', 'True')
	config.set('gpspreview', 'noselection', 'True')
	config.set('gpspreview', 'guides', 'True')
	config.set('gpspreview', 'slate', 'True')
	config.set('gpspreview', 'launchviewer', 'True')
	config.set('gpspreview', 'createqt', 'False')

	write()


def edit(section, key, value):
	"""Set a value and save config file to disk"""

	config.set(section, key, value)

	write()