import sys
from os import path
from typing import List
from queue import Queue
from PyQt5 import QtCore, QtWidgets, Qt, QtGui
import Ui_Simulator

from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from direct.stdpy import threading
from panda3d.core import WindowProperties, Filename, NodePath, PythonTask
if __name__ == "__main__":
	# for debug purposes: for directly running this .py file
	sys.path.append(path.normpath(path.join(sys.path[0], '..')))
from inputManager import KeyboardManager
from utils import Settings
from TableWidgetProperty import TableWidgetProperty

# little hack with Panda3D task manager (Python-level wrapper around the C++ AsyncTaskManager interface)
# for side by side running of Qt & Panda3D threads
from direct.task import Task
Task.signal = None # off the SIGINT signal processing for Posix systems


# create comands queues
pandaQueue = Queue(16) # commands to panda
qtQueue = Queue(16) # commands to qt


class SETTINGS():
	class QT():
		PREFIX = 'main_window'
		ACTOR_PATH = 'actor_path'
		ANIMATION_PATH = 'animation_path'
	class PANDA():
		PREFIX = 'panda_window'
		BACKGROUND = 'background'


class MainWindow(QtWidgets.QMainWindow):
	MODEL_FILES_FILTER = "Panda3D models (*.egg)(*.egg);;All files (*.*)(*.*)"

	def __init__(self):
		super(MainWindow, self).__init__()
		self.ui = Ui_Simulator.Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.retranslateUi(self)
		# setup page: Add model
		self.ui.oActorFiles.setAcceptDrops(True)
		self.ui.oAnimationsFiles.setAcceptDrops(True)
		self.ui.oAddActorFileButton.clicked.connect(self.addActorFiles_clicked)
		self.ui.oAddAnimationFileButton.clicked.connect(self.addAnimationFiles_clicked)
		self.ui.oDeleteActorFilesButton.clicked.connect(self.deleteActorFiles_clicked)
		self.ui.oDeleteAnimationFilesButton.clicked.connect(self.deleteAnimationFiles_clicked)
		self.ui.oActorFiles.itemSelectionChanged.connect(
			lambda: self.ui.oDeleteActorFilesButton.setEnabled(len(self.ui.oActorFiles.selectedItems()) > 0))
		self.ui.oAnimationsFiles.itemSelectionChanged.connect(
			lambda: self.ui.oDeleteAnimationFilesButton.setEnabled(len(self.ui.oAnimationsFiles.selectedItems()) > 0))
		self.ui.oModelName.textChanged.connect(self.refreshAddModelButton)
		self.ui.oModels.itemSelectionChanged.connect(
			lambda: self.ui.oDeleteModelsButton.setEnabled(len(self.ui.oModels.selectedItems()) > 0))
		self.ui.oDeleteModelsButton.clicked.connect(self.__oDeleteModelsButton_clicked)
		self.ui.oAddModelButton.clicked.connect(self.__oAddModelButton_clicked)
		self.recentActorFilePath = None
		self.recentAnimationFilePath = None
		self.ui.oActorFiles.itemSelectionChanged.emit()
		self.ui.oAnimationsFiles.itemSelectionChanged.emit()
		self.ui.oModels.itemSelectionChanged.emit()
		self.refreshAddModelButton()
		# setup page: Screens
		self.refreshScreens()
		self.ui.oScreensRefreshButton.clicked.connect(self.refreshScreens)
		app = QtWidgets.QApplication.instance()
		app.screenAdded.connect(self.refreshScreens)
		app.screenRemoved.connect(self.refreshScreens)
		# restore settings
		self.recentActorFilePath = Settings.value(SETTINGS.QT.PREFIX, SETTINGS.QT.ACTOR_PATH)
		self.recentAnimationFilePath = Settings.value(SETTINGS.QT.PREFIX, SETTINGS.QT.ANIMATION_PATH)
		self.setAcceptDrops(True)
		# add properties to properties table
		self.ui.oSceneProperties.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
		self.ui.oSceneProperties.itemClicked.connect(self.__properties_itemClicked)
		TableWidgetProperty.addPropertyColor(self.ui.oSceneProperties, 'Background', 'background-color', \
			Settings.value(SETTINGS.PANDA.PREFIX, SETTINGS.PANDA.BACKGROUND, QtGui.QColor(128, 128, 128)), \
			self.__propertyBackgroundChanged, True)
		# commands queue processing
		self.startTimer(250)

	# Properties section start

	def __properties_itemClicked(self, item: QtWidgets.QTableWidgetItem):
		"Properties TableWidget item clicked"
		if item.column() == 1:
			for row in range(item.tableWidget().rowCount()):
				if item is item.tableWidget().item(row, 1):
					if item.uiProperty(): # show UI and wait for OK or Cancel
						# OK # property changed by UI
						print(item.propertyName)
						self.__propertyChanged(item.propertyName)

	def __propertyChanged(self, name: str):
		"Use propertyValue/propertySerialize function to get value or serialized to string"
		print('__propertyChanged: ', self.propertyValue(name))
		print('__propertyChanged: ', self.propertySerialize(name))

	def __propertyBackgroundChanged(self, name: str, color: QtGui.QColor):
		pandaQueue.put(PandaCommands.SetBackgroundColor(color.redF(), color.greenF(), color.blueF()))

	# Properties section end

	# Commands section start

	def timerEvent(self, e: QtCore.QTimerEvent):
		# Processes commands queue
		if not qtQueue.empty():
			qtQueue.get().do(self)

	def ModelAdded(self, name: str):
		if name not in [ self.ui.oModels.item(row).text() for row in range(self.ui.oModels.count()) ]:
			self.ui.oModels.addItem(name)

	# Commands section end

	def __oDeleteModelsButton_clicked(self):
		items = self.ui.oModels.selectedItems()
		for i in items:
			i.text()

	def addActorFiles_clicked(self, checked):
		# so, from returned tuple (file_path, filter_name)
		# if cancel: typle with empty strings
		fnames, _ = QtWidgets.QFileDialog.getOpenFileNames(self,
			'Add Actor Files',
			self.recentActorFilePath if self.recentActorFilePath else QtCore.QDir.homePath(),
			self.MODEL_FILES_FILTER)
		if fnames:
			self.addActorFiles(fnames)

	def addAnimationFiles_clicked(self, checked):
		# so, from returned tuple (file_path, filter_name)
		# if cancel: typle with empty strings
		fnames, _ = QtWidgets.QFileDialog.getOpenFileNames(self,
			'Add Animation Files',
			self.recentAnimationFilePath if self.recentAnimationFilePath else QtCore.QDir.homePath(),
			self.MODEL_FILES_FILTER)
		if fnames:
			self.addAnimationFiles(fnames)

	def deleteActorFiles_clicked(self, checked):
		for item in self.ui.oActorFiles.selectedItems():
			i = self.ui.oActorFiles.row(item)
			self.ui.oActorFiles.takeItem(i)
		self.refreshAddModelButton()

	def deleteAnimationFiles_clicked(self, checked):
		for item in self.ui.oAnimationsFiles.selectedItems():
			i = self.ui.oAnimationsFiles.row(item)
			self.ui.oAnimationsFiles.takeItem(i)

	def refreshAddModelButton(self):
		self.ui.oAddModelButton.setEnabled(self.ui.oActorFiles.count() > 0 and len(self.ui.oModelName.text()) > 0)

	def __oAddModelButton_clicked(self):
		files = [ self.ui.oActorFiles.item(row).text() for row in range(self.ui.oActorFiles.count()) ]
		pandaQueue.put(PandaCommands.AddActorFromFiles(self.ui.oModelName.text(), files))

	def closeEvent(self, e: QtGui.QCloseEvent):
		pandaQueue.put(PandaCommands.Close())
		Settings.setValue(SETTINGS.QT.PREFIX, SETTINGS.QT.ACTOR_PATH, self.recentActorFilePath)
		Settings.setValue(SETTINGS.QT.PREFIX, SETTINGS.QT.ANIMATION_PATH, self.recentAnimationFilePath)
		Settings.setValue(SETTINGS.PANDA.PREFIX, SETTINGS.PANDA.BACKGROUND, \
			TableWidgetProperty.propertySerialize(self.ui.oSceneProperties, 'background-color'))

	def addActorFiles(self, files):
		self.recentActorFilePath = path.dirname(files[0])
		if not self.ui.oModelName.text():
			self.ui.oModelName.setText(path.split(files[0])[1])
		if not self.recentAnimationFilePath:
			self.recentAnimationFilePath = self.recentActorFilePath
		self.ui.oActorFiles.addItems(files)
		self.refreshAddModelButton()

	def addAnimationFiles(self, files):
		self.recentAnimationFilePath = path.dirname(files[0])
		if not self.recentAnimationFilePath:
			self.recentAnimationFilePath = self.recentActorFilePath
		self.ui.oAnimationsFiles.addItems(files)

	def dragEnterEvent(self, e):
		if e.mimeData().hasUrls(): # check for files list
			# is URLs list
			actorPos = self.ui.oActorFiles.geometry().translated(self.ui.oActorFiles.mapTo(self, QtCore.QPoint(0, 0)))
			animationPos = self.ui.oAnimationsFiles.geometry().translated(self.ui.oAnimationsFiles.mapTo(self, QtCore.QPoint(0, 0)))
			if actorPos.contains(e.pos()) or animationPos.contains(e.pos()):
				e.acceptProposedAction()

	def dropEvent(self, e):
		if e.mimeData().hasUrls(): # check for files list
			# is URLs list
			print(e.mimeData().urls()) # example: [PyQt5.QtCore.QUrl('file:///home/vika/Opus/Odyssey/models/soldier.egg')]
			actorPos = self.ui.oActorFiles.geometry().translated(self.ui.oActorFiles.mapTo(self, QtCore.QPoint(0, 0)))
			animationPos = self.ui.oAnimationsFiles.geometry().translated(self.ui.oAnimationsFiles.mapTo(self, QtCore.QPoint(0, 0)))
			if actorPos.contains(e.pos()):
				self.addActorFiles([ i.path() for i in e.mimeData().urls() ])
				e.acceptProposedAction()
			elif animationPos.contains(e.pos()):
				self.addAnimationFiles([ i.path() for i in e.mimeData().urls() ])
				e.acceptProposedAction()

	def refreshScreens(self):

		def addScreen():
			"Adds row items (screen properties) to the screen list"

			def addItem(colIndex: int, text: str):
				"Adds column item (screen property) to the screen list"
				item = QtWidgets.QTableWidgetItem(text)
				item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
				self.ui.oScreens.setItem(rowIndex, colIndex, item)

			addItem(0, screen.name())
			addItem(1, '{}x{}'.format(screen.size().width(), screen.size().height()))
			addItem(2, screen.model())
			addItem(3, screen.manufacturer())

		self.ui.oScreens.setRowCount(0) # clear rows (all screens) from screens list
		for screen in QtGui.QGuiApplication.screens():
			rowIndex = self.ui.oScreens.rowCount()
			self.ui.oScreens.setRowCount(rowIndex + 1)
			addScreen()


