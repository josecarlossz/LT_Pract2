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
BWres = 0
retardos = []
codec_param = []
BWll = []
BWst = []
salidaBWST = []
activar = 0
cambiar_codec = 0
idx_codec = 0
# mos = 0
# Nc = 0
# Nl = 0
# Pll = 0
# Tpll = 0
# Rr = 0
# J = 0
# Rorg = 0
# Ralg = []
# Rr = 0
# Rjitter_1 = 0
# Rdest = 0
# Rt1 = 0
# Rt2 = 0
# Rjitter_2 = 0
# Npaq1 = 0
# Npaq2 = 0
# BHT = 0 
# BWll_RTP = 0
# BWll_cRTP = 0
# BWll_RTP = 0
# BWST_cRTP = 0

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
        
        #Generacion informe
        self.button_informe.clicked.connect(self.crear_txt)
            
    def actualiza_valor(self):
        global retardos, calculado, Rt, bht, BWll, BWst, BWres, idx_codec, cambiar_codec, codec_param
        global mos, Nc, Nl, Pll, Tpll, Rr, J
        
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
        global BWst, BWres, salidaBWST
        
        self.label_BWSIPTRUNK_RTP.setText(str(BWst[0]) + ' Mbps')
        self.label_BWSIPTRUNK_cRTP.setText(str(BWst[1]) + ' Mbps')
        
        salida = func.comparaBW(BWres,BWst[0],BWst[1])
        salidaBWST = salida
        
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
            
            self.gridLayoutWidget_6.setEnabled(1)
            
    def combo_codec(self):
        global idx_codec, cambiar_codec
        
        cambiar_codec = 1
        self.spinBox_MOS.setEnabled(0)
        idx_codec = self.comboBox_CODEC.currentIndex()
        self.label_CODEC.setText(str(self.comboBox_CODEC.currentText()))
        self.showPage1()
        
    def crear_txt(self):
        global retardos, codec_param, Rt, BWres, salidaBWST, mos, Nc, Nl, Pll, Tpll, Rr, J, bht, BWll, BWst
        
        informe = open("informe_generado.txt", "w")
        
        informe.write("Se ha realizado el desarrollo de un software para el diseño de redes para VOIP.") 
        informe.write("Este proceso ha sido estudiado para dos buffer antijitter: [x1.5], [x2].\n\n")
        informe.write("Los parámetros de entrada que se han introducido son:\n")
        informe.write("Mos:" + str(mos) + "\n")
        informe.write("Número de empresas:" + str(Nc)+ "\n")
        informe.write("Número de lineas por cliente:" + str (Nl)+ "\n") 
        informe.write("Probabilidad de llamada:"+ str(Pll) + "%\n")
        informe.write("Tiempo medio de llamada:"+ str(Tpll)+ " minutos\n")
        informe.write("Ancho de banda de reserva:" +str(BWres)+ " Mbps\n" )
        informe.write("Retardo total:"+ str(Rt) + " ms\n")
        informe.write("Retardo de red:"+ str(Rr) + " ms\n")
        informe.write("Jitter total:" + str(J) + " ms\n")
        informe.write("\n")
        informe.write("Para el buffer antijitter [x1.5] se han obtenido los siguientes resultados:\n")
        informe.write("Un retardo conjunto, donde se tiene en cuenta el retardo codec+paquetizacion de:" + str(retardos[0]) + " ms\n")
        informe.write("Retardo algoritmico (look ahead):" + str(retardos[1])+ " ms\n")
        informe.write("Retardo de red:" +str(Rr)+" ms\n")
        informe.write("Retardo del buffer antijitter, en este caso (1.5 x J)=" +str(retardos[3])+ " ms\n")
        informe.write("Retardo de codificacion en el destino, (0.1 x VPS)="+ str(retardos[5])+ " ms\n")
        informe.write("Con los cuales obtenemos un Retardo total, mediante la suma de todos ellos, (Rconj + Ralg + Rr + Rjitter + Rdest)=" 
                      + str(retardos[6]) + " ms y un numero de paquetes RTP almacenados en el buffer =" + str(retardos[8]) + " paquetes\n")
        informe.write("\n\n")
        informe.write("Para el buffer antijitter [x2] se han obtenido los siguientes resultados:\n")
        informe.write("Un retardo conjunto, donde se tiene en cuenta el retardo codec+paquetizacion de:" +str(retardos[0]) + " ms\n")
        informe.write("Retardo algoritmico (look ahead):" + str(retardos[1]) + " ms\n")
        informe.write("Retardo de red:" +str(Rr)+" ms\n")
        informe.write("Retardo del buffer antijitter, en este caso (2 x J)=" +str(retardos[4])+" ms\n")
        informe.write("Retardo de codificacion en el destino, (0.1 x VPS)="+ str(retardos[5]) + " ms\n")
        informe.write("Con los cuales obtenemos un Retardo total, mediante la suma de todos ellos, (Rconj + Ralg + Rr + Rjitter + Rdest)=" 
                      + str(retardos[7]) + " ms y un numero de paquetes RTP almacenados en el buffer =" + str(retardos[9]) +" paquetes\n\n")

        informe.write("Teniendo en cuenta que el retardo total no debe superar " + str(Rt) + 
                      " ms, la opcion elegida debe ser aquella que da como resultado " + 
                      self.label_RetardoTotalFinal.text() + " ms, pues queda dentro del limite establecido.\n\n")
        
        informe.write("A continuación, se calculará el trafico de hora cargada:\n\n")
        informe.write("BHT=(Numero de empresas x Numero de lineas por cliente x Tiempo medio de llamada)/60 =" +str(bht) + " Erlangs\n\n")
        informe.write("Por último, tanto para el protocolo RTP como cRTP, se calculará el ancho de banda de una llamada y de SIPTRUNK. ")
        informe.write("Para conocer el ancho de banda de una llamada, debemos calcular la longitud de cabecera y la longitud del paquete en bits para cada protocolo, finalmente: \n\n")
        informe.write("Ancho de banda de una llamada(RTP)=> (Longitud total del paquete RTP x PPS)/1000 ="+ str(BWll[0]) + " kbps\n")
        informe.write("Ancho de banda de una llamada(cRTP)=> (Longitud total del paquete cRTP x PPS)/1000 ="+ str(BWll[1]) + " kbps\n")
        informe.write("Ancho de banda SIPTRUNK(RTP)=> Nllamadas x Ancho de banda de una llamada(RTP)/1000 =" + str(BWst[0]) + " Mbps\n")
        informe.write("ncho de banda SIPTRUNK(cRTP)=> Nllamadas x Ancho de banda de una llamada(cRTP)/1000 =" + str(BWst[1]) + " Mbps\n\n")

        
        informe.write("Por otra parte, como el ancho de banda disponible (en reserva) es de " +
                      str(BWres) + " Mbps, ")
        
        if (salidaBWST[0]):
            informe.write("el protocolo a usar con este codec debe ser RTP, ya que en este caso el" + 
                          "ancho de banda de SIP TRUNK es de " + self.label_BWSIPTRUNK_RTP.text())
        
        elif (salidaBWST[1]):
            informe.write("el protocolo a usar con este codec debe ser cRTP, ya que en este caso el " + 
                          "ancho de banda de SIP TRUNK es de " + self.label_BWSIPTRUNK_cRTP.text())
            
        elif (salidaBWST[0]==1 and salidaBWST[1]==1):
            informe.write("el protocolo a usar con este codec puede ser RTP o cRTP, ya que en este caso" + 
                          "ambos protocolos cumplen con el maximo ancho de banda establecido y es de " + 
                          self.label_BWSIPTRUNK_RTP.text() + " y " + self.label_BWSIPTRUNK_cRTP.text() + 
                          ", respectivamente. Preferiblemente debe escogerse cRTP para una mayor compresion.")
            
        elif (salidaBWST[0]==0 and salidaBWST[1]==0):
            informe.write("y el ancho de banda de SIP TRUNK calculado para RTP y cRTP es de " + 
                          self.label_BWSIPTRUNK_RTP.text() + " y " + self.label_BWSIPTRUNK_cRTP.text() + 
                          " respectivamente, no es posible implementar este codec con los parametros de" +
                          " entrada introducidos, por lo que sera necesario elegir otro codec o cambiar los parametros de entrada.")
        informe.close()
        

if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	windows = MainWindows()
	windows.show()
	app.exec_()


