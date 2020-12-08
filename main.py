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
Rt = 0
bht = 0
retardos = []
BWll = []
BWst = []
activar = 0
cambiar_codec = 0
idx_codec = 0

class MainWindows(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.showPage1()
        
        if (activar==0):
            self.gridLayoutWidget_6.setEnabled(0)
        
    def showPage1(self):
        global cambiar_codec, idx_codec
        
        self.stackedWidget.setCurrentWidget(self.page)
        
        if (cambiar_codec == 0):
            self.spinBox_MOS.setEnabled(1)
            
        self.button_continuar1.clicked.connect(self.showPage2)
        self.cambiavalor_page1()
        
        cambiar_codec = 0
        
    def showPage2(self):
        self.stackedWidget.setCurrentWidget(self.page_2)
        
        self.button_continuar2.clicked.connect(self.showPage3)
        self.button_calcularRt.clicked.connect(self.muestra_Rt)
		
    def showPage3(self):
        global cambiar_codec, idx_codec
        
        self.stackedWidget.setCurrentWidget(self.page_3)
        
        self.button_BHT.clicked.connect(self.muestra_bht)
        self.button_BWll.clicked.connect(self.muestra_bwll)
        self.button_BWSIPTRUNK.clicked.connect(self.muestra_bwst)
        
        #Cambiar de CODEC
        self.comboBox_CODEC.activated.connect(self.combo_codec)
          
        #Cambiar parametros de entrada
        self.button_cambiarParametros.clicked.connect(self.showPage1)
            
    def actualiza_valor(self):
        global retardos, calculado, Rt, bht, BWll, BWst, BWres, idx_codec, cambiar_codec
        
        mos = self.spinBox_MOS.value()
        Nc = self.spinBox_Nc.value()
        Nl = self.spinBox_Nl.value()
        Tpll = self.SpinBox_Tpll.value()
        Pll = self.spinBox_Pll.value()
        BWres = self.spinBox_BWres.value()
        Rt = self.spinBox_Rt.value()
        Rr = self.spinBox_Rr.value()
        J = self.spinBox_jitter.value()
        
        #Identificamos CODEC
        if cambiar_codec==0: 
            idx_codec = func.elige_codec(mos, codecs)
            self.comboBox_CODEC.setCurrentIndex(idx_codec)
            
        codec_param = codecs[idx_codec,:]
        
        #Calculamos valores con las funciones disenadas
        retardos = func.retardo_total(Rr, J, codec_param[4], codec_param[1], Ralg[idx_codec])
        bht = func.calculo_BHT(Nc,Nl,Tpll)
        BWll = func.calculo_BWll(codec_param[0],codec_param[1],codec_param[3])
        BWst = func.calculo_BWST(bht,Pll,BWll[0],BWll[1])
        
        #Actualizamos el CODEC en funcion del MOS y las etiquetas de la 'tabla'
        self.label_VPS.setText(str(codec_param[4]))
        
        if (cambiar_codec==0):
            self.label_CODEC.setText(self.comboBox_CODEC.itemText(idx_codec))
        
        self.label_RetardoConjunto1.setText(str(retardos[0]) + ' ms')
        self.label_RetardoConjunto2.setText(str(retardos[0]) + ' ms')
        self.label_RetardoAlgoritmico1.setText(str(retardos[1]) + ' ms')
        self.label_RetardoAlgoritmico2.setText(str(retardos[1]) + ' ms')
        self.label_RetardoRed1.setText(str(retardos[2]) + ' ms')
        self.label_RetardoRed2.setText(str(retardos[2]) + ' ms')
        self.label_RetardoAntijitter1.setText(str(retardos[3]) + ' ms')
        self.label_RetardoAntijitter2.setText(str(retardos[4]) + ' ms')
        self.label_RetardoDecodificacion1.setText(str(retardos[5]) + ' ms')
        self.label_RetardoDecodificacion1_2.setText(str(retardos[5]) + ' ms')
        
    def cambiavalor_page1(self):
        self.spinBox_MOS.valueChanged.connect(self.actualiza_valor)
        self.spinBox_Nc.valueChanged.connect(self.actualiza_valor)
        self.spinBox_Nl.valueChanged.connect(self.actualiza_valor)
        self.SpinBox_Tpll.valueChanged.connect(self.actualiza_valor)
        self.spinBox_Pll.valueChanged.connect(self.actualiza_valor)
        self.spinBox_BWres.valueChanged.connect(self.actualiza_valor)
        self.spinBox_Rt.valueChanged.connect(self.actualiza_valor)
        self.spinBox_Rr.valueChanged.connect(self.actualiza_valor)
        self.spinBox_jitter.valueChanged.connect(self.actualiza_valor)
        
    def muestra_Rt(self):
        global retardos, Rt, activar
        
        self.label_RetardoTotal1.setText(str(retardos[6]) + ' ms')
        self.label_RetardoTotal2.setText(str(retardos[7]) + ' ms')
        self.label_NpaquetesRTP1.setText(str(retardos[8]) + ' paquetes')
        self.label_NpaquetesRTP2.setText(str(retardos[9]) + ' paquetes')
        
        salida = func.comparaRt(Rt,retardos[6],retardos[7])
        
        if (salida[0]):
            self.label_RetardoTotalFinal.setText(str(retardos[6]))
            self.label_BufferAntijitterElegido.setText("x1.5")
            self.label_RetardoTotalFinal.setStyleSheet("background-color: yellow")
            self.label_RetardoTotal1.setStyleSheet("background-color: lightgreen")
            self.label_RetardoTotal2.setStyleSheet("background-color: red")
        
        elif (salida[1]):
            self.label_RetardoTotalFinal.setText(str(retardos[7]))
            self.label_BufferAntijitterElegido.setText("x2")
            self.label_RetardoTotalFinal.setStyleSheet("background-color: yellow")
            self.label_RetardoTotal2.setStyleSheet("background-color: lightgreen")
            self.label_RetardoTotal1.setStyleSheet("background-color: red")
            
        elif (salida[0]==1 and salida[1]==1):
            self.label_RetardoTotalFinal.setText(str(retardos[7]))
            self.label_BufferAntijitterElegido.setText("x2")
            self.label_RetardoTotalFinal.setStyleSheet("background-color: yellow")
            self.label_RetardoTotal2.setStyleSheet("background-color: lightgreen")
            self.label_RetardoTotal1.setStyleSheet("background-color: lightgreen")
        
        elif (salida[0]==0 and salida[1]==0):
            self.label_RetardoTotalFinal.setText("NO CUMPLE")
            self.label_BufferAntijitterElegido.setText("-")
            self.label_RetardoTotalFinal.setStyleSheet("background-color: yellow")
            self.label_RetardoTotal1.setStyleSheet("background-color: red")
            self.label_RetardoTotal2.setStyleSheet("background-color: red")
        
    def muestra_bht(self):
        global bht
        
        self.label_BHT.setText(str(bht) + ' Erlangs')
        
    def muestra_bwll(self):
        global BWll
        
        self.label_BWll_RTP.setText(str(BWll[0]) + ' Kbps')
        self.label_BWll_cRTP.setText(str(BWll[1]) + ' Kbps')

    def muestra_bwst(self):
        global BWst, BWres
        
        self.label_BWSIPTRUNK_RTP.setText(str(BWst[0]) + ' Mbps')
        self.label_BWSIPTRUNK_cRTP.setText(str(BWst[1]) + ' Mbps')
        
        salida = func.comparaBW(BWres,BWst[0],BWst[1])
        
        if (salida[0]):
            self.label_BWSIPTRUNK_RTP.setStyleSheet("background-color: lightgreen")
            self.label_BWSIPTRUNK_cRTP.setStyleSheet("background-color: red")
        
        elif (salida[1]):
            self.label_BWSIPTRUNK_RTP.setStyleSheet("background-color: red")
            self.label_BWSIPTRUNK_cRTP.setStyleSheet("background-color: lightgreen")
            
        elif (salida[0]==1 and salida[1]==1):
            self.label_BWSIPTRUNK_RTP.setStyleSheet("background-color: lightgreen")
            self.label_BWSIPTRUNK_cRTP.setStyleSheet("background-color: lightgreen")
        
        elif (salida[0]==0 and salida[1]==0):
            self.label_BWSIPTRUNK_RTP.setStyleSheet("background-color: red")
            self.label_BWSIPTRUNK_cRTP.setStyleSheet("background-color: red")
            
            activar = 1
            self.gridLayoutWidget_6.setEnabled(1)
            
    def combo_codec(self):
        global idx_codec, cambiar_codec
        
        cambiar_codec = 1
        self.spinBox_MOS.setEnabled(0)
        idx_codec = self.comboBox_CODEC.currentIndex()
        self.label_CODEC.setText(str(self.comboBox_CODEC.currentText()))
        self.showPage1()
        

if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	windows = MainWindows()
	windows.show()
	app.exec_()


