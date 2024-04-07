from textx import metamodel_from_file, textx_isinstance
import Devices
import DSLEvent


class DSLModelInterpreter():
    def __init__(self, filepath):
        self.DSL_meta = metamodel_from_file("../DSLProcessing/camera_grammar.tx")
        self.filepath = filepath
        self.DSLProgramm = self.DSL_meta.model_from_file(self.filepath)

        self.dictionaryList =  []
        self.DSLEventList = DSLEvent.DSLEventListHandler()

        self.deviceID = 0

    def load_DSLModel(self):
        for command in self.DSLProgramm.commands:
            if textx_isinstance(command, self.DSL_meta["Device"]):
                self.create_device(command)

            if textx_isinstance(command, self.DSL_meta["CustomEvent"]):
                self.create_customEvent(command)

    def create_device(self, device):
        '''creates a dict which for the planList which is loaded in the MainWindow'''
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
        pass
