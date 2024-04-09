from textx import metamodel_from_file, textx_isinstance
import Devices
import DSLEvent
import SavefileHandler

class DSLModelInterpreter():
    def __init__(self, filepath):
        self.DSL_meta = metamodel_from_file("../DSLProcessing/camera_grammar.tx")
        self.filepath = filepath
        self.DSLProgramm = self.DSL_meta.model_from_file(self.filepath)

        self.customEventDictionaryList = []

        self.dictionaryList = []
        self.deviceID = 0

        self.DSLCustomEventListHandler = DSLEvent.DSLEventListHandler()
        self.DSLCustomEventListHandler.DSLEventDictionary["custom"] = {}
        self.eventID = 0

        #self.saveFileHandler = SavefileHandler.DSLEventFileHandler("../savefiles/DSLEvents/BasicCamera/basicCamera01.json")
        #self.basicDSLEvents = self.saveFileHandler.load_basic_DSLEventDict()
        #self.basicDSLEventsNames = [self.basicDSLEvents[key]["name"] for key in self.basicDSLEvents.keys()]


    def load_DSLModel(self):
        for command in self.DSLProgramm.commands:
            if textx_isinstance(command, self.DSL_meta["Device"]):
                self.create_device(command)

            if textx_isinstance(command, self.DSL_meta["CustomEvent"]):
                self.create_customEvent(command)

    def create_device(self, device):
        '''creates a dict for the planList which is loaded in the MainWindow'''
        def create_camera(camera):
            positions = camera.position.replace('(','').replace(')','').split(',')
            dictionary = {
                "id": self.deviceID,
                "class": "camera",
                "positionX": int(positions[0]),
                "positionY": int(positions[1]),
                "positionZ": int(positions[2]),
                "size": 30,
                "name": camera.name,
                "modell": "None",
                "ipAddress": camera.ipAddress,
                "DSLEventIdList": camera.eventName
            }
            self.deviceID += 1
            self.dictionaryList.append(dictionary)

        def create_sensor(sensor):
            positions = sensor.position.replace('(','').replace(')','').split(',')
            dictionary = {
                "id": self.deviceID,
                "class": "sensor",
                "positionX": int(positions[0]),
                "positionY": int(positions[1]),
                "positionZ": int(positions[2]),
                "size": 30,
                "name": sensor.name
            }
            self.deviceID += 1
            self.dictionaryList.append(dictionary)

        def create_connection(connection):
            firstDevice = ""
            secondDevice = ""
            for device in self.dictionaryList:
                if device["name"] == connection.firstDevice:
                    firstDevice = device["id"]
                if device["name"] == connection.secondDevice:
                    secondDevice = device["id"]

            dictionary = {
                "id": self.deviceID,
                "class": "wire",
                "firstDevice": firstDevice,
                "secondDevice": secondDevice,
                "size": 20,
                "name": connection.name
            }
            self.deviceID += 1
            self.dictionaryList.append(dictionary)

        if textx_isinstance(device, self.DSL_meta["Camera"]):
            create_camera(device)
        if textx_isinstance(device, self.DSL_meta["Sensor"]):
            create_sensor(device)
        if textx_isinstance(device, self.DSL_meta["Connection"]):
            create_connection(device)

    def create_customEvent(self, event):
        def create_basicEvent(event):
            dictionary = {}
            if textx_isinstance(event, self.DSL_meta["EventWait"]):
                dictionary["name"] = "DSLEventWait"
                dictionary["duration"] = self.lines_expression(event.duration)
            elif textx_isinstance(event, self.DSL_meta["EventPhotos"]):
                dictionary["name"] = "DSLEventPhoto"
                dictionary["delay"] = self.lines_expression(event.delay)
                dictionary["count"] = self.lines_expression(event.count)
            elif textx_isinstance(event, self.DSL_meta["EventVideo"]):
                dictionary["name"] = "DSLEventVideo"
                dictionary["duration"] = self.lines_expression(event.duration)
            return dictionary

        def create_userEvent(event):
            dictionary = {}
            liste = []
            for command in event.commandList:
                if textx_isinstance(command, self.DSL_meta["BasicEvent"]):
                    liste.append(create_basicEvent(command))
                if textx_isinstance(command, self.DSL_meta["UserEvent"]):
                    for createdDictionary in self.customEventDictionaryList:
                        if createdDictionary["name"] == command.name:
                            liste.append(createdDictionary)

            dictionary["name"] = event.name
            dictionary["DSLEventDictionaryList"] = liste
            self.customEventDictionaryList.append(dictionary)
            return dictionary

        dictionary = create_userEvent(event)
        self.DSLCustomEventListHandler.DSLEventDictionary["custom"][str(self.eventID)] = dictionary
        self.eventID += 1

    def lines_expression(self, operand):
        lines = ""
        if isinstance(operand, str):
            lines += "\"" + operand + "\""
        elif isinstance(operand, bool):
            lines += str(operand)

        elif textx_isinstance(operand, self.DSL_meta["ArithmeticOperation"]):
            for operand in operand.operand:
                if isinstance(operand, str):
                    lines += str(operand)
                else:
                    lines += str(operand.operand)
        return lines
