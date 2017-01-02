#!/usr/bin/python

# [Icarus] icarus__main__.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# Launches and controls the Icarus main UI.


from PySide import QtCore, QtGui
from PySide.QtGui import QStyleFactory
from icarusUI import *
import os, sys, env__init__

# Initialise Icarus environment and add libs to sys path
env__init__.setEnv()

# Import custom modules - note: publish modules are imported on demand rather than all at once at beginning of file
import jobs, launchApps, openDirs, osOps, pblChk, pblOptsPrc, setJob, userPrefs, verbose
import sequence as seq


class icarusApp(QtGui.QDialog):

	def __init__(self, parent = None):
		super(icarusApp, self).__init__(parent)
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		# Set up keyboard shortcuts
		self.shortcutShotInfo = QtGui.QShortcut(self)
		self.shortcutShotInfo.setKey('Ctrl+I')
		self.shortcutShotInfo.activated.connect(self.printShotInfo)


		###########################
		# Connect signals & slots #
		###########################

		self.ui.tabWidget.currentChanged.connect(self.adjustMainUI)

		# Set shot UI
		self.ui.refreshJobs_toolButton.clicked.connect(self.populateJobs)
		self.ui.job_comboBox.currentIndexChanged.connect(self.populateShots)
		self.ui.setShot_pushButton.clicked.connect(self.setupJob)
		self.ui.setNewShot_pushButton.clicked.connect(self.unlockJobUI)

		# App launch buttons - should be dynamic?
		self.ui.maya_pushButton.clicked.connect(self.launchMaya)
		self.ui.mudbox_pushButton.clicked.connect(self.launchMudbox)
		self.ui.nuke_pushButton.clicked.connect(self.launchNuke)
		self.ui.mari_pushButton.clicked.connect(self.launchMari)
		self.ui.realflow_pushButton.clicked.connect(self.launchRealFlow)
		self.ui.openProdBoard_pushButton.clicked.connect(launchApps.prodBoard)
		self.ui.openReview_pushButton.clicked.connect(self.launchHieroPlayer)
		self.ui.openTerminal_pushButton.clicked.connect(self.launchTerminal)
		self.ui.browse_pushButton.clicked.connect(openDirs.openShot)
		self.ui.render_pushButton.clicked.connect(self.launchRenderQueue) # was self.launchRenderSubmit

		# Publishing UI
	#	self.ui.renderPblAdd_pushButton.clicked.connect(self.renderTableAdd)
	#	self.ui.renderPblRemove_pushButton.clicked.connect(self.renderTableRm)
		self.ui.renderPblSetMain_pushButton.clicked.connect(self.setLayerAsMain) # remove when render publishing works properly
		self.ui.renderPblAdd_pushButton.clicked.connect(self.renderTableAdd)
		self.ui.renderPblRemove_pushButton.clicked.connect(self.renderTableRemove)
		#self.ui.renderPblRevert_pushButton.clicked.connect(self.renderTableClear)
		self.ui.renderPbl_treeWidget.currentItemChanged.connect(self.updateRenderPublishUI)
		self.ui.renderPbl_treeWidget.itemDoubleClicked.connect(self.renderPreview)
		# self.ui.dailyPbl_treeWidget.itemDoubleClicked.connect(self.renderPreview) # remove when preview is working correctly
		self.ui.dailyPblType_comboBox.currentIndexChanged.connect(self.setDailyType)
		self.ui.dailyPblAdd_pushButton.clicked.connect(self.dailyTableAdd)
		self.ui.publish_pushButton.clicked.connect(self.initPublish)

		# Header toolbar
		self.ui.about_toolButton.clicked.connect(self.about)
		#self.ui.toolMenu_toolButton.clicked.connect(self.launchBatchRename)

		# Options
		self.ui.minimise_checkBox.stateChanged.connect(self.setMinimiseOnAppLaunch)

		# Set minimise on launch checkbox from user prefs
		self.boolMinimiseOnAppLaunch = userPrefs.config.getboolean('main', 'minimiseonlaunch')
		self.ui.minimise_checkBox.setChecked(self.boolMinimiseOnAppLaunch)


		####################################
		# Add right-click menus to buttons #
		####################################

		# Nuke
		self.ui.nuke_pushButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

		self.actionNuke = QtGui.QAction("Nuke", None)
		self.actionNuke.triggered.connect(self.launchNuke)
		self.ui.nuke_pushButton.addAction(self.actionNuke)

		self.actionNukeX = QtGui.QAction("NukeX", None)
		self.actionNukeX.triggered.connect(self.launchNukeX)
		self.ui.nuke_pushButton.addAction(self.actionNukeX)

		# [removed NukeStudio Launcher until properly supported in Icarus]
	#	self.actionNukeStudio = QtGui.QAction("NukeStudio", None)
	#	self.actionNukeStudio.triggered.connect(self.launchNukeStudio)
	#	self.ui.nuke_pushButton.addAction(self.actionNukeStudio)

		# Review
		self.ui.openReview_pushButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

		self.actionHieroPlayer = QtGui.QAction("HieroPlayer", None)
		self.actionHieroPlayer.triggered.connect(self.launchHieroPlayer)
		self.ui.openReview_pushButton.addAction(self.actionHieroPlayer)

		self.actionDjv = QtGui.QAction("djv_view", None)
		self.actionDjv.triggered.connect(self.launchDjv)
		self.ui.openReview_pushButton.addAction(self.actionDjv)

		# Browse
		self.ui.browse_pushButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

		self.actionOpenShot = QtGui.QAction("Shot", None)
		self.actionOpenShot.triggered.connect(openDirs.openShot)
		self.ui.browse_pushButton.addAction(self.actionOpenShot)

		self.actionOpenJob = QtGui.QAction("Job", None)
		self.actionOpenJob.triggered.connect(openDirs.openJob)
		self.ui.browse_pushButton.addAction(self.actionOpenJob)

		# Render
		self.ui.render_pushButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

		self.actionRenderQueue = QtGui.QAction("Render Queue", None)
		self.actionRenderQueue.triggered.connect(self.launchRenderQueue)
		self.ui.render_pushButton.addAction(self.actionRenderQueue)

		self.actionRenderSubmit = QtGui.QAction("Submit Render", None)
		self.actionRenderSubmit.triggered.connect(self.launchRenderSubmit)
		self.ui.render_pushButton.addAction(self.actionRenderSubmit)

		self.actionBrowseRenders = QtGui.QAction("Browse Renders", None)
		self.actionBrowseRenders.triggered.connect(self.launchRenderBrowser)
		self.ui.render_pushButton.addAction(self.actionBrowseRenders)

		self.actionDeadlineMonitor = QtGui.QAction("Deadline Monitor", None)
		self.actionDeadlineMonitor.triggered.connect(self.launchDeadlineMonitor)
		self.ui.render_pushButton.addAction(self.actionDeadlineMonitor)

		self.actionDeadlineSlave = QtGui.QAction("Deadline Slave", None)
		self.actionDeadlineSlave.triggered.connect(self.launchDeadlineSlave)
		self.ui.render_pushButton.addAction(self.actionDeadlineSlave)

		# Tools menu
		self.ui.toolMenu_toolButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

		self.actionJobManagement = QtGui.QAction("Job Management...", None)
		self.actionJobManagement.triggered.connect(self.launchJobManagement)
		self.ui.toolMenu_toolButton.addAction(self.actionJobManagement)

		self.actionShotCreator = QtGui.QAction("Shot Creator...", None)
		self.actionShotCreator.triggered.connect(self.launchShotCreator)
		self.ui.toolMenu_toolButton.addAction(self.actionShotCreator)

		self.actionBatchRename = QtGui.QAction("Batch Rename", None)
		self.actionBatchRename.triggered.connect(self.launchBatchRename)
		self.ui.toolMenu_toolButton.addAction(self.actionBatchRename)

		# self.actionRenderQueue = QtGui.QAction("Render Queue...", None)
		# self.actionRenderQueue.triggered.connect(self.launchRenderQueue)
		self.ui.toolMenu_toolButton.addAction(self.actionRenderQueue)

		# self.separator = QtGui.QAction(None)
		# self.separator.setSeparator(True)
		# self.ui.toolMenu_toolButton.addAction(self.separator)

		# self.actionIcarusSettings = QtGui.QAction("Global Settings...", None)
		# self.actionIcarusSettings.triggered.connect(self.globalSettings)
		# self.ui.toolMenu_toolButton.addAction(self.actionIcarusSettings)

		# self.actionUserSettings = QtGui.QAction("User Settings...", None)
		# self.actionUserSettings.triggered.connect(self.userSettings)
		# self.ui.toolMenu_toolButton.addAction(self.actionUserSettings)


		# Add status bar
		statusBar = QtGui.QStatusBar(self)
		self.ui.statusBar_horizontalLayout.addWidget(statusBar)
		#statusBar.showMessage("Test message")
		#self.ui.nuke_pushButton.setStatusTip("Test status tip") # status tips not working with this status bar for some reason?
		verbose.registerStatusBar(statusBar) # register the status bar with the verbose module


		######################################
		# Adapt UI for environment awareness #
		######################################

		self.jobMngTab = self.ui.tabWidget.widget(0)
		self.publishTab = self.ui.tabWidget.widget(1)
		self.gatherTab = self.ui.tabWidget.widget(2)
		self.publishAssetTab = self.ui.publishType_tabWidget.widget(0)
		self.publishRenderTab = self.ui.publishType_tabWidget.widget(1)


		##########################
		# Standalone environment #
		##########################

		if os.environ['ICARUSENVAWARE'] == 'STANDALONE':

			# Hide UI items relating to app environment(s)
			uiHideLs = ['setNewShot_pushButton', 'shotEnv_toolButton', 'appIcon_label']
			for uiItem in uiHideLs:
				hideProc = 'self.ui.%s.hide()' % uiItem
				eval(hideProc)

			# Populate 'Job' and 'Shot' drop down menus
			self.populateJobs()

			# Delete all tabs except 'Job Management'
			for i in range(0, self.ui.tabWidget.count()-1):
				self.ui.tabWidget.removeTab(1)

			# Delete 'ma_asset', 'nk_asset', 'Publish' tabs - REMEMBER TO UNCOMMENT THE FOLLOWING TWO LINES
			for i in range(0, 2):
				self.ui.publishType_tabWidget.removeTab(0)

			# Apply job/shot settings pop-up menu to shotEnv label (only in standalone mode)
			self.ui.shotEnv_toolButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

			self.actionJobSettings = QtGui.QAction("Job Settings...", None)
			self.actionJobSettings.triggered.connect(self.jobSettings)
			self.ui.shotEnv_toolButton.addAction(self.actionJobSettings)

			self.actionShotSettings = QtGui.QAction("Shot Settings...", None)
			self.actionShotSettings.triggered.connect(self.shotSettings)
			self.ui.shotEnv_toolButton.addAction(self.actionShotSettings)

			self.ui.shotEnv_toolButton.setEnabled(True)


		####################
		# Maya environment #
		####################

		elif os.environ['ICARUSENVAWARE'] == 'MAYA':
			pixmap = QtGui.QPixmap(":/rsc/rsc/app_icon_maya_disabled.png")
			self.ui.appIcon_label.setPixmap(pixmap)

			# Hide certain UI items
			uiHideLs = ['assetSubType_listWidget', 'toolMenu_toolButton'] # Removed 'icarusBanner', 'ma_assetTypes_frame'
			for uiItem in uiHideLs:
				hideProc = 'self.ui.%s.hide()' % uiItem
				eval(hideProc)

			self.ui.publishType_tabWidget.removeTab(1) # Remove 'nk Asset' tab
			#update shot label in maya env
			self.connectNewSignalsSlots()
			self.populatePblShotLs()
			self.populateGatherShotLs()
			self.updateJobLabel()
			self.ui.tabWidget.removeTab(0)

			# Attempt to set the publish asset type button to remember the last selection - 'self.connectNewSignalsSlots()' must be called already
			try:
				for toolButton in self.ui.ma_assetType_frame.children():
					if isinstance(toolButton, QtGui.QToolButton):
						if toolButton.text() == userPrefs.config.get('main', 'lastpublishma'):
							toolButton.setChecked(True)
			except:
				pass


		####################
		# Nuke environment #
		####################

		elif os.environ['ICARUSENVAWARE'] == 'NUKE':
			pixmap = QtGui.QPixmap(":/rsc/rsc/app_icon_nuke_disabled.png")
			self.ui.appIcon_label.setPixmap(pixmap)

			# Hide certain UI items
			uiHideLs = ['assetSubType_listWidget', 'toolMenu_toolButton'] # Removed 'icarusBanner', 'nk_assetTypes_frame'
			for uiItem in uiHideLs:
				hideProc = 'self.ui.%s.hide()' % uiItem
				eval(hideProc)

			#update shot label in maya env
			self.connectNewSignalsSlots()
			self.populatePblShotLs()
			self.populateGatherShotLs()
			self.updateJobLabel()
			self.ui.tabWidget.removeTab(0)
			#deletes Asset publish tabs
			self.ui.publishType_tabWidget.removeTab(0) # Remove 'ma Asset' tab

			# Attempt to set the publish asset type button to remember the last selection - 'self.connectNewSignalsSlots()' must be called already
			try:
				for toolButton in self.ui.nk_assetType_frame.children():
					if isinstance(toolButton, QtGui.QToolButton):
						if toolButton.text() == userPrefs.config.get('main', 'lastpublishnk'):
							toolButton.setChecked(True)
			except:
				pass

	# end of function __init__


	#########################
	# Generic UI procedures #
	#########################

	def connectNewSignalsSlots(self):
		""" Connects new signals and slots after job and shot env is set.
		"""
		self.ui.publishType_tabWidget.currentChanged.connect(self.adjustPblTypeUI)

		for toolButton in self.ui.ma_assetType_frame.children():
			if isinstance(toolButton, QtGui.QToolButton):
				toolButton.toggled.connect(self.adjustPublishOptsMayaUI)
		for toolButton in self.ui.nk_assetType_frame.children():
			if isinstance(toolButton, QtGui.QToolButton):
				toolButton.toggled.connect(self.adjustPublishOptsNukeUI)

		# self.ui.animation_toolButton.clicked.connect(self.setDropDownToShotEnv)
		# self.ui.shot_toolButton.clicked.connect(self.setDropDownToShotEnv)
		# self.ui.comp_toolButton.clicked.connect(self.setDropDownToShotEnv) #self.adjustPblTypeUI

		self.ui.gatherFromShot_radioButton.clicked.connect(self.adjustMainUI)
		self.ui.gatherFromShot_comboBox.currentIndexChanged.connect(self.adjustMainUI)
		self.ui.gatherFromJob_radioButton.clicked.connect(self.adjustMainUI)
		self.ui.gather_pushButton.clicked.connect(self.initGather)

		self.ui.assetType_listWidget.itemClicked.connect(self.updateAssetNameCol) # currentItemChanged?
		self.ui.assetName_listWidget.itemClicked.connect(self.adjustColumns)
		self.ui.assetSubType_listWidget.itemClicked.connect(self.updateAssetVersionCol)
		self.ui.assetVersion_listWidget.itemClicked.connect(self.updateInfoField)
		self.ui.assetVersion_listWidget.itemClicked.connect(self.updateImgPreview)


	def getMainTab(self):
		""" Gets the current main tab.
		"""
		tabIndex = self.ui.tabWidget.currentIndex()
		tabText = self.ui.tabWidget.tabText(tabIndex)
		return tabIndex, tabText


	def getPblTab(self):
		""" Gets the current publish type tab.
		"""
		tabIndex = self.ui.publishType_tabWidget.currentIndex()
		tabText = self.ui.publishType_tabWidget.tabText(tabIndex)
		return tabIndex, tabText


	def adjustMainUI(self):
		""" Makes UI adjustments and connections based on which tab is currently selected.
		"""
		mainTabName = self.getMainTab()[1]
		if mainTabName == 'Gather' or mainTabName == 'Assets':
			self.defineColumns()
			self.updateAssetTypeCol()


	def adjustPublishOptsMayaUI(self):
		""" Makes UI adjustments based on which asset publish type is currently selected.
		"""
		assetType = self.sender().text()

		self.ui.ma_publishOptions_groupBox.setTitle("Publish options: %s" %assetType)

		self.ui.assetSubType_comboBox.clear()
		self.ui.textures_checkBox.setEnabled(True)
		self.ui.assetName_label.setEnabled(False)
		self.ui.assetName_lineEdit.setEnabled(False)

		if assetType == 'model':
			self.ui.assetSubType_comboBox.addItem('base')
			self.ui.assetSubType_comboBox.addItem('anim')
		elif assetType == 'rig':
			self.ui.assetSubType_comboBox.addItem('anim')
			self.ui.assetSubType_comboBox.addItem('light')
			self.ui.assetSubType_comboBox.addItem('fx')
		elif assetType == 'camera':
			self.ui.assetSubType_comboBox.addItem('render')
			self.ui.assetSubType_comboBox.addItem('mm')
			self.ui.assetSubType_comboBox.addItem('previs')
			self.ui.textures_checkBox.setEnabled(False)
			# self.lockPublishTo(lock=True)
		elif assetType == 'geo':
			self.ui.assetSubType_comboBox.addItem('abc')
			self.ui.assetSubType_comboBox.addItem('obj')
			self.ui.assetSubType_comboBox.addItem('fbx')
		elif assetType == 'geoCache':
			self.ui.assetSubType_comboBox.addItem('anim')
			self.ui.assetSubType_comboBox.addItem('cloth')
			self.ui.assetSubType_comboBox.addItem('rigidBody')
			self.ui.assetSubType_comboBox.addItem('vrmesh')
			self.ui.assetSubType_comboBox.addItem('realflow')
			self.ui.textures_checkBox.setEnabled(False)
		elif assetType == 'animation':
			self.ui.textures_checkBox.setEnabled(False)
		elif assetType == 'scene':
			self.ui.assetName_label.setEnabled(True)
			self.ui.assetName_lineEdit.setEnabled(True)
		elif assetType == 'node':
			self.ui.assetSubType_comboBox.addItem('ma')
			self.ui.assetSubType_comboBox.addItem('ic')
		# elif assetType == 'shot':
		# 	self.lockPublishTo(lock=True)

		if self.ui.assetSubType_comboBox.count():
			self.ui.assetSubType_label.setEnabled(True)
			self.ui.assetSubType_comboBox.setEnabled(True)
			self.ui.subSet_checkBox.setEnabled(False)
			self.ui.subSet_checkBox.setChecked(False)
		else:
			self.ui.assetSubType_label.setEnabled(False)
			self.ui.assetSubType_comboBox.setEnabled(False)
			self.ui.subSet_checkBox.setEnabled(True)

		# Remember last selection with entry in user prefs
		userPrefs.edit('main', 'lastpublishma', assetType)


	def adjustPublishOptsNukeUI(self):
		""" Makes UI adjustments based on which asset publish type is currently selected.
		"""
		assetType = self.sender().text()

		self.ui.nk_publishOptions_groupBox.setTitle("Publish options: %s" %assetType)

		self.ui.nk_PblName_label.setEnabled(True)
		self.ui.nk_PblName_lineEdit.setEnabled(True)

		if assetType == 'comp':
			self.ui.nk_PblName_label.setEnabled(False)
			self.ui.nk_PblName_lineEdit.setEnabled(False)
			# self.lockPublishTo(lock=True)

		# Remember last selection with entry in user prefs
		userPrefs.edit('main', 'lastpublishnk', assetType)


	def adjustPblTypeUI(self):
		""" Makes UI lock adjustments based on which publish type tab is currently selected.
		"""
		tabIndex = self.ui.publishType_tabWidget.currentIndex()
		tabText = self.ui.publishType_tabWidget.tabText(tabIndex)

		if tabText == 'ma Asset':
			self.lockPublishTo(lock=False)

		elif tabText == 'nk Asset':
			self.lockPublishTo(lock=False)
			# if self.ui.comp_toolButton.isChecked() == True:
			# 	self.lockPublishTo(lock=True)
			# 	#self.setDropDownToShotEnv()
			# else:
			# 	self.lockPublishTo(lock=False)

		elif tabText == 'Dailies':
			self.lockPublishTo(lock=True)
			#self.setDropDownToShotEnv()

		elif tabText == 'Render':
			self.lockPublishTo(lock=True)
			#self.setDropDownToShotEnv()


	def lockPublishTo(self, lock=False):
		""" Locks 'Publish To' section of UI based on selection.
		"""
		if lock:
			self.ui.publishToJob_radioButton.setEnabled(False)
			self.ui.publishToShot_radioButton.setChecked(True)
			self.ui.publishToShot_comboBox.setEnabled(False)
			self.setDropDownToShotEnv()
		else:
			self.ui.publishToJob_radioButton.setEnabled(True)
			if self.ui.publishToShot_radioButton.isChecked() == 1:
				self.ui.publishToShot_comboBox.setEnabled(True)
			#self.ui.model_toolButton.setChecked(True)


	def setDropDownToShotEnv(self):
		""" Switches the shot drop down menu to the current environment shot.
			Disables publishing to alternative shot.
		"""
		self.ui.publishToShot_comboBox.setCurrentIndex(self.ui.publishToShot_comboBox.findText(os.environ['SHOT']))


	def fileDialog(self, dialogHome):
		""" Opens a dialog from which to select a single file.
			The env check puts the main window in the background so dialog pop up can return properly when running inside certain applications.
			The window flags bypass a mac bug that made the dialog always appear under the Icarus window. This is ignored in a Linux env.
		"""
		envOverride = ['MAYA', 'NUKE']
		if os.environ['ICARUSENVAWARE'] in envOverride:
			if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
				app.setWindowFlags(QtCore.Qt.WindowStaysOnBottomHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowCloseButtonHint)
				app.show()
			dialog = QtGui.QFileDialog.getOpenFileName(app, self.tr('Files'), dialogHome, 'All files (*.*)')
			if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
				app.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowCloseButtonHint)
				app.show()
		else:
			dialog = QtGui.QFileDialog.getOpenFileName(app, self.tr('Files'), dialogHome, 'All files (*.*)')

		return dialog[0]


	def folderDialog(self, dialogHome):
		""" Opens a dialog from which to select a folder.
			The env check puts the main window in the background so dialog pop up can return properly when running inside certain applications.
			The window flags bypass a mac bug that made the dialog always appear under the Icarus window. This is ignored in a Linux env.
		"""
		envOverride = ['MAYA', 'NUKE']
		if os.environ['ICARUSENVAWARE'] in envOverride:
			if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
				app.setWindowFlags(QtCore.Qt.WindowStaysOnBottomHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowCloseButtonHint)
				app.show()
			dialog = QtGui.QFileDialog.getExistingDirectory(self, self.tr('Directory'), dialogHome, QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly)
			if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
				app.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowCloseButtonHint)
				app.show()
		else:
			dialog = QtGui.QFileDialog.getExistingDirectory(self, self.tr('Directory'), dialogHome, QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly)

		return dialog


	######################
	# Job management tab #
	######################

	def populateJobs(self):
		""" Populates job drop down menu.
		"""
		# Block signals to prevent call to populateShots() each time a new item is added
		self.ui.job_comboBox.blockSignals(True)

		# Remove all items
		self.ui.job_comboBox.clear()

		# Populate 'Job' and 'Shot' drop down menus
		j = jobs.jobs()

		jobLs = j.getActiveJobs()
		if jobLs:
			jobLs = sorted(jobLs, reverse=True)

			# Add jobs...
			for job in jobLs:
				self.ui.job_comboBox.insertItem(0, job)

			# Attempt to set the combo box selections to remember the last shot
			lastJob = None
			try:
				lastJob, lastShot = userPrefs.config.get('main', 'lastjob').split(',')
				#print lastJob, lastShot
				if lastJob in jobLs:
					shotLs = setJob.listShots(lastJob)
					if shotLs:
						if lastShot in shotLs:
							self.ui.job_comboBox.setCurrentIndex(self.ui.job_comboBox.findText(lastJob))
							self.ui.shot_comboBox.setCurrentIndex(self.ui.shot_comboBox.findText(lastShot))

			# Set the combo box to the first item
			except:
				self.ui.job_comboBox.setCurrentIndex(0)

			self.ui.shotSetup_groupBox.setEnabled(True)
			self.ui.shotSetupButtons_groupBox.setEnabled(True)
			self.populateShots()
			self.ui.job_comboBox.blockSignals(False)

		# If no jobs found, disable all job management UI controls
		else:
			#verbose.noJobs()
			msg = "No active jobs found"
			verbose.warning(msg)
			self.ui.job_comboBox.insertItem(0, '[%s]' %msg)
			self.ui.shot_comboBox.clear()
			self.ui.shot_comboBox.insertItem(0, '[None]')
			self.ui.shotSetup_groupBox.setEnabled(False)
			self.ui.shotSetupButtons_groupBox.setEnabled(False)

			# Confirmation dialog
			import pDialog
			dialogTitle = 'No Jobs Found'
			dialogMsg = 'No active jobs were found. Would you like to set up some jobs now?'
			dialog = pDialog.dialog()
			if dialog.dialogWindow(dialogMsg, dialogTitle):
				self.launchJobManagement()
			else:
				pass


	def populateShots(self):
		""" Populates shot drop down menu.
		"""
		# Remove all items
		self.ui.shot_comboBox.clear()

		selJob = self.ui.job_comboBox.currentText()
		shotLs = setJob.listShots(selJob)

		# Add shots...
		if shotLs:
			for shot in shotLs:
				self.ui.shot_comboBox.insertItem(0, shot)

			# Try to set current item in combo box to the current shot 
			try:
				index = self.ui.shot_comboBox.findText(self.shot)
			except AttributeError:
				index = 0

			if 0 <= index < len(shotLs):
				self.ui.shot_comboBox.setCurrentIndex(index)
			else:
				self.ui.shot_comboBox.setCurrentIndex(0)

			self.ui.shot_comboBox.setEnabled(True)
			self.ui.setShot_label.setEnabled(True)
			self.ui.setShot_pushButton.setEnabled(True)

			return True

		# No shots detected...
		else:
			self.ui.shot_comboBox.insertItem(0, '[None]')
			self.ui.shot_comboBox.setEnabled(False)
			self.ui.setShot_label.setEnabled(False)
			self.ui.setShot_pushButton.setEnabled(False)

			# Confirmation dialog
			import pDialog
			dialogTitle = 'No Shots Found'
			dialogMsg = 'No shots were found for this job. Would you like to create some shots now?'
			dialog = pDialog.dialog()
			if dialog.dialogWindow(dialogMsg, dialogTitle):
				self.launchShotCreator()
			else:
				pass

			return False


	#populates publish shot drop down menu
	def populatePblShotLs(self):
		self.ui.publishToShot_comboBox.clear()
		shotLs = setJob.listShots(os.environ['JOB'])
		if shotLs:
			for shot in shotLs:
				self.ui.publishToShot_comboBox.insertItem(0, shot)
			self.ui.publishToShot_comboBox.setCurrentIndex(self.ui.publishToShot_comboBox.findText(os.environ['SHOT']))

	#populates gather shot drop down menu
	def populateGatherShotLs(self):
		self.ui.gatherFromShot_comboBox.clear()
		shotLs = setJob.listShots(os.environ['JOB'])
		if shotLs:
			for shot in shotLs:
				self.ui.gatherFromShot_comboBox.insertItem(0, shot)
			self.ui.gatherFromShot_comboBox.setCurrentIndex(self.ui.gatherFromShot_comboBox.findText(os.environ['SHOT']))

	#updates job tab ui with shot selection
	def updateJobUI(self):
		self.ui.setShot_pushButton.setEnabled(True)


	def setupJob(self):
		""" Sets up shot environment, creates user directories and updates user job log.
		"""
		self.job = self.ui.job_comboBox.currentText()
		self.shot = self.ui.shot_comboBox.currentText()
		if setJob.setup(self.job, self.shot):
			self.adjustPblTypeUI()
			self.populatePblShotLs()
			self.populateGatherShotLs()
			self.connectNewSignalsSlots()
			self.lockJobUI()
		else:
			dialogMsg = 'Unable to load job settings. Default values have been applied.\nPlease review the values in the job settings dialog and click Save when done.\n'
			verbose.print_(dialogMsg, 1)

			# Confirmation dialog
			import pDialog
			dialogTitle = 'Job settings not found'
			dialog = pDialog.dialog()
			dialog.dialogWindow(dialogMsg, dialogTitle, conf=True)

			if self.openSettings("Job", autoFill=True):
				self.setupJob()


	def lockJobUI(self):
		""" Updates and locks UI job tab.
		"""
		self.updateJobLabel()
		self.ui.shotSetup_groupBox.setEnabled(False)
		self.ui.refreshJobs_toolButton.setEnabled(False)
		self.ui.launchApp_groupBox.setEnabled(True)
		self.ui.launchOptions_groupBox.setEnabled(True)
		self.ui.tabWidget.insertTab(1, self.publishTab, 'Publish')
		self.ui.tabWidget.insertTab(2, self.gatherTab, 'Assets')
		self.ui.gather_pushButton.hide()
		self.ui.setShot_pushButton.hide()
		self.ui.shotEnv_toolButton.show()
		self.ui.setNewShot_pushButton.show()
		self.actionJobManagement.setEnabled(False)
		self.actionShotCreator.setEnabled(False)
		verbose.jobSet(self.job, self.shot)


	def unlockJobUI(self):
		""" Unlocks UI if 'Set New Shot' is clicked.
		"""
		# Re-scan for shots
		#self.populateJobs()
		self.populateShots()

		self.ui.shotSetup_groupBox.setEnabled(True)
		self.ui.refreshJobs_toolButton.setEnabled(True)
		self.ui.launchApp_groupBox.setEnabled(False)
		self.ui.launchOptions_groupBox.setEnabled(False)

		self.ui.tabWidget.removeTab(1); self.ui.tabWidget.removeTab(1) # remove publish and assets tab - check this
		self.ui.renderPbl_treeWidget.clear() # clear the render layer tree view widget
		self.ui.dailyPbl_treeWidget.clear() # clear the dailies tree view widget
		self.ui.shotEnv_toolButton.setText('')
		self.ui.shotEnv_toolButton.hide()
		self.ui.setNewShot_pushButton.hide()
		self.ui.setShot_pushButton.show()

		self.actionJobManagement.setEnabled(True)
		self.actionShotCreator.setEnabled(True)