class PandaScene(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)
		# base.useDrive()
		# TODO: Mouse Control
		# base.disableMouse()
		wp = WindowProperties.getDefault()
		wp.setOrigin(0,0)
		base.win.requestProperties(wp)
		# self.waveShader = loader.loadShader("wave.sha")
		# self.UWShader = loader.loadShader("underwater.sha")
		# self.UWMShader = loader.loadShader("UWModel.sha")
		self.mainNode = render.attachNewNode("Main Node")
		print(type(self.mainNode))
		self.selectedNode = render.attachNewNode("Selected")
		self.selectedNode.showTightBounds()
		self.UWNode = render.attachNewNode("Underwater Node")
		self.initScene()
		self.pandaKeys = KeyboardManager(self)
		base.setBackgroundColor(.5, .5, .5)
		# commands queue
		taskMgr.doMethodLater(0, self.processCmdQueue, 'processCmdQueue')

	def initScene(self):
		# self.pool = Pool(self)
		# plight = PointLight('plight')
		# plight.setColor(VBase4(0.0, 0.8, 0.8, 1))
		# plnp = render.attachNewNode(plight)
		# plnp.setPos(0, 3, 1)
		# render.setLight(plnp)
		# self.model = self.loader.loadModel("panda")
		# self.model.reparentTo(self.mainNode)
		# # self.model.setScale(0.25,0.25,0.25)
		# self.model.setPos(-8,42,0)
		# self.camera.setPosHpr(0,0,2,0,0,0)
		# base.enableMouse()
		print("Simulator Initialized")
		# RosManager()

	def getMainNode(self) -> NodePath:
		return self.mainNode

	def showWorldMap(self):
		self.worldMap = base.win.makeDisplayRegion(0.7, 1, 0, 0.3)
		self.worldMap.setClearColor(VBase4(0.8, 0.8, 0.8, 1))
		self.worldMap.setClearColorActive(True)
		self.worldMap.setClearDepthActive(True)
		self.worldMapCam = self.mainNode.attachNewNode(Camera('worldMapCam'))
		self.worldMap.setCamera(self.worldMapCam)
		self.worldMapCam.setPosHpr(0, 0, 200,0,-90,0)
		self.worldMapCam.node().getLens().setAspectRatio(float(self.worldMap.getPixelWidth()) / float(self.worldMap.getPixelHeight()))
		self.worldMapMouse = MouseWatcher('World Map Mouse')
		self.worldMapMouseNode = base.mouseWatcher.getParent().attachNewNode(self.worldMapMouse)
		self.worldMapMouse.setDisplayRegion(self.worldMap)

	def hideWorldMap(self):
		self.worldMapMouseNode.removeNode()
		base.win.removeDisplayRegion(self.worldMap)
		self.worldMapCam.removeNode()

	def processCmdQueue(self, task: PythonTask):
		"Processes commands queue"
		if not pandaQueue.empty():
			pandaQueue.get().do(self)
		# if task.getStartTime() > 3:
		# 	# print('task.getElapsedTime() > 3')
		# 	if pandaQueue.empty():
		# 		# print(task.getStartTime())
		# 		pandaQueue.put(PandaCommands.SetBackgroundColor(.5, .5, .5))
		return task.again


