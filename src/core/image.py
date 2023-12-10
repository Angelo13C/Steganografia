from threading import current_thread
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import math

#Grandezza di un canale
CHANNEL_SIZE = 256
#Numero di bit usati per nascondere l'immagine (più questo numero è alto, maggiore sarà la qualità dell'immagine nascosta.. Ma si vedrà più facilmente ad occhio nudo nell'immagine finale)
HIDING_BITS_COUNT = 3
#Calcoli che vengono fatti una sola volta per la maschera
POWER_OF_2 = (2 ** HIDING_BITS_COUNT - 1)
DIVISOR = CHANNEL_SIZE / POWER_OF_2

def hideImage(publicImage, privateImage):
    if publicImage.isNull() or privateImage.isNull():
        return None
    
    finalImage = QImage(publicImage)
    for y in range(privateImage.height()):
        #Uccidi il thread se l'utente ha cambiato immagine (controlla il file hide_text.py)    
        if current_thread().name == "E":
            return None
        
        #Crea una view di una riga dell'immagine finale che può essere modificata
        finalScanLine = finalImage.scanLine(y)
        finalScanLine.setsize(finalImage.byteCount())
        finalLineView = memoryview(finalScanLine)

        #Crea una view di una riga dell'immagine privata che può essere solo letta
        privateScanLine = privateImage.constScanLine(y)
        privateScanLine.setsize(privateImage.byteCount())
        privateLineView = memoryview(privateScanLine).toreadonly()

        #Nascondi in ogni canale di ogni pixel della riga dell'immagine finale, il canale di quello dell'immagine privata 
        for x in range(privateImage.width()):
            finalLineView[x * 4 + 0] = hideChannel(finalLineView[x * 4 + 0], privateLineView[x * 4 + 0])
            finalLineView[x * 4 + 1] = hideChannel(finalLineView[x * 4 + 1], privateLineView[x * 4 + 1])
            finalLineView[x * 4 + 2] = hideChannel(finalLineView[x * 4 + 2], privateLineView[x * 4 + 2])
        
        #Rilascia la view della riga quando ha finito di calcolare
        finalLineView.release()
        privateLineView.release()
    
    return finalImage

#Usa delle maschere per calcolare il nuovo valore del canale
def hideChannel(publicChannel, privateChannel):
    normalizedChannel = math.floor(privateChannel / DIVISOR)
    #Cancella parte del canale dell'immagine pubblica e poi rimpiazzalo con parte di quello privato (che è stato normalizzato)
    finalChannel = publicChannel & (CHANNEL_SIZE - POWER_OF_2)
    finalChannel |= normalizedChannel
    return finalChannel

#Rivela un'immagine nascosta dentro un'altra immagine
def revealImage(finalImage):
    if finalImage.isNull():
        return None
    
    for y in range(finalImage.height()):
        #Uccidi il thread se l'utente ha cambiato immagine (controlla il file reveal_text.py)   
        if current_thread().name == "E":
            return None
        
        #Crea una view di una riga dell'immagine finale
        finalScanLine = finalImage.scanLine(y)
        finalScanLine.setsize(finalImage.byteCount())
        finalLineView = memoryview(finalScanLine)
        #Per ogni pixel su quella riga, rivela il canale e mettilo nell'immagine finale
        for x in range(finalImage.width()):
            finalLineView[x * 4 + 0] = revealChannel(finalLineView[x * 4 + 0])
            finalLineView[x * 4 + 1] = revealChannel(finalLineView[x * 4 + 1])
            finalLineView[x * 4 + 2] = revealChannel(finalLineView[x * 4 + 2])
        
        finalLineView.release()
    
    return finalImage

#Rivela il canale nascosto di un pixel 
def revealChannel(finalChannel):
    powerOf2 = (2 ** HIDING_BITS_COUNT - 1)
    divisor = CHANNEL_SIZE / powerOf2
    #Cancella i pixel del canale pubblico e poi rimpiazzali
    finalChannel = finalChannel & powerOf2

    finalChannel *= divisor
    if finalChannel > 255:
        finalChannel -= 1
        
    return round(finalChannel)