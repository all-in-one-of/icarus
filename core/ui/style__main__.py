#!/usr/bin/python

# style__main__.py
# Template for PySide / Qt GUI application written in Python
#
# Directions for use:
# 
# Create your UI in Qt Designer and save as 'style.ui'
# Compile UI to Python with command: 'pyside-uic style.ui -o style_ui.py'
# 
# Save your resources file as 'style_rc.qrc'
# Compile resources to Python with command: 'pyside-rcc style.qrc -o style_rc.py'
# 
# Run with command: 'python style__main__.py'


import sys
from PySide import QtCore, QtGui
from style_ui import * # <- modify style_ui to name of your app's UI file (as generated by pyside-uic)


class testApp(QtGui.QMainWindow): # <- modify testApp to name of your app

	def __init__(self, parent = None):
		super(testApp, self).__init__() # <- modify testApp to name of your app
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

	# [application code goes here]


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	#app.setStyle('plastique') # Set UI style - you can also use a flag e.g. '-style plastique'

	qss="style.qss"
	with open(qss, "r") as fh:
		app.setStyleSheet(fh.read())

	myApp = testApp() # <- modify testApp to name of your app
	myApp.show()
	sys.exit(app.exec_())