class PandaSceneThread(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		self.pandaScene = PandaScene()
		self.pandaScene.run()

	def stop(self):
		print('PandaSceneThread.stop')
		if self.isAlive():
			print('PandaSceneThread.stop: isAlive')
			self.pandaScene.userExit()
			print('PandaSceneThread.stop: userExit')
			self.join()
			print('PandaSceneThread.stop: join')


class PandaCommands():
	"Classes to do main job for scene action"

	class Close():
		def do(self, pandaScene):
			print('PandaCommands..Close: userExit')
			pandaScene.userExit()

	class SetBackgroundColor():
		def __init__(self, r, g, b):
			self.r, self.g, self.b = r, g, b
		def do(self, pandaScene: PandaScene):
			pandaScene.setBackgroundColor(self.r, self.g, self.b)

	class AddActorFromFiles():
		def __init__(self, name: str, filesPaths: List[str]):
			self.name = name
			self.filesPaths = filesPaths
		def do(self, pandaScene: PandaScene):
			for modelFilePath in self.filesPaths:
				pandaFile = Filename.fromOsSpecific(modelFilePath)
				print('Load model from file "{}"'.format(pandaFile))
				model = loader.loadModel(pandaFile)
				model.reparentTo(pandaScene.getMainNode())
				# self.model.setPos(0,0,-20)
				model.setPos(0, 100, 0)
				# self.pandaScene.mainNode.setShader(self.pandaScene.UWMShader)
				# self.model.setShaderInput("camPos",base.camera.getX() ,base.camera.getY() ,base.camera.getZ() ,1.0)
				# self.id = str(modelNumber)
				model.setTag('name', self.name)
				model.setTag('selectable', '1')
				# print('Model added: id {}, name "{}"'.format(self.model.getTag("id"), self.modelName))
				qtQueue.put(QtCommands.ActorAdded(self.name))

	class DeleteModels():
		def __init__(self, names: List[str]):
			self.names = names
		def do(self, pandaScene: PandaScene):
			node = pandaScene.getMainNode()
			# node.ne
			# self.names


class QtCommands():
	"Classes to do main job for qt ui action"

	class ActorAdded():
		def __init__(self, name: str):
			self.name = name
		def do(self, wnd: MainWindow):
			wnd.ModelAdded(self.name)


if __name__ == "__main__":
	Settings.init()
	print('Settings file: "{}"'.format(Settings.fileName()))
	app = QtWidgets.QApplication(sys.argv)
	m = MainWindow()
	PandaSceneThread = PandaSceneThread()
	PandaSceneThread.start()
	m.show()
	app.exec_()
	print('app.exec_()')
	PandaSceneThread.stop()
