import SavefileHandler
import DSLEventWidget
from PyQt6.QtWidgets import QFileDialog, QWidget
from abc import ABC, abstractmethod

import logging.config
logging.config.fileConfig('../resources/configurations/logging.conf')
logger = logging.getLogger(__name__)

class DSLEventListHandler:
    def __init__(self, name = "none"):
        self.name = name
        self.DSLEventDictionary = {}
        self.DSLEventDictionary["custom"] = {}
        self.DSLEventList = []


    def create_DSLlines(self):
        lines = ""
        for section in self.DSLEventDictionary.keys():
            if "basic" not in section:
                for id in self.DSLEventDictionary[section]:
                    newDSLEventCustom = DSLEventCustom()
                    newDSLEventCustom.read_in_dictionary(self.DSLEventDictionary[section][id])
                    lines += newDSLEventCustom.create_DSLline()+"\n"
        return lines

    def load_basic_DSLEvents(self, filePath = "../savefiles/DSLEvents/BasicCamera/basicCamera01.json"):
        DSLEventFileHandler = SavefileHandler.DSLEventFileHandler(filePath)
        self.DSLEventDictionary["basic"] = DSLEventFileHandler.load_basic_DSLEventDict()

    def load_custom_DSLEvents(self, filePath):
        DSLEventFileHandler = SavefileHandler.DSLEventFileHandler(filePath)
        self.DSLEventDictionary["custom"] = DSLEventFileHandler.load_custom_DSLEventDict()

    def save_custom_DSLEvents(self):
        path = None
        try:
            path = QFileDialog.getSaveFileName(QWidget(), "Datei wählen", "../savefiles/DSLEvents/CustomCamera", "All Files (*)",)
        except Exception as e:
            logger.debug(f"[save_custom_DSLEvents] Fehler bei Dateiauswahl: {e}")
        if path[0]:
            DSLEventFileHandler = SavefileHandler.DSLEventFileHandler(path[0])
            DSLEventFileHandler.save_custom_DSLEventDict(self.DSLEventDictionary["custom"])

    def add_DSLEvent_to_section(self, name = "none", section = "custom"):
        try:
            if not section in self.DSLEventDictionary:
                self.DSLEventDictionary[section] = {}
            usedIDs = self.DSLEventDictionary["custom"].keys()
            for index in range(len(usedIDs)+1):
                if str(index) not in usedIDs:
                    break
            newDSLEventCustom = DSLEventCustom(name = name)
            newDSLEventCustom.DSLEventList = self.DSLEventList
            self.DSLEventDictionary["custom"][str(index)] = newDSLEventCustom.create_dictionary()

        except Exception as exception:
            logger.debug(f"Fehler beim hinzufügen des neuen Events: {exception}")

    def remove_DSLEvent_from_section(self, DSLEvent, section):
        pass

    def add_DSLEvent_section(self, section):
        pass

    def remove_DSLEvent_section(self, section):
        pass


class DSLEvent(ABC):
    @abstractmethod
    def read_in_dictionary(self, DSLEventDictionary):
        pass
    @abstractmethod
    def create_Widget(self, variables):
        pass
    @abstractmethod
    def create_dictionary(self):
        pass
    @abstractmethod
    def create_DSLline(self):
        pass


