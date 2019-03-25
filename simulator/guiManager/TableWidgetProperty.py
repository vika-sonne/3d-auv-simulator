from PyQt5 import QtCore, QtWidgets, QtGui


class TableWidgetProperty():

	class IProperty():
		"Property value holder and UI to change it"
		def __init__(self, name: str, propertyChangedCallback=None):
			self.propertyName = name
			self.propertyChangedCallback = propertyChangedCallback
		def uiProperty(self) -> bool:
			"Lets user to change a property by showing UI"
			pass
		def setProperty(self, value):
			"Sets property value"
			pass
		def getProperty(self):
			"Gets property value"
			return None
		def serializeProperty(self) -> str:
			"Gets property value as serialized text"
			return ''

	@staticmethod
	def __addProperty(table: QtWidgets.QTableWidget, caption: str, valueItem: QtWidgets.QTableWidgetItem = None, valueWidget: QtWidgets.QWidget = None):
		currentRow = table.rowCount()
		table.setRowCount(table.rowCount() + 1)
		captionItem = QtWidgets.QTableWidgetItem(caption)
		captionItem.setFlags(captionItem.flags() & ~QtCore.Qt.ItemIsEditable)
		table.setItem(currentRow, 0, captionItem)
		if valueItem:
			table.setItem(currentRow, 1, valueItem)
		if valueWidget:
			table.setCellWidget(currentRow, 1, valueWidget)

	@staticmethod
	def addPropertyColor(table: QtWidgets.QTableWidget, caption: str, name: str, color: [str, QtGui.QColor], callback=None, applyNow=False):
		"""Property: RGB color
			Example:
		self.addPropertyColor('Background', 'background-color', QtGui.QColor(128, 128, 128), self.__propertyBackgroundChanged)
		def __propertyBackgroundChanged(self, name: str, color: QtGui.QColor):
			pass
		"""

		class TableWidgetItem(TableWidgetProperty.IProperty, QtWidgets.QTableWidgetItem):

			def __init__(self, caption: str, name: str, color: [str, QtGui.QColor], changedCallback=None):
				TableWidgetProperty.IProperty.__init__(self, name, changedCallback)
				QtWidgets.QTableWidgetItem.__init__(self)
				self.setFlags(self.flags() & ~(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable))
				if type(color) is not QtGui.QColor:
					color = QtGui.QColor(color)
				self.setBackground(QtGui.QBrush(color))
				self.caption = caption

			def uiProperty(self) -> bool:
				newValue = QtWidgets.QColorDialog.getColor(self.getProperty(), title=self.caption) # show dialog with OK & Cancel
				if newValue.isValid():
					# OK pressed
					self.setProperty(newValue)
					if self.propertyChangedCallback:
						self.propertyChangedCallback(self.propertyName, self.getProperty())
					return True
				return False

			def setProperty(self, color: QtGui.QColor):
				self.setBackground(QtGui.QBrush(color))

			def getProperty(self) -> QtGui.QColor:
				return self.background().color()

			def serializeProperty(self) -> str:
				return self.background().color().name()

		item = TableWidgetItem(caption, name, color, callback)
		TableWidgetProperty.__addProperty(table, caption, item)
		if applyNow and callback:
			callback(name, item.getProperty())

	@staticmethod
	def addPropertyBool(table: QtWidgets.QTableWidget, caption: str, name: str, value: bool, callback=None, applyNow=False):
		"""Property: tristate boolean (True, False, None)
			Example:
		self.addPropertyBool('Use background', 'background-user', True, self.__propertyUseBackgroundChanged)
		def __propertyBackgroundChanged(self, name: str, value: bool):
			pass
		"""

		class TableWidgetItem(TableWidgetProperty.IProperty, QtWidgets.QTableWidgetItem):

			def __init__(self, name: str, value: bool, changedCallback=None):
				TableWidgetProperty.IProperty.__init__(self, name, changedCallback)
				QtWidgets.QTableWidgetItem.__init__(self)
				self.setFlags(self.flags() & ~(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable))
				self.setProperty(value)

			def uiProperty(self) -> bool:
				# OK pressed
				# self.setProperty(newValue)
				# if self.propertyChangedCallback:
				# 	self.propertyChangedCallback(self.propertyName, self.getProperty())
				return True

			def setProperty(self, value: bool):
				if value is None:
					self.setCheckState(QtCore.Qt.PartiallyChecked)
				else:
					self.setCheckState(QtCore.Qt.Checked if value else QtCore.Qt.Unchecked)

			def getProperty(self) -> bool:
				if self.checkState() == QtCore.Qt.PartiallyChecked:
					return None
				return True if self.checkState() == QtCore.Qt.Checked else False

			def serializeProperty(self) -> str:
				return str(self.getProperty())

		item = TableWidgetItem(name, value, callback)
		TableWidgetProperty.__addProperty(table, caption, item)
		if applyNow and callback:
			callback(name, item.getProperty())

	@staticmethod
	def addPropertyList(table: QtWidgets.QTableWidget, caption: str, name: str, value: list, callback=None, applyNow=False):
		"""Property: tristate boolean (True, False, None)
			Example:
		self.addPropertyList('Options', 'options', ['ABC', 'bcd'], self.__propertyOptionsChanged)
		def __propertyOptionsChanged(self, name: str, value: (int, str)):
			# value[0] - index, value[1] - str
			pass
		"""

		class ComboBoxWidget(TableWidgetProperty.IProperty, QtWidgets.QComboBox):

			def __init__(self, name: str, value: list, changedCallback=None):
				TableWidgetProperty.IProperty.__init__(self, name, changedCallback)
				QtWidgets.QComboBox.__init__(self)
				self.addItems(value)
				self.currentIndexChanged.connect(self.__currentIndexChanged)

			def __currentIndexChanged(self):
				if self.propertyChangedCallback:
					self.propertyChangedCallback(self.propertyName, (self.currentIndex(), self.currentText()))

			def uiProperty(self) -> bool:
				self.showPopup()
				return False

			def setProperty(self, value: int):
				self.setCurrentIndex(value)

			def getProperty(self) -> (int, str):
				return (self.currentIndex(), self.currentText())

			def serializeProperty(self) -> str:
				return str(self.currentIndex())

		item = ComboBoxWidget(name, value, callback)
		TableWidgetProperty.__addProperty(table, caption, None, item)
		if applyNow and callback:
			callback(name, item.getProperty())

	@staticmethod
	def __propertyValueItemByName(table: QtWidgets.QTableWidget, name: str):
		"Gets value item from properties table"
		for row in range(table.rowCount()):
			if table.item(row, 1).propertyName == name:
				return table.item(row, 1)
		return None

	@staticmethod
	def propertyValue(table: QtWidgets.QTableWidget, name: str):
		item = TableWidgetProperty.__propertyValueItemByName(table, name)
		return item.getProperty() if item else None

	@staticmethod
	def setPropertyValue(table: QtWidgets.QTableWidget, name: str, value):
		item = TableWidgetProperty.__propertyValueItemByName(table, name)
		if item:
			item.setProperty(value)

	@staticmethod
	def propertySerialize(table: QtWidgets.QTableWidget, name: str) -> str:
		item = TableWidgetProperty.__propertyValueItemByName(table, name)
		return item.serializeProperty() if item else ''
