#!/usr/bin/python

# [Icarus] appLauncher.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2017 Gramercy Park Studios
#
# Handles software application launching from Icarus, auto-generates UI,
# creates folder structures, etc.


import math
import os
# import subprocess
# import sys

from Qt import QtCore, QtGui, QtWidgets
import rsc_rc  # Import resource file as generated by pyside-rcc

# Import custom modules
import appPaths
import defaultDirs  # temp
import launchApps   # temp
import osOps
import settingsData
# import recentFiles  # for sorting by most used
# import sequence
import verbose


class AppLauncher(QtWidgets.QDialog):
	""" App launcher UI panel main class.
	"""
	def __init__(self, parent, frame):
		super(AppLauncher, self).__init__(parent)

		self.frame = frame
		self.parent = parent

		self.ap = appPaths.appPaths()
		self.jd = settingsData.settingsData()

		# Set OS identifier strings to get correct app executable paths
		if os.environ['IC_RUNNING_OS'] == 'Windows':
			self.currentOS = 'win'
		elif os.environ['IC_RUNNING_OS'] == 'Darwin':
			self.currentOS = 'osx'
		elif os.environ['IC_RUNNING_OS'] == 'Linux':
			self.currentOS = 'linux'

		# self.setupIconGrid()


	def setupIconGrid(self, job=None, sortBy=None):
		""" Dynamically generate grid of tool button icons.
		"""
		verbose.print_("Populating app launcher icons...", 4)

		ap_load = self.ap.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'appPaths.xml'))
		if job is not None:
			jd_load = self.jd.loadXML(os.path.join(os.environ['JOBDATA'], 'jobData.xml'))
			# self.jd.getApps()  # redundant?

		parentLayout = self.frame.findChildren(QtWidgets.QVBoxLayout, 'launchApp_verticalLayout')[0]

		# Delete any existing layouts
		for layout in parentLayout.findChildren(QtWidgets.QGridLayout):
			if "apps_gridLayout" in layout.objectName():
				for i in reversed(range(layout.count())): 
					layout.itemAt(i).widget().deleteLater()
				layout.deleteLater()

		item_index = 0
		if job:
			all_apps = self.ap.getVisibleApps(sortBy=sortBy)
			app_ls = []
			for app in all_apps:
				# if self.jd.getAppVersion(app.get('id')):  # app.get('name') for backwards-compatibility
				if self.jd.getAppVersion(app.get('name')):  # app.get('name') for backwards-compatibility
					app_ls.append(app)
			self.showToolTips = True
		else:
			app_ls = self.ap.getVisibleApps(sortBy=sortBy)
			self.showToolTips = False

		num_items = len(app_ls)
		rows = self.getRows(num_items)
		for row, num_row_items in enumerate(rows):
			# Create grid layout
			icon_size = self.getIconSize(num_row_items)
			row_gridLayout = QtWidgets.QGridLayout()
			row_gridLayout.setObjectName("apps_gridLayout%d" %row)
			parentLayout.insertLayout(row, row_gridLayout)
			for col in range(num_row_items):
				self.createIcon(app_ls[item_index], icon_size, row_gridLayout, col)
				item_index += 1


	def createIcon(self, app, iconSize, layout, column):
		""" Create tool button icon.
		"""
		appName = app.get('id')
		displayName = app.get('name')
		appVersion = self.jd.getAppVersion(displayName)
		appExecutable = self.ap.getPath(displayName, appVersion, self.currentOS)
		tooltip = ""
		if self.showToolTips:
			tooltip = "Launch %s %s" %(displayName, appVersion)
		# print(layout.objectName(), column, appName)

		toolButton = QtWidgets.QToolButton(self.frame)

		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(toolButton.sizePolicy().hasHeightForWidth())
		toolButton.setSizePolicy(sizePolicy)
		icon = QtGui.QIcon()
		# icon.addPixmap(QtGui.QPixmap(":/rsc/rsc/app_icon_%s.png" %appName), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		# icon.addPixmap(QtGui.QPixmap(":/rsc/rsc/app_icon_%s_disabled.png" %appName), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
		iconNormalPath = osOps.absolutePath("$IC_FORMSDIR/rsc/app_icon_%s.png" %appName)
		iconDisabledPath = osOps.absolutePath("$IC_FORMSDIR/rsc/app_icon_%s_disabled.png" %appName)
		if os.path.isfile(iconNormalPath):
			icon.addPixmap(QtGui.QPixmap(iconNormalPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			icon.addPixmap(QtGui.QPixmap(iconDisabledPath), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
			# icon.addPixmap(QtGui.QPixmap(iconDisabledPath), QtGui.QIcon.Active, QtGui.QIcon.Off)
		else:  # Use generic icon
			icon.addPixmap(QtGui.QPixmap(":/rsc/rsc/icon_editor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			icon.addPixmap(QtGui.QPixmap(":/rsc/rsc/icon_editor_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
			# icon.addPixmap(QtGui.QPixmap(":/rsc/rsc/icon_editor_disabled.png"), QtGui.QIcon.Active, QtGui.QIcon.Off)
		toolButton.setIcon(icon)
		toolButton.setIconSize(QtCore.QSize(iconSize[0], iconSize[1]))  # Vary according to number of items in row - QSize won't accept tuple
		toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
		toolButton.setText(displayName)
		toolButton.setObjectName("%s_toolButton" %appName)
		toolButton.setProperty('displayName', displayName)
		toolButton.setProperty('version', appVersion)
		toolButton.setProperty('executable', appExecutable)

		if not os.path.isfile(appExecutable):
			toolButton.setEnabled(False)
			if self.showToolTips:
				tooltip = "%s %s executable not found" %(displayName, appVersion)

		toolButton.setToolTip(tooltip)
		toolButton.setStatusTip(tooltip)

		# Connect signals & slots
		toolButton.clicked.connect(self.launchApp)

		# Add context menus
		submenus = self.ap.getSubMenus(appName)
		if submenus:
			# self.createSubmenus(submenus, toolButton)
			toolButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
			for entry in submenus:
				menuName = entry[0]
				flags = entry[1]
				actionName = "action%s" %menuName.replace(" ", "")
				# print(actionName, entry)

				action = QtWidgets.QAction(menuName, None)
				action.setIcon(icon)
				action.setObjectName(actionName)
				action.setProperty('displayName', displayName)
				action.setProperty('version', appVersion)
				action.setProperty('executable', appExecutable)
				action.setProperty('flags', flags)
				action.setToolTip(tooltip)    # Does nothing?
				action.setStatusTip(tooltip)  # Does nothing?
				action.triggered.connect(self.launchApp)
				toolButton.addAction(action)

				# Make a class-scope reference to this object
				exec_str = "self.%s = action" %actionName
				exec(exec_str)

		layout.addWidget(toolButton, 0, column, 1, 1)  # CHECK THIS!
		# layout.addWidget(toolButton)

		# Set environment variables


	def getRows(self, num_items):
		""" Calculate icon grid arrangement.
			Returns an integer list with each item representing the number of
			icons in each row.
			N.B. Weird syntax here is to maintain compatibility due to the
			different ways Python 2.x and 3.x handle division between integers
			and floats.
		"""
		# Specify some thresholds at which we cascade on to another row. In
		# this instance it's hardcoded that we increase the number of rows
		# after 4, 10, and thereafter every additional 5 items. There will
		# never be more than 5 items in a row.
		if num_items <= 4:
			num_rows = 1
		elif num_items <= 10:
			num_rows = 2
		else:
			num_rows = int(math.ceil(num_items/5.0))

		max_items_per_row = int(math.ceil(num_items/(num_rows*1.0)))

		# Create list of rows each holding an integer value representing the
		# number of items in each row.
		rows = []
		for i in range(num_rows):
			rows.append(max_items_per_row)

		# Progressively reduce items per row until we have the correct total
		# number of items.
		i = 0
		while sum(rows) > num_items:
			rows[i] -= 1
			i += 1

		# Sort the rows so that the rows with the fewest items appear first,
		# then return the list.
		rows.sort()
		return rows


	def getIconSize(self, num_items):
		""" Return icon size in pixels as a tuple, based on the number of
			icons in the row.
		"""
		if num_items == 5:
			icon_size = 40, 40
		elif num_items == 4:
			icon_size = 48, 48
		elif num_items == 3:
			icon_size = 56, 56
		elif num_items == 2:
			icon_size = 64, 64
		elif num_items == 1:
			icon_size = 80, 80
		else:
			icon_size = 48, 48

		return icon_size


	# @QtCore.Slot()
	def launchApp(self):
		""" Launches an application.
		"""
		app = self.sender().property('displayName')
		version = self.sender().property('version')
		executable = self.sender().property('executable')
		flags = self.sender().property('flags')
		# print(self.sender().objectName(), app, version, executable, flags)

		# Set environment variables - NOT HERE
		# job__env__.setEnv(app)

		# Create the folder structure
		defaultDirs.create(app)

		# Run the executable
		launchApps.launch(app, executable, flags)

		# Minimise the UI if the option is set
		if self.parent.boolMinimiseOnAppLaunch:
			self.parent.showMinimized()

