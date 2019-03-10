from PyQt5 import QtCore

class Settings:

	@staticmethod
	def init():
		QtCore.QCoreApplication.setOrganizationName('Odyssey')
		QtCore.QCoreApplication.setApplicationName('Simulator')

	@staticmethod
	def fileName() -> str:
		"Settings file path & name"
		return QtCore.QSettings().fileName()

	@staticmethod
	def value(prefix: str, name: str) -> str:
		settings = QtCore.QSettings()
		return settings.value(prefix+'/'+name)

	@staticmethod
	def setValue(prefix: str, name: str, value: str):
		settings = QtCore.QSettings()
		settings.setValue(prefix+'/'+name, value)
