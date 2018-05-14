from __future__ import division
import sys
import urllib, json
import numpy as np
import math
import itertools
import string
import copy
import time
import datetime as dt
from ast import literal_eval
import csv
import os
os.chdir( os.path.dirname(__file__) )
from os.path import isfile, join

# -----------------------------
def flujosCaja( costes, ingresos ):
    fc = []
    for i,c in enumerate( costes ) :
        fc.append( ingresos[i] - costes[i] )
    return fc

def roi( inversion, costes, ingresos ):
    res = ( sum( ingresos ) - ( inversion + sum( costes  ) ) ) / ( inversion + sum( costes  ) )
    return  round( res, 3 ) * 100

def vanPeriodo( nPeriodo, fc, tir ):
    vanPer =   fc / ( 1 + (tir/100) )**nPeriodo
    return round( vanPer, 2 )

def vanTotal( periodos, ii, tir_100, fc  ):
    res = 0
    res += -(ii)
    buf = []
    for p in range( periodos ):
        vanPer = vanPeriodo( (p+1), fc[p], tir_100  )
        res +=   vanPer
        buf.append( round( res , 2 ) )
    return [ round( res, 2 ), buf  ] # or buf

def calculateTir( tAprox, periodos, ii, fc ):
    iPos = tAprox[0]
    iNeg = tAprox[1]
    vanPosList =   vanTotal( periodos, ii, iPos , fc )
    vanNegList =   vanTotal( periodos, ii, iNeg , fc )
    vanPos = vanPosList[0]
    vanNeg = vanNegList[0]
    resTir =  (iPos/100) + ( (iNeg/100) - (iPos/100) ) * (  vanPos / ( vanPos - vanNeg ) )
    return { 
        "tir" : round( resTir*100 , 2),
        "vanPerPos" : vanPosList[1],
        "vanPerNeg" : vanNegList[1],
        "vanPos" : vanPosList[0],
        "vanNeg" : vanNegList[0]
    }

# -------------------------------------------------

'''
Cuando el van salga negativo no es conveniente realizar la inversion
Un valor positivo del VAN nos esta diciendo que, ademas del rendimiento minimo esperado

Cuando el tir es mayor a cero, el proyecto devuelve el capital invertido, mas una ganancia adicional
'''

num_periodos = 5
inversion_inicial = 35000
costes      = [ 7500, 7500, 7500, 7500, 7500 ]
ingresos    = [ 8500, 12000, 18000, 18000, 18000 ]
tasa_descuento = 11

i1 = tasa_descuento
i2 = tasa_descuento + 1

# Calcula los flujos de caja o definelos manualmente
#flujos_caja = [ 1000,4500,10500,10500,10500 ]
flujos_caja = flujosCaja( costes, ingresos )

#print vanTotal( num_periodos, inversion_inicial, tasa_descuento , flujos_caja  )
calc =  calculateTir( [ i1, i2 ] , num_periodos, inversion_inicial, flujos_caja  )

print "VAN: ", calc["vanPos"]
print "TIR: ", calc["tir"]
print "VAN por periodos: ", calc["vanPerPos"]
print "ROI:", roi( inversion_inicial, costes, ingresos )





