#!/usr/bin/python

# [Icarus] about.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2017 Gramercy Park Studios
#
# Icarus About Dialog


# import sys
from Qt import QtCompat, QtCore, QtWidgets
import about_rc  # Import resource file as generated by pyside-rcc

# Set the UI and the stylesheet
UI_FILE = "about_ui.ui"


class aboutDialog(QtWidgets.QDialog):
	""" Main application class.
	"""
	def __init__(self, parent=None):
		super(aboutDialog, self).__init__(parent)

		# Load UI
		self.ui = QtCompat.load_ui(fname=UI_FILE)
		# print type(self.ui), type(self)

		# Connect signals & slots
		self.ui.close_toolButton.clicked.connect(self.ui.hide)


	def msg(self, msg):
		""" Display message in about dialog.
		"""
		self.ui.aboutMessage_label.setText(msg)
		self.ui.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)
		# self.ui.setWindowFlags(QtCore.Qt.SplashScreen | QtCore.Qt.WindowStaysOnTopHint)
		self.ui.show()
		self.ui.exec_()


	def mousePressEvent(self, QMouseEvent):
		""" Close about dialog if mouse is clicked. ***BROKEN - need to hit Esc to close***
		"""
		self.ui.hide()

