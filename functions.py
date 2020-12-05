# -*- coding: utf-8 -*-
"""
Funciones para calcular los diferentes parámetros del diseno VoIP

@authors: Jose Carlos, Sergio, Manuel, Alejandro
"""
import numpy as np
import erlang 

def retardo_total(Rr,J,VPS,CSI,Ralg):
    #Retardo conjunto, CODEC + paquetizacion
    Rorg = VPS + 0.1*CSI
    
    #Retardos buffer antijitter
    Rjitter_1 = 1.5*J
    Rjitter_2 = 2*J
    
    #Retardo de decodificacion en el destino
    Rdest = 0.1*VPS

    #Retardo total (buffer antijitter x1.5 y x2)
    Rt1 = Rorg + Ralg + Rr + Rjitter_1 + Rdest
    Rt2 = Rorg + Ralg + Rr + Rjitter_2 + Rdest
    
    #Calculamos el numero de paquetes almacenados en el buffer antijitter
    #en cada caso
    Npaq1 = Rjitter_1//VPS
    Npaq2 = Rjitter_2//VPS
    
    return Rorg, Ralg, Rr, Rjitter_1, Rjitter_2, Rdest, Rt1, Rt2, Npaq1, Npaq2


def comparaRt(Rtmax,Rt1,Rt2):
    salida = np.zeros(2)
    
    if (Rt1 <= Rtmax):
        salida[0] = 1
    if (Rt2 <= Rtmax):
        salida[1] = 1
    
    return salida


def calculo_BHT(Nc,Nl,Tpll):
    BHT=(Nc*Nl*Tpll)/60
    
    return BHT

def calculo_BWll(CSS,CSI,VPS):
    #Calculo de la longitud de la cabecera RTP
    #Ethernet 802.1q+PPP+IP+UDP+RTP
    Lcab_RTP=20+6+20+8+12
    #Longitud total del paquete en bits (RTP)
    Lpaq_RTP=(Lcab_RTP+VPS)*8
    
    #Calculo de la longitud de la cabecera cRTP
    #Ethernet 802.1q+PPP+(IP+UDP+RTP)/10
    Lcab_cRTP=20+6+4
    #Longitud total del paquete en bits (cRTP)
    Lpaq_cRTP=(Lcab_cRTP+VPS)*8
    
    #Calculo CBR (Codec Bit Rate)
    CBR=(CSS*8)/(CSI/1000)#Expresado en bps
    
    #Calculo PPS
    PPS=CBR/(VPS*8) #pps
    
    #Calculo ancho de banda de una llamada
    BWll_RTP=(Lpaq_RTP*PPS)/1000 #kbps
    BWll_cRTP=(Lpaq_cRTP*PPS)/1000 #kbps
    
    return BWll_RTP,BWll_cRTP

def calculo_BWST(BHT,Pb,BWll_RTP,BWll_cRTP):
    Nllamadas=erlang.extended_b_lines(BHT,Pb/100)
    BWST_RTP=Nllamadas*BWll_RTP/1000 #Mbps
    BWST_cRTP=Nllamadas*BWll_cRTP/1000 #Mbps
    
    return BWST_RTP,BWST_cRTP

def comparaBW(BWres,BWST_RTP,BWST_cRTP):
    salida = np.zeros(2)
    
    if (BWST_RTP <= BWres):
        salida[0] = 1
    if (BWST_cRTP <= BWres):
        salida[1] = 1
    
    return salida
    
    
    