from PyQt6.QtWidgets import QSizePolicy, QStackedLayout, QGridLayout, QLabel, QWidget, QLineEdit, QPushButton, QComboBox, QSlider
from PyQt6.QtCore import Qt

'''Eigene Dateien'''
import Devices


import logging.config
logging.config.fileConfig('../resources/configurations/logging.conf')
logger = logging.getLogger(__name__)

class ConfigurationWidget(QWidget):
    def __init__(self, signalUpdate, devicePlan, DSLEventWidgetRoot, variables):
        super().__init__()
        self.setMinimumWidth(400)
        #self.setMaximumWidth(200)
        '''Signals'''
        self.signalUpdate = signalUpdate
        self.variables = variables

        '''Variablen'''
        self.selectedPlanElement = None
        self.selectedDSLEvent = None
        self.devicePlan = devicePlan
        self.DSLEventWidgetRoot = DSLEventWidgetRoot

        '''Define ConfigurationWindow for Cameras'''
        '''Labels, Edits, Buttons'''
        self.labelCameraDevice = QLabel("Typ:")
        self.lineEditCameraDevice = QLabel("Kamera")

        self.labelCameraSize = QLabel("Knopgröße:")
        self.lineEditCameraSize = QSlider(Qt.Orientation.Horizontal)
        self.lineEditCameraSize.setMinimum(10)
        self.lineEditCameraSize.setMaximum(100)
        self.lineEditCameraSize.valueChanged.connect(self.size_slider)

        self.labelCameraId = QLabel("ID:")
        self.lineEditCameraId = QComboBox()
        self.lineEditCameraId.currentTextChanged.connect(self.show_selected_id)

        self.labelCameraName = QLabel("Name:")
        self.lineEditCameraName = QLineEdit()

        self.labelCameraModel = QLabel("Modell:")
        self.lineEditCameraModel = QLineEdit()

        self.labelCameraIpAddress = QLabel("IP-Adresse:")
        self.lineEditCameraIpAddress = QLineEdit()

        self.labelCameraPositionX = QLabel("Position X:")
        self.lineEditCameraPositionX = QLineEdit()

        self.labelCameraPositionY = QLabel("Position Y:")
        self.lineEditCameraPositionY = QLineEdit()

        self.labelCameraPositionZ = QLabel("Position Z:")
        self.lineEditCameraPositionZ = QLineEdit()

        self.labelCameraDSLEvent = QLabel("Event:")
        self.lineEditCameraDSLEvent = QComboBox()

        self.buttonCameraSave = QPushButton("Speichern")
        self.buttonCameraSave.clicked.connect(self.save_configuration)

        spacerCamera = QWidget(self)
        spacerCamera.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Expanding)

        '''define Layout'''
        self.layoutCamera = QGridLayout()
        self.layoutCamera.addWidget(self.labelCameraDevice      ,0,0)
        self.layoutCamera.addWidget(self.labelCameraSize        ,1,0)
        self.layoutCamera.addWidget(self.labelCameraId          ,2,0)
        self.layoutCamera.addWidget(self.labelCameraName        ,3,0)
        self.layoutCamera.addWidget(self.labelCameraModel       ,4,0)
        self.layoutCamera.addWidget(self.labelCameraIpAddress   ,5,0)
        self.layoutCamera.addWidget(self.labelCameraPositionX   ,6,0)
        self.layoutCamera.addWidget(self.labelCameraPositionY   ,7,0)
        self.layoutCamera.addWidget(self.labelCameraPositionZ   ,8,0)
        self.layoutCamera.addWidget(self.labelCameraDSLEvent    ,9,0)
        self.layoutCamera.addWidget(spacerCamera                ,11,0)

        self.layoutCamera.addWidget(self.lineEditCameraDevice       ,0,1)
        self.layoutCamera.addWidget(self.lineEditCameraSize         ,1,1)
        self.layoutCamera.addWidget(self.lineEditCameraId           ,2,1)
        self.layoutCamera.addWidget(self.lineEditCameraName         ,3,1)
        self.layoutCamera.addWidget(self.lineEditCameraModel        ,4,1)
        self.layoutCamera.addWidget(self.lineEditCameraIpAddress    ,5,1)
        self.layoutCamera.addWidget(self.lineEditCameraPositionX    ,6,1)
        self.layoutCamera.addWidget(self.lineEditCameraPositionY    ,7,1)
        self.layoutCamera.addWidget(self.lineEditCameraPositionZ    ,8,1)
        self.layoutCamera.addWidget(self.lineEditCameraDSLEvent     ,9,1)

        self.layoutCamera.addWidget(self.buttonCameraSave, 10, 0, 1, 2)

        self.widgetCamera = QWidget()
        self.widgetCamera.setLayout(self.layoutCamera)

        '''Define ConfigurationWindow for Sensor'''
        '''Labels, Edits, Buttons'''
        self.labelSensorDevice = QLabel("Typ:")
        self.lineEditSensorDevice = QLabel("Sensor")

        self.labelSensorId = QLabel("ID:")
        self.lineEditSensorId = QComboBox()
        self.lineEditSensorId.currentTextChanged.connect(self.show_selected_id)

        self.labelSensorSize = QLabel("Knopgröße:")
        self.lineEditSensorSize = QSlider(Qt.Orientation.Horizontal)
        self.lineEditSensorSize.setMinimum(10)
        self.lineEditSensorSize.setMaximum(100)
        self.lineEditSensorSize.valueChanged.connect(self.size_slider)

        self.labelSensorName = QLabel("Name:")
        self.lineEditSensorName = QLineEdit()

        self.labelSensorPositionX = QLabel("Position X:")
        self.lineEditSensorPositionX = QLineEdit()

        self.labelSensorPositionY = QLabel("Position Y:")
        self.lineEditSensorPositionY = QLineEdit()

        self.labelSensorPositionZ = QLabel("Position Z:")
        self.lineEditSensorPositionZ = QLineEdit()

        self.buttonSensorSave = QPushButton("Speichern")
        self.buttonSensorSave.clicked.connect(self.save_configuration)

        spacerSensor = QWidget(self)
        spacerSensor.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Expanding)

        '''define Layout'''
        self.layoutSensor = QGridLayout()
        self.layoutSensor.addWidget(self.labelSensorDevice      ,0,0)
        self.layoutSensor.addWidget(self.labelSensorSize        ,1,0)
        self.layoutSensor.addWidget(self.labelSensorId          ,2,0)
        self.layoutSensor.addWidget(self.labelSensorName        ,3,0)
        self.layoutSensor.addWidget(self.labelSensorPositionX   ,4,0)
        self.layoutSensor.addWidget(self.labelSensorPositionY   ,5,0)
        self.layoutSensor.addWidget(self.labelSensorPositionZ   ,6,0)
        self.layoutSensor.addWidget(spacerSensor                ,8,0)

        self.layoutSensor.addWidget(self.lineEditSensorDevice       ,0,1)
        self.layoutSensor.addWidget(self.lineEditSensorSize         ,1,1)
        self.layoutSensor.addWidget(self.lineEditSensorId           ,2,1)
        self.layoutSensor.addWidget(self.lineEditSensorName         ,3,1)
        self.layoutSensor.addWidget(self.lineEditSensorPositionX    ,4,1)
        self.layoutSensor.addWidget(self.lineEditSensorPositionY    ,5,1)
        self.layoutSensor.addWidget(self.lineEditSensorPositionZ    ,6,1)

        self.layoutSensor.addWidget(self.buttonSensorSave       ,7,0,1,2)

        self.widgetSensor = QWidget()
        self.widgetSensor.setLayout(self.layoutSensor)


        '''Define ConfigurationWindow for Wire'''
        '''Labels, Edits, Buttons'''
        self.labelWireDevice = QLabel("Typ:")
        self.lineEditWireDevice = QLabel("Kabel")

        self.labelWireSize = QLabel("Knopgröße:")
        self.lineEditWireSize = QSlider(Qt.Orientation.Horizontal)
        self.lineEditWireSize.setMinimum(10)
        self.lineEditWireSize.setMaximum(100)
        self.lineEditWireSize.valueChanged.connect(self.size_slider)

        self.labelWireId = QLabel("ID:")
        self.lineEditWireId = QComboBox()
        self.lineEditWireId.currentTextChanged.connect(self.show_selected_id)

        self.labelWireName = QLabel("Name:")
        self.lineEditWireName = QLineEdit()

        self.labelWireFirstDevice = QLabel("1.Gerät:")
        self.lineEditWireFirstDevice = QComboBox()

        self.labelWireSecondDevice = QLabel("2.Gerät:")
        self.lineEditWireSecondDevice = QComboBox()

        self.buttonWireSave = QPushButton("Speichern")
        self.buttonWireSave.clicked.connect(self.save_configuration)

        spacerWire = QWidget(self)
        spacerWire.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Expanding)

        '''define Layout'''
        self.layoutWire = QGridLayout()
        self.layoutWire.addWidget(self.labelWireDevice      ,0,0)
        self.layoutWire.addWidget(self.labelWireSize        ,1,0)
        self.layoutWire.addWidget(self.labelWireId          ,2,0)
        self.layoutWire.addWidget(self.labelWireName        ,3,0)
        self.layoutWire.addWidget(self.labelWireFirstDevice ,4,0)
        self.layoutWire.addWidget(self.labelWireSecondDevice,5,0)
        self.layoutWire.addWidget(spacerWire                ,7,0)

        self.layoutWire.addWidget(self.lineEditWireDevice       ,0,1)
        self.layoutWire.addWidget(self.lineEditWireSize         ,1,1)
        self.layoutWire.addWidget(self.lineEditWireId           ,2,1)
        self.layoutWire.addWidget(self.lineEditWireName         ,3,1)
        self.layoutWire.addWidget(self.lineEditWireFirstDevice  ,4,1)
        self.layoutWire.addWidget(self.lineEditWireSecondDevice ,5,1)

        self.layoutWire.addWidget(self.buttonWireSave, 6, 0, 1, 2)

        self.widgetWire = QWidget()
        self.widgetWire.setLayout(self.layoutWire)

        '''Define ConfigurationWindow for Event'''
        '''Labels, Edits, Buttons'''

        self.labelDSLEventTitle = QLabel("Typ:")
        self.lineEditDSLEventDevice = QLabel("Event")

        self.labelDSLEventId = QLabel("ID:")
        self.lineEditDSLEventId = QComboBox()
        self.lineEditDSLEventId.currentTextChanged.connect(self.show_DSLEvent)
        self.update_DSLEventBox()

        self.labelDSLEventName = QLabel("Name:")
        self.lineEditDSLEventName = QLineEdit()

        self.buttonDSLEventSave = QPushButton("Speichern")
        self.buttonDSLEventSave.clicked.connect(self.save_DSLEvent)

        spacerDSLEvent = QWidget(self)
        spacerDSLEvent.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Expanding)

        '''define Layout'''
        self.layoutDSLEvent = QGridLayout()
        self.layoutDSLEvent.addWidget(self.labelDSLEventTitle, 0, 0)
        self.layoutDSLEvent.addWidget(self.labelDSLEventId, 1, 0)
        self.layoutDSLEvent.addWidget(self.labelDSLEventName, 2, 0)
        self.layoutDSLEvent.addWidget(spacerDSLEvent, 4, 0)

        self.layoutDSLEvent.addWidget(self.lineEditDSLEventDevice, 0, 1)
        self.layoutDSLEvent.addWidget(self.lineEditDSLEventId, 1, 1)
        self.layoutDSLEvent.addWidget(self.lineEditDSLEventName, 2, 1)

        self.layoutDSLEvent.addWidget(self.buttonDSLEventSave, 3, 0, 1, 2)

        self.widgetDSLEvent = QWidget()
        self.widgetDSLEvent.setLayout(self.layoutDSLEvent)

        '''setup widget stack'''
        self.layoutMain = QStackedLayout()
        self.layoutMain.addWidget(self.widgetCamera)
        self.layoutMain.addWidget(self.widgetSensor)
        self.layoutMain.addWidget(self.widgetWire)
        self.layoutMain.addWidget(self.widgetDSLEvent)

        self.layoutMain.setCurrentIndex(0)
        self.setLayout(self.layoutMain)



    '''This method changes the displayed Widget in the ConfigurationDockWidget'''
    def change_Widget(self, index):
        self.layoutMain.setCurrentIndex(index)


    '''This method shows the parameter of the clicked planElement'''
    def show_planElement_configuration(self, planElement = None):
        if self.variables["selected_tool"] == "delete":
            self.clear_configuration()
            return

        if planElement:
            self.selectedPlanElement = planElement
        elif self.selectedPlanElement == None:
            return

        self.update_idBoxes()
        if isinstance(self.selectedPlanElement, Devices.Camera):
            self.layoutMain.setCurrentIndex(0)
            self.lineEditCameraName.setText(str(self.selectedPlanElement.name))
            self.lineEditCameraSize.setValue(int(self.selectedPlanElement.size))
            self.lineEditCameraModel.setText(str(self.selectedPlanElement.modell))
            self.lineEditCameraIpAddress.setText(str(self.selectedPlanElement.ipAddress))
            self.lineEditCameraPositionX.setText(str(self.selectedPlanElement.positionX))
            self.lineEditCameraPositionY.setText(str(self.selectedPlanElement.positionY))
            self.lineEditCameraPositionZ.setText(str(self.selectedPlanElement.positionZ))
            self.lineEditCameraDSLEvent.setCurrentText(str(self.selectedPlanElement.DSLEventId))
        elif isinstance(self.selectedPlanElement, Devices.Sensor):
            self.layoutMain.setCurrentIndex(1)
            self.lineEditSensorName.setText(str(self.selectedPlanElement.name))
            self.lineEditSensorSize.setValue(int(self.selectedPlanElement.size))
            self.lineEditSensorPositionX.setText(str(self.selectedPlanElement.positionX))
            self.lineEditSensorPositionY.setText(str(self.selectedPlanElement.positionY))
            self.lineEditSensorPositionZ.setText(str(self.selectedPlanElement.positionZ))
        elif isinstance(self.selectedPlanElement, Devices.Wire):
            self.layoutMain.setCurrentIndex(2)
            self.lineEditWireName.setText(str(self.selectedPlanElement.name))
            self.lineEditWireSize.setValue(int(self.selectedPlanElement.size))
            self.lineEditWireFirstDevice.clear()
            self.lineEditWireSecondDevice.clear()
            for element in self.devicePlan.planList:
                if isinstance(element, Devices.Device):
                    self.lineEditWireFirstDevice.addItem(str(element.id) + ":" + element.name)
                    self.lineEditWireSecondDevice.addItem(str(element.id) + ":" + element.name)
            self.lineEditWireFirstDevice.setCurrentText(str(self.selectedPlanElement.firstDevice.id)+":"+self.selectedPlanElement.firstDevice.name)
            self.lineEditWireSecondDevice.setCurrentText(str(self.selectedPlanElement.secondDevice.id)+":"+self.selectedPlanElement.secondDevice.name)
        else:
            logger.debug("not reconized")


    def update_idBoxes(self):
        self.lineEditCameraId.blockSignals(True)
        self.lineEditSensorId.blockSignals(True)
        self.lineEditWireId.blockSignals(True)
        self.lineEditCameraId.clear()
        self.lineEditSensorId.clear()
        self.lineEditWireId.clear()
        for planElement in self.devicePlan.planList:
            if isinstance(planElement, Devices.Camera):
                self.lineEditCameraId.addItem(str(planElement.id) + ":" + planElement.name)
            elif isinstance(planElement, Devices.Sensor):
                self.lineEditSensorId.addItem(str(planElement.id) + ":" + planElement.name)
            elif isinstance(planElement, Devices.Wire):
                self.lineEditWireId.addItem(str(planElement.id) + ":" + planElement.name)
            else:
                logger.debug("not reconized")
        if isinstance(self.selectedPlanElement, Devices.Camera):
            self.lineEditCameraId.setCurrentIndex(self.lineEditCameraId.findText(str(self.selectedPlanElement.id) + ":" + self.selectedPlanElement.name))
        elif isinstance(self.selectedPlanElement, Devices.Sensor):
            self.lineEditSensorId.setCurrentIndex(self.lineEditSensorId.findText(str(self.selectedPlanElement.id) + ":" + self.selectedPlanElement.name))
        elif isinstance(self.selectedPlanElement, Devices.Wire):
            self.lineEditWireId.setCurrentIndex(self.lineEditWireId.findText(str(self.selectedPlanElement.id) + ":" + self.selectedPlanElement.name))
        else:
            logger.debug("not reconized selected PlanElement: " + str(self.selectedPlanElement))

        self.lineEditCameraId.blockSignals(False)
        self.lineEditSensorId.blockSignals(False)
        self.lineEditWireId.blockSignals(False)


    def clear_configuration(self):
        self.selectedPlanElement = None
        self.lineEditCameraName.clear()
        self.lineEditCameraModel.clear()
        self.lineEditCameraIpAddress.clear()
        self.lineEditCameraPositionX.clear()
        self.lineEditCameraPositionY.clear()
        self.lineEditCameraPositionZ.clear()
        self.lineEditSensorName.clear()
        self.lineEditSensorPositionX.clear()
        self.lineEditSensorPositionY.clear()
        self.lineEditSensorPositionZ.clear()
        self.lineEditWireName.clear()
        self.lineEditWireFirstDevice.clear()
        self.lineEditWireSecondDevice.clear()
        self.update_idBoxes()

    '''This Method reads the configurations of devices which the user entered'''
    def save_configuration(self):
        if isinstance(self.selectedPlanElement, Devices.Camera):
            self.selectedPlanElement.size        = self.lineEditCameraSize.value()
            self.selectedPlanElement.name        = self.lineEditCameraName.text()
            self.selectedPlanElement.modell      = self.lineEditCameraModel.text()
            self.selectedPlanElement.ipAddress   = self.lineEditCameraIpAddress.text()
            self.selectedPlanElement.positionX   = int(self.lineEditCameraPositionX.text())
            self.selectedPlanElement.positionY   = int(self.lineEditCameraPositionY.text())
            self.selectedPlanElement.positionZ   = int(self.lineEditCameraPositionZ.text())
            self.selectedPlanElement.DSLEventId  = self.lineEditCameraDSLEvent.currentText()
        elif isinstance(self.selectedPlanElement, Devices.Sensor):
            self.selectedPlanElement.size        = self.lineEditSensorSize.value()
            self.selectedPlanElement.name        = self.lineEditSensorName.text()
            self.selectedPlanElement.positionX   = int(self.lineEditSensorPositionX.text())
            self.selectedPlanElement.positionY   = int(self.lineEditSensorPositionY.text())
            self.selectedPlanElement.positionZ   = int(self.lineEditSensorPositionZ.text())
        elif isinstance(self.selectedPlanElement, Devices.Wire):
            self.selectedPlanElement.size        = self.lineEditWireSize.value()
            self.selectedPlanElement.name        = self.lineEditWireName.text()
            self.selectedPlanElement.firstDevice = self.devicePlan.get_element_by_id(self.lineEditWireFirstDevice.currentText().split(':')[0])
            self.selectedPlanElement.secondDevice = self.devicePlan.get_element_by_id(self.lineEditWireSecondDevice.currentText().split(':')[0])
        else:
            logger.debug("not reconized")
        logger.debug("emit signal")
        self.signalUpdate.emit()
        self.update_idBoxes()


    def size_slider(self, value):
        if self.selectedPlanElement:
            self.selectedPlanElement.size = value
            self.signalUpdate.emit()


    def show_selected_id(self, text):
        texts = text.split(":")
        selectedPlanElement = self.devicePlan.get_element_by_id(texts[0])
        self.show_planElement_configuration(selectedPlanElement)


    '''Methods for DSLEvents'''
    def save_DSLEvent(self):
        self.DSLEventWidgetRoot.readout_widgets()
        #position change
        self.DSLEventWidgetRoot.DSLEventListHandler.add_DSLEvent_to_section(name = self.lineEditDSLEventName.text())
        self.update_DSLEventBox()

    def show_DSLEvent(self, idText):
        texts = idText.split(':')[0].split('.')
        self.selectedDSLEvent = (texts[0], texts[1])

        self.DSLEventWidgetRoot.clear()
        self.DSLEventWidgetRoot.add_DSLEvent_by_section_id(texts[0], texts[1])

    def update_DSLEventBox(self):
        try:
            self.lineEditDSLEventId.blockSignals(True)
            self.lineEditCameraDSLEvent.blockSignals(True)
            self.lineEditDSLEventId.clear()
            self.lineEditCameraDSLEvent.clear()
            for section in self.DSLEventWidgetRoot.DSLEventListHandler.DSLEventDictionary.keys():
                for key in self.DSLEventWidgetRoot.DSLEventListHandler.DSLEventDictionary[section].keys():
                    self.lineEditDSLEventId.addItem(section+"."+key+":"+ self.DSLEventWidgetRoot.DSLEventListHandler.DSLEventDictionary[section][key]["name"])
                    if section == "basic":
                        continue
                    else:
                        self.lineEditCameraDSLEvent.addItem(section+"."+key+":"+ self.DSLEventWidgetRoot.DSLEventListHandler.DSLEventDictionary[section][key]["name"])
            self.lineEditDSLEventId.blockSignals(False)
            self.lineEditCameraDSLEvent.blockSignals(False)
        except Exception as exception:
            logger.debug("Failed to update DSLEventbox:", exception)