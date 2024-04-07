import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFrame, QSizePolicy, QLabel, QDockWidget, QWidget, QStackedLayout, \
    QToolBar, QFileDialog
from PyQt6.QtGui import QIcon, QAction, QPixmap, QPainter
from PyQt6.QtCore import QSize, Qt, pyqtSignal

'''Eigene Dateien'''
import ToolbarWidget
import ConfigurationWidget
import Devices
import SavefileHandler
import MyPushButton
import DSLEventWidget
import DSLEvent
import DSLModelInterpreter


import logging.config
logging.config.fileConfig('../resources/configurations/logging.conf')
logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    signalUpdate = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.setAcceptDrops(True)

        '''Signals'''
        self.signalUpdate.connect(self.update_Map)

        '''Variables'''
        self.wireFirstDevice = None
        self.wireSecondDevice = None

        self.devicePlan = Devices.DevicePlan()
        self.DSLEventList = DSLEvent.DSLEventListHandler()
        self.DSLEventList.load_basic_DSLEvents()
        self.variables = {
            "selected_tool": None,
            "selected_tool_logic": None
        }

        '''Window properties'''
        self.setWindowTitle("DSL-Designer")
        self.setMinimumSize(1400, 1100)

        '''MainCanvas'''
        self.labelMain = QLabel()
        self.labelMain.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.labelMain.setMaximumSize(1000, 1000)
        self.canvasMain = QPixmap(1000, 1000)
        self.canvasMain.fill(Qt.GlobalColor.white)
        self.labelMain.setPixmap(self.canvasMain)
        self.labelMain.setMouseTracking(True)
        self.labelMain.setAcceptDrops(True)

        self.labelMain.setFrameStyle(QFrame.Shape.Panel)
        self.labelMain.setLineWidth(1)

        '''EventWindow'''
        self.DSLEventWidgetRoot = DSLEventWidget.DSLEventRootWidget(self.DSLEventList, self.variables)

        '''ToolbarWidget'''
        self.dockLeft = QDockWidget("Elemente")
        self.toolbarWidget = ToolbarWidget.ToolbarWidget(self.labelMain, self.DSLEventWidgetRoot, self.variables)
        self.dockLeft.setWidget(self.toolbarWidget)
        self.toolbarWidget.buttonCamera.clicked.connect(self.reset_wirePoint)
        self.toolbarWidget.buttonSensor.clicked.connect(self.reset_wirePoint)
        self.toolbarWidget.buttonWires.clicked.connect(self.reset_wirePoint)
        self.toolbarWidget.buttonDelete.clicked.connect(self.reset_wirePoint)

        self.toolbarWidget.buttonEventWait.clicked.connect(lambda: self.DSLEventWidgetRoot.add_DSLEvent_by_section_id(section = "basic", id = "0"))
        self.toolbarWidget.buttonEventPhoto.clicked.connect(lambda: self.DSLEventWidgetRoot.add_DSLEvent_by_section_id(section = "basic", id = "1"))
        self.toolbarWidget.buttonEventVideo.clicked.connect(lambda: self.DSLEventWidgetRoot.add_DSLEvent_by_section_id(section = "basic", id = "2"))

        '''ConfigurationWidget'''
        self.dockRight = QDockWidget("Konfiguration")
        self.configurationWidget = ConfigurationWidget.ConfigurationWidget(self.signalUpdate, self.devicePlan, self.DSLEventWidgetRoot, self.variables)
        self.dockRight.setWidget(self.configurationWidget)

        #connection between ToolbarWidget and ConfigWidget
        self.configurationWidget.buttonDSLEventSave.clicked.connect(self.toolbarWidget.update_customEventBox)

        '''Toolbar for Configwindow'''
        self.toolBarType = QToolBar()
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBarType)
        actionToolBarCamera = QAction("Kamera", self)
        actionToolBarSensor = QAction("Sensor", self)
        actionToolBarWires = QAction("Kabel", self)
        actionToolBarDSLEvent = QAction("Event", self)
        actionToolBarCamera.triggered.connect(lambda: self.configurationWidget.change_Widget(index=0))
        actionToolBarCamera.triggered.connect(lambda: self.change_view(index=0))
        actionToolBarSensor.triggered.connect(lambda: self.configurationWidget.change_Widget(index=1))
        actionToolBarSensor.triggered.connect(lambda: self.change_view(index=0))
        actionToolBarWires.triggered.connect(lambda: self.configurationWidget.change_Widget(index=2))
        actionToolBarWires.triggered.connect(lambda: self.change_view(index=0))
        actionToolBarDSLEvent.triggered.connect(lambda: self.configurationWidget.change_Widget(index=3))
        actionToolBarDSLEvent.triggered.connect(lambda: self.change_view(index=1))

        spacer = QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.toolBarType.addWidget(spacer)
        self.toolBarType.addActions([actionToolBarCamera, actionToolBarSensor, actionToolBarWires, actionToolBarDSLEvent])

        '''Menubar'''
        self.topMenubar = self.menuBar()
        self.actionClose = QAction(QIcon(QPixmap("../resources/icons/close.png")), "Exit")
        self.actionClose.triggered.connect(self.close)
        self.actionSave = QAction(QIcon(QPixmap("../resources/icons/save.png")), "Speichern")
        self.actionSave.triggered.connect(self.save_plan)
        self.actionLoad = QAction(QIcon(QPixmap("../resources/icons/load.png")), "Laden")
        self.actionLoad.triggered.connect(self.load_plan)
        self.actionNew = QAction(QIcon(QPixmap("../resources/icons/new.png")), "Neu")
        self.actionNew.triggered.connect(self.new_plan)
        self.actionDSLGenerate = QAction(QIcon(QPixmap("../resources/icons/generation.png")), "DSL-Modell generieren")
        self.actionDSLGenerate.triggered.connect(self.generate_dslFile)
        self.actionDSLLoad = QAction(QIcon(QPixmap("../resources/icons/generation.png")), "DSL-Modell laden")
        self.actionDSLLoad.triggered.connect(self.read_DSLFile)
        self.actionDevicePlan = QAction(QIcon(QPixmap("../resources/icons/view.png")), "Aufbau")
        self.actionDevicePlan.triggered.connect(lambda: self.change_view(index=0))
        self.actionLogic = QAction(QIcon(QPixmap("../resources/icons/view.png")), "Logik")
        self.actionLogic.triggered.connect(lambda: self.change_view(index=1))

        topMenuFile = self.topMenubar.addMenu("Datei")
        topMenuFile.addAction(self.actionClose)
        topMenuFile.addAction(self.actionSave)
        topMenuFile.addAction(self.actionLoad)
        topMenuFile.addAction(self.actionNew)

        topMenuDSLModell = self.topMenubar.addMenu("DSL-Modell")
        topMenuDSLModell.addAction(self.actionDSLGenerate)
        topMenuDSLModell.addAction(self.actionDSLLoad)

        topMenuView = self.topMenubar.addMenu("Ansicht")
        topMenuView.addAction(self.actionDevicePlan)
        topMenuView.addAction(self.actionLogic)

        '''Statusbar'''
        self.bottomStatusbar = self.statusBar()

        self.labelMousePosition = QLabel("")
        self.bottomStatusbar.addWidget(self.labelMousePosition)

        '''Add dockWidgets set Layout'''
        self.layoutMain = QStackedLayout()
        self.layoutMain.addWidget(self.labelMain)
        self.layoutMain.addWidget(self.DSLEventWidgetRoot)

        self.centralWidget = QWidget()
        self.centralWidget.setMouseTracking(True)
        self.centralWidget.setLayout(self.layoutMain)
        self.setCentralWidget(self.centralWidget)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dockLeft)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dockRight)


    def mouseMoveEvent(self, mouseEvent):
        mouseX = mouseEvent.pos().x()-self.centralWidget.pos().x()
        mouseY = mouseEvent.pos().y()-self.centralWidget.pos().y()
        if 1<=mouseX<=self.centralWidget.width() and 1<=mouseY<=self.centralWidget.height(): 
            self.labelMousePosition.setText(f"Mausposition: ({mouseX},{mouseY})")
        else:
            self.labelMousePosition.setText(f"Mausposition: (____,____)")


    def mousePressEvent(self, mouseEvent):
        if (self.centralWidget.pos().x() < mouseEvent.pos().x() < self.centralWidget.pos().x() + self.centralWidget.width()
                and self.centralWidget.pos().y() < mouseEvent.pos().y() < self.centralWidget.pos().y() + self.centralWidget.height()):
            '''new Camera'''
            if self.toolbarWidget.buttonCamera.isChecked():
                newCamera = MyPushButton.MyPushButton(self.variables, self.labelMain)
                newCamera.setMouseTracking(True)
                newCamera.setIcon(QIcon(QPixmap("../resources/icons/camera.png")))
                planElement = Devices.Camera(
                    self.devicePlan.get_new_id(),
                    newCamera,
                    mouseEvent.pos().x() - self.centralWidget.pos().x(),
                    mouseEvent.pos().y() - self.centralWidget.pos().y(),
                    )
                newCamera.clicked.connect(lambda: self.delete_device(planElement=planElement))
                newCamera.clicked.connect(lambda: self.select_Device(planElement=planElement))
                newCamera.clicked.connect(lambda: self.configurationWidget.show_planElement_configuration(planElement=planElement))
                self.devicePlan.planList.append(planElement)
                self.configurationWidget.show_planElement_configuration(planElement)
                self.update_Map()
                '''new Sensor'''
            elif self.toolbarWidget.buttonSensor.isChecked():
                newSensor = MyPushButton.MyPushButton(self.variables, self.labelMain)
                newSensor.setIcon(QIcon(QPixmap("../resources/icons/sensor.png")))
                newSensor.setMouseTracking(True)
                planElement = Devices.Sensor(
                    self.devicePlan.get_new_id(),
                    newSensor,
                    mouseEvent.pos().x() - self.centralWidget.pos().x(),
                    mouseEvent.pos().y() - self.centralWidget.pos().y(),
                    )
                newSensor.clicked.connect(lambda: self.delete_device(planElement=planElement))
                newSensor.clicked.connect(lambda: self.select_Device(planElement=planElement))
                newSensor.clicked.connect(lambda: self.configurationWidget.show_planElement_configuration(planElement=planElement))
                self.devicePlan.planList.append(planElement)
                self.configurationWidget.show_planElement_configuration(planElement)
                self.update_Map()
                '''new Wire'''
            elif self.toolbarWidget.buttonWires.isChecked():
                logger.debug("please select two devices you want to conncet")
                return

                '''Nothing selected'''
            else:
                logger.debug("nothing happens")


    '''This method updates all Buttons(Devices) and brings them in front of the canvas(Bitmap)'''
    def update_Map(self):
        self.canvasMain.fill(Qt.GlobalColor.white)
        for element in self.devicePlan.planList:
            if not isinstance(element, Devices.Wire):
                element.button.show()
                element.button.setIconSize(QSize(element.size, element.size))
                element.button.setFixedSize(QSize(element.size+5, element.size+5))
                element.button.move(element.positionX-element.button.size().width()//2, element.positionY-element.button.size().height()//2)
                element.button.show()
            else:
                positionX = (element.firstDevice.positionX + element.secondDevice.positionX) // 2
                positionY = (element.firstDevice.positionY + element.secondDevice.positionY) // 2
                element.button.show()
                element.button.setIconSize(QSize(element.size, element.size))
                element.button.setFixedSize(QSize(element.size+5, element.size+5))
                element.button.move(positionX - element.button.size().width() // 2, positionY - element.button.size().height() // 2)
                element.button.show()
                painter = QPainter(self.canvasMain)
                painter.setRenderHints(QPainter.RenderHint.Antialiasing)
                painter.drawLine(element.firstDevice.positionX,
                                 element.firstDevice.positionY,
                                 element.secondDevice.positionX,
                                 element.secondDevice.positionY)
                painter.end()
        self.labelMain.setPixmap(self.canvasMain)
        logger.debug("success")

    '''This method deletes a Button(Device)'''
    def delete_device(self, planElement):
        if self.toolbarWidget.buttonDelete.isChecked():
            self.devicePlan.planList.remove(planElement)
            planElement.button.hide()
            planElement.button.destroy()
            if isinstance(planElement, Devices.Camera) or isinstance(planElement, Devices.Sensor):
                wiresToRemove = []
                for index in range(len(self.devicePlan.planList)):
                    if isinstance(self.devicePlan.planList[index], Devices.Wire) and (self.devicePlan.planList[index].firstDevice == planElement or self.devicePlan.planList[index].secondDevice == planElement):
                        wiresToRemove.append(index)
                for index in reversed(wiresToRemove):
                    self.devicePlan.planList[index].button.hide()
                    self.devicePlan.planList[index].button.destroy()
                    self.devicePlan.planList.pop(index)
            self.update_Map()
            logger.debug("success")


    '''This method shall select Devices and create a wire between them if it is the second one'''
    def select_Device(self, planElement):
        if self.toolbarWidget.buttonWires.isChecked():
            if not self.wireFirstDevice:
                self.wireFirstDevice = planElement
            elif self.wireFirstDevice != planElement:
                self.wireSecondDevice = planElement

                newWire = MyPushButton.MyPushButton(self.variables, self.labelMain)
                newWire.setIcon(QIcon(QPixmap("../resources/icons/wires.png")))
                newWire.setMouseTracking(True)
                planElement = Devices.Wire(
                    self.devicePlan.get_new_id(),
                    newWire,
                    self.wireFirstDevice,
                    self.wireSecondDevice,
                    name = self.wireFirstDevice.name + "_" + self.wireSecondDevice.name,
                    )
                newWire.clicked.connect(lambda: self.delete_device(planElement=planElement))
                newWire.clicked.connect(lambda: self.configurationWidget.show_planElement_configuration(planElement=planElement))
                self.devicePlan.planList.append(planElement)
                self.configurationWidget.show_planElement_configuration(planElement)
                self.update_Map()
                self.reset_wirePoint()

    '''This method resets the currently selected Points for a wire'''
    def reset_wirePoint(self):
        self.wireFirstDevice = None
        self.wireSecondDevice = None


    def save_plan(self):
        """device view"""
        if self.layoutMain.currentIndex() == 0:
            try:
                path = QFileDialog.getSaveFileName(self, "Speicherort wählen", "../savefiles/plans", "All Files (*)",)
            except Exception as e:
                logger.debug(f"Fehler bei Dateiauswahl: {e}")
            if path[0]:
                self.devicePlanFileHandler = SavefileHandler.DevicePlanFileHandler(path)
                self.devicePlanFileHandler.save_devicePlan(self.devicePlan)

        elif self.layoutMain.currentIndex() == 1:
            self.DSLEventList.save_custom_DSLEvents()
        logger.debug("success")


    def load_plan(self):
        """device view"""
        if self.layoutMain.currentIndex() == 0:
            try:
                path = QFileDialog.getOpenFileName(self, "Datei wählen", "../savefiles/plans", "All Files (*)",)
            except Exception as e:
                logger.debug(f"Fehler bei Dateiauswahl: {e}")
            if path[0]:
                self.devicePlanFileHandler = SavefileHandler.DevicePlanFileHandler(path)
                devicePlanList = self.devicePlanFileHandler.load_devicePlan()
                self.new_plan()
                for element in devicePlanList:
                    self.add_devicePlanListItem(element)
            self.configurationWidget.clear_configuration()
            self.update_Map()
        elif self.layoutMain.currentIndex() == 1:
            try:
                path = QFileDialog.getOpenFileName(self, "Datei wählen", "../savefiles/DSLEvents", "All Files (*)",)
            except Exception as e:
                logger.debug(f"Fehler bei Dateiauswahl: {e}")
            if path[0]:
                self.DSLEventList.load_custom_DSLEvents(path[0])
                self.configurationWidget.update_DSLEventBox()
        logger.debug("success")


    '''for some reason it is needed to add every Device element on its own, otherwise the lambda func takes only the latest planElement'''
    def add_devicePlanListItem(self, element):
        if element["class"] == "camera":
            newCamera = MyPushButton.MyPushButton(self.variables, self.labelMain)
            newCamera.setMouseTracking(True)
            newCamera.setIcon(QIcon(QPixmap("../resources/icons/camera.png")))
            planElement = Devices.Camera(
                element["id"],
                newCamera,
                element["positionX"],
                element["positionY"],
                element["positionZ"],
                element["size"],
                element["name"],
                element["modell"],
                element["ipAddress"],
                element["DSLEventIdList"],
            )
            newCamera.clicked.connect(lambda: self.delete_device(planElement=planElement))
            newCamera.clicked.connect(lambda: self.select_Device(planElement=planElement))
            newCamera.clicked.connect(lambda: self.configurationWidget.show_planElement_configuration(planElement=planElement))
            self.devicePlan.planList.append(planElement)

        elif element["class"] == "sensor":
            newSensor = MyPushButton.MyPushButton(self.variables, self.labelMain)
            newSensor.setMouseTracking(True)
            newSensor.setIcon(QIcon(QPixmap("../resources/icons/sensor.png")))
            planElement = Devices.Sensor(
                element["id"],
                newSensor,
                element["positionX"],
                element["positionY"],
                element["positionZ"],
                element["size"],
                element["name"],
            )
            newSensor.clicked.connect(lambda: self.delete_device(planElement=planElement))
            newSensor.clicked.connect(lambda: self.select_Device(planElement=planElement))
            newSensor.clicked.connect(lambda: self.configurationWidget.show_planElement_configuration(planElement=planElement))
            self.devicePlan.planList.append(planElement)

        elif element["class"] == "wire":
            newWire = MyPushButton.MyPushButton(self.variables, self.labelMain)
            newWire.setIcon(QIcon(QPixmap("../resources/icons/wires.png")))
            newWire.setMouseTracking(True)

            for device in self.devicePlan.planList:
                if device.id == element["firstDevice"]:
                    wireFirstDevice = device
                if device.id == element["secondDevice"]:
                    wireSecondDevice = device

            planElement = Devices.Wire(
                element["id"],
                newWire,
                wireFirstDevice,
                wireSecondDevice,
                element["size"],
                element["name"],
            )
            newWire.clicked.connect(lambda: self.delete_device(planElement=planElement))
            newWire.clicked.connect(lambda: self.configurationWidget.show_planElement_configuration(planElement=planElement))
            self.devicePlan.planList.append(planElement)
        else:
            logger.debug("class from loaded file no identified")


    '''Clears the current devicePlan completly'''
    def new_plan(self):
        if self.layoutMain.currentIndex() == 0:
            for index in range(len(self.devicePlan.planList)):
                self.devicePlan.planList[0].button.hide()
                self.devicePlan.planList[0].button.destroy()
                self.devicePlan.planList.pop(0)
            self.update_Map()
        elif self.layoutMain.currentIndex() == 1:
            self.DSLEventWidgetRoot.clear()

        logger.debug("success")


    '''Calls the FileHandeler with the path and the current devicePlan and DSLEvents'''
    def generate_dslFile(self):
        try:
            path = QFileDialog.getSaveFileName(self, "Speicherort wählen", "../savefiles/DSL", "All Files (*)",)
        except Exception as e:
            logger.debug(f"Fehler bei Dateiauswahl: {e}")
        if path[0]:
            DSLFileHandler = SavefileHandler.DSLFileHandler(path[0])
            DSLFileHandler.save_DSLCode(self.devicePlan, self.DSLEventList)
        logger.debug("success")


    '''Loads a .cam file an displays the DSL-Model'''
    def read_DSLFile(self):
        try:
            path = QFileDialog.getOpenFileName(self, "Speicherort wählen", "../savefiles/DSL", "All Files (*)",)
        except Exception as e:
            logger.debug(f"Fehler bei Dateiauswahl: {e}")
        if path[0]:
            try:
                DSLModellreader = DSLModelInterpreter.DSLModelInterpreter(path[0])
                DSLModellreader.load_DSLModel()

                self.new_plan()
                for element in DSLModellreader.dictionaryList:
                    self.add_devicePlanListItem(element)

                self.configurationWidget.clear_configuration()
                self.update_Map()
            except Exception as e:
                logger.debug(f"Fehler beim Interpretieren des DSL-Modells: {e}")
        logger.debug("success")

    def change_view(self, index):
        if index == 1:
            self.configurationWidget.change_Widget(index=3)
        self.layoutMain.setCurrentIndex(index)
        self.toolbarWidget.change_view(index)
        logger.debug("success")


    def dragEnterEvent(self, e):
        e.accept()


    def dropEvent(self, e):
        x = e.position().x() - self.centralWidget.pos().x()
        y = e.position().y() - self.centralWidget.pos().y()
        for element in self.devicePlan.planList:
            if element.button == e.source():
                element.positionX = int(x)
                element.positionY = int(y)
                self.configurationWidget.show_planElement_configuration(self.devicePlan.get_element_by_id(element.id))
        self.update_Map()
        e.accept()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

