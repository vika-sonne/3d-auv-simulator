# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/vika/Work/Odyssey/odyssey/simulator/guiManager/AiObjectBrowser.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(1000, 874)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setMaximumSize(QtCore.QSize(800, 533))
		self.centralwidget.setObjectName("centralwidget")
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		self.groupModels = QtWidgets.QFrame(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.groupModels.sizePolicy().hasHeightForWidth())
		self.groupModels.setSizePolicy(sizePolicy)
		self.groupModels.setObjectName("groupModels")
		self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupModels)
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_4.setObjectName("horizontalLayout_4")
		self.label_3 = QtWidgets.QLabel(self.groupModels)
		self.label_3.setObjectName("label_3")
		self.horizontalLayout_4.addWidget(self.label_3)
		spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_4.addItem(spacerItem)
		self.oDeleteModelsButton = QtWidgets.QPushButton(self.groupModels)
		self.oDeleteModelsButton.setObjectName("oDeleteModelsButton")
		self.horizontalLayout_4.addWidget(self.oDeleteModelsButton)
		self.verticalLayout_2.addLayout(self.horizontalLayout_4)
		self.oModels = QtWidgets.QListWidget(self.groupModels)
		self.oModels.setAlternatingRowColors(True)
		self.oModels.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
		self.oModels.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		self.oModels.setSelectionRectVisible(True)
		self.oModels.setObjectName("oModels")
		self.verticalLayout_2.addWidget(self.oModels)
		self.horizontalLayout_2.addWidget(self.groupModels)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 30))
		self.menubar.setObjectName("menubar")
		self.menuFile = QtWidgets.QMenu(self.menubar)
		self.menuFile.setObjectName("menuFile")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)
		self.toolBar = QtWidgets.QToolBar(MainWindow)
		self.toolBar.setObjectName("toolBar")
		MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
		self.oAddAiObjectWidget = QtWidgets.QDockWidget(MainWindow)
		self.oAddAiObjectWidget.setObjectName("oAddAiObjectWidget")
		self.dockWidgetContents = QtWidgets.QWidget()
		self.dockWidgetContents.setObjectName("dockWidgetContents")
		self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.dockWidgetContents)
		self.verticalLayout_10.setObjectName("verticalLayout_10")
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.labelModelName = QtWidgets.QLabel(self.dockWidgetContents)
		self.labelModelName.setObjectName("labelModelName")
		self.horizontalLayout.addWidget(self.labelModelName)
		self.oModelName = QtWidgets.QLineEdit(self.dockWidgetContents)
		self.oModelName.setObjectName("oModelName")
		self.horizontalLayout.addWidget(self.oModelName)
		self.oAddModelButton = QtWidgets.QPushButton(self.dockWidgetContents)
		self.oAddModelButton.setObjectName("oAddModelButton")
		self.horizontalLayout.addWidget(self.oAddModelButton)
		self.verticalLayout_10.addLayout(self.horizontalLayout)
		self.frame = QtWidgets.QFrame(self.dockWidgetContents)
		self.frame.setObjectName("frame")
		self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame)
		self.verticalLayout_5.setObjectName("verticalLayout_5")
		self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_3.setObjectName("horizontalLayout_3")
		self.label = QtWidgets.QLabel(self.frame)
		self.label.setObjectName("label")
		self.horizontalLayout_3.addWidget(self.label)
		spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_3.addItem(spacerItem1)
		self.oAddActorFileButton = QtWidgets.QPushButton(self.frame)
		self.oAddActorFileButton.setMinimumSize(QtCore.QSize(84, 0))
		self.oAddActorFileButton.setObjectName("oAddActorFileButton")
		self.horizontalLayout_3.addWidget(self.oAddActorFileButton)
		self.oDeleteActorFilesButton = QtWidgets.QPushButton(self.frame)
		self.oDeleteActorFilesButton.setObjectName("oDeleteActorFilesButton")
		self.horizontalLayout_3.addWidget(self.oDeleteActorFilesButton)
		self.verticalLayout_5.addLayout(self.horizontalLayout_3)
		self.oActorFiles = QtWidgets.QListWidget(self.frame)
		self.oActorFiles.setAlternatingRowColors(True)
		self.oActorFiles.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
		self.oActorFiles.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		self.oActorFiles.setSelectionRectVisible(True)
		self.oActorFiles.setObjectName("oActorFiles")
		self.verticalLayout_5.addWidget(self.oActorFiles)
		self.verticalLayout_10.addWidget(self.frame)
		self.frame_2 = QtWidgets.QFrame(self.dockWidgetContents)
		self.frame_2.setObjectName("frame_2")
		self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_2)
		self.verticalLayout_6.setObjectName("verticalLayout_6")
		self.layoutAnimationFilesButtons = QtWidgets.QHBoxLayout()
		self.layoutAnimationFilesButtons.setObjectName("layoutAnimationFilesButtons")
		self.label_2 = QtWidgets.QLabel(self.frame_2)
		self.label_2.setObjectName("label_2")
		self.layoutAnimationFilesButtons.addWidget(self.label_2)
		spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.layoutAnimationFilesButtons.addItem(spacerItem2)
		self.oAddAnimationFileButton = QtWidgets.QPushButton(self.frame_2)
		self.oAddAnimationFileButton.setObjectName("oAddAnimationFileButton")
		self.layoutAnimationFilesButtons.addWidget(self.oAddAnimationFileButton)
		self.oDeleteAnimationFilesButton = QtWidgets.QPushButton(self.frame_2)
		self.oDeleteAnimationFilesButton.setObjectName("oDeleteAnimationFilesButton")
		self.layoutAnimationFilesButtons.addWidget(self.oDeleteAnimationFilesButton)
		self.verticalLayout_6.addLayout(self.layoutAnimationFilesButtons)
		self.oAnimationsFiles = QtWidgets.QListWidget(self.frame_2)
		self.oAnimationsFiles.setAlternatingRowColors(True)
		self.oAnimationsFiles.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
		self.oAnimationsFiles.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		self.oAnimationsFiles.setSelectionRectVisible(True)
		self.oAnimationsFiles.setObjectName("oAnimationsFiles")
		self.verticalLayout_6.addWidget(self.oAnimationsFiles)
		self.verticalLayout_10.addWidget(self.frame_2)
		self.oAddAiObjectWidget.setWidget(self.dockWidgetContents)
		MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.oAddAiObjectWidget)
		self.oSceneWidget = QtWidgets.QDockWidget(MainWindow)
		self.oSceneWidget.setObjectName("oSceneWidget")
		self.dockWidgetContents_3 = QtWidgets.QWidget()
		self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
		self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents_3)
		self.verticalLayout.setObjectName("verticalLayout")
		self.oSceneProperties = QtWidgets.QTableWidget(self.dockWidgetContents_3)
		self.oSceneProperties.setObjectName("oSceneProperties")
		self.oSceneProperties.setColumnCount(2)
		self.oSceneProperties.setRowCount(0)
		item = QtWidgets.QTableWidgetItem()
		self.oSceneProperties.setHorizontalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.oSceneProperties.setHorizontalHeaderItem(1, item)
		self.verticalLayout.addWidget(self.oSceneProperties)
		self.oSceneWidget.setWidget(self.dockWidgetContents_3)
		MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.oSceneWidget)
		self.actionSaveScene = QtWidgets.QAction(MainWindow)
		self.actionSaveScene.setObjectName("actionSaveScene")
		self.actionLoadScene = QtWidgets.QAction(MainWindow)
		self.actionLoadScene.setObjectName("actionLoadScene")
		self.menuFile.addAction(self.actionSaveScene)
		self.menuFile.addAction(self.actionLoadScene)
		self.menubar.addAction(self.menuFile.menuAction())

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.label_3.setText(_translate("MainWindow", "AI Objects"))
		self.oDeleteModelsButton.setToolTip(_translate("MainWindow", "Delete model"))
		self.oDeleteModelsButton.setText(_translate("MainWindow", "-"))
		self.oModels.setSortingEnabled(True)
		self.menuFile.setTitle(_translate("MainWindow", "&File"))
		self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
		self.oAddAiObjectWidget.setWindowTitle(_translate("MainWindow", "&AI Object"))
		self.labelModelName.setText(_translate("MainWindow", "Name:"))
		self.oAddModelButton.setText(_translate("MainWindow", "Add AI object"))
		self.label.setText(_translate("MainWindow", "Actor files"))
		self.oAddActorFileButton.setToolTip(_translate("MainWindow", "Add actor file..."))
		self.oAddActorFileButton.setText(_translate("MainWindow", "+"))
		self.oDeleteActorFilesButton.setToolTip(_translate("MainWindow", "Delete selected actor files"))
		self.oDeleteActorFilesButton.setText(_translate("MainWindow", "-"))
		self.oActorFiles.setSortingEnabled(True)
		self.label_2.setText(_translate("MainWindow", "Animation files"))
		self.oAddAnimationFileButton.setToolTip(_translate("MainWindow", "Add animation file..."))
		self.oAddAnimationFileButton.setText(_translate("MainWindow", "+"))
		self.oDeleteAnimationFilesButton.setToolTip(_translate("MainWindow", "Delete selected animation files"))
		self.oDeleteAnimationFilesButton.setText(_translate("MainWindow", "-"))
		self.oAnimationsFiles.setSortingEnabled(True)
		self.oSceneWidget.setWindowTitle(_translate("MainWindow", "S&cene"))
		item = self.oSceneProperties.horizontalHeaderItem(0)
		item.setText(_translate("MainWindow", "Name"))
		item = self.oSceneProperties.horizontalHeaderItem(1)
		item.setText(_translate("MainWindow", "Value"))
		self.actionSaveScene.setText(_translate("MainWindow", "Save scene..."))
		self.actionLoadScene.setText(_translate("MainWindow", "Load scene..."))