# -*- coding: utf-8 -*-
"""
Funciones para calcular los diferentes parámetros del diseno VoIP

@authors: Jose Carlos, Sergio, Manuel, Alejandro
"""
import numpy as np

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