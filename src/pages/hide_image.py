from os import getcwd
from threading import Thread, current_thread
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from core import image
from gui.button.button import Button
from gui.field.file_field import FileField

from page import Page
from gui.field.text_field import TextField

class HideImage(Page):
    def __init__(self, actionTip):
        super().__init__(actionTip)
        self.hiddenProcessingThread = None
        self.initialize()
    
    def initialize(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(100)
        layout.setContentsMargins(80, 40, 80, 40)
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))

        #Crea un layout verticale per i 2 campi di immagine pubblica e privata
        fieldsLayout = QVBoxLayout()
        fieldsLayout.setAlignment(Qt.AlignCenter)
        fieldsLayout.setSpacing(80)
        fieldsLayout.setContentsMargins(0, 0, 0, 0)

        self.publicImage = FileField("Immagine pubblica")
        self.privateImage = FileField("Immagine privata")

        self.publicImage.fileChosen.connect(self.imageHasBeenSelected)
        self.privateImage.fileChosen.connect(self.imageHasBeenSelected)
        fieldsLayout.addWidget(self.publicImage)
        fieldsLayout.addWidget(self.privateImage)

        layout.addLayout(fieldsLayout)

        #Crea il bottone Nascondi da premere per nascondere l'immagine
        self.hideButton = Button("Nascondi")
        self.hideButton.pressed.connect(self.hideImage)
        layout.addWidget(self.hideButton)

        self.setLayout(layout)

        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))

    #Dato che la manipolazione delle immagini è molto lenta in python, quando l'utente ha selezionato le 2 immagini, parte un thread a parte che calcola già la nuova immagine, in modo che quando l'utente clicchi il bottone debba aspettare di meno 
    def imageHasBeenSelected(self):
        #Se è stata selezionata una nuova immagine, uccidi il thread vecchio che stava già calcolando l'immagine da nascondere
        if self.hiddenProcessingThread != None and self.hiddenProcessingThread.is_alive():
            self.hiddenProcessingThread.setName("E")
        #Fai partire il thread
        if self.publicImage.chosenFilepath() != None and self.privateImage.chosenFilepath() != None:
            self.hiddenProcessingThread = Thread(target = self.processHidden, daemon=False)
            self.hiddenProcessingThread.start()
            self.hiddenProcessingThread.setName("S")
    
    def processHidden(self):
        self.finalImage = self.calculateFinalImage()
    
    def calculateFinalImage(self):
        publicImagePath = self.publicImage.chosenFilepath()
        privateImagePath = self.privateImage.chosenFilepath()

        publicImage = QImage(publicImagePath)
        privateImage = QImage(privateImagePath)
        
        return image.hideImage(publicImage, privateImage)

    def hideImage(self):
        self.checkImageProcessing()
    
    #Quando l'utente preme il bottone nascondi, se l'immagine elaborata nell'altro thread non è ancora disponibile, fai partire un timer di 0.5 secondi e controlla di nuovo dopo quel tempo, altrimenti salva l'immagine
    def checkImageProcessing(self):
        if self.hiddenProcessingThread != None:
            #Per vedere se l'immagine è stata già nascosta, basta vedere se il thread che la sta elaborando è ancora vivo.. Perchè quando finisce l'immagine, il thread finisce (visto che non c'è nessun loop infinito)
            if self.hiddenProcessingThread.is_alive():
                self.setActionTip("Processando l'immagine...")
                QTimer.singleShot(500, self.checkImageProcessing)
            else:            
                self.setActionTip("")

                finalImage = self.finalImage
                
                if finalImage != None:
                    #Fai aprire un file dialog per far scegliere all'utente dove salvare l'immagine e come chiamarla
                    finalImagePath, _ = QFileDialog.getSaveFileName(self, "Salva l'immagine finale",
                                                        getcwd(),"File immagini (*.png)")
                    
                    if finalImagePath != "":
                        pathInfo = QFileInfo(finalImagePath)
                        #L'IMMAGINE DEVE ESSERE IN .PNG PERCHE' E' LOSSLESS A DIFFERENZA DEL .JPG, E IL MIO ALGORITMO NON FUNZIONA CON I FILE JPG
                        finalImagePath = pathInfo.path() + "/" + pathInfo.completeBaseName() + ".png"
                        finalImage.save(finalImagePath)

    def paintEvent(self, _):
        self.hideButton.move(self.width() / 2 - self.hideButton.width() / 2, self.hideButton.y())
                        