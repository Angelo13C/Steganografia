from os import getcwd
from threading import Thread
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from core import image
from gui.button.button import Button
from gui.field.file_field import FileField

from page import Page

class RevealImage(Page):
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

        #Crea il layout verticale per il bottone per scegliere il file dell'immagine pubblica, e il bottone per rivelare l'immagine nasccosta al suo interno
        upperLayout = QVBoxLayout()
        upperLayout.setAlignment(Qt.AlignCenter)
        upperLayout.setSpacing(80)
        upperLayout.setContentsMargins(0, 0, 0, 0)

        self.publicImage = FileField("Immagine pubblica", fileDialogFilter="File immagini (*.png)")
        self.publicImage.fileChosen.connect(self.imageHasBeenSelected)
        self.revealButton = Button("Rivela")
        self.revealButton.pressed.connect(self.revealImage)

        upperLayout.addWidget(self.publicImage)
        upperLayout.addWidget(self.revealButton)

        layout.addLayout(upperLayout)

        self.setLayout(layout)

        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
    
    #Dato che la manipolazione delle immagini è molto lenta in python, quando l'utente ha selezionato l'immagine, parte un thread che inizia a "trovare" già l'immagine nascosta, in modo che quando l'utente clicchi il bottone debba aspettare di meno 
    def imageHasBeenSelected(self):
        #Se è stata selezionata una nuova immagine, uccidi il thread vecchio che stava già trovando l'immagine nascosta vecchia
        if self.hiddenProcessingThread != None and self.hiddenProcessingThread.is_alive():
            self.hiddenProcessingThread.setName("E")
        #Fai partire il thread
        if self.publicImage.chosenFilepath() != None:
            self.hiddenProcessingThread = Thread(target = self.processHidden, daemon=False)
            self.hiddenProcessingThread.start()
            self.hiddenProcessingThread.setName("S")
    
    def processHidden(self):
        self.privateImage = self.calculatePrivateImage()
    
    def calculatePrivateImage(self):
        finalImagePath = self.publicImage.chosenFilepath()
        finalImage = QImage(finalImagePath)

        return image.revealImage(finalImage)

    def revealImage(self):
        self.checkImageProcessing()

    #Quando l'utente preme il bottone rivela, se l'immagine elaborata nell'altro thread non è ancora disponibile, fai partire un timer di 0.5 secondi e controlla di nuovo dopo quel tempo, altrimenti salva l'immagine
    def checkImageProcessing(self):
        if self.hiddenProcessingThread != None:
            if self.hiddenProcessingThread.is_alive():
                self.setActionTip("Processando l'immagine...")
                QTimer.singleShot(500, self.checkImageProcessing)
            else:            
                self.setActionTip("")

                privateImage = self.privateImage
                
                #Fai aprire un file dialog per far scegliere all'utente dove salvare l'immagine e come chiamarla
                privateImagePath, _ = QFileDialog.getSaveFileName(self, "Salva l'immagine nascosta",
                                                    getcwd(),"File immagini (*.png)")
                
                if privateImagePath != "":
                    privateImage.save(privateImagePath)