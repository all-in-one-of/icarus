#!/usr/bin/python

# ui_template.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2018-2019
#
# UI Template - a custom class to act as a template for all windows and
# dialogs.
# This module provides windowing / UI helper functions for better integration
# of PySide / PyQt UIs in supported DCC applications.
# Currently supports Maya and Nuke, and Houdini partially.


import json
import os
import platform
import re
import sys
import textwrap

from Qt import QtCompat, QtCore, QtGui, QtSvg, QtWidgets, __binding__, __binding_version__
import ui_chrome_rc  # Import resource file as generated by pyside-rcc

# Import custom modules
#import oswrapper


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# The vendor string must be set in order to store window geometry
VENDOR = "Gramercy Park Studios"


# ----------------------------------------------------------------------------
# Environment detection
# ----------------------------------------------------------------------------

ENVIRONMENT = os.environ.get('IC_ENV', "STANDALONE")

try:
	import maya.cmds as mc
	ENVIRONMENT = "MAYA"
except ImportError:
	pass

try:
	import hou
	ENVIRONMENT = "HOUDINI"
except ImportError:
	pass

try:
	import nuke
	import nukescripts
	ENVIRONMENT = "NUKE"
except ImportError:
	pass

# ----------------------------------------------------------------------------
# Settings data class
# ----------------------------------------------------------------------------

class SettingsData(object):
	def __init__(self, prefs_file):
		self.prefs_file = prefs_file
		self.prefs_dict = {}
		self.read()

	def read_new(self, prefs_file):
		self.prefs_file = prefs_file
		self.read()

	def read(self):
		try:
			with open(self.prefs_file, 'r') as f:
				self.prefs_dict = json.load(f)
		except:
			pass

	def write(self):
		try:
			with open(self.prefs_file, 'w') as f:
				json.dump(self.prefs_dict, f, indent=4, sort_keys=True)
			return True
		except:
			return False

	def getValue(self, category, attr, default=None):
		try:
			key = "%s.%s" %(category, attr)
			return self.prefs_dict[key]
		except KeyError:
			if default is not None:
				self.prefs_dict[key] = default  # Store default value
				return default
			else:
				return None

	def setValue(self, category, attr, value):
		key = "%s.%s" %(category, attr)
		self.prefs_dict[key] = value

# ----------------------------------------------------------------------------
# End of settings data class
# ============================================================================
# Main window class
# ----------------------------------------------------------------------------

