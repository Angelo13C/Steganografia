from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import pyperclip 

from core.text import *
from gui.button.button import Button

from page import Page
from gui.field.text_field import TextField

class HideText(Page):
    def __init__(self, actionTip):
        super().__init__(actionTip)
        self.initialize()
    
    def initialize(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(150)
        layout.setContentsMargins(80, 40, 80, 40)
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))

        #Crea un layout verticale per i 2 text field di testo pubblico e privato
        fieldsLayout = QVBoxLayout()
        fieldsLayout.setAlignment(Qt.AlignCenter)
        fieldsLayout.setSpacing(80)
        fieldsLayout.setContentsMargins(0, 0, 0, 0)

        self.publicText = TextField("Testo pubblico")
        self.privateText = TextField("Testo privato")

        fieldsLayout.addWidget(self.publicText)
        fieldsLayout.addWidget(self.privateText)

        layout.addLayout(fieldsLayout)

        #Crea il bottone Nascondi che quando viene premuto, copia il testo "elaborato" negli appunti
        self.hideButton = Button("Nascondi")
        self.hideButton.pressed.connect(self.hideText)
        layout.addWidget(self.hideButton)

        self.setLayout(layout)

        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.fieldsLayout = fieldsLayout
    
    #Viene chiamata quando viene premuto il bottone Nascondi
    def hideText(self):
        publicText = self.publicText.text()
        privateText = self.privateText.text()

        #Se il testo privato è vuoto, non c'è nulla da nascondere...
        if privateText == "":
            self.setActionTip("Il testo privato è vuoto")
        else:
            #Converti il testo privato prima in binario, e poi da binaria a "nascosto".. poi il testo finale comprende il testo "nascosto" concatenato al testo pubblico
            finalText = binaryToHidden(stringToBinary(privateText)) + publicText
            #Copia il testo finale negli appunti
            pyperclip.copy(finalText)         

            #Informa l'utente del testo copiato negli appunti
            self.setActionTip("Il testo è stato copiato negli appunti")

    def paintEvent(self, _):
        self.hideButton.move(self.width() / 2 - self.hideButton.width() / 2, self.hideButton.y())
