from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#Funzione per fare un interpolazione lineare di un colore (per fare l'animazione tra colori)
def lerpColor(start, end, time):
    r = time * start.red() + (1-time)*end.red()
    g = (time * start.green() + (1 - time)*end.green())
    b = (time * start.blue() + (1 - time)*end.blue())
    a = (time * start.alpha() + (1 - time)*end.alpha())
    return QColor(r, g, b, a)