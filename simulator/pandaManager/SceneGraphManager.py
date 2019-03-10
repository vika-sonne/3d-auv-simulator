"""

project:		3d-auv-simulator
author:			nishant dania
email: 			nishantdania@gmail.com
modified on:	June 23, 2014

"""

#########################################################################

from .ModelNode import ModelNode
from optionManager import LoadScene
from utils import Globals

class SceneGraphManager(object):

	def __init__(self,pandaScene):
		self.pandaScene = pandaScene

	def addModelNode(self,filename):
		Globals.modelsCount = Globals.modelsCount+1
		Globals.selectedModelIndex = Globals.modelsCount
		self.filename = filename
		Globals.modelsList.append(ModelNode(self.pandaScene))
		Globals.modelsList[Globals.modelsCount].addModel(self.filename,Globals.modelsCount)
		Globals.modelsList[Globals.modelsCount].setFilename(self.filename)		

	def setNodeX(self,posX):
		self.posX = float(posX)
		Globals.modelsList[Globals.selectedModelIndex].setX(self.posX)

	def setNodeY(self,posY):
		self.posY = float(posY)
		Globals.modelsList[Globals.selectedModelIndex].setY(self.posY)

	def setNodeZ(self,posZ):
		self.posZ = float(posZ)
		Globals.modelsList[Globals.selectedModelIndex].setZ(self.posZ)

	def setNodeH(self,posH):
		self.posH = float(posH)
		Globals.modelsList[Globals.selectedModelIndex].setH(self.posH)

	def setNodeP(self,posP):
		self.posP = float(posP)
		Globals.modelsList[Globals.selectedModelIndex].setP(self.posP)

	def setNodeR(self,posR):
		self.posR = float(posR)
		Globals.modelsList[Globals.selectedModelIndex].setR(self.posR)

	def setNodeScale(self,scale):
		self.scale = float(scale)
		Globals.modelsList[Globals.selectedModelIndex].setScale(self.scale)

	def setNodeRelX(self,posRelX):
		self.prevX = Globals.modelsList[Globals.prevSelection].getX()
		self.posRelX = float(self.prevX) + float(posRelX)
		Globals.modelsList[Globals.selectedModelIndex].setX(self.posRelX)

	def setNodeRelY(self,posRelY):
		self.prevY = Globals.modelsList[Globals.prevSelection].getY()
		self.posRelY = float(self.prevY) + float(posRelY)
		Globals.modelsList[Globals.selectedModelIndex].setY(self.posRelY)

	def setNodeRelZ(self,posRelZ):
		self.prevZ = Globals.modelsList[Globals.prevSelection].getZ()
		self.posRelZ = float(self.prevZ) + float(posRelZ)
		Globals.modelsList[Globals.selectedModelIndex].setZ(self.posRelZ)

	def loadScene(self,filename):
		self.loadFilename = str(filename)
		loadScene = LoadScene(self.loadFilename,self)
