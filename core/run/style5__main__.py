#!/usr/bin/python

# style5__main__.py
# Template for PySide2 / Qt5 GUI application written in Python
#
# Directions for use:
# 
# Create your UI in Qt Designer and save as (e.g) 'style.ui'
# No need to compile your UI with pyside-uic as we now load the .ui file
# directly.
# 
# Save your resources file as (e.g.) 'style.qrc'
# Compile resources to with command: 'pyside-rcc style.qrc -o style_rc.py'
# For compatibility with PySide2, replace 'from [PySide/PyQt] import QtCore'
# with 'from Qt import QtCore'
# 
# Run with command: 'python ./style5__main__.py'


# If running as standalone app, initialise Icarus environment and add libs to
# sys path
if __name__ == "__main__":
	import env__init__
	env__init__.setEnv()

import os
import sys

from Qt import QtCompat, QtCore, QtGui, QtWidgets
import rsc_rc  # Import resource file as generated by pyside-rcc / pyrcc5

# Set the UI and the stylesheet
UI_FILE = "style_ui.ui"
STYLESHEET = "style.qss"  # Set to None to use the parent app's stylesheet


class TestApp(QtWidgets.QMainWindow):  # Replace 'TestApp' with the name of your app / Use 'QMainWindow' or 'QDialog' depending on the type of app
	""" Main application class.
	"""
	def __init__(self, parent=None):
		super(TestApp, self).__init__(parent)  # Replace 'TestApp' with the name of your app

		# Load UI
		self.ui = QtCompat.loadUi(os.path.join(os.environ['IC_FORMSDIR'], UI_FILE), self)
		if STYLESHEET is not None:
			qss=os.path.join(os.environ['IC_FORMSDIR'], STYLESHEET)
			with open(qss, "r") as fh:
				self.ui.setStyleSheet(fh.read())
		self.ui.show()

		self.info()

		# Connect signals & slots
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.exit)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.reloadStyleSheet)


	# [Application code goes here]


	def info(self):
		""" Return some version info about Python, Qt, binding, etc.
		"""
		from Qt import __binding__, __binding_version__

		print("Python %d.%d.%d" %(sys.version_info[0], sys.version_info[1], sys.version_info[2]))
		print("%s %s" %(__binding__, __binding_version__))
		print("Qt %s" %QtCore.qVersion())
		print(type(self.ui))


	def reloadStyleSheet(self):
		""" Reload stylesheet.
		"""
		if STYLESHEET is not None:
			qss=os.path.join(os.environ['IC_FORMSDIR'], STYLESHEET)
			with open(qss, "r") as fh:
				self.ui.setStyleSheet(fh.read())


	def exit(self):
		""" Exit the UI.
		"""
		print("Exit the UI.")
		self.ui.hide()
		if __name__ == "__main__":
			sys.exit()


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)

	myApp = TestApp()  # Replace 'TestApp' with the name of your app
	sys.exit(app.exec_())

else:
	myApp = TestApp()  # Replace 'TestApp' with the name of your app

