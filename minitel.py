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
    minitelWrite('\r\n                                                         By ElectricCat.free.fr')
    minitelWrite('\r\n')
    

# Open the serial link with the Minitel
# Pico - GP0:tx, GP1:rx
ser = UART( 0, 4800, bits=7, parity=0, stop=1 ) # 0: Parity EVEN
num_lignes = 24