#	#controls phonon preview player
#	def previewPlayerCtrl(self, show=False, hide=False, play=False, loadImg=None):
#		if self.previewPlayer:
#			if show:
#				self.previewPlayer.show()
#			elif hide:
#				self.previewPlayer.hide()
#			elif play:
#				self.previewPlayer.play()
#			elif loadImg:
#				self.previewPlayer.load(loadImg)


	def updateJobLabel(self):
		""" Updates job label tool button with the current job and shot.
		"""
		if os.environ['ICARUSENVAWARE'] != 'STANDALONE':
			self.job = os.environ['JOB']
			self.shot = os.environ['SHOT']
		self.ui.shotEnv_toolButton.setText('%s - %s' % (self.job, self.shot))


	def setMinimiseOnAppLaunch(self, state):
		""" Sets state of minimise on app launch variable.
			Ultimately, this option should form part of a 'User Prefs' dialog, and be removed from the main UI.
		"""
		if state == QtCore.Qt.Checked:
			self.boolMinimiseOnAppLaunch = True
			userPrefs.edit('main', 'minimiseonlaunch', 'True')
			#print "Minimise on launch enabled"
		else:
			self.boolMinimiseOnAppLaunch = False
			userPrefs.edit('main', 'minimiseonlaunch', 'False')
			#print "Minimise on launch disabled"


	def printShotInfo(self):
		""" Print job / shot information stored in enviroment variables - used for debugging.
		"""
		try:
			print """
     Job/Shot: %s - %s

  Frame range: %s

   Resolution: %s (full)
               %s (proxy)

 Linear units: %s
Angular units: %s
   Time units: %s (%s fps)
""" %(os.environ['JOB'], os.environ['SHOT'],
      os.environ['FRAMERANGE'],
      os.environ['RESOLUTION'],
      os.environ['PROXY_RESOLUTION'],
      os.environ['UNIT'],
      os.environ['ANGLE'],
      os.environ['TIMEFORMAT'], os.environ['FPS'])

			for key in os.environ.keys():
				print "%30s %s \n" % (key, os.environ[key])
		except KeyError:
			print "Environment variable(s) not set."


	def about(self):
		""" Show about dialog.
		"""
		import PySide.QtCore
		python_ver_str = "%d.%d.%d" %(sys.version_info[0], sys.version_info[1], sys.version_info[2])
		pyside_ver_str = PySide.__version__
		qt_ver_str = PySide.QtCore.qVersion()

		about_msg = """
I   C   A   R   U   S

%s

Python %s / PySide %s / Qt %s / %s
Environment: %s

(c) 2013-2016 Gramercy Park Studios
""" %(os.environ['ICARUSVERSION'], python_ver_str, pyside_ver_str, qt_ver_str, os.environ['ICARUS_RUNNING_OS'], os.environ['ICARUSENVAWARE'])

		import about
		about = about.aboutDialog()
		about.msg(about_msg)


	def openSettings(self, settingsType, autoFill=False):
		""" Open settings dialog.
		"""
		if settingsType == "Job":
			categoryLs = ['job', 'time', 'resolution', 'units', 'apps', 'other']
			xmlData = os.path.join(os.environ['JOBDATA'], 'jobData.xml')
		elif settingsType == "Shot":
			categoryLs = ['time', 'resolution', 'units', 'camera']
			xmlData = os.path.join(os.environ['SHOTDATA'], 'shotData.xml')
		elif settingsType == "User":
			categoryLs = ['user', ]
			xmlData = os.path.join(os.environ['ICUSERPREFS'], 'userPrefs.xml')
		elif settingsType == "Global":
			categoryLs = ['global', ]
			xmlData = os.path.join(os.path.join(os.environ['ICCONFIGDIR'], 'globalPrefs.xml'))
		import job_settings__main__ # Change this to generic class when it's ready
		reload(job_settings__main__)
		settingsEditor = job_settings__main__.settingsDialog(settingsType=settingsType, categoryLs=categoryLs, xmlData=xmlData, autoFill=autoFill)
		@settingsEditor.customSignal.connect
		def storeAttr(attr):
			settingsEditor.currentAttr = attr # a bit hacky - need to find a way to add this function to main class
		settingsEditor.show()
		settingsEditor.exec_()
		return settingsEditor.returnValue # return True if user clicked Save, False for Cancel


	def jobSettings(self):
		""" Open job settings dialog wrapper function.
		"""
		if self.openSettings("Job"):
			setJob.setup(self.job, self.shot) # Set up environment variables


	def shotSettings(self):
		""" Open shot settings dialog wrapper function.
		"""
		if self.openSettings("Shot"):
			setJob.setup(self.job, self.shot) # Set up environment variables


	def userSettings(self):
		""" Open user settings dialog wrapper function.
		"""
		if self.openSettings("User"):
			pass


	def globalSettings(self):
		""" Open Icarus global settings dialog wrapper function.
		"""
		if self.openSettings("Global"):
			pass


	def launchMaya(self):
		""" Launches Maya.
		"""
		launchApps.launch('Maya')
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()


	def launchMudbox(self):
		""" Launches Mudbox.
		"""
		launchApps.launch('Mudbox')
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()


	def launchNuke(self):
		""" Launches Nuke.
		"""
		launchApps.launch('Nuke')
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()


	def launchNukeX(self):
		""" Launches NukeX.
		"""
		launchApps.launch('NukeX')
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()


	def launchNukeStudio(self):
		""" Launches Nuke Studio.
		"""
		launchApps.launch('NukeStudio')
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()


	def launchMari(self):
		""" Launches Mari.
		"""
		launchApps.launch('Mari')
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()


	def launchHieroPlayer(self):
		""" Launches Hiero Player.
		"""
		launchApps.launch('HieroPlayer')
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()


	def launchRealFlow(self):
		""" Launches RealFlow.
		"""
		launchApps.launch('RealFlow')
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()


	def launchDeadlineMonitor(self):
		""" Launches Deadline Monitor.
		"""
		launchApps.launch('DeadlineMonitor')
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()


	def launchDeadlineSlave(self):
		""" Launches Deadline Slave.
		"""
		launchApps.launch('DeadlineSlave')
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()


	# Launches djv_view
	def launchDjv(self):
		launchApps.djv()
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()


	#launches terminal locks button
	def launchTerminal(self):
		launchApps.terminal()
	#	self.ui.openTerminal_pushButton.setEnabled(False)
	#	self.ui.setNewShot_pushButton.setEnabled(False)
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()


	# Preview - opens djv_view to preview movie or image sequence
	def preview(self, path=None):
		import djvOps
		verbose.launchApp('djv_view')
		if path is None:
			djvOps.viewer(self.gatherPath) # this is purely a bodge for asset browser - fix at a later date
		else:
			djvOps.viewer(path)


	def launchRenderSubmit(self):
		""" Launches GPS Render Submitter window.
		"""
		import submit__main__
		reload(submit__main__)
		#submit__main__.run_(frameRange='1-10', flags='-rl CurrentLayer')
		try:
			self.renderSubmitApp.show()
			self.renderSubmitApp.raise_()
		except AttributeError:
			self.renderSubmitApp = submit__main__.gpsRenderSubmitApp()
			#print self.renderSubmitApp
			self.renderSubmitApp.show()


	def launchRenderQueue(self):
		""" Launches GPS Render Queue Manager window.
		"""
		import queue__main__
		reload(queue__main__)
		try:
			self.renderQueueApp.show()
			self.renderQueueApp.raise_()
		except AttributeError:
			self.renderQueueApp = queue__main__.gpsRenderQueueApp()
			#print self.renderQueueApp
			self.renderQueueApp.show()


	# def launchRenderSlave(self):
	# 	""" Launches GPS Render Slave window.
	# 	"""
	# 	import slave__main__
	# 	reload(slave__main__)


	def launchRenderBrowser(self):
		""" Launches GPS render browser window.
		"""
		import rb__main__
		reload(rb__main__)


	def launchBatchRename(self):
		""" Launches GPS sequence rename tool.
		"""
		import rename__main__
		reload(rename__main__)


	def launchJobManagement(self):
		""" Launches job management dialog.
		"""
		import job_management__main__
		reload(job_management__main__)
		jobManagementEditor = job_management__main__.jobManagementApp()