class DSLEventCustom(DSLEvent):
    def __init__(self, name = "none", DSLEventList = None):
        if DSLEventList is None:
            self.DSLEventList = []
        self.name = name

    def read_in_dictionary(self, DSLEventDictionary):
        self.DSLEventList.clear()
        self.name = DSLEventDictionary["name"]
        for DSLEventDictionary in DSLEventDictionary["DSLEventDictionaryList"]:
            if "DSLEventDictionaryList" not in DSLEventDictionary.keys():
                newDSLEvent = self.add_basic_DSLEvent(DSLEventDictionary)
                self.DSLEventList.append(newDSLEvent)

            else:
                nestedDSLEventCustom = DSLEventCustom()
                nestedDSLEventCustom.read_in_dictionary(DSLEventDictionary)
                self.DSLEventList.append(nestedDSLEventCustom)


    def add_basic_DSLEvent(self, DSLEventDictionary):
        try:
            match DSLEventDictionary["name"]:
                case "DSLEventWait":
                    newDSLEvent = DSLEventWait()
                    newDSLEvent.read_in_dictionary(DSLEventDictionary)
                case "DSLEventPhoto":
                    newDSLEvent = DSLEventPhoto()
                    newDSLEvent.read_in_dictionary(DSLEventDictionary)
                case "DSLEventVideo":
                    newDSLEvent = DSLEventVideo()
                    newDSLEvent.read_in_dictionary(DSLEventDictionary)
            return newDSLEvent

        except Exception as exception:
            logger.debug(f"Failed to ad basic DSLEvent: {exception}")

    def create_Widget(self, variables):
        widget = DSLEventWidget.DSLEventCustomWidget(self, variables)
        return widget

    def create_dictionary(self):
        DSLDictionaryList = []
        for DSLEvent in self.DSLEventList:
            DSLDictionaryList.append(DSLEvent.create_dictionary())
        dictionary = {
            "name": self.name,
            "DSLEventDictionaryList": DSLDictionaryList
        }
        return dictionary


    def create_DSLline(self):
        line = ""
        for DSLEvent in self.DSLEventList:
            if isinstance(DSLEvent, DSLEventCustom):
                if not line:
                    line += f"Event({DSLEvent.name})"
                else:
                    line += f"\n\t\t\t,Event({DSLEvent.name})"
                #line += DSLEvent.create_DSLline()+", "
            else:
                if not line:
                    line += f"{DSLEvent.create_DSLline()}"
                else:
                    line += f",\n\t\t\t{DSLEvent.create_DSLline()}"
        if self.name:
            name = self.name
        else:
            name = "none"
        line = f"Event({name}, [{line}])"
        return line


class DSLEventWait(DSLEvent):
    def __init__(self, duration = 0):
        self.name = "Wait"
        self.duration = duration

    def read_in_dictionary(self, DSLEventDictionary):
        self.duration = DSLEventDictionary["duration"]

    def create_Widget(self, variables):
        widget = DSLEventWidget.DSLEventWaitWidget(self, variables)
        return widget

    def create_dictionary(self):
        dictionary = {
            "name": "DSLEventWait",
            "duration": self.duration,
        }
        return dictionary

    def create_DSLline(self):
        line = (f"Event({self.name}, {self.duration})")
        return line

class DSLEventPhoto(DSLEvent):
    def __init__(self, delay = 1, count = 1):
        self.name = "Photos"
        self.delay = delay
        self.count = count

    def read_in_dictionary(self, DSLEventDictionary):
        self.delay = DSLEventDictionary["delay"]
        self.count = DSLEventDictionary["count"]

    def create_Widget(self, variables):
        widget = DSLEventWidget.DSLEventPhotosWidget(self, variables)
        return widget

    def create_dictionary(self):
        dictionary = {
            "name": "DSLEventPhoto",
            "delay": self.delay,
            "count": self.count,
        }
        return dictionary

    def create_DSLline(self):
        line = (
            f"Event({self.name}, {self.delay}, {self.count})")
        return line

class DSLEventVideo(DSLEvent):
    def __init__(self, duration = 0):
        self.name = "Video"
        self.duration = duration

    def read_in_dictionary(self, DSLEventDictionary):
        self.duration = DSLEventDictionary["duration"]

    def create_Widget(self, variables):
        widget = DSLEventWidget.DSLEventVideoWidget(self, variables)
        return widget

    def create_dictionary(self):
        dictionary = {
            "name": "DSLEventVideo",
            "duration": self.duration,
        }
        return dictionary

    def create_DSLline(self):
        line = (
            f"Event({self.name}, {self.duration})")
        return line