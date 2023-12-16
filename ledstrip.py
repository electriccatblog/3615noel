# Author: http://electriccat.free.fr/
# Contact: electriccat@free.fr
# Github: https://github.com/electriccatblog/3615noel
# Part of 3615noel project

#  LedStrip management

from argbled_lib import Neopixel
import random
import time

#Led colours
c_off = (0, 0, 0) #black, LED OFF
c_white = (255, 255, 255)
c_red = (255, 0, 0)
c_blue = (0, 0, 255)
c_green = (0, 255, 0)
c_yellow = (255, 255, 0)
c_orange = (255, 50, 0)
c_purple = (127, 0, 255)
c_brown = (188, 101, 29)

ledList = [('OFF', c_off, 'Off'), ('B', c_white, 'Blanc'), ('BL', c_blue, 'Bleu'), ('J', c_yellow, 'Jaune'), ('O', c_orange, 'Orange'), ('R', c_red, 'Rouge'), ('V', c_green, 'Vert'), ('VI', c_purple, 'Violet'), ('M', c_brown, 'Marron')]

# Number of LEDs
numpix = 1020

#Test if value exists
def existsInList(value):
    for i in ledList:
        if (i[0] == value):
            return True;
    return False;

def getItemFromList(value):
    index = 0
    for i in ledList:
        if (i[0] == value):
            return ledList[index];
        index = index + 1
    return null;

def getColours():
    result = "Choix Couleurs:\r\n";
    for i in ledList:
        result += i[0] + "=" + i[2] + " ";
    return result;

#Change the colour of a single LED (ledNumber) with the value given
def updateLed(ledNumber, value):
    ledChoice = getItemFromList(value);
    if (ledChoice):
        ledstrip.set_pixel(ledNumber, ledChoice[1])
        ledstrip.show()
        return ledChoice

#Change the colour of a list of LEDs based on the given number with the value 
def updateLedList(ledNumberList, value, progressiveMode):
    ledChoice = getItemFromList(value);
    if (ledChoice):
        for ledNumber in ledNumberList:
            ledstrip.set_pixel(ledNumber, ledChoice[1])
        if progressiveMode == True:
            ledstrip.show()
    return ledChoice

#Fill the entire strip with the colour
def fillStrip(value):
    ledChoice = getItemFromList(value)
    if(ledChoice):
        ledstrip.fill(ledChoice[1])
        ledstrip.show()
        return ledChoice

def displayFRFlag():
    numpixpercolor = int(numpix / 3)
    ledstrip.set_pixel_line(0, numpixpercolor, c_blue)
    numpixStartIndex = 1
    numpixEndIndex = 2
    ledstrip.set_pixel_line(numpixpercolor * numpixStartIndex + 1, numpixpercolor * numpixEndIndex, c_white)
    numpixStartIndex = 2
    ledstrip.set_pixel_line(numpixpercolor * numpixStartIndex + 1, numpix -1, c_red)
    ledstrip.show()

def displayRainbow():
    numpixpercolor = int(numpix / 6)
    #print('numpixpercolor %i ' % numpixpercolor)
    ledstrip.set_pixel_line_gradient(0, numpixpercolor, c_purple, c_blue)
    numpixStartIndex = 1
    numpixEndIndex = 2
    ledstrip.set_pixel_line_gradient(numpixpercolor * numpixStartIndex + 1, numpixpercolor * numpixEndIndex, c_blue, c_green)
    numpixStartIndex = numpixStartIndex+ 1
    numpixEndIndex = numpixEndIndex+ 1
    ledstrip.set_pixel_line_gradient(numpixpercolor * numpixStartIndex + 1, numpixpercolor * numpixEndIndex, c_green, c_yellow)
    numpixStartIndex = numpixStartIndex+ 1
    numpixEndIndex = numpixEndIndex+ 1
    ledstrip.set_pixel_line_gradient(numpixpercolor * numpixStartIndex + 1, numpixpercolor * numpixEndIndex, c_yellow, c_orange)
    numpixStartIndex = numpixStartIndex+ 1
    numpixEndIndex = numpixEndIndex+ 1
    ledstrip.set_pixel_line_gradient(numpixpercolor * numpixStartIndex + 1, numpixpercolor * numpixEndIndex, c_orange, c_red)
    numpixStartIndex = numpixStartIndex+ 1
    #print('numpixStartIndex %i ' % numpixStartIndex)
    ledstrip.set_pixel_line_gradient(numpixpercolor * numpixStartIndex + 1, numpix -1, c_red, c_brown)
    ledstrip.show()

def displayGradient(ledChoice1, ledChoice2):
    ledstrip.set_pixel_line_gradient(0, numpix - 1, ledChoice1[1], ledChoice2[1])
    ledstrip.show()

def displayAlgo(algoChoice, colorList, progressiveMode):
    numLed = 0
    for x in range(algoChoice):
        ledColorList = []
        for y in range(numpix):
            if numLed == algoChoice:
                numLed = 0
            if numLed == x:
                ledColorList.append(y)
            numLed = numLed + 1
        updateLedList(ledColorList,colorList[x],progressiveMode)
    if progressiveMode == False:
        ledstrip.show()

# Initialize LED string
ledstrip = Neopixel(numpix, 0, 28, "GRB")

brightness = 50
ledstrip.brightness(brightness)
##Switch off the LED
fillStrip('OFF')
ledstrip.show()
