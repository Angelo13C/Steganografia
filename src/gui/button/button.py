from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .. import utils

PRIMARY_COLOR = QColor("#96B3D5")
SECONDARY_BACKGROUND_COLOR = QColor("#252525")

class Button(QWidget):
    pressed = pyqtSignal()

    def __init__(self, text, borderSize = 12):
        super().__init__()
        self.initialize(text, borderSize)
    
    def initialize(self, text, borderSize):
        self.borderSize = borderSize

        self.setAutoFillBackground(True)
        self.setFixedSize(400, 80)

        self.textStyle = """
            font-family: 'Inter';
            font-style: normal;
            font-weight: 700;
            font-size: 30px;
            line-height: 36px;
            
            background-color: transparent;
        """

        self.label = QLabel(self)
        self.label.setText(text)
        self.label.setAutoFillBackground(True)
        self.label.setAlignment(Qt.AlignCenter)

        self.animation = QVariantAnimation(
            self,
            valueChanged=self.animate,
            startValue=0.0,
            duration=400
        )
        self.animation.setKeyValueAt(0.35, 1.0)
        self.animation.setKeyValueAt(0.65, 1.0)
        self.animation.setKeyValueAt(1.0, 0.0)
    
    def getLabel(self):
        return self.label

    def setTextStyle(self, style):
        self.textStyle = style
        self.animate(self.t)
    
    def animate(self, t):
        self.backgroundColor = utils.lerpColor(PRIMARY_COLOR, QColorConstants.Transparent, t)

        textColor = utils.lerpColor(SECONDARY_BACKGROUND_COLOR, PRIMARY_COLOR, t)
        style = self.textStyle 
        style += "color: rgba({r}, {g}, {b}, {a});".format(r = textColor.red(), g = textColor.green(), b = textColor.blue(), a = textColor.alpha())
        self.label.setStyleSheet(style)

        self.t = t
        self.update()

    def paintEvent(self, event):
        cornerRadius = self.height() / 2

        # Create the painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Create the path
        path = QPainterPath()
        # Set painter colors to given values.
        pen = QPen(PRIMARY_COLOR, self.borderSize)
        painter.setPen(pen)
        brush = QBrush(self.backgroundColor)
        painter.setBrush(brush)

        rect = QRectF(self.rect())

        # Add the rect to path.
        path.addRoundedRect(rect, cornerRadius, cornerRadius)
        painter.setClipPath(path)

        # Fill shape, draw the border and center the text.
        painter.fillPath(path, painter.brush())
        painter.strokePath(path, painter.pen())
        #painter.setPen(self.backgroundColor)
        
        self.label.resize(self.size()) 
        #self.label.drawFrame(painter)
    
    def mousePressEvent(self, _):
        self.pressed.emit()
        self.animation.start()