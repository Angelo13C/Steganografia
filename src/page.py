from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Page(QWidget):
    def __init__(self, actionTip):
        super().__init__()
        self.actionTip = actionTip

    def setActionTip(self, text):
        self.actionTip.setText(text)