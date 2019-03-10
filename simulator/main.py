"""
Ὀδύσσεια
Odyssey
project:		3d-auv-simulator
author:			nishant dania
email: 			nishantdania@gmail.com
modified on:	June 8, 2014

"""

#########################################################################


from pandaManager import PandaScene
from pandaManager import SceneGraphManager
from guiManager import Gui
from queue import Queue
from eventManager import EventManager
from guiManager import GuiThread
from utils import Settings

def main():
	Settings.init()
	print('Settings file: "{}"'.format(Settings.fileName()))
	q = Queue(1)
	pandaScene = PandaScene()
	sceneGraphManager = SceneGraphManager(pandaScene)
	eventManager = EventManager(sceneGraphManager)
	gui = GuiThread(q,eventManager)
	gui.start()
	pandaScene.run()


if __name__=='__main__':
	main()