class TemplateUI(object):
	""" Template UI class.

		Subclasses derived from this class need to also inherit QMainWindow or
		QDialog. This class has no __init__ constructor as a fudge to get
		around the idiosyncracies of multiple inheritance whilst retaining
		compatibility with both Python 2 and 3.
	"""
	#def setupUI(self, **cfg):
	def setupUI(
		self, 
		window_object, 
		window_title="", 
		ui_file="", 
		stylesheet="", 
		prefs_file=None, 
		store_window_geometry=True):
		""" Setup the UI.
		"""
		# Instantiate preferences data file
		self.prefs = SettingsData(prefs_file)

		# Load UI file
		self.ui = QtCompat.loadUi(self.checkFilePath(ui_file), self)

		# Store some system UI colours & define colour palette
		self.col = {}
		self.col['text'] = QtGui.QColor(204, 204, 204)
		self.col['disabled'] = QtGui.QColor(102, 102, 102)
		self.col['highlighted-text'] = QtGui.QColor(255, 255, 255)

		# Load and set stylesheet
		self.stylesheet = self.checkFilePath(stylesheet)
		self.loadStyleSheet()

		# Set window title
		self.setObjectName(window_object)
		if window_title:
			self.setWindowTitle(window_title)
		else:
			window_title = self.windowTitle()

		# Perform custom widget setup
		self.setupWidgets(self.ui)

		# Restore window geometry and state
		self.store_window_geometry = store_window_geometry
		if self.store_window_geometry:

			# Use QSettings to store window geometry and state.
			if ENVIRONMENT == 'STANDALONE':
				print("Restoring window geometry for '%s'." %self.objectName())
				try:
					self.settings = QtCore.QSettings(VENDOR, window_title)
					self.restoreGeometry(self.settings.value("geometry", ""))
				except:
					pass

			# Makes Maya perform magic which makes the window stay on top in
			# OS X and Linux. As an added bonus, it'll make Maya remember the
			# window position.
			elif ENVIRONMENT == 'MAYA':
				self.setProperty("saveWindowPref", True)

			elif ENVIRONMENT == 'NUKE':
				pass

		# Set up keyboard shortcuts
		self.shortcutUnloadStyleSheet = QtWidgets.QShortcut(self)
		self.shortcutUnloadStyleSheet.setKey('Ctrl+Shift+R')
		self.shortcutUnloadStyleSheet.activated.connect(self.unloadStyleSheet)

		self.shortcutReloadStyleSheet = QtWidgets.QShortcut(self)
		self.shortcutReloadStyleSheet.setKey('Ctrl+R')
		self.shortcutReloadStyleSheet.activated.connect(self.loadStyleSheet)


	def getInfo(self):
		""" Return some version info about Python, Qt, binding, etc.
		"""
		info = {}
		info['Python'] = "%d.%d.%d" %(sys.version_info[0], sys.version_info[1], sys.version_info[2])
		info[__binding__] = __binding_version__
		info['Qt'] = QtCore.qVersion()
		info['OS'] = platform.system()
		info['Environment'] = ENVIRONMENT

		return info


	def promptDialog(self, message, title="Message", infotext=None, conf=False, modal=True):
		""" Opens a message box dialog.
		"""
		message_box = QtWidgets.QMessageBox(parent=self)
		message_box.setWindowTitle(title)

		if infotext and infotext != '':
			text = "{}\n\n{}".format(message, "\n".join(textwrap.wrap(infotext, width=100)))
		else:
			text = message
		message_box.setText(text)

		if conf:
			message_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
		else:
			message_box.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
		message_box.setDefaultButton(QtWidgets.QMessageBox.Ok);

		if message_box.exec_() == message_box.Cancel:
			return False
		else:
			return True


	def fileDialog(self, startingDir, fileFilter='All files (*.*)'):
		""" Opens a dialog from which to select a single file.
		"""
		dialog = QtWidgets.QFileDialog.getOpenFileName(self, self.tr('Files'), startingDir, fileFilter)

		try:
			return dialog #[0]
		except IndexError:
			return None


	def folderDialog(self, startingDir):
		""" Opens a dialog from which to select a folder.
		"""
		dialog = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr('Directory'), startingDir, QtWidgets.QFileDialog.DontResolveSymlinks | QtWidgets.QFileDialog.ShowDirsOnly)

		return dialog


	def colorPickerDialog(self, current_color=None):
		""" Opens a system dialog for choosing a colour.
			Return the selected colour as a QColor object, or None if the
			dialog is cancelled.
		"""
		color_dialog = QtWidgets.QColorDialog()
		#color_dialog.setOption(QtWidgets.QColorDialog.DontUseNativeDialog)

		# Set current colour
		if current_color is not None:
			color_dialog.setCurrentColor(current_color)

		# Only return a color if valid / dialog accepted
		if color_dialog.exec_() == color_dialog.Accepted:
			color = color_dialog.selectedColor()
			return color


	# ------------------------------------------------------------------------
	# Widget handlers

	def setupWidgets(
		self, 
		parentObject, 
		forceCategory=None, 
		storeProperties=True, 
		updateOnly=False):
		""" Set up all the child widgets of the specified parent object.

			If 'forceCategory' is specified, this will override the category
			of all child widgets.
			If 'storeProperties' is True, the values will be stored in the XML
			data as well as applied to the widgets.
			If 'updateOnly' is True, only the widgets' values will be updated.
		"""
		if forceCategory is not None:
			category = forceCategory

		if updateOnly:
			storeProperties = False

		for widget in parentObject.findChildren(QtWidgets.QWidget):

			# Enable expansion of custom rollout group box controls...
			if widget.property('expandable'):
				if isinstance(widget, QtWidgets.QGroupBox):
					widget.setCheckable(True)
					# widget.setChecked(expand)
					widget.setFixedHeight(widget.sizeHint().height())
					if not updateOnly:
						widget.toggled.connect(self.toggleExpandGroup)

			# Set up handler for push buttons...
			if widget.property('exec'):
				if isinstance(widget, QtWidgets.QPushButton):
					if not updateOnly:
						widget.clicked.connect(self.execPushButton)

			# Set up handlers for different widget types & apply values
			attr = widget.property('xmlTag')
			if attr:
				self.base_widget = widget.objectName()
				if forceCategory is None:
					category = self.findCategory(widget)
				if category:
					widget.setProperty('xmlCategory', category)

					value = self.prefs.getValue(category, attr)

					# Sliders...
					if isinstance(widget, QtWidgets.QSlider):
						if value is not None:
							widget.setValue(int(value))
						if storeProperties:
							self.storeValue(category, attr, widget.value())
						if not updateOnly:
							widget.valueChanged.connect(self.storeSliderValue)

					# Spin boxes...
					if isinstance(widget, QtWidgets.QSpinBox):
						if value is not None:
							widget.setValue(int(value))
						if storeProperties:
							self.storeValue(category, attr, widget.value())
						if not updateOnly:
							widget.valueChanged.connect(self.storeSpinBoxValue)

					# Double spin boxes...
					elif isinstance(widget, QtWidgets.QDoubleSpinBox):
						if value is not None:
							widget.setValue(float(value))
						if storeProperties:
							self.storeValue(category, attr, widget.value())
						if not updateOnly:
							widget.valueChanged.connect(self.storeSpinBoxValue)

					# Line edits...
					elif isinstance(widget, QtWidgets.QLineEdit):
						if value is not None:
							widget.setText(value)
						if storeProperties:
							self.storeValue(category, attr, widget.text())
						if not updateOnly:
							# widget.textEdited.connect(self.storeLineEditValue)
							widget.textChanged.connect(self.storeLineEditValue)

					# Plain text edits...
					elif isinstance(widget, QtWidgets.QPlainTextEdit):
						if value is not None:
							widget.setPlainText(value)
						if storeProperties:
							self.storeValue(category, attr, widget.toPlainText())
						if not updateOnly:
							widget.textChanged.connect(self.storeTextEditValue)

					# Check boxes...
					elif isinstance(widget, QtWidgets.QCheckBox):
						if value is not None:
							if value == True:
								widget.setCheckState(QtCore.Qt.Checked)
							elif value == False:
								widget.setCheckState(QtCore.Qt.Unchecked)
						if storeProperties:
							self.storeValue(category, attr, self.getCheckBoxValue(widget))
						if not updateOnly:
							widget.toggled.connect(self.storeCheckBoxValue)

					# Radio buttons...
					elif isinstance(widget, QtWidgets.QRadioButton):
						if value is not None:
							widget.setAutoExclusive(False)
							if value == widget.text():
								widget.setChecked(True)
							else:
								widget.setChecked(False)
							widget.setAutoExclusive(True)
						if storeProperties:
							if widget.isChecked():
								self.storeValue(category, attr, widget.text())
						if not updateOnly:
							widget.toggled.connect(self.storeRadioButtonValue)

					# Combo boxes...
					elif isinstance(widget, QtWidgets.QComboBox):
						# Add items if history is enabled
						if widget.property('storeHistory'):
							widget.setInsertPolicy(widget.InsertAtTop)
							history = self.prefs.getValue(category, "%s_history" % attr)
							if history:
								widget.addItems(history)
						# Add/set current item
						if value is not None:
							if widget.findText(value) == -1:
								widget.insertItem(0, value)
							widget.setCurrentIndex(widget.findText(value))
						# Store value in external file
						if storeProperties:
							self.storeValue(category, attr, widget.currentText())
						# Connect signals & slots
						if not updateOnly:
							# widget.currentTextChanged.connect(self.storeComboBoxValue)
							if widget.isEditable():
								widget.editTextChanged.connect(self.storeComboBoxValue)
							else:
								widget.currentIndexChanged.connect(self.storeComboBoxValue)

					# Enable colour chooser buttons...
					elif isinstance(widget, QtWidgets.QToolButton):
						if widget.property('colorChooser'):
							if value is not None:
								widget.setStyleSheet("QWidget { background-color: %s }" % value)
							# if storeProperties:
							# 	self.storeValue(category, attr, widget.currentText())
							if not updateOnly:
								widget.clicked.connect(self.storeColor)


	def findCategory(self, widget):
		""" Recursively check the parents of the given widget until a custom
			property 'xmlCategory' is found.
		"""
		if widget.property('xmlCategory'):
			#print("Category '%s' found for '%s'." %(widget.property('xmlCategory'), widget.objectName()))
			return widget.property('xmlCategory')
		else:
			# Stop iterating if the widget's parent in the main window...
			if isinstance(widget.parent(), QtWidgets.QMainWindow):
				#print("No category could be found for '%s'. The widget's value cannot be stored." %self.base_widget)
				return None
			else:
				return self.findCategory(widget.parent())


	def addContextMenu(self, widget, name, command, icon=None):
		""" Add context menu item to widget.

			'widget' should be a Push Button or Tool Button.
			'name' is the text to be displayed in the menu.
			'command' is the function to run when the item is triggered.
			'icon' is a pixmap to use for the item's icon (optional).
		"""
		widget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		actionName = "action%s" %re.sub(r"[^\w]", "_", name)

		action = QtWidgets.QAction(name, None)
		if icon:
			action.setIcon(self.iconSet(icon))
		action.setObjectName(actionName)
		action.triggered.connect(command)
		widget.addAction(action)

		# Make a class-scope reference to this object
		# (won't work without it for some reason)
		exec_str = "self.%s = action" %actionName
		exec(exec_str)


	def iconSet(self, icon_name, tintNormal=True):
		""" Return a QIcon using the specified image.
			Generate tinted pixmaps for normal/disabled/active/selected
			states.
			tintNormal (bool): whether to tint the normal state icon or leave
			it as-is.
		"""
		icon = QtGui.QIcon()
		if tintNormal:
			icon.addPixmap(self.iconTint(icon_name, self.col['text']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		else:
			icon.addPixmap(self.iconTint(icon_name), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		icon.addPixmap(self.iconTint(icon_name, self.col['disabled']), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
		icon.addPixmap(self.iconTint(icon_name, self.col['highlighted-text']), QtGui.QIcon.Active, QtGui.QIcon.Off)
		icon.addPixmap(self.iconTint(icon_name, self.col['highlighted-text']), QtGui.QIcon.Selected, QtGui.QIcon.Off)
		return icon


	def iconTint(self, icon_name, tint=None):
		""" Return a QIcon using the specified PNG image.
			If tint (QColor) is given, tint the image with the given color.
		"""
		if icon_name.endswith('svg'):
			w, h = 64, 64
			svg_renderer = QtSvg.QSvgRenderer(self.checkFilePath('icons/%s' %icon_name))
			image = QtGui.QImage(w, h, QtGui.QImage.Format_ARGB32)
			image.fill(0x00000000)  # Set the ARGB to 0 to prevent rendering artifacts
			svg_renderer.render(QtGui.QPainter(image))
			pixmap = QtGui.QPixmap.fromImage(image)
		else:
			pixmap = QtGui.QPixmap(self.checkFilePath('icons/%s' %icon_name))

		# Initialize painter to draw on a pixmap and set composition mode
		if tint is not None:
			painter = QtGui.QPainter()
			painter.begin(pixmap)
			painter.setCompositionMode(painter.CompositionMode_SourceIn)
			painter.setBrush(tint)
			painter.setPen(tint)
			painter.drawRect(pixmap.rect())
			painter.end()

		return pixmap


	def conformFormLayoutLabels(self, parentObject, padding=8):
		""" Conform the widths of all labels in formLayouts under the
			specified parentObject for a more coherent appearance.

			'padding' is an amount in pixels to add to the max width.
		"""
		labels = []
		labelWidths = []

		# Find all labels in form layouts
		for layout in parentObject.findChildren(QtWidgets.QFormLayout):
			# print(layout.objectName())
			items = (layout.itemAt(i) for i in range(layout.count()))
			for item in items:
				widget = item.widget()
				if isinstance(widget, QtWidgets.QLabel):
					labels.append(widget)

		# Find labels in first column of grid layouts
		for layout in parentObject.findChildren(QtWidgets.QGridLayout):
			# print(layout.objectName())
			items = (layout.itemAt(i) for i in range(layout.count()))
			for item in items:
				widget = item.widget()
				if isinstance(widget, QtWidgets.QLabel):
					# Only items in first column (there's probably a neater
					# way to do this)
					if layout.getItemPosition(layout.indexOf(widget))[1] == 0:
						labels.append(widget)

		# Find label widths
		for label in labels:
			fontMetrics = QtGui.QFontMetrics(label.font())
			width = fontMetrics.width(label.text())
			#print('Width of "%s": %d px' %(label.text(), width))
			labelWidths.append(width)

		# Get widest label & set all labels widths to match
		if labelWidths:
			maxWidth = max(labelWidths)
			#print("Max label width : %d px (%d inc padding)" %(maxWidth, maxWidth+padding))
			for label in labels:
				label.setFixedWidth(maxWidth+padding)
				label.setAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignRight)
				label.setProperty('formLabel', True)  # Set custom property for styling


	def toggleFormField(self, parentObject, field, enabled):
		""" Enable/disable a field in a form layout including its label.
		"""
		layout = parentObject.findChildren(QtWidgets.QFormLayout)[0]
		label = layout.labelForField(field)

		field.setEnabled(enabled)
		label.setEnabled(enabled)


	def hideFormField(self, parentObject, field):
		""" Hide a field in a form layout including its label, and close up
			the remaining empty space.
		"""
		layout = parentObject.findChildren(QtWidgets.QFormLayout)[0]
		label = layout.labelForField(field)

		field.hide()
		label.hide()
		layout.removeWidget(field)
		layout.removeWidget(label)

		parentObject.toggled.emit(True)  # Force refresh


	def getCheckBoxValue(self, checkBox):
		""" Get the value from a checkbox and return a Boolean value.
		"""
		if checkBox.checkState() == QtCore.Qt.Checked:
			return True
		else:
			return False


	def getWidgetMeta(self, widget):
		""" 
		"""
		category = widget.property('xmlCategory')
		attr = widget.property('xmlTag')
		return category, attr


	# @QtCore.Slot()
	def execPushButton(self):
		""" Execute the function associated with a button.
			***NOT YET IMPLEMENTED***
		"""
		print("%s %s" %(self.sender().objectName(), self.sender().property('exec')))


	# @QtCore.Slot()
	def storeColor(self):
		""" Get the colour from a dialog opened from a colour chooser button.
		"""
		widget = self.sender()

		# Get current colour and pass to function
		current_color = widget.palette().color(QtGui.QPalette.Background)
		color = self.colorPickerDialog(current_color)
		if color:
			widget.setStyleSheet("QWidget { background-color: %s }" %color.name())
			category, attr = self.getWidgetMeta(self.sender())
			self.storeValue(category, attr, color.name())


	# @QtCore.Slot()
	def storeSliderValue(self):
		""" Get the value from a Slider and store in XML data.
		"""
		category, attr = self.getWidgetMeta(self.sender())
		value = self.sender().value()
		self.storeValue(category, attr, value)


	# @QtCore.Slot()
	def storeSpinBoxValue(self):
		""" Get the value from a Spin Box and store in XML data.
		"""
		category, attr = self.getWidgetMeta(self.sender())
		value = self.sender().value()
		self.storeValue(category, attr, value)


	# @QtCore.Slot()
	def storeLineEditValue(self):
		""" Get the value from a Line Edit and store in XML data.
		"""
		category, attr = self.getWidgetMeta(self.sender())
		value = self.sender().text()
		self.storeValue(category, attr, value)


	# @QtCore.Slot()
	def storeTextEditValue(self):
		""" Get the value from a Plain Text Edit and store in XML data.
		"""
		category, attr = self.getWidgetMeta(self.sender())
		value = self.sender().toPlainText()
		self.storeValue(category, attr, value)


	# @QtCore.Slot()
	def storeCheckBoxValue(self):
		""" Get the value from a Check Box and store in XML data.
		"""
		category, attr = self.getWidgetMeta(self.sender())
		value = self.getCheckBoxValue(self.sender())
		self.storeValue(category, attr, value)


	# @QtCore.Slot()
	def storeRadioButtonValue(self):
		""" Get the value from a Radio Button group and store in XML data.
		"""
		if self.sender().isChecked():
			category, attr = self.getWidgetMeta(self.sender())
			value = self.sender().text()
			self.storeValue(category, attr, value)


	# @QtCore.Slot()
	def storeComboBoxValue(self):
		""" Get the value from a Combo Box and store in XML data.
		"""
		category, attr = self.getWidgetMeta(self.sender())
		value = self.sender().currentText()
		self.storeValue(category, attr, value)

		# Store combo box history
		if self.sender().property('storeHistory'):
			max_count = self.sender().maxCount()
			self.sender().setMaxCount(max_count-1)
			self.sender().setMaxCount(max_count)
			items = [self.sender().itemText(i) for i in range(self.sender().count())]
			self.storeValue(category, "%s_history" % attr, items)


	def storeValue(self, category, attr, value=""):
		""" Store value in XML data.
		"""
		#print("%20s %s.%s=%s" % (type(value), category, attr, value))
		self.prefs.setValue(category, attr, value)


	# @QtCore.Slot()
	def toggleExpandGroup(self):
		""" Toggle expansion of custom rollout group box control.
		"""
		groupBox = self.sender()
		state = groupBox.isChecked()
		if state:
			groupBox.setFixedHeight(groupBox.sizeHint().height())
		else:
			groupBox.setFixedHeight(20)  # Slightly hacky - needs to match value defined in QSS

		#self.setFixedHeight(self.sizeHint().height())  # Resize window


	def populateComboBox(self, comboBox, contents, replace=True, addEmptyItems=False):
		""" Use a list (contents) to populate a combo box.
			If 'replace' is true, the existing items will be replaced,
			otherwise the contents will be appended to the existing items.
		"""
		# Store current value
		current = comboBox.currentText()

		# Clear menu
		if replace:
			comboBox.clear()

		# Populate menu
		if contents:
			for item in contents:
				if addEmptyItems:
					comboBox.addItem(item)
				else:
					if item:
						comboBox.addItem(item)

		# Set to current value
		index = comboBox.findText(current)
		if index == -1:
			comboBox.setCurrentIndex(0)
		else:
			comboBox.setCurrentIndex(index)

	# End widget handlers
	# ------------------------------------------------------------------------


	def checkFilePath(self, filename, searchpath=[]):
		""" Check if 'filename' exists. If not, search through list of folders
			given in the optional searchpath, then check in the current dir.
		"""
		if filename is None:
			return None
		if os.path.isfile(filename):
			return filename
		else:
			# Append current dir to searchpath and try each in turn
			searchpath.append(os.path.dirname(__file__))
			for folder in searchpath:
				filepath = os.path.join(folder, filename)
				if os.path.isfile(filepath):
					return filepath

			# File not found
			return None


	def loadStyleSheet(self):
		""" Load/reload stylesheet.
		"""
		if self.stylesheet:
			with open(self.stylesheet, 'r') as fh:
				stylesheet = fh.read()

			self.setStyleSheet(stylesheet)
			return stylesheet


	def unloadStyleSheet(self):
		""" Unload stylesheet.
		"""
		self.setStyleSheet("")


	def storeWindow(self):
		""" Store window geometry.
		"""
		if ENVIRONMENT == 'STANDALONE':
			if self.store_window_geometry:
				print("Storing window geometry for '%s'." %self.objectName())
				try:
					self.settings.setValue("geometry", self.saveGeometry())
				except:
					pass


	# def showEvent(self, event):
	# 	""" Event handler for when window is shown.
	# 	"""
	# 	pass


	# def closeEvent(self, event):
	# 	""" Event handler for when window is closed.
	# 	"""
	# 	self.storeWindow()
	# 	QtWidgets.QMainWindow.closeEvent(self, event)
	# 	#self.closeEvent(self, event)


	def save(self):
		""" Save data.
		"""
		if self.prefs.write():
			return True
		else:
			return False


	# def saveAndExit(self):
	# 	""" Save data and close window.
	# 	"""
	# 	if self.save():
	# 		self.returnValue = True
	# 		self.hide()
	# 		self.ui.hide()
	# 		#self.exit()
	# 	else:
	# 		self.exit()


	# def exit(self):
	# 	""" Exit the window with negative return value.
	# 	"""
	# 	self.storeWindow()
	# 	#self.returnValue = False
	# 	self.hide()

# ----------------------------------------------------------------------------
# End of main window class
# ============================================================================
# DCC application helper functions
# ----------------------------------------------------------------------------

########
# MAYA #
########

def _maya_main_window():
	""" Return Maya's main window.
	"""
	for obj in QtWidgets.QApplication.topLevelWidgets():
		if obj.objectName() == 'MayaWindow':
			return obj
	raise RuntimeError("Could not find MayaWindow instance")


def _maya_delete_ui(window_object, window_title):
	""" Delete existing UI in Maya.
	"""
	if mc.window(window_object, query=True, exists=True):
		mc.deleteUI(window_object)  # Delete window
	if mc.dockControl('MayaWindow|' + window_title, query=True, exists=True):
		mc.deleteUI('MayaWindow|' + window_title)  # Delete docked window


###########
# HOUDINI #
###########

def _houdini_get_session():
	return hou.session


def _houdini_main_window():
	""" Return Houdini's main window.
	"""
	return hou.qt.mainWindow()
	raise RuntimeError("Could not find Houdini's main window instance")


# def _houdini_delete_ui(window_object, window_title):
# 	""" Delete existing UI in Houdini.
# 	"""
# 	pass


########
# NUKE #
########

def _nuke_main_window():
	""" Returns Nuke's main window.
	"""
	for obj in QtWidgets.QApplication.topLevelWidgets():
		if (obj.inherits('QMainWindow') and obj.metaObject().className() == 'Foundry::UI::DockMainWindow'):
			return obj
	raise RuntimeError("Could not find DockMainWindow instance")


def _nuke_delete_ui(window_object, window_title):
	""" Delete existing UI in Nuke.
	"""
	for obj in QtWidgets.QApplication.allWidgets():
		if obj.objectName() == window_object:
			obj.deleteLater()


def _nuke_set_zero_margins(widget_object):
	""" Remove Nuke margins when docked UI.
		More info:
		https://gist.github.com/maty974/4739917
	"""
	parentApp = QtWidgets.QApplication.allWidgets()
	parentWidgetList = []
	for parent in parentApp:
		for child in parent.children():
			if widget_object.__class__.__name__ == child.__class__.__name__:
				parentWidgetList.append(parent.parentWidget())
				parentWidgetList.append(parent.parentWidget().parentWidget())
				parentWidgetList.append(parent.parentWidget().parentWidget().parentWidget())

				for sub in parentWidgetList:
					for tinychild in sub.children():
						try:
							tinychild.setContentsMargins(0, 0, 0, 0)
						except:
							pass
