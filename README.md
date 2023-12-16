# 3615 Noel : Projet Raspberry Pico pour controler un ruban LED depuis un Minitel
Code en MicroPython � charger sur un Raspberry Pico W.
![photo](docs/3615noel-minitel-sapin.png)
## Fichiers
* main.py : programme principal lanc� automatiquement par le Pico au d�marrage
* minitel.py : liaison s�rie UART avec le minitel pour afficher le contenu � l'�cran
* ledstrip.py : fonctions pour le ruban Led WS2812B

## Librairies externes
* [Neopixel](https://github.com/blaz-r/pi_pico_neopixel)
* [PicoZero](https://pypi.org/project/picozero/)


## Installation
Modifier le code du fichier main.py pour adapter le nombre de led � piloter en fonction des rubans leds install�s.
Copier les 3 fichiers sur le Raspberry Pico.


Sch�ma Fritzing : 

![sch�ma Fritzing](docs/3615noel-fritzing.png)

Plus de d�tails disponibles sur le site [ElectricCat](http://electriccat.free.fr/3615noel/)

