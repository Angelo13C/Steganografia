from os import getcwd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from gui.button.button import Button

from .. import utils

PRIMARY_COLOR = QColor("#96B3D5")

BACKGROUND_TEXT_SPACING = 8
NO_FOCUS_BACKGROUND_COLOR = QColor("#ACACAC")

class FileField(QWidget):
    fileChosen = pyqtSignal()

    def __init__(self, descriptorText, placeholderText = "Inserisci qualcosa", backgroundHeight = 5, fileDialogFilter = "File immagini (*.jpg *.png)"):
        super().__init__()

        self.filepath = None
        self.fileDialogFilter = fileDialogFilter

        self.initialize(descriptorText, placeholderText, backgroundHeight)
    
    def initialize(self, descriptorText, placeholderText, backgroundHeight):
        self.backgroundHeight = backgroundHeight
        self.setFixedWidth(400)

        layout = QVBoxLayout()
        layout.setSpacing(40)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, BACKGROUND_TEXT_SPACING * 2)

        self.descriptor = QLabel(self)
        self.descriptor.setText(descriptorText)
        self.descriptor.setFixedHeight(41)
        self.descriptor.setAutoFillBackground(True)
        self.descriptor.setAlignment(Qt.AlignCenter)
        self.descriptor.setStyleSheet("""
            font-family: 'Inter';
            font-style: normal;
            font-weight: 800;
            font-size: 34px;
            line-height: 41px;

            color: #FFFFFF;
            background-color: transparent;
        """)

        self.chooseFileButton = Button("Scegli file")
        self.chooseFileButton.setFixedSize(200, 80)
        self.chooseFileButton.setTextStyle("""
            font-family: 'Inter';
            font-style: normal;
            font-weight: 700;
            font-size: 20px;
            line-height: 24px;
            text-align: center;

            background-color: transparent;
        """)
        self.chooseFileButton.pressed.connect(self.pressChooseFile)
        self.backgroundColor = PRIMARY_COLOR

        layout.addWidget(self.descriptor)
        layout.addWidget(self.chooseFileButton)
        self.chooseFileButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setLayout(layout)

        """
        self.animation = QVariantAnimation(
            self,
            valueChanged=self.animate,
            startValue=0.0,
            endValue=1.0,
            duration=250
        )"""
    
    def chosenFilepath(self):
        return self.filepath

    def pressChooseFile(self):
        if self.filepath == None:
            QTimer.singleShot(200, self.chooseFile)
        else:
            self.filepath = None
            self.chooseFileButton.getLabel().setText("Scegli file")
    
    def chooseFile(self):
        filepath, _ = QFileDialog.getOpenFileName(self, 'Apri immagine',
                    getcwd(), self.fileDialogFilter)

        if filepath == "":
            self.filepath = None
        else:
            self.filepath = filepath
            
            self.fileChosen.emit()
            self.chooseFileButton.getLabel().setText("Rimuovi file")

    def paintEvent(self, _):
        self.chooseFileButton.move(self.width() / 2 - self.chooseFileButton.width() / 2, self.chooseFileButton.y())
    