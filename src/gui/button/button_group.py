from tabnanny import check
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from gui.button.checkbox import Checkbox

class ButtonGroup(QWidget):
    def __init__(self, oneMustBeSelected = True):
        super().__init__()
        self.oneMustBeSelected = oneMustBeSelected
        self.initialize()
    
    def initialize(self):
        self.buttons = []
    
    def addButton(self, checkbox):
        checkbox.setButtonGroupIndex(len(self.buttons))
        checkbox.changed.connect(lambda index: self.onButtonChanged(index))
        self.buttons.append(checkbox)

        if self.oneMustBeSelected and len(self.buttons) == 1:
            checkbox.check()

    def pressedButton(self):
        for button in self.buttons:
            if button.checked:
                return button
        return None
    
    @pyqtSlot(int)
    def onButtonChanged(self, changedIndex):
        for index, button in enumerate(self.buttons):
            if index != changedIndex and button.checked:
                button.check(False)