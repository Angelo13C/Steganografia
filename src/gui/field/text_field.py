from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .. import utils

PRIMARY_COLOR = QColor("#96B3D5")

BACKGROUND_TEXT_SPACING = 8
NO_FOCUS_BACKGROUND_COLOR = QColor("#ACACAC")

class TextField(QWidget):
    def __init__(self, descriptorText, placeholderText = "Inserisci qualcosa", backgroundHeight = 5):
        super().__init__()

        self.initialize(descriptorText, placeholderText, backgroundHeight)
    
    def initialize(self, descriptorText, placeholderText, backgroundHeight):
        self.backgroundHeight = backgroundHeight
        self.setFixedWidth(400)

        layout = QVBoxLayout()
        layout.setSpacing(40)
        #layout.setAlignment(Qt.AlignCenter)
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

        self.textEdit = QTextEdit(self)
        self.textEdit.setFixedHeight(35)
        self.textEdit.setPlaceholderText(placeholderText)
        self.textEdit.setAutoFillBackground(True)
        self.textEdit.textChanged.connect(lambda: self.textEdit.setFixedHeight(max(35, self.textEdit.document().size().height())))
        self.textEdit.setAlignment(Qt.AlignLeft)
        self.textEdit.setStyleSheet("""
            font-family: 'Inter';
            font-style: normal;
            font-weight: 400;
            font-size: 22px;
            line-height: 27px;

            color: #FFFFFF;
            background-color: transparent;
            border: 0;
            margin-left: 15px;
            margin-right: 15px;
        """)
        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textEdit.installEventFilter(self)
        self.backgroundColor = PRIMARY_COLOR

        layout.addWidget(self.descriptor)
        layout.addWidget(self.textEdit)
        self.setLayout(layout)

        """
        self.animation = QVariantAnimation(
            self,
            valueChanged=self.animate,
            startValue=0.0,
            endValue=1.0,
            duration=250
        )"""
    
    def text(self):
        return self.textEdit.toPlainText()
    
    def paintEvent(self, event):
        cornerRadius = self.backgroundHeight / 2
        
        # Create the painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Create the path
        path = QPainterPath()
        # Set painter colors to given values.
        pen = QPen(self.backgroundColor, cornerRadius)
        painter.setPen(pen)
        brush = QBrush(self.backgroundColor)
        painter.setBrush(brush)

        rect = QRectF(event.rect())
        rectY = self.textEdit.y() + self.textEdit.height() + BACKGROUND_TEXT_SPACING
        rect.setCoords(0, rectY, self.size().width(), rectY + self.backgroundHeight)
        # Slighly shrink dimensions to account for bordersize.
        #rect.adjust(self.borderSize/2, self.borderSize/2, -self.borderSize/2, -self.borderSize/2)

        # Add the rect to path.
        path.addRoundedRect(rect, cornerRadius, cornerRadius)
        painter.setClipPath(path)

        # Fill shape, draw the border and center the text.
        painter.fillPath(path, painter.brush())
        painter.strokePath(path, painter.pen())
        #painter.setPen(self.backgroundColor)
        
        self.descriptor.resize(self.size())        
        self.descriptor.drawFrame(painter)
    
    """
    def animate(self, t):
        print("T: ", t)
        self.backgroundColor = utils.lerpColor(PRIMARY_COLOR, NO_FOCUS_BACKGROUND_COLOR, t)

    def eventFilter(self, source, event):
        if event.type() == QEvent.FocusIn:
            self.animation.setDirection(QAbstractAnimation.Forward)
            print("Focus in")
            self.animation.start()
        elif event.type() == QEvent.FocusOut:
            self.animation.setDirection(QAbstractAnimation.Backward)
            print("Focus out")
            self.animation.start()


        return super(TextField, self).eventFilter(source, event)"""