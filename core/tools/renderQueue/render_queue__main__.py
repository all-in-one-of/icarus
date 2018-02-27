#!/usr/bin/python

# [Icarus] render_queue__main__.py
#
# Mike Bonnington <mike.Bonnington@gps-ldn.com>
# (c) 2016-2018 Gramercy Park Studios
#
# Batch Render Queue Manager
# A UI for managing the render queue, as well as executing render jobs.


import datetime
import math
import os
import socket
import sys
import time

# Initialise Icarus environment
# sys.path.append(os.environ['IC_WORKINGDIR'])
# import env__init__
# env__init__.setEnv()

from Qt import QtCore, QtGui, QtWidgets
import ui_template as UI

# Import custom modules
import renderQueue
import sequence
import verbose


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

VENDOR = "Gramercy Park Studios"
COPYRIGHT = "(c) 2016-2018"
DEVELOPERS = "Mike Bonnington"

# Set window title and object names
WINDOW_TITLE = "Render Queue"
WINDOW_OBJECT = "renderQueueUI"

# Set the UI and the stylesheet
UI_FILE = "render_queue_ui.ui"
STYLESHEET = "style.qss"  # Set to None to use the parent app's stylesheet

# Other options
STORE_WINDOW_GEOMETRY = True


# ----------------------------------------------------------------------------
# Main application class
# ----------------------------------------------------------------------------

