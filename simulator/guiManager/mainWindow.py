import sys
from os import path
from PyQt5 import QtWidgets, QtGui, QtCore
# from utils import Settings
import Ui_MainWindow

from direct.showbase.ShowBase import ShowBase
from direct.stdpy import threading
from panda3d.core import WindowProperties
sys.path.append('..') # for debug purposes: for directly running this .py file
from inputManager import KeyboardManager

# little hack with Panda3D task manager (Python-level wrapper around the C++ AsyncTaskManager interface)
# for side by side running of Qt & Panda3D threads
from direct.task import Task
Task.signal = None # off the SIGINT signal processing for Posix systems


class SETTINGS():
	PREFIX = 'main_window'
	ACTOR_PATH = 'actor_path'
	ANIMATION_PATH = 'animation_path'


class MainWindow(QtWidgets.QMainWindow):
	MODEL_FILES_FILTER = "Panda3D models (*.egg)(*.egg);;All files (*.*)(*.*)"

	def __init__(self):
		super(MainWindow, self).__init__()
		self.ui = Ui_MainWindow.Ui_MainWindow()
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
		# self.recentActorFilePath = Settings.value(SETTINGS.PREFIX, SETTINGS.ACTOR_PATH)
		# self.recentAnimationFilePath = Settings.value(SETTINGS.PREFIX, SETTINGS.ANIMATION_PATH)
		self.setAcceptDrops(True)

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

	def closeEvent(self, e):
		pass
		# Settings.setValue(SETTINGS.PREFIX, SETTINGS.ACTOR_PATH, self.recentActorFilePath)
		# Settings.setValue(SETTINGS.PREFIX, SETTINGS.ANIMATION_PATH, self.recentAnimationFilePath)

	def addActorFiles(self, files):
		self.recentActorFilePath = path.dirname(files[0])
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
		self.selectedNode = render.attachNewNode("Selected")
		self.selectedNode.showTightBounds()
		self.UWNode = render.attachNewNode("Underwater Node")
		self.initScene()
		self.pandaKeys = KeyboardManager(self)
		base.setBackgroundColor(1.0, 1.0, 1.0)

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

	def getMainNode(self):
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


class GuiThread(threading.Thread):

	def __init__(self, pandaScene: PandaScene):
		threading.Thread.__init__(self)
		self.pandaScene = pandaScene

	def run(self):
		self.app = QtWidgets.QApplication(sys.argv)
		m = MainWindow()
		m.show()
		self.app.exec_()
		self.pandaScene.userExit()

	def stop(self):
		self.app.closeAllWindows()


class SceneThread(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		self.pandaScene = PandaScene()
		self.pandaScene.run()

	def stop(self):
		if self.isAlive():
			self.pandaScene.userExit()
			self.join()


# if __name__ == "__main__":
# 	pandaScene = PandaScene()
# 	gui = GuiThread(pandaScene)
# 	gui.start()
# 	pandaScene.run()
# 	if gui.started:
# 		gui.stop()
# 		print('gui stopped')

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	m = MainWindow()
	sceneThread = SceneThread()
	sceneThread.start()
	m.show()
	app.exec_()
	sceneThread.stop()