#		jobManagementEditor.show()
		jobManagementEditor.exec_()
		if jobManagementEditor.returnValue == True: # return True if user clicked Save, False for Cancel
			self.populateJobs()


	def launchShotCreator(self):
		""" Launches shot creator dialog.
		"""
		import shot_creator__main__
		reload(shot_creator__main__)
		shotCreatorEditor = shot_creator__main__.shotCreatorApp( self.ui.job_comboBox.currentText() )
#		shotCreatorEditor.show()
		shotCreatorEditor.exec_()
		self.populateJobs()



	###############
	# Publish tab #
	###############

	###################adjusting ui####################				


#	#populates the render publish table
#	def renderTableAdd(self):
#		#processes latest path added to self.renderPaths
#		renderPath = self.renderPblBrowse()
#		renderPath = renderPath.replace(os.environ['SHOTPATH'], '$SHOTPATH')
#		renderDic = {}
#		if renderPath:
#			renderDic = pblOptsPrc.renderPath_prc(renderPath)
#		if renderDic:
#			autoMainLayer = None
#			for layer in renderDic.keys():
#				layerPath = renderDic[layer]
#				layerItem = QtGui.QTableWidgetItem(layer)
#				pathItem = QtGui.QTableWidgetItem(layerPath)
#				mainItem = QtGui.QTableWidgetItem()
#				#check if layers already exist
#				layerChk = True
#				rowCount = self.ui.renderPbl_tableWidget.rowCount()
#				for row in range(0, rowCount):
#					if layer == self.ui.renderPbl_tableWidget.item(row, 0).text():
#						layerChk = False
#						break
#				#adding items and locking table
#				if layerChk:
#					newRow = self.ui.renderPbl_tableWidget.insertRow(0)
#					self.ui.renderPbl_tableWidget.setItem(0, 0, layerItem)
#					layerItem.setFlags(~QtCore.Qt.ItemIsEditable)
#					self.ui.renderPbl_tableWidget.setItem(0, 1, pathItem)
#					pathItem.setFlags(~QtCore.Qt.ItemIsEditable)
#					self.ui.renderPbl_tableWidget.setItem(0, 2, mainItem)
#					mainItem.setFlags(~QtCore.Qt.ItemIsEditable)
#					mainItem.setText('layer')
#					self.ui.renderPbl_tableWidget.resizeColumnsToContents()
#					#making layer main if autoDetected
#					if layer == 'main':
#						autoMainLayer = layerItem
#						self.setLayerAsMain(autoMainLayer)
#					elif layer in ('masterLayer', 'master', 'beauty'):
#						if not autoMainLayer:
#							autoMainLayer = layerItem
#							self.setLayerAsMain(autoMainLayer)

