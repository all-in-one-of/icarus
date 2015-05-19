# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_job_ui.ui'
#
# Created: Tue May 19 18:09:44 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_settings_frame(object):
    def setupUi(self, settings_frame):
        settings_frame.setObjectName("settings_frame")
        settings_frame.resize(400, 240)
        settings_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.formLayout = QtGui.QFormLayout(settings_frame)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.projnum_label = QtGui.QLabel(settings_frame)
        self.projnum_label.setObjectName("projnum_label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.projnum_label)
        self.projnum_spinBox = QtGui.QSpinBox(settings_frame)
        self.projnum_spinBox.setMinimum(0)
        self.projnum_spinBox.setMaximum(999999)
        self.projnum_spinBox.setProperty("value", 0)
        self.projnum_spinBox.setObjectName("projnum_spinBox")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.projnum_spinBox)
        self.jobnum_label = QtGui.QLabel(settings_frame)
        self.jobnum_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.jobnum_label.setObjectName("jobnum_label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.jobnum_label)
        self.jobnum_spinBox = QtGui.QSpinBox(settings_frame)
        self.jobnum_spinBox.setMinimum(0)
        self.jobnum_spinBox.setMaximum(9999999)
        self.jobnum_spinBox.setProperty("value", 0)
        self.jobnum_spinBox.setObjectName("jobnum_spinBox")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.jobnum_spinBox)
        self.client_label = QtGui.QLabel(settings_frame)
        self.client_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.client_label.setObjectName("client_label")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.client_label)
        self.client_lineEdit = QtGui.QLineEdit(settings_frame)
        self.client_lineEdit.setObjectName("client_lineEdit")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.client_lineEdit)
        self.brand_label = QtGui.QLabel(settings_frame)
        self.brand_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.brand_label.setObjectName("brand_label")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.brand_label)
        self.brand_lineEdit = QtGui.QLineEdit(settings_frame)
        self.brand_lineEdit.setObjectName("brand_lineEdit")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.brand_lineEdit)
        self.title_label = QtGui.QLabel(settings_frame)
        self.title_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.title_label.setObjectName("title_label")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.title_label)
        self.title_lineEdit = QtGui.QLineEdit(settings_frame)
        self.title_lineEdit.setObjectName("title_lineEdit")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.title_lineEdit)
        self.deliverable_label = QtGui.QLabel(settings_frame)
        self.deliverable_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.deliverable_label.setObjectName("deliverable_label")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.deliverable_label)
        self.deliverable_lineEdit = QtGui.QLineEdit(settings_frame)
        self.deliverable_lineEdit.setObjectName("deliverable_lineEdit")
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.deliverable_lineEdit)

        self.retranslateUi(settings_frame)
        QtCore.QMetaObject.connectSlotsByName(settings_frame)
        settings_frame.setTabOrder(self.projnum_spinBox, self.jobnum_spinBox)
        settings_frame.setTabOrder(self.jobnum_spinBox, self.client_lineEdit)
        settings_frame.setTabOrder(self.client_lineEdit, self.brand_lineEdit)
        settings_frame.setTabOrder(self.brand_lineEdit, self.title_lineEdit)
        settings_frame.setTabOrder(self.title_lineEdit, self.deliverable_lineEdit)

    def retranslateUi(self, settings_frame):
        settings_frame.setWindowTitle(QtGui.QApplication.translate("settings_frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.projnum_label.setText(QtGui.QApplication.translate("settings_frame", "Project number:", None, QtGui.QApplication.UnicodeUTF8))
        self.jobnum_label.setText(QtGui.QApplication.translate("settings_frame", "Job number:", None, QtGui.QApplication.UnicodeUTF8))
        self.client_label.setText(QtGui.QApplication.translate("settings_frame", "Client:", None, QtGui.QApplication.UnicodeUTF8))
        self.brand_label.setText(QtGui.QApplication.translate("settings_frame", "Brand:", None, QtGui.QApplication.UnicodeUTF8))
        self.title_label.setText(QtGui.QApplication.translate("settings_frame", "Title:", None, QtGui.QApplication.UnicodeUTF8))
        self.deliverable_label.setText(QtGui.QApplication.translate("settings_frame", "Deliverable:", None, QtGui.QApplication.UnicodeUTF8))

