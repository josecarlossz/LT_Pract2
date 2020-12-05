# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 12:54:39 2020

@author: Sergio, Jose Carlos, Manuel, Alejandro
"""

from main_ui import *

class MainWindows(QtWidgets.QMainWindow, Ui_MainWindow,):
	def __init__(self, *args, **kwargs):
		QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
		self.setupUi(self)

# 		self.lPruebas.setText("Aquí con mis cosas")
# 		self.pbCalcular.setText("Hacer cosas")
# 		self.pbCalcular.clicked.connect(self.actualizarBoton)

# 	def actualizarBoton(self):
# 		self.lPruebas.setText("Pos sa acabó")
# 		self.tabWidget.setEnabled(1)

		
	pass


if __name__ == "__main__":
	app = QtWidgets.QApplication([]) #Pasar los parámetros
	windows = MainWindows()
	windows.show()
	app.exec_()


