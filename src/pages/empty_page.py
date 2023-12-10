from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from page import Page

class EmptyPage(Page):
    def __init__(self, actionTip):
        super().__init__(actionTip)
