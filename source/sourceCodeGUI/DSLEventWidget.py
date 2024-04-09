from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QSizePolicy, QPushButton
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag, QPixmap
import DSLEvent

import logging.config
logging.config.fileConfig('../resources/configurations/logging.conf')
logger = logging.getLogger(__name__)

'''A graphical representation is required for each basic event and a root widget on which they are placed'''
class DSLEventRootWidget(QWidget):
    def __init__(self, DSLEventListHandler, variables, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)

        self.variables = variables
        self.DSLEventListHandler = DSLEventListHandler
        self.DSLEventWidgetList = []

        self.layoutMain = QVBoxLayout()
        self.layoutMain.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layoutMain)

    '''Reads in the user data from the GUI and reorder the Events according to the Widgets'''
    def readout_widgets(self):
        for DSLEventWidget in self.DSLEventWidgetList:
            logger.debug(f"Try to readout {DSLEventWidget}")
            DSLEventWidget.readout_widget()

        currentWidgetListOrder = []
        for index in range(self.layoutMain.count()):
            currentWidgetListOrder.append(self.layoutMain.itemAt(index).widget())

        newOrder = []
        for indexEvent in range(len(self.DSLEventListHandler.DSLEventList)):
            for indexWidget in range(len(currentWidgetListOrder)):
                if self.DSLEventListHandler.DSLEventList[indexEvent] == currentWidgetListOrder[indexWidget].DSLEvent:
                    #print("neworder","Eventindex:", indexEvent, "WidgetIndex:", indexWidget)
                    newOrder.append(indexWidget)

        self.DSLEventListHandler.DSLEventList = [self.DSLEventListHandler.DSLEventList[index] for index in newOrder]

    '''Adds a widget to the root layout'''
    def add_DSLEventWidget(self, DSLEventWidget):
        self.layoutMain.addWidget(DSLEventWidget)
        self.DSLEventWidgetList.append(DSLEventWidget)


    def add_DSLEvent_by_section_id(self, section, id):
        logger.debug(f"Try to add section:{section}, id:{id}")
        try:
            if section == "basic":
                self.add_basic_DSLEventWidget(self.DSLEventListHandler.DSLEventDictionary[section][id]["name"])

            elif section in self.DSLEventListHandler.DSLEventDictionary.keys() and id in self.DSLEventListHandler.DSLEventDictionary[section].keys():
                newDSLEventCustom = DSLEvent.DSLEventCustom()
                newDSLEventCustom.read_in_dictionary(self.DSLEventListHandler.DSLEventDictionary[section][id])
                newDSLEventCustomWidget = newDSLEventCustom.create_Widget(self.variables)
                newDSLEventCustomWidget.clicked.connect(lambda: self.delete_DSLEvent(DSLEventWidget=newDSLEventCustomWidget))
                self.DSLEventListHandler.DSLEventList.append(newDSLEventCustom)
                self.add_DSLEventWidget(newDSLEventCustomWidget)

            else:
                logger.debug("[add_DSLEvent_by_section_id] combination not known:", section, id)

        except Exception as exception:
            logger.debug(f"Failed to add DSLEvent from Dictionary: {exception}")


    def add_basic_DSLEventWidget(self, DSLEventName, newDSLEventDictionary = None):
        try:
            match DSLEventName:
                case "DSLEventWait":
                    newDSLEventWait = DSLEvent.DSLEventWait()
                    if newDSLEventDictionary:
                        newDSLEventWait.read_in_dictionary(newDSLEventDictionary)
                    self.DSLEventListHandler.DSLEventList.append(newDSLEventWait)
                    newDSLEventWaitWidget = newDSLEventWait.create_Widget(self.variables)
                    newDSLEventWaitWidget.clicked.connect(lambda: self.delete_DSLEvent(DSLEventWidget=newDSLEventWaitWidget))
                    self.add_DSLEventWidget(newDSLEventWaitWidget)
                case "DSLEventPhoto":
                    newDSLEventPhoto = DSLEvent.DSLEventPhoto()
                    if newDSLEventDictionary:
                        newDSLEventPhoto.read_in_dictionary(newDSLEventDictionary)
                    self.DSLEventListHandler.DSLEventList.append(newDSLEventPhoto)
                    newDSLEventPhotoWidget = newDSLEventPhoto.create_Widget(self.variables)
                    newDSLEventPhotoWidget.clicked.connect(lambda: self.delete_DSLEvent(DSLEventWidget=newDSLEventPhotoWidget))
                    self.add_DSLEventWidget(newDSLEventPhotoWidget)
                case "DSLEventVideo":
                    newDSLEventVideo = DSLEvent.DSLEventVideo()
                    if newDSLEventDictionary:
                        newDSLEventVideo.read_in_dictionary(newDSLEventDictionary)
                    self.DSLEventListHandler.DSLEventList.append(newDSLEventVideo)
                    newDSLEventVideoWidget = newDSLEventVideo.create_Widget(self.variables)
                    newDSLEventVideoWidget.clicked.connect(lambda: self.delete_DSLEvent(DSLEventWidget=newDSLEventVideoWidget))
                    self.add_DSLEventWidget(newDSLEventVideoWidget)

        except Exception as exception:
            logger.debug("Failed to ad basic DSLWidget:", exception)


    def delete_DSLEvent(self, DSLEventWidget):
        try:
            if self.variables["selected_tool_logic"] == "delete":
                self.DSLEventListHandler.DSLEventList.remove(DSLEventWidget.DSLEvent)

                self.DSLEventWidgetList.remove(DSLEventWidget)
                DSLEventWidget.setParent(None)
                self.layoutMain.removeWidget(DSLEventWidget)
        except Exception as exception:
            logger.debug("Failed to delete DSLWidget:", exception)

    def clear(self):
        try:
            self.DSLEventListHandler.DSLEventList.clear()
            self.DSLEventWidgetList.clear()
            for index in range(self.layoutMain.count()):
                self.layoutMain.itemAt(index).widget().deleteLater()
        except Exception as exception:
            logger.debug(f"Failed to clear LogicView: {exception}")


    def dragEnterEvent(self, e):
        e.accept()


    def dropEvent(self, e):
        new_x = e.position().x()
        new_y = e.position().y()
        dropedWidget = e.source()

        self.layoutMain.removeWidget(dropedWidget)
        for index in range(self.layoutMain.count()):
            widget = self.layoutMain.itemAt(index).widget()
            if widget.pos().y() + widget.size().height() // 2 > new_y:
                break
        else:
            if index > 0:
                index += 1

        self.layoutMain.insertWidget(index, dropedWidget)



