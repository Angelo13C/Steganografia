from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from pages.hide_text import HideText
from pages.hide_image import HideImage
from pages.reveal_image import RevealImage
from pages.reveal_text import RevealText
from pages.empty_page import EmptyPage

from gui.button.checkbox import Checkbox
from gui.button.button_group import ButtonGroup

import gui

class Window(QWidget):
    def __init__(self, title, iconPath):
        self.actionTip = None
        self.scrollArea = None

        super().__init__()
        self.initialize(title, iconPath)
        
        self.changePage()
    
    #Inizializza la finestra creando la testa, il corpo e il piede dell'applicazione
    def initialize(self, title, iconPath):
        #Personalizza icona e titolo della finestra
        windowIcon = QPixmap(iconPath)
        if windowIcon.isNull():
            windowIcon = QPixmap("Codice/" + iconPath)
        self.setWindowIcon(QIcon(windowIcon))
        self.setWindowTitle(title)
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.show()

        self.actionTip = self.createActionTip()

        #Crea una palette colori
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#2F2F2F"))
        palette.setColor(QPalette.WindowText, QColor("#c4c4c4"))
        palette.setColor(QPalette.Base, QColor("#121212"))
        palette.setColor(QPalette.Text, QColor("#c4c4c4"))
        self.setPalette(palette)

        #Crea un layout verticale in modo da avere testa, corpo e piede uno sotto l'altro
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(30)
        layout.setAlignment(Qt.AlignCenter)

        credits = self.createCredits()
        
        #Inizialmente crea una pagina vuota, che però non durerà neanche per pochi instanti, visto che poco dopo viene cambiata la pagina nel costruttore
        self.page = EmptyPage(self.actionTip)

        #Fai in modo che il corpo della finestra sia "scrollabile" se il suo contenuto non ci entra (mostrando una slider bar al lato destro)
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMaximumHeight(self.height())
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setContentsMargins(0, 0, 0, 0)
        self.scrollArea.verticalScrollBar().setStyleSheet("""
        QScrollBar:vertical 
        {
            border: 0px;
            background-color: #252525;
            border-radius: 6px;
            width: 13px;    
            margin: 0px 0px 0px 0px;
        }

        QScrollBar::handle 
        {
            background: #96B3D5;
            border: 0px;
            border-radius: 6px;
        }

        QScrollBar::add-line:vertical 
        {
            height: 0px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }

        QScrollBar::sub-line:vertical 
        {
            height: 0 px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }

        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        """)
        self.scrollArea.setViewportMargins(0, 0, 20, 0)

        self.foot = self.createFoot()
        
        layout.addWidget(credits)
        #layout.addWidget(self.page)
        layout.addWidget(self.scrollArea)
        layout.addWidget(self.foot)
        layout.setStretchFactor(self.page, 1)
        self.setLayout(layout)

    #Crea il piede della finestra (il quale permette di scegliere se nascondere il testo, rivelarlo, nascondere un immagine o rivelarla)
    def createFoot(self):
        foot = QWidget()
        foot.setStyleSheet("""
            background: #252525;
        """)
        foot.setFixedHeight(120)
        foot.setAutoFillBackground(True)
        foot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        footLayout = QHBoxLayout()
        footLayout.setSpacing(40)
        footLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        
        #Crea un layout verticale per i bottoni Nascondi e Rivela
        modeLayout = QVBoxLayout()
        modeLayout.setSpacing(5)
        CHECKBOX_SIZE = QSize(180, 40)
        self.hideCheckbox = Checkbox("Nascondi")
        self.hideCheckbox.setFixedSize(CHECKBOX_SIZE)
        modeLayout.addWidget(self.hideCheckbox)
        self.revealCheckbox = Checkbox("Rivela")
        self.revealCheckbox.setFixedSize(CHECKBOX_SIZE)
        modeLayout.addWidget(self.revealCheckbox)
        self.modeButtonGroup = ButtonGroup(True)
        
        #Crea un layout verticale per i bottoni Testo e Immagine
        contentLayout = QVBoxLayout()
        contentLayout.setSpacing(5)
        CHECKBOX_SIZE = QSize(180, 40)
        self.textCheckbox = Checkbox("testo")
        self.textCheckbox.setFixedSize(CHECKBOX_SIZE)
        contentLayout.addWidget(self.textCheckbox)
        self.imageCheckbox = Checkbox("immagine")
        self.imageCheckbox.setFixedSize(CHECKBOX_SIZE)
        contentLayout.addWidget(self.imageCheckbox)
        self.contentButtonGroup = ButtonGroup(True)
        
        #Metti tutti i bottoni (o meglio checkbox) di sopra in due gruppi in modo che solo uno tra Nascondi e Rivela sia selezionato e la stessa cosa per Testo e Immagine
        self.modeButtonGroup.addButton(self.hideCheckbox)
        self.modeButtonGroup.addButton(self.revealCheckbox)

        self.contentButtonGroup.addButton(self.textCheckbox)
        self.contentButtonGroup.addButton(self.imageCheckbox)
        
        #Connetti il click del bottone con il cambio della pagina
        self.hideCheckbox.changed.connect(self.changePage)
        self.revealCheckbox.changed.connect(self.changePage)
        self.textCheckbox.changed.connect(self.changePage)
        self.imageCheckbox.changed.connect(self.changePage)

        footLayout.addLayout(modeLayout)
        footLayout.addLayout(contentLayout)
        foot.setLayout(footLayout)
        
        footLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))

        return foot

    #Crea la scritta dei crediti da mostrare nella testa della finestra
    def createCredits(self):
        credits = QLabel("Angelo Cipriani")
        credits.setStyleSheet("""
            font-family: 'Inter';
            font-style: normal;
            font-weight: 400;
            font-size: 22px;
            line-height: 27px;
            text-align: center;

            color: rgba(255, 255, 255, 60%);
        """)
        credits.setFixedHeight(60)
        credits.setAlignment(Qt.AlignCenter)

        return credits
    
    #Cambia la pagina, mostrando quella corretta tra Nascondi testo, Rivela testo, Nascondi immagine e Rivela immagine
    def changePage(self):
        self.actionTip.setText("")

        mode = self.modeButtonGroup.pressedButton()
        content = self.contentButtonGroup.pressedButton()

        if mode == self.hideCheckbox:
            if content == self.textCheckbox:
                newPage = HideText(self.actionTip)
                self.setMinimumSize(640, 900)
            elif content == self.imageCheckbox:
                newPage = HideImage(self.actionTip)

        elif mode == self.revealCheckbox:
            if content == self.textCheckbox:
                newPage = RevealText(self.actionTip)
            elif content == self.imageCheckbox:
                newPage = RevealImage(self.actionTip)
        
        if self.scrollArea.widget() != None:
            self.scrollArea.takeWidget().deleteLater()
        self.scrollArea.setWidget(newPage)
    
    #Crea la scritta in basso che da un indizio all'utente su cosa sta facendo l'applicazione (tipo "Testo copiato negli appunti"..)
    def createActionTip(self):
        actionTip = QLabel(self)
        actionTip.setParent(self)
        actionTip.setFixedSize(500, 30)
        actionTip.setAutoFillBackground(True)
        actionTip.setAlignment(Qt.AlignCenter)
        actionTip.setStyleSheet("""            
            font-family: 'Inter';
            font-style: normal;
            font-weight: 400;
            font-size: 14px;
            line-height: 17px;

            color: #FFFFFF;
            background-color: transparent;
        """)
        actionTip.show()

        return actionTip

    def resizeEvent(self, event):
        if self.actionTip != None:
            self.actionTip.move(self.width() / 2 - self.actionTip.width() / 2, self.height() - 160)
        if self.scrollArea != None:   
            self.scrollArea.setMaximumHeight(self.height())
            self.scrollArea.setMinimumSize(self.page.minimumSize())