#	#removes items from the render table
#	def renderTableRm(self):
#		rmRowLs = []
#		for selIndex in self.ui.renderPbl_tableWidget.selectedIndexes():
#			selItem = self.ui.renderPbl_tableWidget.itemFromIndex(selIndex)
#			selRow = self.ui.renderPbl_tableWidget.row(selItem)
#			if selRow not in rmRowLs:
#				rmRowLs.append(selRow)
#		rmRowLs = sorted(rmRowLs, reverse=True)
#		for rmRow in rmRowLs:
#			self.ui.renderPbl_tableWidget.removeRow(rmRow)


	# #sets the selected render layer as the main layer
	# def setLayerAsMain(self, autoMainLayer=None):
	# 	font = QtGui.QFont()
	# 	for rowItem in range(0, self.ui.renderPbl_tableWidget.rowCount()):
	# 		font.setBold(False)
	# 		mainItem = self.ui.renderPbl_tableWidget.item(rowItem, 2)
	# 		mainItem.setText('layer')
	# 		mainItem.setFont(font)
	# 		#mainItem.setBackground(QtGui.QColor(34,34,34))
	# 		rowItem1 = self.ui.renderPbl_tableWidget.item(rowItem, 1)
	# 		rowItem1.setFont(font)
	# 		#rowItem1.setBackground(QtGui.QColor(34,34,34))
	# 		rowItem0 = self.ui.renderPbl_tableWidget.item(rowItem, 0)
	# 		rowItem0.setFont(font)
	# 		#rowItem0.setBackground(QtGui.QColor(34,34,34))
	# 	rowLs = []
	# 	if autoMainLayer:
	# 		selRow = self.ui.renderPbl_tableWidget.row(autoMainLayer)
	# 		rowLs.append(selRow)
	# 	else:
	# 		for selIndex in self.ui.renderPbl_tableWidget.selectedIndexes():
	# 			selItem = self.ui.renderPbl_tableWidget.itemFromIndex(selIndex)
	# 			selRow = self.ui.renderPbl_tableWidget.row(selItem)
	# 			if selRow not in rowLs and selRow != -1:
	# 				rowLs.append(selRow)
	# 	if len(rowLs) == 1:
	# 		font.setBold(True)
	# 		mainItem = self.ui.renderPbl_tableWidget.item(rowLs[0], 2)
	# 		mainItem.setText('main')
	# 		mainItem.setFont(font)
	# 		#mainItem.setBackground(QtGui.QColor(60,75,40))
	# 		passItem = self.ui.renderPbl_tableWidget.item(rowLs[0], 1)
	# 		passName = passItem.text()
	# 		passItem.setFont(font)
	# 		#passItem.setBackground(QtGui.QColor(60,75,40))
	# 		layerItem = self.ui.renderPbl_tableWidget.item(rowLs[0], 0)
	# 		layerName = passItem.text()
	# 		layerItem.setFont(font)
	# 		#layerItem.setBackground(QtGui.QColor(60,75,40))
	# 	#app hide and show forces thw window to update
	# #	app.hide()
	# #	app.show() # This was causing an issue with the UI closing so I've commented it out fot the time being. The widget still seems to auto update.


	def updateRenderPublishUI(self, current, previous):
		""" Update the render publish UI based on the current selection.
		"""
		# print self.sender()
		# print current, previous


	def renderPreview(self, item, column):
		""" Launches sequence viewer when entry is double-clicked.
		"""
		path = seq.getFirst( item.text(3) )
		self.preview(path)


	def setLayerAsMain(self):
		""" Sets the selected render layer as the main layer.
		"""
		rowCount = self.ui.renderPbl_treeWidget.topLevelItemCount()
		for row in range(0, rowCount):
			item = self.ui.renderPbl_treeWidget.topLevelItem(row)
			item.setText(2, 'layer')

		for item in self.ui.renderPbl_treeWidget.selectedItems():
			# item.setText(2, 'main')
			try:
				selectedItem = self.ui.renderPbl_treeWidget.topLevelItem( self.ui.renderPbl_treeWidget.indexOfTopLevelItem(item) )
				selectedItem.setText(2, 'main')
			except AttributeError:
				print "Warning: Only render layers (not render passes / AOVs) can be set as the main layer."

		self.ui.renderPbl_treeWidget.resizeColumnToContents(2)


	def renderTableAdd(self):
		""" Adds entries to the render layer tree view widget.
		"""
		self.renderPath = self.folderDialog(os.environ['MAYARENDERSDIR'])
		self.renderTableUpdate()


	def renderTableRemove(self):
		""" Removes the selected entry from the render layer tree view widget.
		"""
		root = self.ui.renderPbl_treeWidget.invisibleRootItem()
		for item in self.ui.renderPbl_treeWidget.selectedItems():
			(item.parent() or root).removeChild(item)
		# for item in self.ui.renderPbl_treeWidget.selectedItems():
		# 	print self.ui.renderPbl_treeWidget.indexFromItem(item)
		# 	print type(item)
		# 	#self.ui.renderPbl_treeWidget.takeTopLevelItem( self.ui.renderPbl_treeWidget.indexOfTopLevelItem(item) )


	def renderTableUpdate(self):
		""" Populates the render layer tree view widget with entries.
		"""
		renderPath = self.renderPath
		if renderPath:
			renderLayerDirs = []

			# Get subdirectories
			subdirs = next(os.walk(renderPath))[1]
			if subdirs:
				for subdir in subdirs:
					if not subdir.startswith('.'): # ignore directories that start with a dot
						renderLayerDirs.append(subdir)
			if renderLayerDirs:
				renderLayerDirs.sort()
			else: # use parent dir
				renderLayerDirs = [os.path.basename(renderPath)]
				renderPath = os.path.dirname(renderPath)

			# self.ui.renderPbl_treeWidget.setIconSize(QtCore.QSize(128, 72))

			# Add render layers
			for renderLayerDir in renderLayerDirs:
				renderPasses = seq.getBases(os.path.join(renderPath, renderLayerDir))

				if renderPasses: # only continue if render pass sequences exist in this directory
					renderLayerItem = QtGui.QTreeWidgetItem(self.ui.renderPbl_treeWidget)
					# renderLayerItem.setText(0, '%s (%d)' % (renderLayerDir, len(renderPasses)))
					renderLayerItem.setText(0, renderLayerDir)
					renderLayerItem.setText(2, 'layer')
					renderLayerItem.setText(3, osOps.relativePath(os.path.join(renderPath, renderLayerDir), 'SHOTPATH'))

					self.ui.renderPbl_treeWidget.addTopLevelItem(renderLayerItem)
					renderLayerItem.setExpanded(True)

					# Add render passes
					for renderPass in renderPasses:
						renderPassItem = QtGui.QTreeWidgetItem(renderLayerItem)
						path, prefix, fr_range, ext, num_frames = seq.getSequence( os.path.join(renderPath, renderLayerDir), renderPass )

						renderPassItem.setText(0, prefix)
						renderPassItem.setText(1, fr_range)
						if not fr_range == os.environ['FRAMERANGE']: # set red text for sequence mismatch
							renderPassItem.setForeground(1, QtGui.QBrush(QtGui.QColor("#c33")))
						renderPassItem.setText(2, ext.split('.', 1)[1])
						renderPassItem.setText(3, osOps.relativePath(os.path.join(renderPath, renderLayerDir, renderPass), 'SHOTPATH'))

						self.ui.renderPbl_treeWidget.addTopLevelItem(renderPassItem)

			# Resize columns
			self.ui.renderPbl_treeWidget.resizeColumnToContents(0)
			self.ui.renderPbl_treeWidget.resizeColumnToContents(1)
			self.ui.renderPbl_treeWidget.resizeColumnToContents(2)


	def dailyTableAdd(self):
		""" Populates the dailies publish table.
		"""
		# Parse the file path
		dailyPath = self.dailyPblBrowse() # dailyPath is a full path to a file

		if dailyPath:
			self.ui.dailyPbl_treeWidget.clear()

			path, prefix, fr_range, ext, num_frames = seq.detectSeq(dailyPath)

			if prefix:
				dailyItem = QtGui.QTreeWidgetItem(self.ui.dailyPbl_treeWidget)
				dailyItem.setText(0, '%s%s' % (prefix, ext))
				dailyItem.setText(1, fr_range)
				if not fr_range == os.environ['FRAMERANGE']: # set red text for sequence mismatch
					dailyItem.setForeground(1, QtGui.QBrush(QtGui.QColor("#c33")))
				dailyItem.setText(2, self.dailyType)
				dailyItem.setText(3, osOps.relativePath(path, 'SHOTPATH'))
				self.ui.dailyPbl_treeWidget.addTopLevelItem(dailyItem)
				#dailyItem.setExpanded(True)

			else:
				verbose.noSeq(os.path.basename(dailyPath))

		# Resize columns
		self.ui.dailyPbl_treeWidget.resizeColumnToContents(0)
		self.ui.dailyPbl_treeWidget.resizeColumnToContents(1)
		self.ui.dailyPbl_treeWidget.resizeColumnToContents(2)


	def setDailyType(self):
		""" Sets the dailies type and locks/unlocks the add and remove button accordingly.
		"""
		self.dailyType = self.ui.dailyPblType_comboBox.currentText()

		if self.dailyType:
			self.ui.dailyPblAdd_pushButton.setEnabled(True)
		else:
			self.ui.dailyPblAdd_pushButton.setEnabled(False)


	################browse dialogs###############	
	# Browse for assets to publish
	def assetPblBrowse(self):
		dialogHome = os.environ['JOBPATH']
		self.ui.pathToAsset_lineEdit.setText(self.fileDialog(dialogHome))

