# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'submit_ui.ui'
#
# Created: Fri Jul 08 10:59:49 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(512, 360)
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
        self.render_groupBox = QtGui.QGroupBox(self.main_frame)
        self.render_groupBox.setObjectName("render_groupBox")
        self.formLayout_4 = QtGui.QFormLayout(self.render_groupBox)
        self.formLayout_4.setObjectName("formLayout_4")
        self.type_label = QtGui.QLabel(self.render_groupBox)
        self.type_label.setObjectName("type_label")
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.type_label)
        self.scene_label = QtGui.QLabel(self.render_groupBox)
        self.scene_label.setObjectName("scene_label")
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.scene_label)
        self.type_horizontalLayout = QtGui.QHBoxLayout()
        self.type_horizontalLayout.setObjectName("type_horizontalLayout")
        self.type_comboBox = QtGui.QComboBox(self.render_groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.type_comboBox.sizePolicy().hasHeightForWidth())
        self.type_comboBox.setSizePolicy(sizePolicy)
        self.type_comboBox.setObjectName("type_comboBox")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/rsc/rsc/app_icon_maya.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/rsc/rsc/app_icon_maya_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/rsc/rsc/app_icon_maya.png"), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        self.type_comboBox.addItem(icon, "")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/rsc/rsc/app_icon_nuke.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/rsc/rsc/app_icon_nuke_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/rsc/rsc/app_icon_nuke.png"), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        self.type_comboBox.addItem(icon1, "")
        self.type_horizontalLayout.addWidget(self.type_comboBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.type_horizontalLayout.addItem(spacerItem)
        self.formLayout_4.setLayout(0, QtGui.QFormLayout.FieldRole, self.type_horizontalLayout)
        self.scene_horizontalLayout = QtGui.QHBoxLayout()
        self.scene_horizontalLayout.setObjectName("scene_horizontalLayout")
        self.scene_comboBox = QtGui.QComboBox(self.render_groupBox)
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
        self.sceneBrowse_toolButton = QtGui.QToolButton(self.render_groupBox)
        self.sceneBrowse_toolButton.setObjectName("sceneBrowse_toolButton")
        self.scene_horizontalLayout.addWidget(self.sceneBrowse_toolButton)
        self.formLayout_4.setLayout(1, QtGui.QFormLayout.FieldRole, self.scene_horizontalLayout)
        self.verticalLayout.addWidget(self.render_groupBox)
        self.overrideFrameRange_groupBox = QtGui.QGroupBox(self.main_frame)
        self.overrideFrameRange_groupBox.setCheckable(True)
        self.overrideFrameRange_groupBox.setObjectName("overrideFrameRange_groupBox")
        self.formLayout = QtGui.QFormLayout(self.overrideFrameRange_groupBox)
        self.formLayout.setObjectName("formLayout")
        self.frameRange_label = QtGui.QLabel(self.overrideFrameRange_groupBox)
        self.frameRange_label.setObjectName("frameRange_label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.frameRange_label)
        self.frameRange_horizontalLayout = QtGui.QHBoxLayout()
        self.frameRange_horizontalLayout.setObjectName("frameRange_horizontalLayout")
        self.frameRange_lineEdit = QtGui.QLineEdit(self.overrideFrameRange_groupBox)
        self.frameRange_lineEdit.setText("")
        self.frameRange_lineEdit.setObjectName("frameRange_lineEdit")
        self.frameRange_horizontalLayout.addWidget(self.frameRange_lineEdit)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.frameRange_horizontalLayout)
        self.taskSize_label = QtGui.QLabel(self.overrideFrameRange_groupBox)
        self.taskSize_label.setObjectName("taskSize_label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.taskSize_label)
        self.taskSize_horizontalLayout = QtGui.QHBoxLayout()
        self.taskSize_horizontalLayout.setObjectName("taskSize_horizontalLayout")
        self.taskSize_spinBox = QtGui.QSpinBox(self.overrideFrameRange_groupBox)
        self.taskSize_spinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
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
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.taskSize_horizontalLayout)
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
        self.priority_spinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
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
        self.comment_label = QtGui.QLabel(self.submit_groupBox)
        self.comment_label.setObjectName("comment_label")
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.comment_label)
        self.comment_horizontalLayout = QtGui.QHBoxLayout()
        self.comment_horizontalLayout.setObjectName("comment_horizontalLayout")
        self.comment_lineEdit = QtGui.QLineEdit(self.submit_groupBox)
        self.comment_lineEdit.setText("")
        self.comment_lineEdit.setObjectName("comment_lineEdit")
        self.comment_horizontalLayout.addWidget(self.comment_lineEdit)
        self.formLayout_3.setLayout(1, QtGui.QFormLayout.FieldRole, self.comment_horizontalLayout)
        self.verticalLayout.addWidget(self.submit_groupBox)
        self.verticalLayout_2.addWidget(self.main_frame)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
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
        Dialog.setTabOrder(self.close_pushButton, self.taskSize_spinBox)
        Dialog.setTabOrder(self.taskSize_spinBox, self.taskSize_slider)
        Dialog.setTabOrder(self.taskSize_slider, self.flags_groupBox)
        Dialog.setTabOrder(self.flags_groupBox, self.flags_lineEdit)
        Dialog.setTabOrder(self.flags_lineEdit, self.priority_spinBox)
        Dialog.setTabOrder(self.priority_spinBox, self.priority_slider)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Submit Render", None, QtGui.QApplication.UnicodeUTF8))
        self.render_groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Render options", None, QtGui.QApplication.UnicodeUTF8))
        self.type_label.setText(QtGui.QApplication.translate("Dialog", "Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.scene_label.setText(QtGui.QApplication.translate("Dialog", "Scene:", None, QtGui.QApplication.UnicodeUTF8))
        self.type_comboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "Maya", None, QtGui.QApplication.UnicodeUTF8))
        self.type_comboBox.setItemText(1, QtGui.QApplication.translate("Dialog", "Nuke", None, QtGui.QApplication.UnicodeUTF8))
        self.sceneBrowse_toolButton.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.overrideFrameRange_groupBox.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>Allows the frame range(s) to be explicitly stated.</p><p>If unchecked, the start and end frames will be read from the scene.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.overrideFrameRange_groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Override frame range", None, QtGui.QApplication.UnicodeUTF8))
        self.frameRange_label.setText(QtGui.QApplication.translate("Dialog", "Frames:", None, QtGui.QApplication.UnicodeUTF8))
        self.frameRange_lineEdit.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>List of frames to be rendered.</p><p>Individual frames should be separated with commas, and sequences can be specified using a hyphen, e.g. 1, 5-10.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.taskSize_label.setText(QtGui.QApplication.translate("Dialog", "Task size:", None, QtGui.QApplication.UnicodeUTF8))
        self.taskSize_spinBox.setToolTip(QtGui.QApplication.translate("Dialog", "How many frames to submit for each task.", None, QtGui.QApplication.UnicodeUTF8))
        self.taskSize_spinBox.setSuffix(QtGui.QApplication.translate("Dialog", " frame(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.taskSize_slider.setToolTip(QtGui.QApplication.translate("Dialog", "How many frames to submit for each task.", None, QtGui.QApplication.UnicodeUTF8))
        self.flags_groupBox.setToolTip(QtGui.QApplication.translate("Dialog", "Allows additional command-line flags to be specified.", None, QtGui.QApplication.UnicodeUTF8))
        self.flags_groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Additional command-line flags", None, QtGui.QApplication.UnicodeUTF8))
        self.submit_groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Submission options", None, QtGui.QApplication.UnicodeUTF8))
        self.priority_label.setText(QtGui.QApplication.translate("Dialog", "Priority:", None, QtGui.QApplication.UnicodeUTF8))
        self.priority_spinBox.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>Set the priority for this render job.</p><p>Higher priority jobs will be rendered first. Setting the priority to zero will submit the job as paused.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.priority_slider.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>Set the priority for this render job.</p><p>Higher priority jobs will be rendered first. Setting the priority to zero will submit the job as paused.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.comment_label.setText(QtGui.QApplication.translate("Dialog", "Comment:", None, QtGui.QApplication.UnicodeUTF8))
        self.comment_lineEdit.setToolTip(QtGui.QApplication.translate("Dialog", "Add notes about this render job (optional).", None, QtGui.QApplication.UnicodeUTF8))
        self.submit_pushButton.setText(QtGui.QApplication.translate("Dialog", "Submit", None, QtGui.QApplication.UnicodeUTF8))
        self.close_pushButton.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

import rsc_rc
