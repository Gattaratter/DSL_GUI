from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag, QPixmap

import logging.config
logging.config.fileConfig('../resources/configurations/logging.conf')
logger = logging.getLogger(__name__)

class MyPushButton(QPushButton):
    def __init__(self, variables, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.variables = variables

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton and self.variables["selected_tool"] == None:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)
            drag.exec(Qt.DropAction.MoveAction)
