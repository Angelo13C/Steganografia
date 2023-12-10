import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from window import Window

TITLE = "Steganografia"
ICON_PATH = "WindowIcon.png"

def run():
    app = QApplication(sys.argv)

    window = Window(TITLE, ICON_PATH)

    sys.exit(app.exec_())

run()