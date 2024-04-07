from PyQt6.QtWidgets import QApplication, QSizePolicy, QVBoxLayout, QComboBox, QMainWindow, QTextEdit, QVBoxLayout, QStackedLayout, QMessageBox, QToolBar, QLabel, QDockWidget, QWidget, QFormLayout, QLineEdit, QPushButton
from PyQt6.QtGui import QIcon, QAction, QPixmap, QCursor
from PyQt6.QtCore import QSize, Qt

import logging.config
logging.config.fileConfig('../resources/configurations/logging.conf')
logger = logging.getLogger(__name__)

class ToolbarWidget(QWidget):
    def __init__(self, labelMain, DSLEventWidgetRoot, variables):
        super().__init__()
        self.labelMain = labelMain
        self.DSLEventWidgetRoot = DSLEventWidgetRoot
        self.variables = variables

        self.setMinimumWidth(170)
        self.setMaximumWidth(170)

        '''Buttons for ToolsDevices'''
        self.buttonCamera = QPushButton()
        self.buttonCamera.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.buttonCamera.setIcon(QIcon(QPixmap("../resources/icons/camera.png")))
        self.buttonCamera.setIconSize(QSize(50, 50))
        self.buttonCamera.setCheckable(True)

        self.buttonSensor = QPushButton()
        self.buttonSensor.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.buttonSensor.setIcon(QIcon(QPixmap("../resources/icons/sensor.png")))
        self.buttonSensor.setIconSize(QSize(50, 50))
        self.buttonSensor.setCheckable(True)

        self.buttonWires = QPushButton()
        self.buttonWires.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.buttonWires.setIcon(QIcon(QPixmap("../resources/icons/wires.png")))
        self.buttonWires.setIconSize(QSize(50, 50))
        self.buttonWires.setCheckable(True)

        self.buttonDelete = QPushButton()
        self.buttonDelete.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.buttonDelete.setIcon(QIcon(QPixmap("../resources/icons/delete.png")))
        self.buttonDelete.setIconSize(QSize(50, 50))
        self.buttonDelete.setCheckable(True)

        '''Buttons for ToolsEvents'''
        self.buttonEventWait = QPushButton()
        self.buttonEventWait.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.buttonEventWait.setIcon(QIcon(QPixmap("../resources/icons/wait.png")))
        self.buttonEventWait.setIconSize(QSize(50, 50))

        self.buttonEventPhoto = QPushButton()
        self.buttonEventPhoto.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.buttonEventPhoto.setIcon(QIcon(QPixmap("../resources/icons/foto.png")))
        self.buttonEventPhoto.setIconSize(QSize(50, 50))

        self.buttonEventVideo = QPushButton()
        self.buttonEventVideo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.buttonEventVideo.setIcon(QIcon(QPixmap("../resources/icons/video.png")))
        self.buttonEventVideo.setIconSize(QSize(50, 50))

        self.buttonEventCustom = QPushButton()
        self.buttonEventCustom.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.buttonEventCustom.setIcon(QIcon(QPixmap("../resources/icons/customEvent.png")))
        self.buttonEventCustom.setIconSize(QSize(50, 50))
        self.layoutMain = QVBoxLayout()
        self.customEventComboBox = QComboBox()
        self.layoutMain.addWidget(self.customEventComboBox, alignment=Qt.AlignmentFlag.AlignTop)
        self.buttonEventCustom.setLayout(self.layoutMain)
        self.buttonEventCustom.clicked.connect(self.add_customEvent)

        self.buttonEventDelete = QPushButton()
        self.buttonEventDelete.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.buttonEventDelete.setIcon(QIcon(QPixmap("../resources/icons/delete.png")))
        self.buttonEventDelete.setIconSize(QSize(50, 50))
        self.buttonEventDelete.setCheckable(True)

        '''Deselect every other button when button is pressed'''
        self.buttons = [self.buttonCamera, self.buttonSensor, self.buttonWires, self.buttonDelete]
        self.buttonCamera.clicked.connect(lambda: self.uncheck_buttons_exept(button=self.buttonCamera))
        self.buttonSensor.clicked.connect(lambda: self.uncheck_buttons_exept(button=self.buttonSensor))
        self.buttonWires.clicked.connect(lambda: self.uncheck_buttons_exept(button=self.buttonWires))
        self.buttonDelete.clicked.connect(lambda: self.uncheck_buttons_exept(button=self.buttonDelete))

        self.buttonsEvent = [self.buttonEventDelete]
        self.buttonEventDelete.clicked.connect(lambda: self.uncheck_buttonsEvent_exept(button=self.buttonEventDelete))

        '''define Layout'''
        self.layoutToolsDevices = QVBoxLayout()
        self.layoutToolsDevices.addWidget(self.buttonCamera)
        self.layoutToolsDevices.addWidget(self.buttonSensor)
        self.layoutToolsDevices.addWidget(self.buttonWires)
        self.layoutToolsDevices.addWidget(self.buttonDelete)
        self.widgetToolsDevices = QWidget()
        self.widgetToolsDevices.setLayout(self.layoutToolsDevices)

        self.layoutToolsEvents = QVBoxLayout()
        self.layoutToolsEvents.addWidget(self.buttonEventWait)
        self.layoutToolsEvents.addWidget(self.buttonEventPhoto)
        self.layoutToolsEvents.addWidget(self.buttonEventVideo)
        self.layoutToolsEvents.addWidget(self.buttonEventCustom)
        self.layoutToolsEvents.addWidget(self.buttonEventDelete)
        self.widgetToolsEvents = QWidget()
        self.widgetToolsEvents.setLayout(self.layoutToolsEvents)

        self.layoutMain = QStackedLayout()
        self.layoutMain.addWidget(self.widgetToolsDevices)
        self.layoutMain.addWidget(self.widgetToolsEvents)

        self.setLayout(self.layoutMain)


    def uncheck_buttons_exept(self, button):
        cursor = QCursor(Qt.CursorShape.ArrowCursor)
        for index in range(len(self.buttons)):
            if self.buttons[index] != button:
                self.buttons[index].setChecked(False)
            if self.buttons[index].isChecked():
                match index:
                    case 0:
                        cursor = QCursor(QPixmap('../resources/icons/camera.png').scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatioByExpanding))
                    case 1:
                        cursor = QCursor(QPixmap('../resources/icons/sensor.png').scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatioByExpanding))
                    case 2:
                        cursor = QCursor(QPixmap('../resources/icons/wires.png').scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatioByExpanding))
                    case 3:
                        cursor = QCursor(QPixmap('../resources/icons/delete.png').scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatioByExpanding))

        self.set_selected_tool()
        self.labelMain.setCursor(cursor)


    def set_selected_tool(self):
        if self.buttonCamera.isChecked():
            self.variables["selected_tool"] = "camera"
        elif self.buttonSensor.isChecked():
            self.variables["selected_tool"] = "sensor"
        elif self.buttonWires.isChecked():
            self.variables["selected_tool"] = "wire"
        elif self.buttonDelete.isChecked():
            self.variables["selected_tool"] = "delete"
        else:
            self.variables["selected_tool"] = None


    def uncheck_buttonsEvent_exept(self, button):
        cursor = QCursor(Qt.CursorShape.ArrowCursor)
        for index in range(len(self.buttonsEvent)):
            if self.buttonsEvent[index] != button:
                self.buttonsEvent[index].setChecked(False)
            if self.buttonsEvent[index].isChecked():
                match index:
                    case 0:
                        cursor = QCursor(QPixmap('../resources/icons/delete.png').scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatioByExpanding))

        self.set_selected_tool_logic()
        self.DSLEventWidgetRoot.setCursor(cursor)


    def set_selected_tool_logic(self):
        if self.buttonEventDelete.isChecked():
            self.variables["selected_tool_logic"] = "delete"
        else:
            self.variables["selected_tool_logic"] = None

    def change_view(self, index):
        self.layoutMain.setCurrentIndex(index)

    def update_customEventBox(self):
        try:
            for key in self.DSLEventWidgetRoot.DSLEventListHandler.DSLEventDictionary["custom"].keys():
                self.customEventComboBox.addItem("custom"+"."+key+":"+self.DSLEventWidgetRoot.DSLEventListHandler.DSLEventDictionary["custom"][key]["name"])
        except Exception as exception:
            logger.debug("Failed to update customEventbox:", exception)

    def add_customEvent(self):
        try:
            idText = self.customEventComboBox.currentText()
            texts = idText.split(':')[0].split('.')
            self.selectedDSLEvent = (texts[0], texts[1])

            self.DSLEventWidgetRoot.add_DSLEvent_by_section_id(texts[0], texts[1])
        except Exception as exception:
            logger.debug("Failed to set customEvent from customEventbox", exception)