# Author: http://electriccat.free.fr/
# Contact: electriccat@free.fr
# Github: https://github.com/electriccatblog/3615noel

import time

from picozero import pico_temp_sensor

from machine import Pin

#Local files
from ledstrip import *
from minitel  import *

#STAR xmas tree led on GPIO 13
led=Pin(13,Pin.OUT)

#Update Minitel screen info
def updateScreen():
    temp = pico_temp_sensor.temp
    ##Clear the screen
    for i in range(num_lignes-10):
        minitelWrite('\r\n')
    ##3615 Noel
    displayNoel()
    ##Infos
    minitelWrite( chr(24) + ' LED Etoile sapin : %s ' % statutLED )
    minitelWrite( '- Temperature : %i\r\n' % temp)
    minitelWrite( chr(24) + chr(24) + ' L1 pour allumer, L0 pour eteindre, LC pour clignoter\r\n')
    minitelWrite( chr(24) + ' RUBAN %i LEDS' % numpix)
    minitelWrite( ' - Brightness : %i (1/2  : -/+)  \r\n' % brightnessValue)
    minitelWrite( chr(24) + chr(24) + ' %s\r\n' % statusLedStrip)
    minitelWrite( chr(24) + ' Couleurs : B : blanc - BL : bleu - J : jaune - M : marron\r\n')
    minitelWrite( chr(24) + '            O : orange - R : rouge - V : vert - VI : violet\r\n')
    minitelWrite( chr(24) + '            Couleur RGB : <code r>,<code g>,<code b>. Ex : 255,100,10\r\n')
    minitelWrite( chr(24) + chr(24) + ' 0 : eteindre - <code couleur> : remplir ruban led - * : Reset\r\n') 
    minitelWrite( chr(24) + chr(24) + ' C : clignoter (on/off), C<number> : delai en ms, CP/CM : vitesse +/-\r\n')
    minitelWrite( chr(24) + chr(24) + ' P1 : Arc en ciel - FR : Drapeau FR -  A : algorithme - D : degrade\r\n')
    bip()

global blinkState, currentProg

statutLED = "ON"
statusLedStrip="OFF"

#Current Program: "" (none), fill, grad, algo
currentProg = ""
fillColor = ""

#gradient color 1 & 2
gradColor1 = ""
gradColor2 = ""
custom_color = (0,0,0)
#default brightness
brightnessValue = 50
brightnessOffset = 30

#Strip Led Blink variables
blink = False
blinkState = False
blinkCounter = -1
blinkSpeed = 500
#Led Blink variable
blinkLed = False
blinkStateLed = False
blinkCounterLed = -1

#Algo variables
algoEnabled = 0
algoChoice = 0
lastAlgoChoice = 0
currentLedChoice = 0
algoName = ""
lastAlgoName = ""
buffer = ''
#Algo color list
colorList = []
lastcolorList = []

updateScreen()
#list of colors 
colorChoicePrompt = getColours()

#Star led on
led.value(1)

def showLastLedStrip():
    if currentProg == "fill" or currentProg == "fillrgb" or currentProg == "rainbow" or currentProg == "fr" or currentProg == "grad":
        if currentProg == "fill":
            fillStrip(fillColor)
            ledstrip.show()
        elif currentProg == "fillrgb":
            ledstrip.fill(custom_color)
            ledstrip.show()
        elif currentProg == "rainbow":
            displayRainbow()
        elif currentProg == "fr":
            displayFRFlag()
        elif currentProg == "grad" and gradColor1!= "" and gradColor2!= "":
            ledChoice1 = getItemFromList(gradColor1)
            ledChoice2 = getItemFromList(gradColor2)
            displayGradient(ledChoice1, ledChoice2)

#Extract counter value for the strip led blink speed
def extractCounterValue(c):
    #Test if the first char is 'c'
    if len(c) > 1 and c[0] == 'C':
       #Remove the 1st char
       x = c[1:]
       print (x)
       if len(x) > 0:
           #Convert to intr
           try:
               y = int(x)
               print (y)
               if y < 90000 and y > 0:
                   print ("OK int")
                   return y
           except:
               print("not int")
    return -1
               
