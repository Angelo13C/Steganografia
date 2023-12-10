from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import pyperclip 

from core.text import *
from gui.button.button import Button

from page import Page
from gui.field.text_field import TextField

class RevealText(Page):
    def __init__(self, actionTip):
        super().__init__(actionTip)
        self.initialize()
    
    def initialize(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(100)
        layout.setContentsMargins(80, 40, 80, 40)
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))

        upperLayout = QVBoxLayout()
        upperLayout.setAlignment(Qt.AlignCenter)
        upperLayout.setSpacing(80)
        upperLayout.setContentsMargins(0, 0, 0, 0)

        self.publicText = TextField("Testo pubblico")

        self.hideButton = Button("Rivela")
        self.hideButton.pressed.connect(self.revealText)

        upperLayout.addWidget(self.publicText)
        upperLayout.addWidget(self.hideButton)

        #Crea la label (per adesso vuota) che mostrerà all'utente il testo privato rivelato
        self.privateText = QLabel("")
        self.privateText.setContentsMargins(50, 0, 50, 0)
        self.privateText.setAutoFillBackground(True)
        self.privateText.setAlignment(Qt.AlignCenter)
        self.privateText.setStyleSheet("""
            font-family: 'Inter';
            font-style: normal;
            font-weight: 400;
            font-size: 22px;
            line-height: 27px;

            text-align: center;

            color: #FFFFFF;
            background-color: transparent;
        """)

        layout.addLayout(upperLayout)
        layout.addWidget(self.privateText)

        self.setLayout(layout)

        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
    
    #Rivela il testo nascosto quando viene premuto il bottone Rivela
    def revealText(self):
        publicText = self.publicText.text()

        #Converti il testo "nascosto" in binario, e poi convertilo da binario a stringa
        privateText = binaryToString(hiddenToBinary(publicText))
        self.privateText.setText(privateText)

        #Se non è stato trovato nessun testo nascosto, informa l'utente
        if privateText == "":
            self.setActionTip("Non è stato trovato nessun testo nascosto!")
