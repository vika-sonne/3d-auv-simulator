"""

project:        3d-auv-simulator
author:         nishant dania
email:          nishantdania@gmail.com
modified on:    June 23, 2014

"""

#########################################################################


from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from optionManager import SaveScene
from utils import Settings

class Gui(QtWidgets.QMainWindow):

	# add model signals
	addModel = QtCore.pyqtSignal()
	sendAddModel = QtCore.pyqtSignal()

	# setX emitter
	setXEmit = QtCore.pyqtSignal()
	sendSetXEmit = QtCore.pyqtSignal()

	# setY emitter
	setYEmit = QtCore.pyqtSignal()
	sendSetYEmit = QtCore.pyqtSignal()

	# setZ emitter
	setZEmit = QtCore.pyqtSignal()
	sendSetZEmit = QtCore.pyqtSignal()

	# setH emitter
	setHEmit = QtCore.pyqtSignal()
	sendSetHEmit = QtCore.pyqtSignal()

	# setP emitter
	setPEmit = QtCore.pyqtSignal()
	sendSetPEmit = QtCore.pyqtSignal()

	# setR emitter
	setREmit = QtCore.pyqtSignal()
	sendSetREmit = QtCore.pyqtSignal()

	# setScale emitter
	setScaleEmit = QtCore.pyqtSignal()
	sendSetScaleEmit = QtCore.pyqtSignal()

	# loadScene emitter
	loadSceneEmit = QtCore.pyqtSignal()
	sendLoadSceneEmit = QtCore.pyqtSignal()

	# setRelX emitter
	setRelXEmit = QtCore.pyqtSignal()
	sendSetRelXEmit = QtCore.pyqtSignal()

	# setRelY emitter
	setRelYEmit = QtCore.pyqtSignal()
	sendSetRelYEmit = QtCore.pyqtSignal()

	# setRelZ emitter
	setRelZEmit = QtCore.pyqtSignal()
	sendSetRelZEmit = QtCore.pyqtSignal()

	def __init__(self):
		super(Gui, self).__init__()
		self.initUI()
		recentModels = Settings.recentModels()
		if recentModels:
			self.modelFileEdit.setText(recentModels)
		
	def initUI(self):

		# Browse and add model
		self.modelFileLabel = QtWidgets.QLabel('Model File:')
		self.modelFileEdit = QtWidgets.QLineEdit()
		self.browseModelFileBtn = QtWidgets.QPushButton('Browse', self)
		self.browseModelFileBtn.clicked.connect(self.openModelFileDialog)
		self.browseModelFileBtn.setStatusTip('Open a new model file')
		self.addModelBtn = QtWidgets.QPushButton('Add Model', self)
		self.addModelBtn.clicked.connect(self.addModelEmitter)
		self.addModelBtn.setStatusTip('Add model to scene')    

		# Set model position and orientation and scale
		self.setXLabel = QtWidgets.QLabel('X:')
		self.setXEdit = QtWidgets.QLineEdit()
		self.setXBtn = QtWidgets.QPushButton('Set X', self)
		self.setXBtn.clicked.connect(self.setXEmitter)
		self.setXBtn.setStatusTip('Set X coordinate')

		self.setYLabel = QtWidgets.QLabel('Y:')
		self.setYEdit = QtWidgets.QLineEdit()
		self.setYBtn = QtWidgets.QPushButton('Set Y', self)
		self.setYBtn.clicked.connect(self.setYEmitter)
		self.setYBtn.setStatusTip('Set Y coordinate')

		self.setZLabel = QtWidgets.QLabel('Z:')
		self.setZEdit = QtWidgets.QLineEdit()
		self.setZBtn = QtWidgets.QPushButton('Set Z', self)
		self.setZBtn.clicked.connect(self.setZEmitter)
		self.setZBtn.setStatusTip('Set Z coordinate')

		self.setHLabel = QtWidgets.QLabel('H:')
		self.setHEdit = QtWidgets.QLineEdit()
		self.setHBtn = QtWidgets.QPushButton('Set H', self)
		self.setHBtn.clicked.connect(self.setHEmitter)
		self.setHBtn.setStatusTip('Set H')

		self.setPLabel = QtWidgets.QLabel('P:')
		self.setPEdit = QtWidgets.QLineEdit()
		self.setPBtn = QtWidgets.QPushButton('Set P', self)
		self.setPBtn.clicked.connect(self.setPEmitter)
		self.setPBtn.setStatusTip('Set P')

		self.setRLabel = QtWidgets.QLabel('R:')
		self.setREdit = QtWidgets.QLineEdit()
		self.setRBtn = QtWidgets.QPushButton('Set R', self)
		self.setRBtn.clicked.connect(self.setREmitter)
		self.setRBtn.setStatusTip('Set R')

		self.setScaleLabel = QtWidgets.QLabel('Scale:')
		self.setScaleEdit = QtWidgets.QLineEdit()
		self.setScaleBtn = QtWidgets.QPushButton('Set Scale', self)
		self.setScaleBtn.clicked.connect(self.setScaleEmitter)
		self.setScaleBtn.setStatusTip('Set Scale')

		self.setRelXLabel = QtWidgets.QLabel('X(rel.):')
		self.setRelXEdit = QtWidgets.QLineEdit()
		self.setRelXBtn = QtWidgets.QPushButton('Set X(rel.)', self)
		self.setRelXBtn.clicked.connect(self.setRelXEmitter)
		self.setRelXBtn.setStatusTip('Set X coordinate relative to selected object')

		self.setRelYLabel = QtWidgets.QLabel('Y(rel.):')
		self.setRelYEdit = QtWidgets.QLineEdit()
		self.setRelYBtn = QtWidgets.QPushButton('Set Y(rel.)', self)
		self.setRelYBtn.clicked.connect(self.setRelYEmitter)
		self.setRelYBtn.setStatusTip('Set Y coordinate relative to selected object')

		self.setRelZLabel = QtWidgets.QLabel('Z(rel.):')
		self.setRelZEdit = QtWidgets.QLineEdit()
		self.setRelZBtn = QtWidgets.QPushButton('Set Z(rel.)', self)
		self.setRelZBtn.clicked.connect(self.setRelZEmitter)
		self.setRelZBtn.setStatusTip('Set Z coordinate relative to selected object')

		self.cWidget = QtWidgets.QWidget(self)
		self.grid = QtWidgets.QGridLayout(self.cWidget)

		self.grid.addWidget(self.modelFileLabel, 1, 0)
		self.grid.addWidget(self.modelFileEdit, 1, 1)
		self.grid.addWidget(self.browseModelFileBtn, 1, 2)
		self.grid.addWidget(self.addModelBtn, 1, 3)

		self.grid.addWidget(self.setXLabel, 2, 0)
		self.grid.addWidget(self.setXEdit, 2, 1)
		self.grid.addWidget(self.setXBtn, 2, 2)

		self.grid.addWidget(self.setYLabel, 3, 0)
		self.grid.addWidget(self.setYEdit, 3, 1)
		self.grid.addWidget(self.setYBtn, 3, 2)

		self.grid.addWidget(self.setZLabel, 4, 0)
		self.grid.addWidget(self.setZEdit, 4, 1)
		self.grid.addWidget(self.setZBtn, 4, 2)

		self.grid.addWidget(self.setHLabel, 5, 0)
		self.grid.addWidget(self.setHEdit, 5, 1)
		self.grid.addWidget(self.setHBtn, 5, 2)

		self.grid.addWidget(self.setPLabel, 6, 0)
		self.grid.addWidget(self.setPEdit, 6, 1)
		self.grid.addWidget(self.setPBtn, 6, 2)

		self.grid.addWidget(self.setRLabel, 7, 0)
		self.grid.addWidget(self.setREdit, 7, 1)
		self.grid.addWidget(self.setRBtn, 7, 2)

		self.grid.addWidget(self.setScaleLabel, 8, 0)
		self.grid.addWidget(self.setScaleEdit, 8, 1)
		self.grid.addWidget(self.setScaleBtn, 8, 2)

		self.grid.addWidget(self.setRelXLabel, 9, 0)
		self.grid.addWidget(self.setRelXEdit, 9, 1)
		self.grid.addWidget(self.setRelXBtn, 9, 2)

		self.grid.addWidget(self.setRelYLabel, 10, 0)
		self.grid.addWidget(self.setRelYEdit, 10, 1)
		self.grid.addWidget(self.setRelYBtn, 10, 2)

		self.grid.addWidget(self.setRelZLabel, 11, 0)
		self.grid.addWidget(self.setRelZEdit, 11, 1)
		self.grid.addWidget(self.setRelZBtn, 11, 2)


		self.setCentralWidget(self.cWidget)

		self.setWindowTitle('3D AUV Simulator')
		
		exitAction = QtWidgets.QAction(QtGui.QIcon.fromTheme('exit'), '&Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit Application')
		exitAction.triggered.connect(QtCore.QCoreApplication.instance().quit)
		
		browseFile = QtWidgets.QAction(QtGui.QIcon.fromTheme('open'), '&Browse', self)
		browseFile.setShortcut('Ctrl+B')
		browseFile.setStatusTip('Open new model file')
		browseFile.triggered.connect(self.openModelFileDialog)
		
		# Save Action
		saveAction = QtWidgets.QAction(QtGui.QIcon.fromTheme('save'), '&Save', self)
		saveAction.setShortcut('Ctrl+S')
		saveAction.setStatusTip('Save Scene')
		saveAction.triggered.connect(self.saveActionTrigger)

		# Load Action
		loadAction = QtWidgets.QAction(QtGui.QIcon.fromTheme('open'), '&Load', self)
		loadAction.setShortcut('Ctrl+L')
		loadAction.setStatusTip('Load Scene')
		loadAction.triggered.connect(self.loadSceneEmitter)
		
		self.statusBar().showMessage('Ready')
		
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(browseFile)
		fileMenu.addAction(saveAction)
		fileMenu.addAction(loadAction)
		fileMenu.addAction(exitAction)
		
		self.toolbar = self.addToolBar('Exit')
		self.toolbar.addAction(exitAction)
		
		self.move(900,0)

	def openModelFileDialog(self):
		# so, from returned tuple (file_path, filter_name)
		# if cancel: typle with empty strings
		self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(self,
			'Open File',
			QtCore.QDir.homePath(),
			"Panda3D models (*.egg)(*.egg);;All files (*.*)(*.*)")
		if self.fname:
			self.modelFileEdit.setText(self.fname)
			Settings.setRecentModels(self.fname)

		""" Functions to add model """
	def addModelEmitter(self):
		self.addModel.emit()
		self.sendAddModel.emit()

	def getModelName(self):
		return self.modelFileEdit.text()

		""" Functions to setX """
	def setXEmitter(self):
		self.setXEmit.emit()
		self.sendSetXEmit.emit()

	def getPosX(self):
		return self.setXEdit.text()

		""" Functions to setY """
	def setYEmitter(self):
		self.setYEmit.emit()
		self.sendSetYEmit.emit()

	def getPosY(self):
		return self.setYEdit.text()

		""" Functions to setZ """
	def setZEmitter(self):
		self.setZEmit.emit()
		self.sendSetZEmit.emit()

	def getPosZ(self):
		return self.setZEdit.text()

		""" Functions to setH """
	def setHEmitter(self):
		self.setHEmit.emit()
		self.sendSetHEmit.emit()

	def getPosH(self):
		return self.setHEdit.text()

		""" Functions to setP """
	def setPEmitter(self):
		self.setPEmit.emit()
		self.sendSetPEmit.emit()

	def getPosP(self):
		return self.setPEdit.text()

		""" Functions to setR """
	def setREmitter(self):
		self.setREmit.emit()
		self.sendSetREmit.emit()

	def getPosR(self):
		return self.setREdit.text()

		""" Functions to setScale """
	def setScaleEmitter(self):
		self.setScaleEmit.emit()
		self.sendSetScaleEmit.emit()

	def getScale(self):
		return self.setScaleEdit.text()

		""" Functions to save scene """
	def saveActionTrigger(self):
		filename, ok = QtWidgets.QInputDialog.getText(self, 'Save','Enter filename:')
		print(filename)
		self.saveScene = SaveScene(filename)
		self.saveScene.saveModels()

		""" Functions to load scene """
	def loadSceneEmitter(self):
		self.filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Load File', '/home')
		self.loadSceneEmit.emit()
		self.sendLoadSceneEmit.emit()

	def getSavedFile(self):
		return(self.filename)

		""" Functions to setRelX """
	def setRelXEmitter(self):
		self.setRelXEmit.emit()
		self.sendSetRelXEmit.emit()

	def getRelPosX(self):
		return(self.setRelXEdit.text())

		""" Functions to setRelY """
	def setRelYEmitter(self):
		self.setRelYEmit.emit()
		self.sendSetRelYEmit.emit()

	def getRelPosY(self):
		return self.setRelYEdit.text()

		""" Functions to setRelZ """
	def setRelZEmitter(self):
		self.setRelZEmit.emit()
		self.sendSetRelZEmit.emit()

	def getRelPosZ(self):
		return(self.setRelZEdit.text())