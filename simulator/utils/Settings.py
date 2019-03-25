from PyQt5 import QtCore

class Settings:

	@staticmethod
	def init(organizationName='Odyssey', applicationName='Simulator'):
		QtCore.QCoreApplication.setOrganizationName(organizationName)
		QtCore.QCoreApplication.setApplicationName(applicationName)

	@staticmethod
	def fileName() -> str:
		"Settings file path & name"
		return QtCore.QSettings().fileName()

	@staticmethod
	def value(prefix: str, name: str, default=None) -> str:
		settings = QtCore.QSettings()
		ret = settings.value(prefix+'/'+name)
		return ret if ret is not None else default

	@staticmethod
	def setValue(prefix: str, name: str, value: str):
		settings = QtCore.QSettings()
		settings.setValue(prefix+'/'+name, value)
