#!/usr/bin/python

# [Icarus] Title source_filename.py
# v0.1
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2016 Gramercy Park Studios
#
# Description.


from PySide import QtCore, QtGui
from myDialog_ui import * # <- import your app's UI file (as generated by pyside-uic)
import os, sys

# Import custom modules


class dialog(QtGui.QDialog):

	def __init__(self, parent = None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