while True:
    _data = ser.read()
    #Strip LED Blink
    if blink == True and currentProg != "algo":
        blinkCounter += 1
        if blinkCounter > blinkSpeed:
            if blinkState == False:
                fillStrip('OFF')
                ledstrip.show()
                blinkState = True
                blinkCounter = -1
            else:
                showLastLedStrip()
                blinkState = False
                blinkCounter = -1
    #LED Blink
    if blinkLed == True:
        blinkCounterLed += 1
        if blinkCounterLed > 500:
            if blinkStateLed == False:
                led.value(0)
                blinkStateLed = True
                blinkCounterLed = -1
            else:
                led.value(1)
                blinkStateLed = False
                blinkCounterLed = -1
    if _data != None:
        buffer += _data.decode('ASCII')
        if '\r' in _data: # CR, \r
            validEntry = False
            inputvalue = buffer.replace('\r','').replace('\n','').upper()
            print(inputvalue)
            #Check if RGB
            if inputvalue.count(',') == 2:
                continueCheck = True
                r,g,b = inputvalue.split(',')
                try:
                    r_value = int(r)
                except:
                    print("not int")
                    continueCheck = False
                if r_value < 256 and r_value > -1 and continueCheck == True:
                    print (r_value)
                    try:
                        g_value = int(g)
                    except:
                        print("not int")
                        continueCheck = False
                    if g_value < 256 and g_value > -1 and continueCheck == True:
                        print (g_value)
                        try:
                            b_value = int(b)
                        except:
                            print("not int")
                            scontinue = False
                        if b_value < 256 and b_value > -1 and continueCheck == True:
                            print (b_value)
                            custom_color = (r_value, g_value, b_value)
                            bip()
                            ledstrip.fill(custom_color)
                            ledstrip.show()
                            validEntry = True
                            currentProg = "fillrgb"
                            statusLedStrip = "RGB " + inputvalue
                            buffer = ''
            #Reset screen
            elif inputvalue == '*':
                validEntry = True
            #Change brightness (1: -, 2: +)
            elif inputvalue == '1' or inputvalue == '2':
                if brightnessValue < 254 and inputvalue == '2':
                    brightnessValue += brightnessOffset
                elif brightnessValue > -1 and inputvalue == '1':
                    brightnessValue -= brightnessOffset
                if brightnessValue > 254:
                    brightnessValue = 255
                if brightnessValue < 0:
                    brightnessValue = 0
                ledstrip.brightness(brightnessValue)
                ledstrip.show()
                ledstrip.show()
                print(brightnessValue)
            #LED
            elif inputvalue == 'L0' or inputvalue == 'L1' or inputvalue == 'LC':
                ##LED OFF
                if inputvalue == 'L0':
                    led.value(0) 
                    statutLED = "OFF"
                    blinkLed = False
                    print( statutLED )
                    validEntry = True
                ##LED ON
                elif inputvalue == 'L1':
                    led.value(1)
                    statutLED = "ON"
                    blinkLed = False
                    print( statutLED )
                    validEntry = True
                ##Blinking LED
                elif inputvalue == 'LC' and statutLED == "ON":
                    if blinkLed == False:
                        blinkLed = True
                        print('blinkLed on')
                        blinkCounterLed = -1
                    else:
                        led.value(1)
                        blinkLed = False
                buffer = ''
            else:
                if inputvalue == 'C':
                    if blink == False:
                        blink = True
                        blinkCounter = -1
                    else:
                        showLastLedStrip()
                        blink = False
                elif inputvalue == 'CP' and blink == True and blinkSpeed > 0:
                        blinkSpeed -= 150
                        print (blinkSpeed)
                elif inputvalue == 'CM' and blink == True and blinkSpeed < 3000:
                        blinkSpeed += 150
                        print (blinkSpeed)
                #Counter value
                elif len(inputvalue) > 1 and inputvalue[0] == 'C':
                    testCount = extractCounterValue(inputvalue)
                    if testCount > -1:
                        blinkSpeed = extractCounterValue(inputvalue)
                        print (blinkSpeed)
                    else:
                        print (testCount)
                elif inputvalue == '0':
                    statusLedStrip="OFF"
                    fillStrip('OFF')
                    ledstrip.show()
                    blink = False 
                    validEntry = True
                #Algo OFF : fill if colour matches, P1/rainbow, P2/drapeau, A ou G = activer algo, 
                elif algoEnabled == 0:
                    #Fill LED
                    if existsInList(inputvalue) == True:
                        bip()
                        ledChoice = fillStrip(inputvalue)
                        validEntry = True
                        currentProg = "fill"
                        fillColor = inputvalue
                        statusLedStrip = ledChoice[2]
                    #stripLed Rainbow
                    if inputvalue == 'P1':
                        bip()
                        displayRainbow()
                        validEntry = True
                        statusLedStrip="Arc en ciel"
                        currentProg = "rainbow"
                        fillColor = ""
                    if inputvalue == 'FR':
                        bip()
                        displayFRFlag()
                        validEntry = True
                        statusLedStrip="Drapeau FR"
                        currentProg = "fr"
                        fillColor = ""
                    ##Algo or Gradient part 1
                    if inputvalue == 'A' or inputvalue == 'D':
                        algoEnabled = 1
                        ##Vider la liste colorList
                        colorList.clear()
                        fillColor = ""
                        minitelWrite( chr(24) + chr(24) )
                        if inputvalue == 'A':
                            if lastAlgoChoice > 0:
                                minitelWrite( ' Algorithme: choisir l\'une des valeurs suivantes :\r\n')
                                minitelWrite( chr(24) + chr(24) +  ' 3-4-5-6-10, D (dernier choix), ou Q pour Quitter\r\n')
                            else:
                                minitelWrite( ' Algorithme: choisir l\'une des valeurs suivantes :\r\n')
                                minitelWrite( chr(24) + chr(24) + ' 3-4-5-6-10 ou Q pour Quitter\r\n')
                            currentProg = "algo"
                        elif inputvalue == 'D':
                            currentLedChoice = 1
                            minitelWrite (' Degrade > Choisir la couleur %i\r\n' % currentLedChoice)
                            currentProg = "grad"
                            algoName = "Degrade "
                #Algo or Gradient Enabled
                elif algoEnabled == 1:
                    if currentProg == "algo":
                        print ("algoChoice %i " % algoChoice)
                        if inputvalue == "Q":
                            print ("exit")
                            algoEnabled = 0
                            algoChoice = 0
                            currentLedChoice = 0
                            algoName = ""
                            currentProg = ""
                            fillColor = ""
                            validEntry = True
                        elif algoChoice == 0:
                            if inputvalue!="Q" and inputvalue!="D" and inputvalue!="3" and inputvalue!="4" and inputvalue!="5" and inputvalue!="6" and inputvalue!="10":
                                minitelWrite( chr(24) + chr(24) + 'Choix invalide! Choisir une valeur 3-4-5-6-10, D (dernier choix), ou Q\r\n')
                            elif inputvalue=="D" and lastAlgoChoice > 0:
                                minitelWrite( chr(24) + chr(24) + ' Reponse = dernier choix\r\n')
                                print (lastAlgoChoice)
                                numLed = 0
                                for x in range(numpix):
                                    if numLed == lastAlgoChoice:
                                        numLed = 0
                                    updateLed(x,lastcolorList[numLed])
                                    numLed = numLed + 1
                                algoEnabled = 0
                                algoChoice = 0
                                currentLedChoice = 0
                                statusLedStrip = lastAlgoName
                                validEntry = True
                            else:
                                minitelWrite( chr(24) + chr(24) + ' Reponse = %s\r\n' % inputvalue)
                                algoName = "Algo " + inputvalue + " couleurs\r\n"
                                algoChoice = int(inputvalue)
                                minitelWrite( chr(24) + chr(24) )
                                minitelWrite (colorChoicePrompt)
                                minitelWrite ('\r\n' + chr(24) + chr(24) )
                                currentLedChoice = 1
                                minitelWrite (' > Choisir la couleur %i\r\n' % currentLedChoice)
                        elif algoChoice > 0:
                            if existsInList(inputvalue) == False:
                                minitelWrite( chr(24) + chr(24) + ' Choix couleur invalide\r\n'+ chr(24) + chr(24) )
                                minitelWrite (colorChoicePrompt)
                                minitelWrite( chr(24) + chr(24) )
                                minitelWrite (' > Choisir la couleur %i\r\n' % currentLedChoice)
                            else:
                                ledChoice = getItemFromList(inputvalue)
                                minitelWrite( chr(24) + chr(24) )
                                minitelWrite (' Reponse = %s\r\n' % ledChoice[2])
                                algoName = algoName + ledChoice[2] + " "
                                colorList.append(inputvalue)
                                if currentLedChoice == algoChoice:
                                    numLed = 0
                                    for x in range(numpix):
                                        if numLed == algoChoice:
                                            numLed = 0
                                        updateLed(x,colorList[numLed])
                                        numLed = numLed + 1
                                    statusLedStrip = algoName
                                    lastAlgoName = algoName
                                    #copy colorList to lastcolorList
                                    lastcolorList = colorList.copy()
                                    algoEnabled = 0
                                    lastAlgoChoice = algoChoice
                                    algoChoice = 0
                                    algoName = ""
                                    currentLedChoice = 0
                                    validEntry = True
                                else:
                                    currentLedChoice = currentLedChoice + 1
                                    minitelWrite( chr(24) + chr(24) )
                                    minitelWrite (' > Choisir la couleur %i\r\n' % currentLedChoice)
                    #gradient
                    elif currentProg == "grad":
                        if existsInList(inputvalue) == False:
                            minitelWrite( chr(24) + chr(24) + ' Choix couleur invalide\r\n')
                            minitelWrite( chr(24) + chr(24) )
                            minitelWrite (colorChoicePrompt)
                            minitelWrite ('\r\n')
                            minitelWrite( chr(24) + chr(24) )
                            minitelWrite (' > Choisir la couleur %i\r\n' % currentLedChoice)
                        else:
                            ledChoice = getItemFromList(inputvalue)
                            minitelWrite( chr(24) + chr(24) )
                            minitelWrite (' Reponse = %s\r\n' % ledChoice[2])
                            if currentLedChoice == 1:
                                gradColor1 = inputvalue
                                algoName = algoName + ledChoice[2] + " -> "
                                currentLedChoice = currentLedChoice + 1
                                minitelWrite( chr(24) + chr(24) )
                                minitelWrite (' > Choisir la couleur %i\r\n' % currentLedChoice)
                            elif currentLedChoice > 1:
                                algoName = algoName + ledChoice[2]
                                gradColor2 = inputvalue
                                print (gradColor1 + " " + gradColor2)
                                ledChoice1 = getItemFromList(gradColor1)
                                displayGradient(ledChoice1, ledChoice)
                                statusLedStrip= algoName
                                algoEnabled = 0
                                algoChoice = 0
                                algoName = ""
                                validEntry = True
            if validEntry and algoEnabled == 0:
                updateScreen()
            buffer = ''


