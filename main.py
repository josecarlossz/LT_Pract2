# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 12:54:39 2020

@author: Sergio, Jose Carlos, Manuel, Alejandro
"""

from main_ui import *

class MainWindows(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.showPage1()
        
    def showPage1(self):
        self.stackedWidget.setCurrentWidget(self.page)
        self.button_continuar1.clicked.connect(self.showPage2)
        
    def showPage2(self):
        self.stackedWidget.setCurrentWidget(self.page_2)
        self.button_continuar2.clicked.connect(self.showPage3)
		
    def showPage3(self):
        self.stackedWidget.setCurrentWidget(self.page_3)
        self.button_cambiarParametros.clicked.connect(self.showPage1)

if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	windows = MainWindows()
	windows.show()
	app.exec_()