#	# Browse for renders to publish
#	def renderPblBrowse(self):
#		return self.folderDialog(os.environ['MAYARENDERSDIR'])

	# Browse for dailies to publish
	def dailyPblBrowse(self):
		if self.dailyType in ('modeling', 'texturing', 'animation', 'anim', 'fx', 'previs', 'tracking', 'rigging'):
			return self.fileDialog(os.environ['MAYAPLAYBLASTSDIR'])
		elif self.dailyType in ('lighting', 'shading', 'lookdev'):
			return self.fileDialog(os.environ['MAYARENDERSDIR'])
		elif self.dailyType in ('comp', ):
			return self.fileDialog(os.environ['NUKERENDERSDIR'])
		else:
			return self.fileDialog(os.environ['SHOTPATH'])


	#################getting ui options################

	def getMainPblOpts(self):
		""" Get basic publish options before publishing.
		"""
	#	self.approved, self.mail = '', ''
		self.pblNotes = self.ui.notes_textEdit.text() #.toPlainText() # Edited line as notes box is now line edit widget, not text edit
		self.pblType = self.getPblTab()[1]
		self.slShot = self.ui.publishToShot_comboBox.currentText()

		# Get path to publish to. If selected shot doesn't match shot the correct publish path is assigned based on the selected shot
		if self.ui.publishToShot_radioButton.isChecked() == 1:
			if self.slShot == os.environ['SHOT']: # publish to current shot
				self.pblTo = os.environ['SHOTPUBLISHDIR']
			else: # publish to user-specified shot
				self.pblTo = os.path.join(os.environ['JOBPATH'], self.slShot, os.environ["PUBLISHRELATIVEDIR"])
		elif self.ui.publishToJob_radioButton.isChecked() == 1: # publish to job
			self.pblTo = os.environ["JOBPUBLISHDIR"]
		elif self.ui.publishToLibrary_radioButton.isChecked() == 1: # publish to library
			self.pblTo = os.environ["GLOBALPUBLISHDIR"]

	#	if self.ui.approved_checkBox.checkState() == 2:
	#		self.approved = True
	#	if self.ui.mail_checkBox.checkState() == 2:
	#		self.mail = True


	def get_maya_assetPblOpts(self, genericAsset=False):
		""" Get Maya asset publish options.
		"""
		self.textures, self.subsetName, self.sceneName = '', '', ''
		self.chkLs = [] #self.chkLs = [self.pblNotes]
		if self.ui.textures_checkBox.checkState() == 2:
			self.textures = True
		if self.ui.subSet_checkBox.checkState() == 2:
			self.subsetName = '%s_sbs' % self.ui.subSetName_lineEdit.text()
			self.chkLs.append(self.subsetName)
		if self.ui.scene_toolButton.isChecked() == True:
			self.sceneName = self.ui.assetName_lineEdit.text()
			self.chkLs.append(self.sceneName)


	def get_nuke_assetPblOpts(self, name=True):
		""" Get Nuke asset publish options.
		"""
		self.chkLs = [self.pblNotes]
		if name:
			self.pblName = self.ui.nk_PblName_lineEdit.text()
			self.chkLs.append(self.pblName)


	def getDailyPblOpts(self):
		""" Get information about dailies before publishing.
		"""
		rowCount = self.ui.dailyPbl_treeWidget.topLevelItemCount()

		if rowCount == 1: # only allow one sequence to be published at a time
			dailyItem = self.ui.dailyPbl_treeWidget.topLevelItem(0)
			dailyPblOpts = (dailyItem.text(0), dailyItem.text(1), dailyItem.text(2), dailyItem.text(3))

		else:
			rowCount = None
			dailyPblOpts = None

		#self.chkLs = [self.pblNotes, rowCount]
		self.chkLs = [rowCount]
		return dailyPblOpts


	def getRenderPblOpts(self):
		""" Get information about renders before publishing. - THIS NEEDS RE-CODING
		"""
		self.renderDic = {}
		self.streamPbl, self.mainLayer = '', ''
		if self.ui.streamPbl_checkBox.checkState() == 2:
			self.streamPbl = True

		rowCount = self.ui.renderPbl_treeWidget.topLevelItemCount()
		for row in range(0, rowCount):
			renderLayerItem = self.ui.renderPbl_treeWidget.topLevelItem(row)

			layerName = renderLayerItem.text(0)
			filePath = renderLayerItem.text(3)
			self.renderDic[layerName] = filePath

			if renderLayerItem.text(2) == 'main':
				self.mainLayer = layerName

		if not rowCount:
			rowCount = None

		#self.chkLs = [self.pblNotes, rowCount]
		self.chkLs = [rowCount]
		print self.renderDic, self.streamPbl, self.mainLayer


	def initPublish(self):
		""" Initialises publish.
			Ultimately this whole system should be rewritten.
		"""
		self.getMainPblOpts()
		print self.pblTo, self.pblNotes, self.pblType, self.slShot

		###############
		# MAYA ASSETS #
		###############
		if self.pblType == 'ma Asset':

			self.get_maya_assetPblOpts()
			#print self.chkLs
			if not pblChk.chkOpts(self.chkLs):
				return

			# Model
			elif self.ui.model_toolButton.isChecked() == True:
				import ma_mdlPbl
				subtype = self.ui.assetSubType_comboBox.currentText()
				ma_mdlPbl.publish(self.pblTo, self.slShot, subtype, self.textures, self.pblNotes)
				#assetPublish.publish(genericOpts, 'ma_model', assetTypeOpts)

			# Rig
			elif self.ui.rig_toolButton.isChecked() == True:
				import ma_rigPbl
				subtype = self.ui.assetSubType_comboBox.currentText()
				ma_rigPbl.publish(self.pblTo, self.slShot, subtype, self.textures, self.pblNotes)

			# Camera
			if self.ui.camera_toolButton.isChecked() == True:
				import ma_camPbl
				subtype = self.ui.assetSubType_comboBox.currentText()
				ma_camPbl.publish(self.pblTo, self.slShot, subtype, self.pblNotes)

			# Geo
			elif self.ui.geo_toolButton.isChecked() == True:
				import ma_geoPbl
				subtype = self.ui.assetSubType_comboBox.currentText()
				ma_geoPbl.publish(self.pblTo, self.slShot, subtype, self.textures, self.pblNotes)

			# Geo cache
			elif self.ui.geoCache_toolButton.isChecked() == True:
				import ma_geoChPbl
				subtype = self.ui.assetSubType_comboBox.currentText()
				ma_geoChPbl.publish(self.pblTo, self.slShot, subtype, self.pblNotes)

			# Animation
			elif self.ui.animation_toolButton.isChecked() == True:
				import ma_animPbl
				ma_animPbl.publish(self.pblTo, self.slShot, self.pblNotes)

			# Shader
			elif self.ui.shader_toolButton.isChecked() == True:
				import ma_shdPbl
				ma_shdPbl.publish(self.pblTo, self.slShot, self.subsetName, self.textures, self.pblNotes)

			# FX
			elif self.ui.fx_toolButton.isChecked() == True:
				import ma_fxPbl
				ma_fxPbl.publish(self.pblTo, self.slShot, self.subsetName, self.textures, self.pblNotes)

			# Point cloud
			elif self.ui.ma_pointCloud_toolButton.isChecked() == True:
				import ma_pointCloudPbl
				ma_pointCloudPbl.publish(self.pblTo, self.slShot, self.subsetName, self.textures, self.pblNotes)

			# Shot
			elif self.ui.shot_toolButton.isChecked() == True:
				import ma_shotPbl
				ma_shotPbl.publish(self.pblTo, self.pblNotes) # self.subsetName, self.textures ?

			# Scene
			elif self.ui.scene_toolButton.isChecked() == True:
				import ma_scnPbl
				ma_scnPbl.publish(self.pblTo, self.slShot, self.sceneName, self.subsetName, self.textures, self.pblNotes)

			# Node
			elif self.ui.ma_node_toolButton.isChecked() == True:
				import ma_nodePbl
				subtype = self.ui.assetSubType_comboBox.currentText()
				ma_nodePbl.publish(self.pblTo, self.slShot, subtype, self.textures, self.pblNotes)

		###############
		# NUKE ASSETS #
		###############
		if self.pblType == 'nk Asset':

			self.get_nuke_assetPblOpts()
			if not pblChk.chkOpts(self.chkLs):
				return

			# Card
			if self.ui.card_toolButton.isChecked() == True:
				import nk_setupPbl
				self.pblType = 'card'
				nk_setupPbl.publish(self.pblTo, self.slShot, self.pblType, self.pblName, self.pblNotes)

			# Point cloud
			elif self.ui.nk_pointCloud_toolButton.isChecked() == True:
				import nk_setupPbl
				self.pblType = 'pointCloud'
				nk_setupPbl.publish(self.pblTo, self.slShot, self.pblType, self.pblName, self.pblNotes)

			# Node
			elif self.ui.nk_node_toolButton.isChecked() == True:
				import nk_setupPbl
				self.pblType = 'node'
				nk_setupPbl.publish(self.pblTo, self.slShot, self.pblType, self.pblName, self.pblNotes)

			# Comp
			elif self.ui.comp_toolButton.isChecked() == True:
				self.get_nuke_assetPblOpts(name=False)
				if not pblChk.chkOpts(self.chkLs):
					return
				import nk_compPbl
				self.pblType = 'comp'
				nk_compPbl.publish(self.pblTo, self.slShot, self.pblType, self.pblNotes)

			# Pre-comp
			elif self.ui.precomp_toolButton.isChecked() == True:
				import nk_setupPbl
				self.pblType = 'preComp'
				nk_setupPbl.publish(self.pblTo, self.slShot, self.pblType, self.pblName, self.pblNotes)

			# Setup
			elif self.ui.setup_toolButton.isChecked() == True:
				import nk_setupPbl
				self.pblType = 'setup'
				nk_setupPbl.publish(self.pblTo, self.slShot, self.pblType, self.pblName, self.pblNotes)	

		###########
		# DAILIES #
		###########
		elif self.pblType == 'Dailies':
			import ic_dailyPbl;
			self.getDailyPblOpts() # required just to get self.checkLs
			if not pblChk.chkOpts(self.chkLs): # check for entries in mandatory fields
				return
			ic_dailyPbl.publish(self.getDailyPblOpts(), self.pblTo, self.pblNotes)

		###########
		# RENDERS #
		###########
		elif self.pblType == 'Render':
			import ic_renderPbl
			self.getRenderPblOpts()
			#if not pblChk.chkOpts(self.chkLs): # check for entries in mandatory fields
			#	return
			ic_renderPbl.publish(self.renderDic, self.pblTo, self.mainLayer, self.streamPbl, self.pblNotes)


	##############
	# Gather tab #
	##############

	#ui adjustments
	def adjustGatherTab(self, showGatherButton = False):
		self.ui.gather_pushButton.setEnabled(False)
		if showGatherButton:
			self.ui.gather_pushButton.setEnabled(True)


	def getGatherFrom(self):
		""" Get location from which to gather assets.
		"""
		slShot = self.ui.gatherFromShot_comboBox.currentText()

		# Get path to gather from. If selected shot doesn't match shot the correct publish path is assigned based on the selected shot
		if self.ui.gatherFromShot_radioButton.isChecked() == 1:
			if slShot == os.environ['SHOT']: # gather from current shot
				self.gatherFrom = os.environ['SHOTPUBLISHDIR']
			else: # gather from user-specified shot
				self.gatherFrom = os.path.join(os.environ['JOBPATH'], slShot, os.environ["PUBLISHRELATIVEDIR"])
		elif self.ui.gatherFromJob_radioButton.isChecked() == 1: # gather from job
			self.gatherFrom = os.environ['JOBPUBLISHDIR']
		elif self.ui.gatherFromLibrary_radioButton.isChecked() == 1: # gather from library
			self.gatherFrom = os.environ["GLOBALPUBLISHDIR"]


	###################columns system, info and preview img update##################
	#defines columns to shorten name
	def defineColumns(self):
		self.aTypeCol = self.ui.assetType_listWidget
		self.aNameCol = self.ui.assetName_listWidget
		self.aSubTypeCol = self.ui.assetSubType_listWidget
		self.aVersionCol = self.ui.assetVersion_listWidget

	#clears columns
	def clearColumn(self, column):
		for i in range(0, column.count()):
			column.takeItem(0)
	
	#returns a list of items to display in gather based on running environment
	def getAssetEnvPrefix(self):
		if os.environ['ICARUSENVAWARE'] == 'MAYA':
			return ('ma', 'ic')
		elif os.environ['ICARUSENVAWARE'] == 'NUKE':
			return ('nk', 'ic', 'render')
		else:
			return ('ma', 'nk', 'ic', 'render', 'daily', 'dailies') # daily -> dailies
		
	#populates columns
	def fillColumn(self, column, searchPath):
		envPrefix = self.getAssetEnvPrefix()
		itemLs = os.listdir(searchPath); itemLs.sort()
		#making in progress publishes not visible
		if column == self.aVersionCol:
			for item in itemLs:
				if os.path.isdir(os.path.join(searchPath, item)):
					if 'in_progress.tmp' in os.listdir(os.path.join(searchPath, item)):
						itemLs.remove(item)
			#reversing order to facilitate user gather
			itemLs.reverse()
		if column == self.aTypeCol:
			for item in itemLs:
				if item[:2] in envPrefix or item in envPrefix:
					column.addItem(item)
		else:
			for item in itemLs:
				if not item.startswith('.'):
					column.addItem(item)
		#column.item(0).setSelected(True) # select the first item automatically
		#self.updateInfoField()
		#self.updateImgPreview()
	
	#adjust UI columns to accodmodate assetSubType column
	def adjustColumns(self):
		#checks for versioned items inside assetName folder. If not found displays subset column
		self.getGatherFrom()
		self.assetName = self.aNameCol.currentItem().text()
		vItemsPath = os.path.join(self.gatherFrom, self.assetType, self.assetName)
		if not pblChk.versionedItems(vItemsPath, vb=False):
			self.subType = True
			self.ui.assetSubType_listWidget.show()
			self.updateAssetSubTypeCol()
		else:
			self.subType = None
			self.ui.assetSubType_listWidget.hide()
			self.updateAssetVersionCol()

	#updates assetType column
	def updateAssetTypeCol(self):
		self.getGatherFrom()
		self.adjustGatherTab()
		self.clearColumn(self.aTypeCol)
		self.clearColumn(self.aNameCol)
		self.clearColumn(self.aSubTypeCol)
		self.clearColumn(self.aVersionCol)
		self.ui.gatherInfo_textEdit.setText('')
	#	self.previewPlayerCtrl(hide=True)
		pixmap = QtGui.QPixmap(None)
		self.ui.gatherImgPreview_label.setPixmap(pixmap)
		self.fillColumn(self.aTypeCol, self.gatherFrom)
	
	#updates assetName column
	def updateAssetNameCol(self):
		self.adjustGatherTab()
		self.assetType = self.aTypeCol.currentItem().text()
		self.clearColumn(self.aNameCol)
		self.clearColumn(self.aSubTypeCol)
		self.clearColumn(self.aVersionCol)
		self.ui.gatherInfo_textEdit.setText('')
	#	self.previewPlayerCtrl(hide=True)
		pixmap = QtGui.QPixmap(None)
		self.ui.gatherImgPreview_label.setPixmap(pixmap)
		searchPath = os.path.join(self.gatherFrom, self.assetType)
		self.fillColumn(self.aNameCol, searchPath)

	#updates assetSubType column
	def updateAssetSubTypeCol(self):
		self.adjustGatherTab()
		self.clearColumn(self.aSubTypeCol)
		self.clearColumn(self.aVersionCol)
		self.ui.gatherInfo_textEdit.setText('')
	#	self.previewPlayerCtrl(hide=True)
		pixmap = QtGui.QPixmap(None)
		self.ui.gatherImgPreview_label.setPixmap(pixmap)
		searchPath = os.path.join(self.gatherFrom, self.assetType, self.assetName)
		self.fillColumn(self.aSubTypeCol, searchPath)

	#updates assetVersion column
	def updateAssetVersionCol(self):
		self.adjustGatherTab()
		self.clearColumn(self.aVersionCol)
		if self.subType:
			self.assetSubType = self.aSubTypeCol.currentItem().text()
		else:
			self.assetSubType = ''
		self.ui.gatherInfo_textEdit.setText('')
	#	self.previewPlayerCtrl(hide=True)
		pixmap = QtGui.QPixmap(None)
		self.ui.gatherImgPreview_label.setPixmap(pixmap)
		searchPath = os.path.join(self.gatherFrom, self.assetType, self.assetName, self.assetSubType)
		self.fillColumn(self.aVersionCol, searchPath)


	def updateImgPreview(self):
		""" Update image preview field with snapshot.
		"""
		# Apply context menu to open viewer - DO THIS SOMEWHERE ELSE
	#	self.ui.gatherImgPreview_label.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
	#	self.actionPreview = QtGui.QAction("Preview...", None)
	#	self.actionPreview.triggered.connect(self.preview)
	#	self.ui.gatherImgPreview_label.addAction(self.actionPreview)

		import previewImg
		imgPath = previewImg.getImg(self.gatherPath, forceExt='jpg')
	#	self.previewPlayerCtrl(hide=True)
		# pixmap = QtGui.QPixmap(None)
		# self.ui.gatherImgPreview_label.setPixmap(pixmap)
		pixmap = QtGui.QPixmap(imgPath)
		self.ui.gatherImgPreview_label.setScaledContents(True)
		self.ui.gatherImgPreview_label.setPixmap(pixmap)

