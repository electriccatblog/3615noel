# Author: http://electriccat.free.fr/
# Contact: electriccat@free.fr
# Github: https://github.com/electriccatblog/3615noel
# Part of 3615noel project

#  Minitel

from machine import UART
import time

def bip():
    minitelWrite(chr(7))

def minitelWrite(text):
    ser.write(text.encode('ASCII'))
    time.sleep(0.002)
    
def displayNoel():
    minitelWrite('\r\n*******   ******   ******   *******   ***     ******   ******   ******   ******\r\n')
    minitelWrite('\r\n  $$$$     $$$$      $$     $$$$$$            $$  $$    $$$$    $$$$$$   $$')
    minitelWrite('\r\n $$  $$   $$  $$     $$     $$                $$$ $$   $$  $$   $$       $$')
    minitelWrite('\r\n     $$   $$        $$$     $$$$$             $$$$$$   $$  $$   $$       $$')
    minitelWrite('\r\n   $$$    $$$$$      $$         $$    $$$     $$$$$$   $$  $$   $$$$     $$')
    minitelWrite('\r\n     $$   $$  $$     $$         $$            $$ $$$   $$  $$   $$       $$')
    minitelWrite('\r\n $$  $$   $$  $$     $$     $$  $$            $$  $$   $$  $$   $$       $$')
    minitelWrite('\r\n  $$$$     $$$$    $$$$$$    $$$$             $$  $$    $$$$    $$$$$$   $$$$$$\r\n')
    minitelWrite('\r\n*******   ******   ******   *******   ***     ******   ******   ******   ******')
    minitelWrite('\r\n                                                                By Jack & Papa')
    minitelWrite('\r\n')  

def displayCat():
    minitelWrite('\r\n*******************************************************************************\r\n')
    minitelWrite('\r\n       _           _        _               _      __                  __      ')
    minitelWrite('\r\n      I I         I I      (_)             I I    / _I                / _I     ')
    minitelWrite('\r\n   ___I I ___  ___I I_ _ __ _  ___ ___ __ _I I_  I I_ _ __ ___  ___  I I_ _ __ ')
    minitelWrite('\r\n  / _ : I/ _ :/ __I __I  __I I/ __/ __/ _/ I __I I  _I I__/ _ :/ _ : I  _I  _I')
    minitelWrite('\r\n I  __/ I  __/ (__I I_I I  I I (_I (_I (_I I I_ _I I I I I  __/  __/_I I I I   ')
    minitelWrite('\r\n  :___I_I:___|:___I:__I_I  I_I:___:___:__,_I:__(_)Il I_I  :___I:___(_)_l I_I   ')
    minitelWrite('\r\n\r\n*******************************************************************************\r\n')
    minitelWrite('\r\n                                                         By ElectricCat.free.fr')
    minitelWrite('\r\n')
    
# Open the serial link with the Minitel
# Pico - GP0:tx, GP1:rx
ser = UART( 0, 4800, bits=7, parity=0, stop=1 ) # 0: Parity EVEN
num_lignes = 24
