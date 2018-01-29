#!/usr/bin/python

# [Icarus] rename__main__.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2016-2018 Gramercy Park Studios
#
# Batch Rename Tool
# A UI for batch renaming / renumbering of files and folders.
# TODO: Use unified dialog for Maya advanced rename tools.


import os
import re
import sys

# Initialise Icarus environment
# sys.path.append(os.environ['IC_WORKINGDIR'])
# import env__init__
# env__init__.setEnv()

# Use NSURL as a workaround to Pyside/Qt4 behaviour for dragging and dropping
# on OSX
if os.environ['IC_RUNNING_OS'] == 'Darwin':
	from Foundation import NSURL

from Qt import QtCore, QtGui, QtWidgets
import ui_template as UI

# Import custom modules
import osOps
import rename
import sequence
import verbose


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# Set window title and object names
WINDOW_TITLE = "Batch Rename"
WINDOW_OBJECT = "batchRenameUI"

# Set the UI and the stylesheet
UI_FILE = "rename_ui.ui"
STYLESHEET = "style.qss"  # Set to None to use the parent app's stylesheet

# Other options
STORE_WINDOW_GEOMETRY = True


# ----------------------------------------------------------------------------
# Main application class
# ----------------------------------------------------------------------------

class BatchRenameApp(QtWidgets.QMainWindow, UI.TemplateUI):
	""" Main application class.
	"""
	def __init__(self, parent=None):
		super(BatchRenameApp, self).__init__(parent)
		self.parent = parent

		xml_data = os.path.join(os.environ['IC_USERPREFS'], 'batchRename.xml')

		self.setupUI(window_object=WINDOW_OBJECT, 
					 window_title=WINDOW_TITLE, 
					 ui_file=UI_FILE, 
					 stylesheet=STYLESHEET, 
					 xml_data=xml_data, 
					 store_window_geometry=STORE_WINDOW_GEOMETRY)  # re-write as **kwargs ?

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Tool)

		# Set other Qt attributes
		#self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

		# Connect signals & slots
		# self.ui.find_lineEdit.textEdited.connect(self.updateTaskListView)
		# self.ui.replace_lineEdit.textEdited.connect(self.updateTaskListView)
		self.ui.find_comboBox.editTextChanged.connect(self.updateTaskListView)
		self.ui.replace_comboBox.editTextChanged.connect(self.updateTaskListView)
		self.ui.ignoreCase_checkBox.stateChanged.connect(self.updateTaskListView)
		self.ui.regex_checkBox.stateChanged.connect(self.updateTaskListView)

		self.ui.preserveNumbering_checkBox.stateChanged.connect(self.updateTaskListView)
		self.ui.start_spinBox.valueChanged.connect(self.updateTaskListView)
		self.ui.step_spinBox.valueChanged.connect(self.updateTaskListView)
		self.ui.autoPadding_checkBox.stateChanged.connect(self.updateTaskListView)
		self.ui.padding_spinBox.valueChanged.connect(self.updateTaskListView)

		self.ui.addDir_toolButton.clicked.connect(self.addDirectory)
		self.ui.addSeq_toolButton.clicked.connect(self.addSequence)
		self.ui.remove_toolButton.clicked.connect(self.removeSelection)
		self.ui.clear_toolButton.clicked.connect(self.clearTaskList)
		self.ui.rename_toolButton.clicked.connect(self.performFileRename)
		# self.ui.delete_pushButton.clicked.connect(self.performFileDelete)

		self.ui.taskList_treeWidget.itemDoubleClicked.connect(self.loadFindStr)

		# Set input validators
		alphanumeric_filename_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[\w\.-]+'), self.ui.replace_comboBox)
		self.ui.replace_comboBox.setValidator(alphanumeric_filename_validator)

		# self.ui.delete_pushButton.hide()  # Hide the delete button - too dangerous!

		self.renameTaskLs = []
		self.lastDir = None

		# Get current dir in which to rename files, and update render layer
		# tree view widget
		self.updateTaskListDir(os.getcwd())


	def folderDialog(self, dialogHome):
		""" Opens a dialog from which to select a directory to browse.
		"""
		dialog = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr('Directory'), dialogHome, 
				 QtWidgets.QFileDialog.DontResolveSymlinks | QtWidgets.QFileDialog.ShowDirsOnly)

		self.lastDir = os.path.dirname(dialog)
		if dialog:
			return osOps.absolutePath(dialog)
		else:
			return '.'


	def fileDialog(self, dialogHome):
		""" Opens a dialog from which to select a single file.
		"""
		dialog = QtWidgets.QFileDialog.getOpenFileName(self, self.tr('Files'), dialogHome, 'All files (*.*)')

		self.lastDir = os.path.dirname(dialog[0])
		return osOps.absolutePath(dialog[0])


	def getBrowseDir(self):
		""" Decide which directory to start browsing from.
		"""
		if self.lastDir:
			browseDir = self.lastDir
		elif os.environ.get('MAYARENDERSDIR') is not None:
			browseDir = os.environ['MAYARENDERSDIR']
		else:
			browseDir = os.getcwd()

		return browseDir


	def addDirectory(self):
		""" Scan a directory for sequences to be added to the task list.
		"""
		self.updateTaskListDir(self.folderDialog( self.getBrowseDir() ))


	def addSequence(self):
		""" Scan a directory for sequences to be added to the task list.
		"""
		self.updateTaskListFile(self.fileDialog( self.getBrowseDir() ))


	def removeSelection(self):
		""" Removes selected items from the task list.
		"""
		indices = []

		for item in self.ui.taskList_treeWidget.selectedItems():
			indices.append(self.ui.taskList_treeWidget.indexOfTopLevelItem(item))
		#	self.ui.taskList_treeWidget.takeTopLevelItem(index)

		indices.sort(reverse=True)  # Iterate over the list in reverse order to prevent the indices changing mid-operation

		for index in indices:
			#print("Deleting item at index %d" %index)
			del self.renameTaskLs[index]

		self.updateTaskListView()


	def clearTaskList(self):
		""" Clears the task list.
		"""
		self.renameTaskLs = []
		self.updateTaskListView()


	def updateTaskListDir(self, dirpath):
		""" Update task list with detected file sequences in given directory.
			Pre-existing tasks will not be added, to avoid duplication.
		"""
		bases = sequence.getBases(dirpath)

		for base in bases:
			path, prefix, fr_range, ext, num_frames = sequence.getSequence(dirpath, base)
			data = (path, prefix+'.', fr_range, ext, num_frames)
			if data not in self.renameTaskLs:
				self.renameTaskLs.append(data)

		self.updateTaskListView()


	def updateTaskListFile(self, filepath):
		""" Update task list with detected file sequence given a file path.
			Pre-existing tasks will not be added, to avoid duplication.
		"""
		if os.path.isfile(filepath):
			path, prefix, fr_range, ext, num_frames = sequence.detectSeq(filepath) #, ignorePadding=True)
			data = (path, prefix+'.', fr_range, ext, num_frames)
			if data not in self.renameTaskLs:
				self.renameTaskLs.append(data)

			self.updateTaskListView()


	def updateTaskListView(self):
		""" Populates the rename list tree view widget with entries.
		"""
		renameCount = 0
		totalCount = 0

		# Get find & replace options
		findStr = self.ui.find_comboBox.currentText()
		replaceStr = self.ui.replace_comboBox.currentText()
		ignoreCase = self.getCheckBoxValue(self.ui.ignoreCase_checkBox)
		regex = self.getCheckBoxValue(self.ui.regex_checkBox)

		# Get renumbering options
		start = self.ui.start_spinBox.value()
		step = self.ui.step_spinBox.value()
		padding = self.ui.padding_spinBox.value()
		preserve = self.getCheckBoxValue(self.ui.preserveNumbering_checkBox)
		autopad = self.getCheckBoxValue(self.ui.autoPadding_checkBox)

		self.ui.taskList_treeWidget.clear()

		for task in self.renameTaskLs:
			path, prefix, fr_range, ext, num_frames = task

			# Add entries
			file = "%s[%s]%s" %(prefix, fr_range, ext)
			taskItem = QtWidgets.QTreeWidgetItem(self.ui.taskList_treeWidget)

			taskItem.setText(0, str(num_frames))
			taskItem.setText(1, file)

			renamedPrefix = rename.replaceTextRE(prefix, findStr, replaceStr, ignoreCase, regex)
			numLs = sequence.numList(fr_range)
			renumberedLs, padding = rename.renumber(numLs, start, step, padding, preserve, autopad)
			renumberedRange = sequence.numRange(renumberedLs, padding)
			renamedFile = "%s[%s]%s" %(renamedPrefix, renumberedRange, ext)
			taskItem.setText(2, renamedFile)

			if file == renamedFile: # set text colour to indicate status
				taskItem.setForeground(2, QtGui.QBrush(QtGui.QColor("#666")))
				#taskItem.setForeground(2, QtGui.QBrush(QtGui.QColor("#f92672")))
			else:
				renameCount += num_frames

			taskItem.setText(3, path)

			self.ui.taskList_treeWidget.addTopLevelItem(taskItem)
			#taskItem.setExpanded(True)

			totalCount += num_frames

		# Resize columns
		self.ui.taskList_treeWidget.resizeColumnToContents(0)
		self.ui.taskList_treeWidget.resizeColumnToContents(1)
		self.ui.taskList_treeWidget.resizeColumnToContents(2)
		self.ui.taskList_treeWidget.resizeColumnToContents(3)
		#self.ui.taskList_treeWidget.setColumnHidden(3, True)

		self.checkConflicts()

		# Update button text
		if renameCount:
			self.ui.rename_toolButton.setText("Rename %d Files" %renameCount)
			self.ui.rename_toolButton.setEnabled(True)
		else:
			self.ui.rename_toolButton.setText("Rename")
			self.ui.rename_toolButton.setEnabled(False)

		# if totalCount:
		# 	self.ui.delete_pushButton.setText("Delete %d Files" %totalCount)
		# 	self.ui.delete_pushButton.setEnabled(True)
		# else:
		# 	self.ui.delete_pushButton.setText("Delete")
		# 	self.ui.delete_pushButton.setEnabled(False)


	def checkConflicts(self):
		""" Checks renamed files for conflicts with existing files.
		"""
		#results = []
		children = []
		root = self.ui.taskList_treeWidget.invisibleRootItem()
		child_count = root.childCount()
		for i in range(child_count):
			children.append(root.child(i))

		for i, item1 in enumerate(children, 1):
			for item2 in children[i:]:
				if (item1.text(2) == item2.text(2)) and (item1.text(3) == item2.text(3)):
					verbose.warning("Rename conflict found. %s is not unique." %item1.text(2))
					item1.setBackground(2, QtGui.QBrush(QtGui.QColor("#f92672")))
					item1.setForeground(2, QtGui.QBrush(QtGui.QColor("#fff")))
					item2.setBackground(2, QtGui.QBrush(QtGui.QColor("#f92672")))
					item2.setForeground(2, QtGui.QBrush(QtGui.QColor("#fff")))


	def loadFindStr(self, item, column):
		""" Copies the selected file name prefix to the 'Find' text field when
			the item is double-clicked.
		"""
		index = self.ui.taskList_treeWidget.indexOfTopLevelItem(item)

		#text = item.text(1)
		text = self.renameTaskLs[index][1]

		# self.ui.find_lineEdit.setText(text)
		if self.ui.find_comboBox.findText(text) == -1:
			self.ui.find_comboBox.addItem(text)
		self.ui.find_comboBox.setCurrentIndex(self.ui.find_comboBox.findText(text))
		self.updateTaskListView()


	def expandSeq(self, inputDir, inputFileSeq):
		""" Expand a filename sequence in the format 'name.[start-end].ext' to
			a list of individual frames.
			Return a list containing the full path to each file in the
			sequence.
		"""
		fileLs = []

		# Split filename and separate sequence numbering
		prefix, fr_range, ext = re.split(r'[\[\]]', inputFileSeq)
		padding = len( re.split(r'[-,\s]', fr_range)[-1] ) # detect padding
		numList = sequence.numList(fr_range)

		for i in numList:
			frame = str(i).zfill(padding)
			file = "%s%s%s" %(prefix, frame, ext)
			filePath = os.path.join(inputDir, file) #.replace("\\", "/")
			fileLs.append(filePath)

		return fileLs


	def performFileRename(self):
		""" Perform the file rename operation(s).
		"""
		newTaskLs = []

		root = self.ui.taskList_treeWidget.invisibleRootItem()
		child_count = root.childCount()

		for i in range(child_count):
			item = root.child(i)
			if not item.text(1) == item.text(2): # only rename if the operation will make any changes
				verbose.print_("Renaming '%s' to '%s' ..." %(item.text(1), item.text(2)),)
				src_fileLs = self.expandSeq(item.text(3), item.text(1))
				dst_fileLs = self.expandSeq(item.text(3), item.text(2))
				for j in range(len(src_fileLs)):
					osOps.rename( src_fileLs[j], dst_fileLs[j] )

				verbose.print_("Done")
				newTaskLs.append(dst_fileLs[j])

		verbose.print_("Batch rename job completed.\n")
		self.clearTaskList()

		# Update the task list to reflect the renamed files
		for newTask in newTaskLs:
			self.updateTaskListFile(newTask)


	def performFileDelete(self):
		""" Perform the file rename operation(s).
			TODO: confirmation dialog
		"""
		#QtWidgets.QMessageBox.about(self, 'Title','Message')
		root = self.ui.taskList_treeWidget.invisibleRootItem()
		child_count = root.childCount()

		for i in range(child_count):
			item = root.child(i)
			verbose.print_("Deleting '%s' ..." %item.text(1),)
			src_fileLs = self.expandSeq(item.text(3), item.text(1))
			for j in range(len(src_fileLs)):
				osOps.recurseRemove( src_fileLs[j] )

			verbose.print_("Done")

		verbose.print_("Batch deletion job completed.\n")
		self.clearTaskList()


	# The following three methods set up dragging and dropping for the app
	def dragEnterEvent(self, e):
		if e.mimeData().hasUrls:
			e.accept()
		else:
			e.ignore()

	def dragMoveEvent(self, e):
		if e.mimeData().hasUrls:
			e.accept()
		else:
			e.ignore()

	def dropEvent(self, e):
		"""
		Drop files directly onto the widget

		File locations are stored in fname
		:param e:
		:return:
		"""
		if e.mimeData().hasUrls:
			e.setDropAction(QtCore.Qt.CopyAction)
			e.accept()
			# Workaround for OSX dragging and dropping
			for url in e.mimeData().urls():
				if os.environ['IC_RUNNING_OS'] == 'Darwin':
					fname = str(NSURL.URLWithString_(str(url.toString())).filePathURL().path())
				else:
					fname = str(url.toLocalFile())

			#self.fname = fname
			verbose.print_("Dropped '%s' on to window." %fname)
			if os.path.isdir(fname):
				self.updateTaskListDir(fname)
			elif os.path.isfile(fname):
				self.updateTaskListFile(fname)
		else:
			e.ignore()


	def hideEvent(self, event):
		""" Event handler for when window is hidden.
		"""
		self.save()  # Save settings
		self.storeWindow()  # Store window geometry

# ----------------------------------------------------------------------------
# End of main application class
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# Run as standalone app
# ----------------------------------------------------------------------------

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)

	# Initialise Icarus environment
	sys.path.append(os.environ['IC_WORKINGDIR'])
	import env__init__
	env__init__.setEnv()
	#env__init__.appendSysPaths()

	import rsc_rc

	# Set UI style - you can also use a flag e.g. '-style plastique'
	#app.setStyle('fusion')

	# Apply UI style sheet
	if STYLESHEET is not None:
		qss=os.path.join(os.environ['ICWORKINGDIR'], STYLESHEET)
		with open(qss, "r") as fh:
			app.setStyleSheet(fh.read())

	myApp = BatchRenameApp()
	myApp.show()
	sys.exit(app.exec_())

# else:
# 	myApp = BatchRenameApp()
# 	print(myApp)
# 	myApp.show()