#		if self.previewPlayer:
#			imgPath = previewImg.getImg(self.gatherPath, forceExt='mov')
#			if imgPath:
#				self.previewPlayerCtrl(hide=True)
#				pixmap = QtGui.QPixmap(None)
#				self.ui.gatherImgPreview_label.setPixmap(pixmap)
#				self.previewPlayerCtrl(loadImg=imgPath)
#				self.previewPlayerCtrl(show=True)
#				self.previewPlayerCtrl(play=True)
#
#				# Add preview context menu
#				self.ui.gatherImgPreview_label.addAction(self.actionPreview)
#
#		if not imgPath or not self.previewPlayer:
#			imgPath = previewImg.getImg(self.gatherPath, forceExt='jpg')
#			if imgPath:
#				self.previewPlayerCtrl(hide=True)
#				pixmap = QtGui.QPixmap(None)
#				self.ui.gatherImgPreview_label.setPixmap(pixmap)
#				pixmap = QtGui.QPixmap(imgPath)
#				self.ui.gatherImgPreview_label.setScaledContents(True)
#				self.ui.gatherImgPreview_label.setPixmap(pixmap)
#
#				# Remove preview context menu
#				self.ui.gatherImgPreview_label.removeAction(self.actionPreview)


	def updateInfoField(self):
		""" Update info field with notes and other relevant data.
		"""
		self.adjustGatherTab(showGatherButton = True)
		self.assetVersion = self.aVersionCol.currentItem().text()
		self.gatherPath = os.path.join(self.gatherFrom, self.assetType, self.assetName, self.assetSubType, self.assetVersion)

	#	sys.path.append(self.gatherPath)
	#	import icData; reload(icData)
	#	sys.path.remove(self.gatherPath)
	#	self.ui.gatherInfo_textEdit.setText(icData.notes)

		import jobSettings
		# Instantiate XML data classes
		assetData = jobSettings.jobSettings()
		assetDataLoaded = assetData.loadXML(os.path.join(self.gatherPath, 'assetData.xml'))

		# If XML files don't exist, create defaults, and attempt to convert data from Python data files
		if not assetDataLoaded:
			import legacySettings

			# Try to convert from icData.py to XML (legacy assets)
			if legacySettings.convertAssetData(self.gatherPath, assetData):
				assetData.loadXML()
			else:
				return False

		# Print info to text field
		infoText = ""
		notes = assetData.getValue('asset', 'notes')
		if notes:
			infoText += "%s\n\n" % notes
		infoText += "Published by %s\n%s" % (assetData.getValue('asset', 'user'), assetData.getValue('asset', 'timestamp'))
		source = assetData.getValue('asset', 'assetSource')
		if source:
			infoText += "\nFrom '%s'" % source #os.path.basename(source)

		self.ui.gatherInfo_textEdit.setText(infoText)


	def initGather(self):
		""" Initialise gather.
		"""
		if os.environ['ICARUSENVAWARE'] == 'MAYA':
			if self.assetType == 'ma_anim':
				import ma_animGather
				ma_animGather.gather(self.gatherPath)
			else:
				import ma_assetGather
				ma_assetGather.gather(self.gatherPath)

		elif os.environ['ICARUSENVAWARE'] == 'NUKE':
			if self.assetType in ('ic_geo', 'ic_pointCloud'):
				import nk_geoGather
				nk_geoGather.gather(self.gatherPath)
			elif self.assetType == 'render':
				import nk_renderGather
				app.hide()
				nk_renderGather.gather(self.gatherPath)
				app.show()
			else:
				import nk_assetGather
				nk_assetGather.gather(self.gatherPath)