class DSLEventWidget(QPushButton):
    def __init__(self, variables, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.variables = variables
        self.setStyleSheet('background-color: white;')
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton and self.variables["selected_tool_logic"] == None:
            if isinstance(self.parent(), DSLEventRootWidget):

                drag = QDrag(self)
                mime = QMimeData()
                drag.setMimeData(mime)

                pixmap = QPixmap(self.size())
                self.render(pixmap)
                drag.setPixmap(pixmap)
                drag.exec(Qt.DropAction.MoveAction)



class DSLEventCustomWidget(DSLEventWidget):
    def __init__(self, DSLEventCustom, variables, *args, **kwargs):
        super().__init__(variables, *args, **kwargs)
        self.DSLEvent = DSLEventCustom
        self.DSLEventWidgetList = []

        self.layoutMain = QVBoxLayout()
        for DSLEvent in DSLEventCustom.DSLEventList:
            newDSLEventWidget = DSLEvent.create_Widget(variables)
            self.layoutMain.addWidget(newDSLEventWidget)
            self.DSLEventWidgetList.append(newDSLEventWidget)

        self.setLayout(self.layoutMain)

    def readout_widget(self):
        for DSLEventWidget in self.DSLEventWidgetList:
            DSLEventWidget.readout_widget()

    def delete_DSLEvent(self, DSLEventWidget):
        try:
            if self.variables["selected_tool_logic"] == "delete":
                DSLEventWidget.setParent(None)
                self.DSLEventWidgetList.remove(DSLEventWidget)
                self.layoutMain.removeWidget(DSLEventWidget)
        except Exception as exception:
            logger.debug("Failed to delete DSLWidget:", exception)



class DSLEventWaitWidget(DSLEventWidget):
    def __init__(self, DSLEventWait, variables, *args, **kwargs):
        super().__init__(variables, *args, **kwargs)

        self.DSLEvent = DSLEventWait

        self.labelLeft = QLabel("Warte", alignment = Qt.AlignmentFlag.AlignRight)
        self.labelLeft.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.labelRight = QLabel("Sekunden")
        self.labelRight.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.lineEditDuration = QLineEdit(str(DSLEventWait.duration))
        self.lineEditDuration.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.layoutMain = QHBoxLayout()
        self.layoutMain.addWidget(self.labelLeft)
        self.layoutMain.addWidget(self.lineEditDuration)
        self.layoutMain.addWidget(self.labelRight)

        self.setLayout(self.layoutMain)

    def readout_widget(self):
        try:
            self.DSLEvent.duration = self.lineEditDuration.text()
        except Exception as exception:
            logger.debug(f"Failed to readout: {exception}")


class DSLEventPhotosWidget(DSLEventWidget):
    def __init__(self, DSLEventPhoto, variables, *args, **kwargs):
        super().__init__(variables, *args, **kwargs)

        self.DSLEvent = DSLEventPhoto

        self.labelLeft = QLabel("Mache", alignment = Qt.AlignmentFlag.AlignRight)
        self.labelLeft.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.lineEditCount = QLineEdit(str(DSLEventPhoto.count))
        self.lineEditCount.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.labelMiddle = QLabel("mal ein Foto, im Abstand von")
        self.labelMiddle.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.lineEditDelay = QLineEdit(str(DSLEventPhoto.delay))
        self.lineEditDelay.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.labelRight = QLabel("Sekunden")
        self.labelRight.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.layoutMain = QHBoxLayout()
        self.layoutMain.addWidget(self.labelLeft)
        self.layoutMain.addWidget(self.lineEditCount)
        self.layoutMain.addWidget(self.labelMiddle)
        self.layoutMain.addWidget(self.lineEditDelay)
        self.layoutMain.addWidget(self.labelRight)

        self.setLayout(self.layoutMain)

    def readout_widget(self):
        try:
            self.DSLEvent.count = self.lineEditCount.text()
            self.DSLEvent.delay = self.lineEditDelay.text()
        except Exception as exception:
            logger.debug(f"Failed to readout: {exception}")

class DSLEventVideoWidget(DSLEventWidget):
    def __init__(self, DSLEventVideo, variables,  *args, **kwargs):
        super().__init__(variables, *args, **kwargs)

        self.DSLEvent = DSLEventVideo

        self.labelLeft = QLabel("Filme für", alignment = Qt.AlignmentFlag.AlignRight)
        self.labelLeft.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.lineEditDuration = QLineEdit(str(DSLEventVideo.duration))
        self.lineEditDuration.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.labelRight = QLabel("Sekunden")
        self.labelRight.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.layoutMain = QHBoxLayout()
        self.layoutMain.addWidget(self.labelLeft)
        self.layoutMain.addWidget(self.lineEditDuration)
        self.layoutMain.addWidget(self.labelRight)

        self.setLayout(self.layoutMain)

    def readout_widget(self):
        try:
            self.DSLEvent.duration = self.lineEditDuration.text()
        except Exception as exception:
            logger.debug(f"Failed to readout: {exception}")