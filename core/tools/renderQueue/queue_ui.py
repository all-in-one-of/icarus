# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'queue_ui.ui'
#
# Created: Mon May 23 19:23:31 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 576)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.renderQueueToolbar_frame = QtGui.QFrame(self.centralwidget)
        self.renderQueueToolbar_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.renderQueueToolbar_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.renderQueueToolbar_frame.setObjectName("renderQueueToolbar_frame")
        self.horizontalLayout_10 = QtGui.QHBoxLayout(self.renderQueueToolbar_frame)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.view_groupBox = QtGui.QGroupBox(self.renderQueueToolbar_frame)
        self.view_groupBox.setObjectName("view_groupBox")
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.view_groupBox)
        self.horizontalLayout_4.setContentsMargins(6, 4, 6, 4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.jobSubmit_toolButton = QtGui.QToolButton(self.view_groupBox)
        self.jobSubmit_toolButton.setMinimumSize(QtCore.QSize(64, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/rsc/rsc/app_icon_maya.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/rsc/rsc/app_icon_maya_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.jobSubmit_toolButton.setIcon(icon)
        self.jobSubmit_toolButton.setIconSize(QtCore.QSize(32, 32))
        self.jobSubmit_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.jobSubmit_toolButton.setObjectName("jobSubmit_toolButton")
        self.horizontalLayout_4.addWidget(self.jobSubmit_toolButton)
        self.refresh_toolButton = QtGui.QToolButton(self.view_groupBox)
        self.refresh_toolButton.setMinimumSize(QtCore.QSize(64, 0))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/rsc/rsc/icon_refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/rsc/rsc/icon_refresh_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.refresh_toolButton.setIcon(icon1)
        self.refresh_toolButton.setIconSize(QtCore.QSize(32, 32))
        self.refresh_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.refresh_toolButton.setObjectName("refresh_toolButton")
        self.horizontalLayout_4.addWidget(self.refresh_toolButton)
        self.horizontalLayout_10.addWidget(self.view_groupBox)
        self.job_groupBox = QtGui.QGroupBox(self.renderQueueToolbar_frame)
        self.job_groupBox.setObjectName("job_groupBox")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.job_groupBox)
        self.horizontalLayout_3.setContentsMargins(6, 4, 6, 4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.jobPause_toolButton = QtGui.QToolButton(self.job_groupBox)
        self.jobPause_toolButton.setMinimumSize(QtCore.QSize(64, 0))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/rsc/rsc/icon_pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/rsc/rsc/icon_pause_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.jobPause_toolButton.setIcon(icon2)
        self.jobPause_toolButton.setIconSize(QtCore.QSize(32, 32))
        self.jobPause_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.jobPause_toolButton.setObjectName("jobPause_toolButton")
        self.horizontalLayout_3.addWidget(self.jobPause_toolButton)
        self.jobKill_toolButton = QtGui.QToolButton(self.job_groupBox)
        self.jobKill_toolButton.setEnabled(False)
        self.jobKill_toolButton.setMinimumSize(QtCore.QSize(64, 0))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/rsc/rsc/icon_cross.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon3.addPixmap(QtGui.QPixmap(":/rsc/rsc/icon_cross_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.jobKill_toolButton.setIcon(icon3)
        self.jobKill_toolButton.setIconSize(QtCore.QSize(32, 32))
        self.jobKill_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.jobKill_toolButton.setObjectName("jobKill_toolButton")
        self.horizontalLayout_3.addWidget(self.jobKill_toolButton)
        self.jobDelete_toolButton = QtGui.QToolButton(self.job_groupBox)
        self.jobDelete_toolButton.setMinimumSize(QtCore.QSize(64, 0))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/rsc/rsc/icon_delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon4.addPixmap(QtGui.QPixmap(":/rsc/rsc/icon_delete_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.jobDelete_toolButton.setIcon(icon4)
        self.jobDelete_toolButton.setIconSize(QtCore.QSize(32, 32))
        self.jobDelete_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.jobDelete_toolButton.setObjectName("jobDelete_toolButton")
        self.horizontalLayout_3.addWidget(self.jobDelete_toolButton)
        self.jobResubmit_toolButton = QtGui.QToolButton(self.job_groupBox)
        self.jobResubmit_toolButton.setEnabled(False)
        self.jobResubmit_toolButton.setMinimumSize(QtCore.QSize(64, 0))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/rsc/rsc/icon_resubmit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon5.addPixmap(QtGui.QPixmap(":/rsc/rsc/icon_resubmit_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.jobResubmit_toolButton.setIcon(icon5)
        self.jobResubmit_toolButton.setIconSize(QtCore.QSize(32, 32))
        self.jobResubmit_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.jobResubmit_toolButton.setObjectName("jobResubmit_toolButton")
        self.horizontalLayout_3.addWidget(self.jobResubmit_toolButton)
        spacerItem = QtGui.QSpacerItem(8, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.jobPriority_label = QtGui.QLabel(self.job_groupBox)
        self.jobPriority_label.setObjectName("jobPriority_label")
        self.horizontalLayout_3.addWidget(self.jobPriority_label)
        self.jobPriority_slider = QtGui.QSlider(self.job_groupBox)
        self.jobPriority_slider.setMinimumSize(QtCore.QSize(100, 0))
        self.jobPriority_slider.setMinimum(-100)
        self.jobPriority_slider.setMaximum(100)
        self.jobPriority_slider.setPageStep(0)
        self.jobPriority_slider.setProperty("value", 0)
        self.jobPriority_slider.setTracking(False)
        self.jobPriority_slider.setOrientation(QtCore.Qt.Horizontal)
        self.jobPriority_slider.setObjectName("jobPriority_slider")
        self.horizontalLayout_3.addWidget(self.jobPriority_slider)
        self.horizontalLayout_10.addWidget(self.job_groupBox)
        self.task_groupBox = QtGui.QGroupBox(self.renderQueueToolbar_frame)
        self.task_groupBox.setObjectName("task_groupBox")
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.task_groupBox)
        self.horizontalLayout_5.setContentsMargins(6, 4, 6, 4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.taskComplete_toolButton = QtGui.QToolButton(self.task_groupBox)
        self.taskComplete_toolButton.setMinimumSize(QtCore.QSize(64, 0))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/rsc/rsc/icon_tick.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon6.addPixmap(QtGui.QPixmap(":/rsc/rsc/icon_tick_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.taskComplete_toolButton.setIcon(icon6)
        self.taskComplete_toolButton.setIconSize(QtCore.QSize(32, 32))
        self.taskComplete_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.taskComplete_toolButton.setObjectName("taskComplete_toolButton")
        self.horizontalLayout_5.addWidget(self.taskComplete_toolButton)
        self.taskRequeue_toolButton = QtGui.QToolButton(self.task_groupBox)
        self.taskRequeue_toolButton.setMinimumSize(QtCore.QSize(64, 0))
        self.taskRequeue_toolButton.setIcon(icon5)
        self.taskRequeue_toolButton.setIconSize(QtCore.QSize(32, 32))
        self.taskRequeue_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.taskRequeue_toolButton.setObjectName("taskRequeue_toolButton")
        self.horizontalLayout_5.addWidget(self.taskRequeue_toolButton)
        self.horizontalLayout_10.addWidget(self.task_groupBox)
        self.render_groupBox = QtGui.QGroupBox(self.renderQueueToolbar_frame)
        self.render_groupBox.setObjectName("render_groupBox")
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.render_groupBox)
        self.horizontalLayout_6.setContentsMargins(6, 4, 6, 4)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.slave_toolButton = QtGui.QToolButton(self.render_groupBox)
        self.slave_toolButton.setMinimumSize(QtCore.QSize(64, 0))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/rsc/rsc/icon_render.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon7.addPixmap(QtGui.QPixmap(":/rsc/rsc/icon_render_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.slave_toolButton.setIcon(icon7)
        self.slave_toolButton.setIconSize(QtCore.QSize(32, 32))
        self.slave_toolButton.setCheckable(True)
        self.slave_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.slave_toolButton.setObjectName("slave_toolButton")
        self.horizontalLayout_6.addWidget(self.slave_toolButton)
        self.horizontalLayout_10.addWidget(self.render_groupBox)
        self.verticalLayout_5.addWidget(self.renderQueueToolbar_frame)
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.renderQueue_treeWidget = QtGui.QTreeWidget(self.splitter)
        self.renderQueue_treeWidget.setAlternatingRowColors(True)
        self.renderQueue_treeWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.renderQueue_treeWidget.setRootIsDecorated(True)
        self.renderQueue_treeWidget.setUniformRowHeights(True)
        self.renderQueue_treeWidget.setAnimated(True)
        self.renderQueue_treeWidget.setHeaderHidden(False)
        self.renderQueue_treeWidget.setExpandsOnDoubleClick(True)
        self.renderQueue_treeWidget.setObjectName("renderQueue_treeWidget")
        self.renderQueue_treeWidget.header().setSortIndicatorShown(True)
        self.slave_tabWidget = QtGui.QTabWidget(self.splitter)
        self.slave_tabWidget.setObjectName("slave_tabWidget")
        self.info_tab = QtGui.QWidget()
        self.info_tab.setObjectName("info_tab")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.info_tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.slaveInfo_horizontalLayout = QtGui.QHBoxLayout()
        self.slaveInfo_horizontalLayout.setObjectName("slaveInfo_horizontalLayout")
        self.slaveStatus_label = QtGui.QLabel(self.info_tab)
        self.slaveStatus_label.setStyleSheet("QLabel {\n"
"        font-size: 18px;\n"
"}")
        self.slaveStatus_label.setObjectName("slaveStatus_label")
        self.slaveInfo_horizontalLayout.addWidget(self.slaveStatus_label)
        self.processKill_toolButton = QtGui.QToolButton(self.info_tab)
        self.processKill_toolButton.setMinimumSize(QtCore.QSize(64, 0))
        self.processKill_toolButton.setIconSize(QtCore.QSize(32, 32))
        self.processKill_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.processKill_toolButton.setObjectName("processKill_toolButton")
        self.slaveInfo_horizontalLayout.addWidget(self.processKill_toolButton)
        self.dequeue_toolButton = QtGui.QToolButton(self.info_tab)
        self.dequeue_toolButton.setMinimumSize(QtCore.QSize(64, 0))
        self.dequeue_toolButton.setIconSize(QtCore.QSize(32, 32))
        self.dequeue_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.dequeue_toolButton.setObjectName("dequeue_toolButton")
        self.slaveInfo_horizontalLayout.addWidget(self.dequeue_toolButton)
        self.stopAfterTask_checkBox = QtGui.QCheckBox(self.info_tab)
        self.stopAfterTask_checkBox.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stopAfterTask_checkBox.sizePolicy().hasHeightForWidth())
        self.stopAfterTask_checkBox.setSizePolicy(sizePolicy)
        self.stopAfterTask_checkBox.setChecked(False)
        self.stopAfterTask_checkBox.setObjectName("stopAfterTask_checkBox")
        self.slaveInfo_horizontalLayout.addWidget(self.stopAfterTask_checkBox)
        self.verticalLayout_4.addLayout(self.slaveInfo_horizontalLayout)
        self.taskInfo_horizontalLayout = QtGui.QHBoxLayout()
        self.taskInfo_horizontalLayout.setObjectName("taskInfo_horizontalLayout")
        self.taskInfo_label = QtGui.QLabel(self.info_tab)
        self.taskInfo_label.setObjectName("taskInfo_label")
        self.taskInfo_horizontalLayout.addWidget(self.taskInfo_label)
        self.runningTime_label = QtGui.QLabel(self.info_tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runningTime_label.sizePolicy().hasHeightForWidth())
        self.runningTime_label.setSizePolicy(sizePolicy)
        self.runningTime_label.setObjectName("runningTime_label")
        self.taskInfo_horizontalLayout.addWidget(self.runningTime_label)
        self.verticalLayout_4.addLayout(self.taskInfo_horizontalLayout)
        self.command_lineEdit = QtGui.QLineEdit(self.info_tab)
        self.command_lineEdit.setReadOnly(True)
        self.command_lineEdit.setObjectName("command_lineEdit")
        self.verticalLayout_4.addWidget(self.command_lineEdit)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.slave_tabWidget.addTab(self.info_tab, "")
        self.output_tab = QtGui.QWidget()
        self.output_tab.setObjectName("output_tab")
        self.verticalLayout = QtGui.QVBoxLayout(self.output_tab)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.output_textEdit = QtGui.QTextEdit(self.output_tab)
        font = QtGui.QFont()
        font.setFamily("Consolas, Lucidatypewriter, Fixed, monospace")
        self.output_textEdit.setFont(font)
        self.output_textEdit.setStyleSheet("QTextEdit {\n"
"    font-family: \'Consolas, Lucidatypewriter, Fixed, monospace\';\n"
"}")
        self.output_textEdit.setReadOnly(True)
        self.output_textEdit.setObjectName("output_textEdit")
        self.verticalLayout.addWidget(self.output_textEdit)
        self.slave_tabWidget.addTab(self.output_tab, "")
        self.verticalLayout_5.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.slave_tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Render Queue", None, QtGui.QApplication.UnicodeUTF8))
        self.view_groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Queue", None, QtGui.QApplication.UnicodeUTF8))
        self.jobSubmit_toolButton.setText(QtGui.QApplication.translate("MainWindow", "Submit", None, QtGui.QApplication.UnicodeUTF8))
        self.refresh_toolButton.setText(QtGui.QApplication.translate("MainWindow", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.job_groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Job", None, QtGui.QApplication.UnicodeUTF8))
        self.jobPause_toolButton.setText(QtGui.QApplication.translate("MainWindow", "Pause", None, QtGui.QApplication.UnicodeUTF8))
        self.jobKill_toolButton.setText(QtGui.QApplication.translate("MainWindow", "Kill", None, QtGui.QApplication.UnicodeUTF8))
        self.jobDelete_toolButton.setText(QtGui.QApplication.translate("MainWindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.jobResubmit_toolButton.setText(QtGui.QApplication.translate("MainWindow", "Resubmit", None, QtGui.QApplication.UnicodeUTF8))
        self.jobPriority_label.setText(QtGui.QApplication.translate("MainWindow", "Reprioritise:", None, QtGui.QApplication.UnicodeUTF8))
        self.task_groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Task", None, QtGui.QApplication.UnicodeUTF8))
        self.taskComplete_toolButton.setText(QtGui.QApplication.translate("MainWindow", "Complete", None, QtGui.QApplication.UnicodeUTF8))
        self.taskRequeue_toolButton.setText(QtGui.QApplication.translate("MainWindow", "Requeue", None, QtGui.QApplication.UnicodeUTF8))
        self.render_groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Render", None, QtGui.QApplication.UnicodeUTF8))
        self.slave_toolButton.setText(QtGui.QApplication.translate("MainWindow", "Start Local Slave", None, QtGui.QApplication.UnicodeUTF8))
        self.renderQueue_treeWidget.setSortingEnabled(True)
        self.renderQueue_treeWidget.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Job / Task", None, QtGui.QApplication.UnicodeUTF8))
        self.renderQueue_treeWidget.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "ID", None, QtGui.QApplication.UnicodeUTF8))
        self.renderQueue_treeWidget.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "Frames", None, QtGui.QApplication.UnicodeUTF8))
        self.renderQueue_treeWidget.headerItem().setText(3, QtGui.QApplication.translate("MainWindow", "Status", None, QtGui.QApplication.UnicodeUTF8))
        self.renderQueue_treeWidget.headerItem().setText(4, QtGui.QApplication.translate("MainWindow", "Priority", None, QtGui.QApplication.UnicodeUTF8))
        self.renderQueue_treeWidget.headerItem().setText(5, QtGui.QApplication.translate("MainWindow", "User", None, QtGui.QApplication.UnicodeUTF8))
        self.renderQueue_treeWidget.headerItem().setText(6, QtGui.QApplication.translate("MainWindow", "Submitted", None, QtGui.QApplication.UnicodeUTF8))
        self.renderQueue_treeWidget.headerItem().setText(7, QtGui.QApplication.translate("MainWindow", "Running time", None, QtGui.QApplication.UnicodeUTF8))
        self.renderQueue_treeWidget.headerItem().setText(8, QtGui.QApplication.translate("MainWindow", "Slave", None, QtGui.QApplication.UnicodeUTF8))
        self.renderQueue_treeWidget.headerItem().setText(9, QtGui.QApplication.translate("MainWindow", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.slaveStatus_label.setText(QtGui.QApplication.translate("MainWindow", "hostname", None, QtGui.QApplication.UnicodeUTF8))
        self.processKill_toolButton.setText(QtGui.QApplication.translate("MainWindow", "Kill", None, QtGui.QApplication.UnicodeUTF8))
        self.dequeue_toolButton.setText(QtGui.QApplication.translate("MainWindow", "Dequeue", None, QtGui.QApplication.UnicodeUTF8))
        self.stopAfterTask_checkBox.setToolTip(QtGui.QApplication.translate("MainWindow", "Stop this slave when the current task completes.", None, QtGui.QApplication.UnicodeUTF8))
        self.stopAfterTask_checkBox.setText(QtGui.QApplication.translate("MainWindow", "Stop after current task", None, QtGui.QApplication.UnicodeUTF8))
        self.taskInfo_label.setText(QtGui.QApplication.translate("MainWindow", "Task info", None, QtGui.QApplication.UnicodeUTF8))
        self.runningTime_label.setText(QtGui.QApplication.translate("MainWindow", "Running time", None, QtGui.QApplication.UnicodeUTF8))
        self.slave_tabWidget.setTabText(self.slave_tabWidget.indexOf(self.info_tab), QtGui.QApplication.translate("MainWindow", "Info", None, QtGui.QApplication.UnicodeUTF8))
        self.slave_tabWidget.setTabText(self.slave_tabWidget.indexOf(self.output_tab), QtGui.QApplication.translate("MainWindow", "Output", None, QtGui.QApplication.UnicodeUTF8))

import rsc_rc
