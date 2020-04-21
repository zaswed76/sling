
import datetime
import random

from jinja2 import Template

import paths
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class DropFrame(QFrame):
    def __init__(self, objectName, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.setObjectName(objectName)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        mime = e.mimeData()
        text = mime.text()
        print(text)
        e.accept()






