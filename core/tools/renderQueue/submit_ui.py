# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'submit_ui.ui'
#
# Created: Wed Jul 06 15:09:38 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(512, 320)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.main_frame = QtGui.QFrame(Dialog)
        self.main_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.main_frame.setFrameShadow(QtGui.QFrame.Plain)
        self.main_frame.setLineWidth(0)
        self.main_frame.setObjectName("main_frame")
        self.verticalLayout = QtGui.QVBoxLayout(self.main_frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.basic_formLayout = QtGui.QFormLayout()
        self.basic_formLayout.setObjectName("basic_formLayout")
        self.scene_label = QtGui.QLabel(self.main_frame)
        self.scene_label.setObjectName("scene_label")
        self.basic_formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.scene_label)
        self.type_label = QtGui.QLabel(self.main_frame)
        self.type_label.setObjectName("type_label")
        self.basic_formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.type_label)
        self.scene_horizontalLayout = QtGui.QHBoxLayout()
        self.scene_horizontalLayout.setObjectName("scene_horizontalLayout")
        self.scene_comboBox = QtGui.QComboBox(self.main_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scene_comboBox.sizePolicy().hasHeightForWidth())
        self.scene_comboBox.setSizePolicy(sizePolicy)
        self.scene_comboBox.setEditable(False)
        self.scene_comboBox.setMaxCount(10)
        self.scene_comboBox.setInsertPolicy(QtGui.QComboBox.InsertAtTop)
        self.scene_comboBox.setObjectName("scene_comboBox")
        self.scene_horizontalLayout.addWidget(self.scene_comboBox)
        self.sceneBrowse_toolButton = QtGui.QToolButton(self.main_frame)
        self.sceneBrowse_toolButton.setObjectName("sceneBrowse_toolButton")
        self.scene_horizontalLayout.addWidget(self.sceneBrowse_toolButton)
        self.basic_formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.scene_horizontalLayout)
        self.type_horizontalLayout = QtGui.QHBoxLayout()
        self.type_horizontalLayout.setObjectName("type_horizontalLayout")
        self.type_comboBox = QtGui.QComboBox(self.main_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.type_comboBox.sizePolicy().hasHeightForWidth())
        self.type_comboBox.setSizePolicy(sizePolicy)
        self.type_comboBox.setObjectName("type_comboBox")
        self.type_comboBox.addItem("")
        self.type_comboBox.addItem("")
        self.type_horizontalLayout.addWidget(self.type_comboBox)
        self.basic_formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.type_horizontalLayout)
        self.verticalLayout.addLayout(self.basic_formLayout)
        self.line = QtGui.QFrame(self.main_frame)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.overrideFrameRange_groupBox = QtGui.QGroupBox(self.main_frame)
        self.overrideFrameRange_groupBox.setCheckable(True)
        self.overrideFrameRange_groupBox.setObjectName("overrideFrameRange_groupBox")
        self.formLayout = QtGui.QFormLayout(self.overrideFrameRange_groupBox)
        self.formLayout.setObjectName("formLayout")
        self.taskSize_label = QtGui.QLabel(self.overrideFrameRange_groupBox)
        self.taskSize_label.setObjectName("taskSize_label")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.taskSize_label)
        self.frameRange_label = QtGui.QLabel(self.overrideFrameRange_groupBox)
        self.frameRange_label.setObjectName("frameRange_label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.frameRange_label)
        self.frameRange_lineEdit = QtGui.QLineEdit(self.overrideFrameRange_groupBox)
        self.frameRange_lineEdit.setText("")
        self.frameRange_lineEdit.setObjectName("frameRange_lineEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.frameRange_lineEdit)
        self.taskSize_horizontalLayout = QtGui.QHBoxLayout()
        self.taskSize_horizontalLayout.setObjectName("taskSize_horizontalLayout")
        self.taskSize_spinBox = QtGui.QSpinBox(self.overrideFrameRange_groupBox)
        self.taskSize_spinBox.setMinimum(1)
        self.taskSize_spinBox.setMaximum(9999)
        self.taskSize_spinBox.setObjectName("taskSize_spinBox")
        self.taskSize_horizontalLayout.addWidget(self.taskSize_spinBox)
        self.taskSize_slider = QtGui.QSlider(self.overrideFrameRange_groupBox)
        self.taskSize_slider.setMinimum(1)
        self.taskSize_slider.setMaximum(100)
        self.taskSize_slider.setProperty("value", 1)
        self.taskSize_slider.setOrientation(QtCore.Qt.Horizontal)
        self.taskSize_slider.setTickPosition(QtGui.QSlider.NoTicks)
        self.taskSize_slider.setTickInterval(10)
        self.taskSize_slider.setObjectName("taskSize_slider")
        self.taskSize_horizontalLayout.addWidget(self.taskSize_slider)
        self.formLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.taskSize_horizontalLayout)
        self.verticalLayout.addWidget(self.overrideFrameRange_groupBox)
        self.flags_groupBox = QtGui.QGroupBox(self.main_frame)
        self.flags_groupBox.setCheckable(True)
        self.flags_groupBox.setChecked(False)
        self.flags_groupBox.setObjectName("flags_groupBox")
        self.formLayout_2 = QtGui.QFormLayout(self.flags_groupBox)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.flags_lineEdit = QtGui.QLineEdit(self.flags_groupBox)
        self.flags_lineEdit.setText("")
        self.flags_lineEdit.setObjectName("flags_lineEdit")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.flags_lineEdit)
        self.verticalLayout.addWidget(self.flags_groupBox)
        self.submit_groupBox = QtGui.QGroupBox(self.main_frame)
        self.submit_groupBox.setObjectName("submit_groupBox")
        self.formLayout_3 = QtGui.QFormLayout(self.submit_groupBox)
        self.formLayout_3.setObjectName("formLayout_3")
        self.priority_label = QtGui.QLabel(self.submit_groupBox)
        self.priority_label.setObjectName("priority_label")
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.priority_label)
        self.priority_horizontalLayout = QtGui.QHBoxLayout()
        self.priority_horizontalLayout.setObjectName("priority_horizontalLayout")
        self.priority_spinBox = QtGui.QSpinBox(self.submit_groupBox)
        self.priority_spinBox.setMinimum(0)
        self.priority_spinBox.setMaximum(100)
        self.priority_spinBox.setProperty("value", 50)
        self.priority_spinBox.setObjectName("priority_spinBox")
        self.priority_horizontalLayout.addWidget(self.priority_spinBox)
        self.priority_slider = QtGui.QSlider(self.submit_groupBox)
        self.priority_slider.setMinimum(0)
        self.priority_slider.setMaximum(100)
        self.priority_slider.setProperty("value", 50)
        self.priority_slider.setOrientation(QtCore.Qt.Horizontal)
        self.priority_slider.setTickPosition(QtGui.QSlider.NoTicks)
        self.priority_slider.setTickInterval(10)
        self.priority_slider.setObjectName("priority_slider")
        self.priority_horizontalLayout.addWidget(self.priority_slider)
        self.formLayout_3.setLayout(0, QtGui.QFormLayout.FieldRole, self.priority_horizontalLayout)
        self.verticalLayout.addWidget(self.submit_groupBox)
        self.verticalLayout_2.addWidget(self.main_frame)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.buttonBox_horizontalLayout = QtGui.QHBoxLayout()
        self.buttonBox_horizontalLayout.setObjectName("buttonBox_horizontalLayout")
        self.submit_pushButton = QtGui.QPushButton(Dialog)
        self.submit_pushButton.setAutoDefault(False)
        self.submit_pushButton.setObjectName("submit_pushButton")
        self.buttonBox_horizontalLayout.addWidget(self.submit_pushButton)
        self.close_pushButton = QtGui.QPushButton(Dialog)
        self.close_pushButton.setAutoDefault(False)
        self.close_pushButton.setObjectName("close_pushButton")
        self.buttonBox_horizontalLayout.addWidget(self.close_pushButton)
        self.verticalLayout_2.addLayout(self.buttonBox_horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.priority_spinBox, QtCore.SIGNAL("valueChanged(int)"), self.priority_slider.setValue)
        QtCore.QObject.connect(self.priority_slider, QtCore.SIGNAL("valueChanged(int)"), self.priority_spinBox.setValue)
        QtCore.QObject.connect(self.taskSize_spinBox, QtCore.SIGNAL("valueChanged(int)"), self.taskSize_slider.setValue)
        QtCore.QObject.connect(self.taskSize_slider, QtCore.SIGNAL("valueChanged(int)"), self.taskSize_spinBox.setValue)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.submit_pushButton, self.close_pushButton)
        Dialog.setTabOrder(self.close_pushButton, self.overrideFrameRange_groupBox)
        Dialog.setTabOrder(self.overrideFrameRange_groupBox, self.frameRange_lineEdit)
        Dialog.setTabOrder(self.frameRange_lineEdit, self.taskSize_spinBox)
        Dialog.setTabOrder(self.taskSize_spinBox, self.taskSize_slider)
        Dialog.setTabOrder(self.taskSize_slider, self.flags_groupBox)
        Dialog.setTabOrder(self.flags_groupBox, self.flags_lineEdit)
        Dialog.setTabOrder(self.flags_lineEdit, self.priority_spinBox)
        Dialog.setTabOrder(self.priority_spinBox, self.priority_slider)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Submit Render", None, QtGui.QApplication.UnicodeUTF8))
        self.scene_label.setText(QtGui.QApplication.translate("Dialog", "Scene:", None, QtGui.QApplication.UnicodeUTF8))
        self.type_label.setText(QtGui.QApplication.translate("Dialog", "Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.sceneBrowse_toolButton.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.type_comboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "Maya", None, QtGui.QApplication.UnicodeUTF8))
        self.type_comboBox.setItemText(1, QtGui.QApplication.translate("Dialog", "Nuke", None, QtGui.QApplication.UnicodeUTF8))
        self.overrideFrameRange_groupBox.setToolTip(QtGui.QApplication.translate("Dialog", "Allows the frame range(s) to be explicitly stated. If unchecked, the start and end frames will be read from the scene.", None, QtGui.QApplication.UnicodeUTF8))
        self.overrideFrameRange_groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Override frame range", None, QtGui.QApplication.UnicodeUTF8))
        self.taskSize_label.setText(QtGui.QApplication.translate("Dialog", "Task size:", None, QtGui.QApplication.UnicodeUTF8))
        self.frameRange_label.setText(QtGui.QApplication.translate("Dialog", "Frames:", None, QtGui.QApplication.UnicodeUTF8))
        self.frameRange_lineEdit.setToolTip(QtGui.QApplication.translate("Dialog", "List of frames to be rendered. Individual frames should be separated with commas, and sequences can be specified using a hyphen, e.g. 1, 5-10.", None, QtGui.QApplication.UnicodeUTF8))
        self.taskSize_spinBox.setToolTip(QtGui.QApplication.translate("Dialog", "How many frames to submit for each task.", None, QtGui.QApplication.UnicodeUTF8))
        self.taskSize_spinBox.setSuffix(QtGui.QApplication.translate("Dialog", " frame(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.flags_groupBox.setToolTip(QtGui.QApplication.translate("Dialog", "Allows additional command-line flags to be specified.", None, QtGui.QApplication.UnicodeUTF8))
        self.flags_groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Additional command-line flags", None, QtGui.QApplication.UnicodeUTF8))
        self.submit_groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Submission options", None, QtGui.QApplication.UnicodeUTF8))
        self.priority_label.setText(QtGui.QApplication.translate("Dialog", "Priority:", None, QtGui.QApplication.UnicodeUTF8))
        self.priority_spinBox.setToolTip(QtGui.QApplication.translate("Dialog", "Set the priority for this render job. Setting the priority to zero will pause the job.", None, QtGui.QApplication.UnicodeUTF8))
        self.submit_pushButton.setText(QtGui.QApplication.translate("Dialog", "Submit", None, QtGui.QApplication.UnicodeUTF8))
        self.close_pushButton.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

