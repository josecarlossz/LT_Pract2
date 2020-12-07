# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 12:54:39 2020

@author: Sergio, Jose Carlos, Manuel, Alejandro
"""

from main_ui import *
import functions as func
import numpy as np

codecs = np.loadtxt(open("codecs.csv", "rb"), delimiter=";")
Ralg = np.loadtxt(open("ralg.csv", "rb"), delimiter=";")
calculado = 0
retardos = []

class MainWindows(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.showPage1()
        
    def showPage1(self):
        self.stackedWidget.setCurrentWidget(self.page)
        self.button_continuar1.clicked.connect(self.showPage2)
        self.cambiavalor_page1()
        
    def showPage2(self):
        global calculado
        self.stackedWidget.setCurrentWidget(self.page_2)
        
        if (calculado == 1):
            a = 0 #CAMBIAR
        
        self.button_continuar2.clicked.connect(self.showPage3)
		
    def showPage3(self):
        self.stackedWidget.setCurrentWidget(self.page_3)
        self.button_cambiarParametros.clicked.connect(self.showPage1)
        
        
    def calculos(self):
        global retardos, calculado
        
        mos = self.spinBox_MOS.value()
        Nc = self.spinBox_Nc.value()
        Nl = self.spinBox_Nl.value()
        Tpll = self.SpinBox_Tpll.value()
        Pll = self.spinBox_Pll.value()
        BWres = self.spinBox_BWres.value()
        Rt = self.spinBox_Rt.value()
        Rr = self.spinBox_Rr.value()
        J = self.spinBox_jitter.value()
        
        idx_codec = func.elige_codec(mos, codecs)
        codec_param = codecs[:,idx_codec]
        
        retardos = func.retardo_total(Rr, J, codec_param[4], codec_param[1], Ralg[idx_codec])
        
        calculado = 1
        
    def cambiavalor_page1(self):
        self.spinBox_MOS.valueChanged.connect(self.calculos)
        self.spinBox_Nc.valueChanged.connect(self.calculos)
        self.spinBox_Nl.valueChanged.connect(self.calculos)
        self.SpinBox_Tpll.valueChanged.connect(self.calculos)
        self.spinBox_Pll.valueChanged.connect(self.calculos)
        self.spinBox_BWres.valueChanged.connect(self.calculos)
        self.spinBox_Rt.valueChanged.connect(self.calculos)
        self.spinBox_Rr.valueChanged.connect(self.calculos)
        self.spinBox_jitter.valueChanged.connect(self.calculos)
        
if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	windows = MainWindows()
	windows.show()
	app.exec_()