class RenderQueueApp(QtWidgets.QMainWindow, UI.TemplateUI):
	""" Main application class.
	"""
	def __init__(self, parent=None):
		super(RenderQueueApp, self).__init__(parent)
		self.parent = parent

		self.setupUI(window_object=WINDOW_OBJECT, 
		             window_title=WINDOW_TITLE, 
		             ui_file=UI_FILE, 
		             stylesheet=STYLESHEET, 
		             store_window_geometry=STORE_WINDOW_GEOMETRY)  # re-write as **kwargs ?

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Window)

		# Set other Qt attributes
		#self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

		# Define global variables
		self.timeFormatStr = "%Y/%m/%d %H:%M:%S"
		self.localhost = socket.gethostname()
		self.selection = []
		self.renderOutput = ""
		#verbose.registerStatusBar(self.ui.statusbar)

		# Define standard UI colours
		self.colBlack         = QtGui.QColor("#000000")  # black
		self.colWhite         = QtGui.QColor("#ffffff")  # white
		self.colBorder        = QtGui.QColor("#222222")  # dark grey
		self.colInactive      = QtGui.QColor("#666666")  # grey
		self.colActive        = QtGui.QColor("#00b2ee")  # bright blue
		self.colCompleted     = QtGui.QColor("#709e32")  # green
		self.colCompletedDark = QtGui.QColor("#577927")  # dark green
		self.colError         = QtGui.QColor("#bc0000")  # red

		# Instantiate render queue class and load data
		self.rq = renderQueue.renderQueue()
		self.rq.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'renderQueue.xml'), use_template=False)

		# Create a QProcess object to handle the rendering process
		# asynchronously
		self.renderProcess = QtCore.QProcess(self)
		self.renderProcess.finished.connect(self.renderComplete)
		self.renderProcess.readyReadStandardOutput.connect(self.updateSlaveView)

		# Connect signals & slots
		self.ui.renderQueue_treeWidget.itemSelectionChanged.connect(self.updateToolbarUI)
		self.ui.renderQueue_treeWidget.header().sectionResized.connect(lambda logicalIndex, oldSize, newSize: self.updateColumn(logicalIndex, oldSize, newSize))  # Resize progress indicator

		self.ui.jobSubmit_toolButton.clicked.connect(self.launchRenderSubmit)
		self.ui.refresh_toolButton.clicked.connect(self.rebuildRenderQueueView)

		self.ui.jobPause_toolButton.clicked.connect(lambda *args: self.changePriority(0, absolute=True))  # this lambda function is what's causing the multiple windows issue, no idea why though
		#self.ui.jobKill_toolButton.clicked.connect(self.killJob)  # not yet implemented
		self.ui.jobDelete_toolButton.clicked.connect(self.deleteJob)
		#self.ui.jobResubmit_toolButton.clicked.connect(self.resubmitJob)  # not yet implemented
		self.ui.jobPriority_slider.sliderMoved.connect(lambda value: self.changePriority(value)) # this lambda function is what's causing the multiple windows issue, no idea why though
		self.ui.jobPriority_slider.sliderReleased.connect(self.updatePriority)

		self.ui.taskComplete_toolButton.clicked.connect(self.completeTask)
		self.ui.taskRequeue_toolButton.clicked.connect(self.requeueTask)

		# Add context menu items to job submit tool button
		# self.ui.jobSubmit_toolButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

		# self.actionSubmitMaya = QtWidgets.QAction("Maya...", None)
		# mayaIcon = QtGui.QIcon()
		# mayaIcon.addPixmap(QtGui.QPixmap(":/rsc/rsc/app_icon_maya.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		# mayaIcon.addPixmap(QtGui.QPixmap(":/rsc/rsc/app_icon_maya_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
		# self.actionSubmitMaya.setIcon(mayaIcon)
		# self.actionSubmitMaya.triggered.connect(self.launchRenderSubmit)
		# self.ui.jobSubmit_toolButton.addAction(self.actionSubmitMaya)
		# #self.actionSubmitMaya.setEnabled(False)

		# self.actionSubmitNuke = QtWidgets.QAction("Nuke...", None)
		# nukeIcon = QtGui.QIcon()
		# nukeIcon.addPixmap(QtGui.QPixmap(":/rsc/rsc/app_icon_nuke.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		# nukeIcon.addPixmap(QtGui.QPixmap(":/rsc/rsc/app_icon_nuke_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
		# self.actionSubmitNuke.setIcon(nukeIcon)
		# self.actionSubmitNuke.triggered.connect(self.launchRenderSubmit)
		# self.ui.jobSubmit_toolButton.addAction(self.actionSubmitNuke)
		# #self.actionSubmitNuke.setEnabled(False)

		# Add context menu items to slave control tool button
		self.ui.slaveControl_toolButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

		self.actionSlaveStart = QtWidgets.QAction("Start Slave", None)
		self.actionSlaveStart.triggered.connect(self.toggleSlave)
		self.ui.slaveControl_toolButton.addAction(self.actionSlaveStart)

		self.actionSlaveStop = QtWidgets.QAction("Stop Slave", None)
		self.actionSlaveStop.triggered.connect(self.toggleSlave)
		self.ui.slaveControl_toolButton.addAction(self.actionSlaveStop)

		self.actionKillTask = QtWidgets.QAction("Stop Slave Immediately and Kill Current Task", None)
		self.actionKillTask.triggered.connect(self.killRenderProcess)
		self.ui.slaveControl_toolButton.addAction(self.actionKillTask)

		self.actionSlaveContinueAfterTask = QtWidgets.QAction("Continue After Current Task Completion", None)
		self.actionSlaveContinueAfterTask.setCheckable(True)
		self.ui.slaveControl_toolButton.addAction(self.actionSlaveContinueAfterTask)

		self.actionSlaveStopAfterTask = QtWidgets.QAction("Stop Slave After Current Task Completion", None)
		self.actionSlaveStopAfterTask.setCheckable(True)
		self.ui.slaveControl_toolButton.addAction(self.actionSlaveStopAfterTask)

		slaveControlAfterTaskGroup = QtWidgets.QActionGroup(self)
		slaveControlAfterTaskGroup.addAction(self.actionSlaveContinueAfterTask)
		slaveControlAfterTaskGroup.addAction(self.actionSlaveStopAfterTask)
		self.actionSlaveContinueAfterTask.setChecked(True)

		# Set local slave as disabled initially
		self.setSlaveStatus("disabled")  # Store this as a preference or something

		self.rebuildRenderQueueView()  # Move these to show() event hander function?
		self.updateSlaveView()
		self.updateToolbarUI()


	def launchRenderSubmit(self):
		""" Launch Render Submitter window.
		"""
		import render_submit
		try:
			self.renderSubmitUI.display()
		except AttributeError:
			self.renderSubmitUI = render_submit.RenderSubmitUI(parent=self)
			self.renderSubmitUI.display()


	def rebuildRenderQueueView(self):
		""" Clears and rebuilds the render queue tree view widget, populating
			it with entries for render jobs and tasks.
		"""
		# Clear tree widget
		self.ui.renderQueue_treeWidget.clear()

		# Populate tree widget with render jobs and tasks
		self.updateRenderQueueView()

		# Resize all columns to fit content
		for i in range(0, self.ui.renderQueue_treeWidget.columnCount()):
			self.ui.renderQueue_treeWidget.resizeColumnToContents(i)

		# Hide ID column
		self.ui.renderQueue_treeWidget.setColumnHidden(1, True)

		# Sort by submit time column - move this somewhere else?
		self.ui.renderQueue_treeWidget.sortByColumn(7, QtCore.Qt.DescendingOrder)

		#self.updateSlaveView()


	def updateRenderQueueView(self, reloadDatabase=True):
		""" Update the render queue tree view widget with entries for render
			jobs and tasks.
			This function will refresh the view by updating the existing
			items, without completely rebuilding it.
			TODO: we probably shouldn't be writing to the XML file here, this
			function should be read only.
		"""
		if reloadDatabase:
			self.rq.loadXML(quiet=True)  # Reload XML data

		# Stop the widget from emitting signals
		self.ui.renderQueue_treeWidget.blockSignals(True)

		# Populate tree widget with render jobs
		for jobElement in self.rq.getJobs():

			# Get values from XML
			jobID = jobElement.get('id')
			jobName = self.rq.getValue(jobElement, 'name')
			jobType = self.rq.getValue(jobElement, 'type')
			jobFrames = self.rq.getValue(jobElement, 'frames')
			jobPriority = self.rq.getValue(jobElement, 'priority')
			jobStatus = self.rq.getValue(jobElement, 'status')
			jobUser = self.rq.getValue(jobElement, 'user')
			jobSubmitTime = self.rq.getValue(jobElement, 'submitTime')
			jobComment = self.rq.getValue(jobElement, 'comment')

			# Get the render job item or create it if it doesn't exist
			renderJobItem = self.getQueueItem(self.ui.renderQueue_treeWidget.invisibleRootItem(), jobID)

			# Fill columns with data
			renderJobItem.setText(0, jobName)
			renderJobItem.setText(1, jobID)
			renderJobItem.setText(2, jobType)
			renderJobItem.setText(3, jobFrames)
			renderJobItem.setText(4, jobStatus)
			renderJobItem.setText(5, jobPriority)
			renderJobItem.setText(6, jobUser)
			renderJobItem.setText(7, jobSubmitTime)

			# Initialise counters and timers
			jobTotalTimeSeconds = 0
			inProgressTaskCount = 0
			completedTaskCount = 0
			inProgressTaskFrameCount = 0
			completedTaskFrameCount = 0
			if not jobFrames or jobFrames == 'Unknown':
				totalFrameCount = -1
			else:
				totalFrameCount = len(sequence.numList(jobFrames))

			# Populate render tasks
			taskElements = jobElement.findall('task')
			for taskElement in taskElements:

				# Get values from XML
				taskID = taskElement.get('id')
				taskFrames = self.rq.getValue(taskElement, 'frames')
				taskStatus = self.rq.getValue(taskElement, 'status')
				taskTotalTime = self.rq.getValue(taskElement, 'totalTime')
				taskSlave = self.rq.getValue(taskElement, 'slave')

				# Get the render task item or create it if it doesn't exist
				renderTaskItem = self.getQueueItem(renderJobItem, taskID)

				# Fill columns with data
				renderTaskItem.setText(0, "Task %s" %taskID)
				renderTaskItem.setText(1, taskID)
				renderTaskItem.setText(3, taskFrames)
				renderTaskItem.setText(4, taskStatus)

				# Calculate progress
				if taskFrames == 'Unknown':
					if taskStatus == "In Progress":
						inProgressTaskCount += 1
						inProgressTaskFrameCount = -1
					if taskStatus == "Done":
						completedTaskCount += 1
						completedTaskFrameCount = -1
				else:
					taskFrameCount = len(sequence.numList(taskFrames))
					if taskStatus == "In Progress":
						inProgressTaskCount += 1
						inProgressTaskFrameCount += taskFrameCount
					if taskStatus == "Done":
						completedTaskCount += 1
						completedTaskFrameCount += taskFrameCount

				# Colour the status text
				# if taskStatus == "In Progress": # and taskSlave == self.localhost:
				# 	renderTaskItem.setForeground(4, QtGui.QBrush(self.colActive))
				# elif taskStatus == "Done": # and taskSlave == self.localhost:
				# 	renderTaskItem.setForeground(4, QtGui.QBrush(self.colCompleted))

				# Update timers
				try:
					totalTimeSeconds = float(taskTotalTime)  # Use float and round for millisecs
					jobTotalTimeSeconds += totalTimeSeconds
					totalTime = str(datetime.timedelta(seconds=int(totalTimeSeconds)))
				except (TypeError, ValueError):
					totalTime = None

				renderTaskItem.setText(8, totalTime)
				renderTaskItem.setText(9, taskSlave)

			# Calculate job progress and update status
			colProgress = self.colCompletedDark
			if completedTaskFrameCount == 0:
				if inProgressTaskFrameCount == 0:
					jobStatus = "Queued"
				else:
					jobStatus = "[0%] In Progress"
			elif completedTaskFrameCount == totalFrameCount:
				jobStatus = "Done"
			else:
				percentComplete = (float(completedTaskFrameCount) / float(totalFrameCount)) * 100
				if inProgressTaskFrameCount == 0:
					jobStatus = "[%d%%] Waiting" %percentComplete
					colProgress = self.colInactive
				else:
					jobStatus = "[%d%%] In Progress" %percentComplete
					colProgress = self.colCompleted

			self.drawJobProgressIndicator(renderJobItem, completedTaskFrameCount, inProgressTaskFrameCount, totalFrameCount, colProgress)

			self.rq.setStatus(jobID, jobStatus)  # Write to XML if status has changed
			renderJobItem.setText(4, jobStatus)

			# Calculate time taken
			try:
				jobTotalTime = str(datetime.timedelta(seconds=int(jobTotalTimeSeconds)))
			except (TypeError, ValueError):
				jobTotalTime = None

			renderJobItem.setText(8, str(jobTotalTime))
			renderJobItem.setText(9, "%d %s rendering" %(inProgressTaskCount, verbose.pluralise("slave", inProgressTaskCount)))
			renderJobItem.setText(10, jobComment)

		# Re-enable signals
		self.ui.renderQueue_treeWidget.blockSignals(False)


	def getQueueItem(self, parent, itemID=None):
		""" Return the render queue item identified by 'itemID' belonging to
			'parent'.
			If it doesn't exist, return a new item.
			If 'itemID' is not specified, return a list of all the child
			items.
		"""
		child_count = parent.childCount()

		if itemID is None:
			items = []
			for i in range(child_count):
				items.append(parent.child(i))
			return items

		else:
			for i in range(child_count):
				item = parent.child(i)
				if item.text(1) == itemID:
					return item

			return QtWidgets.QTreeWidgetItem(parent)


	def drawJobProgressIndicator(self, renderJobItem, completedTaskFrameCount,
								 inProgressTaskFrameCount, totalFrameCount,
								 colProgress):
		""" Draw a pixmap to represent the progress of a job.
		"""
		border = 1
		width = self.ui.renderQueue_treeWidget.columnWidth(4)
		height = self.ui.renderQueue_treeWidget.rowHeight(self.ui.renderQueue_treeWidget.indexFromItem(renderJobItem))
		barWidth = width - (border*2)
		barHeight = height - (border*2)
		completedRatio = float(completedTaskFrameCount) / float(totalFrameCount)
		inProgressRatio = float(inProgressTaskFrameCount) / float(totalFrameCount)
		completedLevel = math.ceil(completedRatio*barWidth)
		inProgressLevel = math.ceil((completedRatio+inProgressRatio)*barWidth)

		image = QtGui.QPixmap(width, height)

		qp = QtGui.QPainter()
		qp.begin(image)
		pen = QtGui.QPen()
		pen.setStyle(QtCore.Qt.NoPen)
		qp.setPen(pen)
		qp.setBrush(self.colBorder)
		qp.drawRect(0, 0, width, height)
		qp.setBrush(self.colBlack)
		qp.drawRect(border, border, barWidth, barHeight)
		qp.setBrush(self.colActive)
		qp.drawRect(border, border, inProgressLevel, barHeight)
		qp.setBrush(colProgress)
		qp.drawRect(border, border, completedLevel, barHeight)
		qp.end()

		# renderJobItem.setBackground(4, image)  # PyQt5 doesn't like this
		renderJobItem.setBackground(4, QtGui.QBrush(image))  # Test with Qt4/PySide
		renderJobItem.setForeground(4, QtGui.QBrush(self.colWhite))


	def updateColumn(self, logicalIndex, oldSize, newSize):
		""" Update the progress indicator when the column is resized.
		"""
		#print "Column %s resized from %s to %s pixels" %(logicalIndex, oldSize, newSize)

		if logicalIndex == 4:
			# renderJobItems = self.getQueueItem(self.ui.renderQueue_treeWidget.invisibleRootItem())
			# for renderJobItem in renderJobItems:
			# 	self.drawJobProgressIndicator(renderJobItem, 0, 0, 100, self.colInactive)

			self.updateRenderQueueView(reloadDatabase=False)


	def updateToolbarUI(self):
		""" Store the current selection.
			Only allow jobs OR tasks to be selected, not both.
			Update the toolbar UI based on the selection in the render queue
			view.
		"""
		self.selection = []
		selectionType = None

		for item in self.ui.renderQueue_treeWidget.selectedItems():
			if item.parent():  # Task is selected
				currentItem = self.ui.renderQueue_treeWidget.currentItem()
				if selectionType == "Job":
					self.selection = []
					self.ui.renderQueue_treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
					self.ui.renderQueue_treeWidget.clearSelection()
					self.ui.renderQueue_treeWidget.setCurrentItem(currentItem)
				else:
					selectionType = "Task"
					self.ui.renderQueue_treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
					jobTaskID = int(item.parent().text(1)), int(item.text(1))
					#print "Task selected: %s %s" %jobTaskID
					self.selection.append(jobTaskID)
					self.ui.job_groupBox.setEnabled(False)
					self.ui.task_groupBox.setEnabled(True)
			else:  # Job is selected
				currentItem = self.ui.renderQueue_treeWidget.currentItem()
				if selectionType == "Task":
					self.selection = []
					self.ui.renderQueue_treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
					self.ui.renderQueue_treeWidget.clearSelection()
					self.ui.renderQueue_treeWidget.setCurrentItem(currentItem)
				else:
					selectionType = "Job"
					self.ui.renderQueue_treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
					jobTaskID = int(item.text(1)), -1
					#print "Job selected: %s %s" %jobTaskID
					self.selection.append(jobTaskID)
					self.ui.job_groupBox.setEnabled(True)
					self.ui.task_groupBox.setEnabled(False)

		if not self.selection:  # Nothing is selected
			#print "Nothing selected."
			self.ui.job_groupBox.setEnabled(False)
			self.ui.task_groupBox.setEnabled(False)

		# Disable submit button if shot is not set (temporary)
		try:
			os.environ['SHOT']
			self.ui.jobSubmit_toolButton.setEnabled(True)
		except KeyError:
			self.ui.jobSubmit_toolButton.setEnabled(False)

		#print self.selection


	def updateSlaveView(self):
		""" Update the information in the slave info area.
			This function is also called by the render process signal in order
			to capture its output and display in the UI widget.
		"""
		self.ui.slaveControl_toolButton.setText("%s (%s)" %(self.localhost, self.slaveStatus))

		try:
			line = str(self.renderProcess.readAllStandardOutput(), 'utf-8')
		except TypeError:  # Python 2.x compatibility
			line = str(self.renderProcess.readAllStandardOutput())
		self.renderOutput += line
		self.ui.output_textEdit.setPlainText(self.renderOutput)
		self.ui.output_textEdit.moveCursor(QtGui.QTextCursor.End)


	def restoreSelection(self):
		""" Reselect items in the render queue view.
			This function is now redundant.
		"""
		expandedJobs = []
		root = self.ui.renderQueue_treeWidget.invisibleRootItem()
		for j in range(root.childCount()):
			jobItem = root.child(j)
			jobID = int(jobItem.text(1))
			jobTaskID = jobID, -1
			if jobTaskID in self.selection:
				jobItem.setSelected(True)

			for t in range(jobItem.childCount()):
				taskItem = jobItem.child(t)
				taskID = int(taskItem.text(1))
				jobTaskID = jobID, taskID
				#jobTaskID = int(taskItem.parent().text(1)), int(taskItem.text(1))
				if jobTaskID in self.selection:
					taskItem.setSelected(True)


	def deleteJob(self):
		""" Removes selected render job(s) from the database and updates the
			view.
		"""
		try:
			for item in self.ui.renderQueue_treeWidget.selectedItems():
				# If item has no parent then it must be a top level item, and
				# therefore also a job
				if not item.parent():
					jobID = int(item.text(1))

					# Remove item from view
					if self.rq.deleteJob(jobID):
						self.ui.renderQueue_treeWidget.takeTopLevelItem( self.ui.renderQueue_treeWidget.indexOfTopLevelItem(item) )
						verbose.message("Job ID %s deleted." %jobID)
					else:
						verbose.warning("Job ID %s cannot be deleted while in progress." %jobID)

			#self.updateRenderQueueView()

		except ValueError:
			pass


	def changePriority(self, amount=0, absolute=False):
		""" Changes priority of the selected render.
			This function is called with 'absolute=False' when the
			'Reprioritise' slider is dragged.
			And 'absolute=True' when we want to set the priority directly,
			e.g. when a job is paused.
		"""
		self.timerUpdateView.stop()  # Don't update the view when dragging the slider

		try:
			for item in self.ui.renderQueue_treeWidget.selectedItems():
				# If item has no parent then it must be a top level item, and
				# therefore also a job
				if not item.parent():
					index = int(item.text(1))
					minPriority = 0
					maxPriority = 100

					if absolute:
						newPriority = amount
					else:
						currentPriority = self.rq.getPriority(index)
						newPriority = currentPriority+amount

					if newPriority <= minPriority:
						item.setText(5, str(minPriority))
					elif newPriority >= maxPriority:
						item.setText(5, str(maxPriority))
					else:
						item.setText(5, str(newPriority))

					if absolute:
						self.updatePriority()

		except ValueError:
			pass


	def updatePriority(self):
		""" Read the the changed priority value(s) from the UI and store in
			the database.
			This function is called when the 'Reprioritise' slider is
			released, or when we want to set the priority directly.
		"""
		try:
			for item in self.ui.renderQueue_treeWidget.selectedItems():
				# If item has no parent then it must be a top level item, and
				# therefore also a job
				if not item.parent():
					index = int(item.text(1))
					priority = int(item.text(5))
					self.rq.setPriority(index, priority)

			self.updateRenderQueueView()

		except ValueError:
			pass

		self.ui.jobPriority_slider.setValue(0)  # Reset priority slider to zero when released
		self.timerUpdateView.start()  # Restart the timer to periodically update the view


	# def resubmitJob(self):
	# 	""" Resubmit selected job(s) to render queue.
	# 	"""
	# 	try:
	# 		for item in self.ui.renderQueue_treeWidget.selectedItems():
	# 			if not item.parent(): # if item has no parent then it must be a top level item, and therefore also a job

	# 				jobName = self.rq.getValue(item, 'name')
	# 				jobType = self.rq.getValue(item, 'type')
	# 				priority = self.rq.getValue(item, 'priority')
	# 				frames = self.rq.getValue(item, 'frames')
	# 				taskSize = self.rq.getValue(item, 'taskSize')

	# 				mayaScene = self.rq.getValue(item, 'mayaScene')
	# 				mayaProject = self.rq.getValue(item, 'mayaProject')
	# 				mayaFlags = self.rq.getValue(item, 'mayaFlags')
	# 				mayaRenderCmd = self.rq.getValue(item, 'mayaRenderCmd')

	# 				taskList = []

	# 				genericOpts = jobName, jobType, priority, frames, taskSize
	# 				mayaOpts = mayaScene, mayaProject, mayaFlags, mayaRenderCmd

	# 				self.rq.newJob(genericOpts, mayaOpts, taskList, os.environ['IC_USERNAME'], time.strftime(self.timeFormatStr))

	# 	except ValueError:
	# 		pass


	def completeTask(self):
		""" Mark the selected task as completed.
		"""
		jobTaskIDs = []  # This will hold a tuble containing (job id, task id)

		try:
			for item in self.ui.renderQueue_treeWidget.selectedItems():
				# If item has parent then it must be a subitem, and therefore
				# also a task
				if item.parent():
					jobTaskID = int(item.parent().text(1)), int(item.text(1))
					jobTaskIDs.append(jobTaskID)

			for jobTaskID in jobTaskIDs:
				self.rq.completeTask(jobTaskID[0], jobTaskID[1], taskTime=0)
				verbose.message("Job ID %d: task ID %d marked as Done." %jobTaskID)

			self.updateRenderQueueView()

		except ValueError:
			pass


	def requeueTask(self):
		""" Requeue the selected task.
		"""
		jobTaskIDs = []  # This will hold a tuple containing (job id, task id)

		try:
			for item in self.ui.renderQueue_treeWidget.selectedItems():
				# If item has parent then it must be a subitem, and therefore
				# also a task
				if item.parent():
					jobTaskID = int(item.parent().text(1)), int(item.text(1))
					jobTaskIDs.append(jobTaskID)

			for jobTaskID in jobTaskIDs:
				self.rq.requeueTask(jobTaskID[0], jobTaskID[1])
				verbose.message("Job ID %d: task ID %d requeued." %jobTaskID)

			self.updateRenderQueueView()

		except ValueError:
			pass


	def toggleSlave(self):
		""" Enable or disable the local slave.
		"""
		if self.slaveStatus == "disabled":
			self.setSlaveStatus("idle")
		else:
			self.setSlaveStatus("disabled")

		self.updateSlaveView()


	def setSlaveStatus(self, status):
		""" Set the local slave status, and update the tool button and menu.
		"""
		statusIcon = QtGui.QIcon()
		self.slaveStatus = status

		if status == "disabled":
			self.ui.slaveControl_toolButton.setChecked(False)
			statusIcon.addPixmap(QtGui.QPixmap(":/rsc/rsc/status_icon_stopped.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.actionSlaveStart.setVisible(True)
			self.actionSlaveStop.setVisible(False)
			self.actionKillTask.setVisible(False)
			self.actionSlaveContinueAfterTask.setVisible(False)
			self.actionSlaveStopAfterTask.setVisible(False)
			self.actionSlaveContinueAfterTask.setChecked(True)  # Reset this option for the next time the slave is enabled

			self.ui.taskInfo_label.setText("")
			self.ui.runningTime_label.setText("")

		elif status == "idle":
			self.ui.slaveControl_toolButton.setChecked(True)
			statusIcon.addPixmap(QtGui.QPixmap(":/rsc/rsc/status_icon_ready.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.actionSlaveStart.setVisible(False)
			self.actionSlaveStop.setVisible(True)
			self.actionKillTask.setVisible(False)
			self.actionSlaveContinueAfterTask.setVisible(False)
			self.actionSlaveStopAfterTask.setVisible(False)

			self.ui.taskInfo_label.setText("")
			self.ui.runningTime_label.setText("")

		elif status == "rendering":
			self.ui.slaveControl_toolButton.setChecked(True)
			statusIcon.addPixmap(QtGui.QPixmap(":/rsc/rsc/status_icon_ok.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.actionSlaveStart.setVisible(False)
			self.actionSlaveStop.setVisible(False)
			self.actionKillTask.setVisible(True)
			self.actionSlaveContinueAfterTask.setVisible(True)
			self.actionSlaveStopAfterTask.setVisible(True)

			# self.ui.taskInfo_label.setText("Rendering %s %s from '%s'" %(verbose.pluralise("frame", len(frameList)), frames, self.rq.getValue(jobElement, 'name')))
			# self.ui.runningTime_label.setText(startTime)  # change this to display the task running time

		verbose.message("[%s] Local slave %s." %(self.localhost, self.slaveStatus))
		self.ui.slaveControl_toolButton.setText("%s (%s)" %(self.localhost, self.slaveStatus))
		self.ui.slaveControl_toolButton.setIcon(statusIcon)

		#self.updateSlaveView()


	def dequeue(self):
		""" Dequeue a render task from the queue and start rendering.
			THIS IS ALL A BIT ROPEY ATM
		"""
		if self.slaveStatus != "idle":
			return False
		#elif self.slaveStatus != "rendering":

		self.renderTaskInterrupted = False
		self.renderOutput = ""
		self.startTimeSec = time.time()  # Used for measuring the time spent rendering
		startTime = time.strftime(self.timeFormatStr)

		#self.rq.loadXML(quiet=True)  # Reload XML data - this is being done by the dequeuing function

		# Look for a suitable job to render - perhaps check here for a few
		# easy-to-detect errors, i.e. existence of scene, render command, etc.
		jobElement = self.rq.dequeueJob()
		if jobElement is None:
			verbose.message("[%s] No jobs to render." %self.localhost)
			return False
		self.renderJobID = jobElement.get('id')

		# Look for tasks to start rendering
		self.renderTaskID, frames = self.rq.dequeueTask(self.renderJobID, self.localhost)
		if not self.renderTaskID:
			verbose.message("[%s] Job ID %s: No tasks to render." %(self.localhost, self.renderJobID))
			return False

		verbose.message("[%s] Job ID %s, Task ID %s: Starting render..." %(self.localhost, self.renderJobID, self.renderTaskID))
		if frames == 'Unknown':
			frameList = frames
		else:
			frameList = sequence.numList(frames)
			startFrame = min(frameList)
			endFrame = max(frameList)


		jobType = self.rq.getValue(jobElement, 'type')
		if jobType == 'Maya':
			# try:
			# 	renderCmd = '"%s"' %os.environ['MAYARENDERVERSION'] # store this in XML as maya version may vary with project
			# except KeyError:
			# 	print "ERROR: Path to Maya Render command executable not found. This can be set with the environment variable 'MAYARENDERVERSION'."
			#renderCmd = '"%s"' %os.path.normpath(self.rq.getValue(jobElement, 'mayaRenderCmd'))
			renderCmd = self.rq.getValue(jobElement, 'mayaRenderCmd')
			# if not os.path.isfile(renderCmd): # disabled this check 
			# 	print "ERROR: Maya render command not found: %s" %renderCmd
			# 	return False

			sceneName = self.rq.getValue(jobElement, 'mayaScene')
			# if not os.path.isfile(sceneName): # check scene exists - disabled for now as could cause slave to get stuck in a loop
			# 	print "ERROR: Scene not found: %s" %sceneName
			# 	self.rq.requeueTask(self.renderJobID, self.renderTaskID)
			# 	#self.rq.setStatus(self.renderJobID, "Failed")
			# 	return False

			cmdStr = ''
			args = '-proj "%s"' %self.rq.getValue(jobElement, 'mayaProject')

			mayaFlags = self.rq.getValue(jobElement, 'mayaFlags')
			if mayaFlags is not None:
				args += ' %s' %mayaFlags

			# Construct command(s)
			if frames == 'Unknown':
				cmdStr = '"%s" %s "%s"' %(renderCmd, args, sceneName)
			else:
				cmdStr += '"%s" %s -s %d -e %d "%s"' %(renderCmd, args, int(startFrame), int(endFrame), sceneName)

		elif jobType == 'Nuke':
			renderCmd = self.rq.getValue(jobElement, 'nukeRenderCmd')
			scriptName = self.rq.getValue(jobElement, 'nukeScript')

			cmdStr = ''
			args = ''

			nukeFlags = self.rq.getValue(jobElement, 'nukeFlags')
			if nukeFlags is not None:
				args += ' %s' %nukeFlags

			# Construct command(s)
			if frames == 'Unknown':
				cmdStr = '"%s" %s -x "%s"' %(renderCmd, args, scriptName)
			else:
				cmdStr += '"%s" %s -F %s -x "%s"' %(renderCmd, args, frames, scriptName)


		# Set rendering status
#		verbose.print_(cmdStr, 4)

		# Fill info fields
		self.ui.taskInfo_label.setText("Rendering %s %s from '%s'" %(verbose.pluralise("frame", len(frameList)), frames, self.rq.getValue(jobElement, 'name')))
		#self.ui.runningTime_label.setText(startTime)  # change this to display the task running time
		self.ui.runningTime_label.setText( str(datetime.timedelta(seconds=0)) )

		self.setSlaveStatus("rendering")
		self.renderProcess.start(cmdStr)
		self.updateRenderQueueView()


	def updateTimers(self):
		""" Calculate elapsed time and update relevant UI fields.
		"""
		if self.slaveStatus == "rendering":
			elapsedTimeSec = time.time() - self.startTimeSec
			self.ui.runningTime_label.setText( str(datetime.timedelta(seconds=int(elapsedTimeSec))) )
			# this could also update the appropriate render queue tree widget item, if I can figure out how to do that


	def renderComplete(self):
		""" This code should only be executed after successful task
			completion.
		"""
		totalTimeSec = time.time() - self.startTimeSec  # Calculate time spent rendering task

		# self.ui.taskInfo_label.setText("")
		# self.ui.runningTime_label.setText("")
		if self.renderTaskInterrupted:
			self.rq.requeueTask(self.renderJobID, self.renderTaskID)  # perhaps set a special status to indicate render was killed, allowing the user to requeue manually?
		else:
			self.rq.completeTask(self.renderJobID, self.renderTaskID, self.localhost, taskTime=totalTimeSec)

		# Set slave status based on user option
		if self.actionSlaveStopAfterTask.isChecked():
			self.setSlaveStatus("disabled")
		else:
			self.setSlaveStatus("idle")
			self.dequeue()  # Dequeue next task immediately to prevent wait for next polling interval

		self.updateRenderQueueView()


	def killRenderProcess(self):
		""" Kill the rendering process. This will also stop the local slave.
		"""
		verbose.message("Attempting to kill process %s" %self.renderProcess)

		self.actionSlaveStopAfterTask.setChecked(True)  # This is a fudge to prevent the renderComplete function from re-enabling the slave after rendering task was killed by user
		self.renderTaskInterrupted = True

		if self.slaveStatus == "rendering":
			#self.renderProcess.terminate()
			self.renderProcess.kill()
		else:
			verbose.message("No render in progress.")

		#totalTimeSec = time.time() - self.startTimeSec  # Calculate time spent rendering task

		# self.ui.taskInfo_label.setText("")
		# self.ui.runningTime_label.setText("")
		#self.rq.completeTask(self.renderJobID, self.renderTaskID)
		#self.rq.requeueTask(self.renderJobID, self.renderTaskID)  # perhaps set a special status to indicate render was killed, allowing the user to requeue manually?

		#self.setSlaveStatus("disabled")

		#self.updateRenderQueueView()


	def showEvent(self, event):
		""" Event handler for when window is shown.
		"""
		# Create timers to refresh the view, dequeue tasks, and update elapsed
		# time readouts every n milliseconds
		self.timerUpdateView = QtCore.QTimer(self)
		self.timerUpdateView.timeout.connect(self.updateRenderQueueView)
		self.timerUpdateView.start(5000)

		self.timerDequeue = QtCore.QTimer(self)
		self.timerDequeue.timeout.connect(self.dequeue)
		self.timerDequeue.start(5000)  # Should only happen when slave is enabled

		self.timerUpdateTimer = QtCore.QTimer(self)
		self.timerUpdateTimer.timeout.connect(self.updateTimers)
		self.timerUpdateTimer.start(1000)

		self.updateRenderQueueView()
		#self.rebuildRenderQueueView()
		self.updateToolbarUI()


	def closeEvent(self, event):
		""" Event handler for when window is closed.
		"""

		# Confirmation dialog
		if self.slaveStatus == "rendering":
			import pDialog

			dialogTitle = 'Render in progress'
			dialogMsg = ''
			dialogMsg += 'There is currently a render in progress on the local slave. Closing the Render Queue window will also kill the render.\n'
			dialogMsg += 'Are you sure you want to quit?'

			dialog = pDialog.dialog()
			if dialog.display(dialogMsg, dialogTitle):
				event.accept()
			else:
				event.ignore()
				return

		self.killRenderProcess()

		# Stop timers
		self.timerUpdateView.stop()
		self.timerDequeue.stop()
		self.timerUpdateTimer.stop()

		# Store window geometry and state
		self.storeWindow()  # Store window geometry
		# # (Save state may cause issues with PyQt5)
		# try:
		# 	self.settings.setValue("geometry", self.saveGeometry())
		# 	self.settings.setValue("windowState", self.saveState())
		# except:
		# 	pass

		QtWidgets.QMainWindow.closeEvent(self, event)

# ----------------------------------------------------------------------------
# End of main application class
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# Run as standalone app
# ----------------------------------------------------------------------------

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)

	# Apply application style
	styles = QtWidgets.QStyleFactory.keys()
	if 'Fusion' in styles:  # Qt5
		app.setStyle('Fusion')
	elif 'Plastique' in styles:
		app.setStyle('Plastique')  # Qt4

	# Apply UI style sheet
	if STYLESHEET is not None:
		qss=os.path.join(os.environ['IC_FORMSDIR'], STYLESHEET)
		with open(qss, "r") as fh:
			app.setStyleSheet(fh.read())

	# Instantiate main application class
	rqApp = RenderQueueApp()

	# Set Window flags
	rqApp.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)

	# Show the application UI
	rqApp.show()
	sys.exit(app.exec_())

