from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .. import utils

PRIMARY_COLOR = QColor("#96B3D5")
SECONDARY_BACKGROUND_COLOR = QColor("#252525")

class Checkbox(QRadioButton):
    changed = pyqtSignal(int)

    def __init__(self, text, borderSize = 20):
        super().__init__()
        self.initialize(text, borderSize)
    
    def initialize(self, text, borderSize):
        self.label = QLabel(self)
        self.label.setText(text)
        self.label.setAutoFillBackground(True)
        self.label.setAlignment(Qt.AlignCenter)
        self.borderSize = borderSize

        self.checked = False

        self.animation = QVariantAnimation(
            self,
            valueChanged=self.animate,
            startValue=0.0,
            endValue=1.0,
            duration=250
        )
    
    def animate(self, t):
        style = """
            font-family: 'Inter';
            font-style: normal;
            font-weight: 700;
            font-size: 18px;
            line-height: 22px;
            text-align: center;
            
            background-color: transparent;
        """

        primaryColor = QColor(PRIMARY_COLOR.red(), PRIMARY_COLOR.green(), PRIMARY_COLOR.blue(), 128)
        textColor = utils.lerpColor(SECONDARY_BACKGROUND_COLOR, primaryColor, t)
        animated = "color: rgba({r}, {g}, {b}, {a});".format(r = textColor.red(), g = textColor.green(), b = textColor.blue(), a = textColor.alpha())
        style += animated
        self.label.setStyleSheet(style)

        self.backgroundColor = utils.lerpColor(PRIMARY_COLOR, SECONDARY_BACKGROUND_COLOR, t)

    def paintEvent(self, event):
        
        # Create the painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Create the path
        path = QPainterPath()
        # Set painter colors to given values.
        pen = QPen(self.backgroundColor, self.borderSize)
        painter.setPen(pen)
        brush = QBrush(self.backgroundColor)
        painter.setBrush(brush)

        rect = QRectF(event.rect())
        # Slighly shrink dimensions to account for bordersize.
        #rect.adjust(self.borderSize/2, self.borderSize/2, -self.borderSize/2, -self.borderSize/2)

        # Add the rect to path.
        path.addRoundedRect(rect, self.borderSize, self.borderSize)
        painter.setClipPath(path)

        # Fill shape, draw the border and center the text.
        painter.fillPath(path, painter.brush())
        painter.strokePath(path, painter.pen())
        #painter.setPen(self.backgroundColor)
        
        self.label.resize(self.size())        
        self.label.drawFrame(painter)
    
    def check(self, emitSignal = True):
        self.checked = not self.checked

        if emitSignal:
            self.changed.emit(self.index)

        if self.checked:
            self.animation.setDirection(QAbstractAnimation.Forward)
        else:
            self.animation.setDirection(QAbstractAnimation.Backward)
        self.animation.start()

    def setButtonGroupIndex(self, index):
        self.index = index
    
    def mousePressEvent(self, event):
        if not self.checked:
            self.check()