#########################################
# RUN ICARUS WITH ENVIRONMENT AWARENESS #
#########################################

# Read user prefs config file - if it doesn't exist it will be created
userPrefs.read()

# Set verbosity
try:
	os.environ['IC_VERBOSITY'] = userPrefs.config.get('main', 'verbosity')
except:
	userPrefs.edit('main', 'verbosity', '2')
	os.environ['IC_VERBOSITY'] = userPrefs.config.get('main', 'verbosity')

# Version message
verbose.icarusLaunch(os.environ['ICARUSVERSION'], os.environ['PIPELINE'])

# Python version check
try:
	assert sys.version_info >= (2,7)
except AssertionError:
	sys.exit("ERROR: Icarus requires Python version 2.7 or above.")

# Detect environment and run application
if os.environ['ICARUSENVAWARE'] == 'MAYA' or os.environ['ICARUSENVAWARE'] == 'NUKE':
	app = icarusApp()

	# Apply UI style sheet
	qss=os.path.join(os.environ['ICWORKINGDIR'], "style.qss")
	with open(qss, "r") as fh:
		app.setStyleSheet(fh.read())

	# Set Qt window flags based on running OS
	if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
		app.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint)
	else:
		app.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint)
		#app.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

	# Centre window
#	app.move(QtGui.QDesktopWidget().availableGeometry(1).center() - app.frameGeometry().center())
	app.show()

#CLARISSE ENV - Waiting until clarisse purchase
#elif os.environ['ICARUSENVAWARE'] == 'CLARISSE':
#	import clarisse_icarusEventLoop
#	try:
#		mainApp = QtGui.QApplication('Icarus')
#	except RuntimeError:
#		mainApp = QtCore.QCoreApplication.instance()
#	app = icarusApp()
#	app.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint)
#	app.show()
#	icarus_clarisseWrap.exec_(mainApp)


#################################
# RUN ICARUS IN STANDALONE MODE #
#################################

else:
	if __name__ == '__main__':
		mainApp = QtGui.QApplication(sys.argv)
		mainApp.setApplicationName('Icarus')

		# Apply UI style sheet
		qss=os.path.join(os.environ['ICWORKINGDIR'], "style.qss")
		with open(qss, "r") as fh:
			mainApp.setStyleSheet(fh.read())

		app = icarusApp()

		# Window flags
		app.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)

		# Centre window
		#app.move(QtGui.QDesktopWidget().availableGeometry(1).center() - app.frameGeometry().center())

		app.show()
		sys.exit(app.exec_())

