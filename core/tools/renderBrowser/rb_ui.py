# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rb_ui.ui'
#
# Created: Mon Jan 18 15:54:41 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(720, 320)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.renderPblToolbar_frame = QtGui.QFrame(self.centralwidget)
        self.renderPblToolbar_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.renderPblToolbar_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.renderPblToolbar_frame.setObjectName("renderPblToolbar_frame")
        self.horizontalLayout_10 = QtGui.QHBoxLayout(self.renderPblToolbar_frame)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 6)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.renderPblAdd_pushButton = QtGui.QPushButton(self.renderPblToolbar_frame)
        self.renderPblAdd_pushButton.setDefault(False)
        self.renderPblAdd_pushButton.setFlat(False)
        self.renderPblAdd_pushButton.setObjectName("renderPblAdd_pushButton")
        self.horizontalLayout_10.addWidget(self.renderPblAdd_pushButton)
        self.renderPblRemove_pushButton = QtGui.QPushButton(self.renderPblToolbar_frame)
        self.renderPblRemove_pushButton.setDefault(False)
        self.renderPblRemove_pushButton.setFlat(False)
        self.renderPblRemove_pushButton.setObjectName("renderPblRemove_pushButton")
        self.horizontalLayout_10.addWidget(self.renderPblRemove_pushButton)
        self.renderPblSetMain_pushButton = QtGui.QPushButton(self.renderPblToolbar_frame)
        self.renderPblSetMain_pushButton.setEnabled(True)
        self.renderPblSetMain_pushButton.setCheckable(False)
        self.renderPblSetMain_pushButton.setDefault(False)
        self.renderPblSetMain_pushButton.setFlat(False)
        self.renderPblSetMain_pushButton.setObjectName("renderPblSetMain_pushButton")
        self.horizontalLayout_10.addWidget(self.renderPblSetMain_pushButton)
        self.renderPblRevert_pushButton = QtGui.QPushButton(self.renderPblToolbar_frame)
        self.renderPblRevert_pushButton.setEnabled(False)
        self.renderPblRevert_pushButton.setObjectName("renderPblRevert_pushButton")
        self.horizontalLayout_10.addWidget(self.renderPblRevert_pushButton)
        self.renderPreview_pushButton = QtGui.QPushButton(self.renderPblToolbar_frame)
        self.renderPreview_pushButton.setObjectName("renderPreview_pushButton")
        self.horizontalLayout_10.addWidget(self.renderPreview_pushButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem)
        self.streamPbl_checkBox = QtGui.QCheckBox(self.renderPblToolbar_frame)
        self.streamPbl_checkBox.setChecked(True)
        self.streamPbl_checkBox.setObjectName("streamPbl_checkBox")
        self.horizontalLayout_10.addWidget(self.streamPbl_checkBox)
        self.verticalLayout.addWidget(self.renderPblToolbar_frame)
        self.renderPbl_treeWidget = QtGui.QTreeWidget(self.centralwidget)
        self.renderPbl_treeWidget.setAlternatingRowColors(False)
        self.renderPbl_treeWidget.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.renderPbl_treeWidget.setUniformRowHeights(True)
        self.renderPbl_treeWidget.setAnimated(True)
        self.renderPbl_treeWidget.setHeaderHidden(False)
        self.renderPbl_treeWidget.setObjectName("renderPbl_treeWidget")
        self.verticalLayout.addWidget(self.renderPbl_treeWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Render Browser", None, QtGui.QApplication.UnicodeUTF8))
        self.renderPblAdd_pushButton.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.renderPblRemove_pushButton.setText(QtGui.QApplication.translate("MainWindow", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.renderPblSetMain_pushButton.setText(QtGui.QApplication.translate("MainWindow", "Set as Main", None, QtGui.QApplication.UnicodeUTF8))
        self.renderPblRevert_pushButton.setText(QtGui.QApplication.translate("MainWindow", "Revert", None, QtGui.QApplication.UnicodeUTF8))
        self.renderPreview_pushButton.setText(QtGui.QApplication.translate("MainWindow", "Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.streamPbl_checkBox.setText(QtGui.QApplication.translate("MainWindow", "Stream Publish", None, QtGui.QApplication.UnicodeUTF8))
        self.renderPbl_treeWidget.setSortingEnabled(False)
        self.renderPbl_treeWidget.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Layer / Pass", None, QtGui.QApplication.UnicodeUTF8))
        self.renderPbl_treeWidget.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "Frames", None, QtGui.QApplication.UnicodeUTF8))
        self.renderPbl_treeWidget.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.renderPbl_treeWidget.headerItem().setText(3, QtGui.QApplication.translate("MainWindow", "Path", None, QtGui.QApplication.UnicodeUTF8))

