import logging.config
logging.config.fileConfig('../resources/configurations/logging.conf')
logger = logging.getLogger(__name__)

class Device:
    def __init__(self, id, button, positionX, positionY, positionZ=0, size = 30, name="/"):
        self.id = id
        self.button = button
        self.positionX = positionX
        self.positionY = positionY
        self.positionZ = positionZ
        self.size = size
        self.name = name

class Camera(Device):
    def __init__(self, id, button, positionX, positionY, positionZ = 0, size = 30, name="/", modell = "/", ipAddress = "0.0.0.0", DSLEventId = None):
        super().__init__(id, button, positionX, positionY, positionZ, size, name)
        self.modell = modell
        self.ipAddress = ipAddress
        self.DSLEventId = DSLEventId

    def create_dictionary(self):
        dictionary = {
            "id": self.id,
            "class": "camera",
            "positionX": self.positionX,
            "positionY": self.positionY,
            "positionZ": self.positionZ,
            "size": self.size,
            "name": self.name,
            "modell": self.modell,
            "ipAddress": self.ipAddress,
            "DSLEventIdList": self.DSLEventId,
        }
        return dictionary

    def create_DSLline(self):
        line = (f"Camera({self.name}_{self.id}, ({self.positionX},{self.positionY},{self.positionZ}), \"{self.ipAddress}\", {self.DSLEventId})")
        return line

class Sensor(Device):
    def __init__(self, id, button, positionX, positionY, positionZ = 0, size = 30, name="/"):
        super().__init__(id, button, positionX, positionY, positionZ, size, name)

    def create_dictionary(self):
        dictionary = {
            "id": self.id,
            "class": "sensor",
            "positionX": self.positionX,
            "positionY": self.positionY,
            "positionZ": self.positionZ,
            "size": self.size,
            "name": self.name,
        }
        return dictionary


    def create_DSLline(self):
        line = (f"Sensor({self.name}_{self.id}, ({self.positionX},{self.positionY},{self.positionZ}))")
        return line

class Wire:
    def __init__(self, id, button, firstDevice, secondDevice, size = 20, name = "/"):
        self.id = id
        self.button = button
        self.firstDevice = firstDevice
        self.secondDevice = secondDevice
        self.name = name
        self.size = size

    def create_dictionary(self):
        dictionary = {
            "id": self.id,
            "class": "wire",
            "firstDevice": self.firstDevice.id,
            "secondDevice": self.secondDevice.id,
            "size": self.size,
            "name": self.name,
        }
        return dictionary


    def create_DSLline(self):
        line = (f"connect({self.firstDevice.name}_{self.firstDevice.id}, {self.secondDevice.name}_{self.secondDevice.id})")
        return line


class DevicePlan:
    def __init__(self, planList = []):
        self.planList = planList

    '''This method returns the first unused id it can find'''
    def get_new_id(self):
        usedID = []
        for element in self.planList:
            usedID.append(element.id)
        for index in range(len(self.planList)+1):
            if index not in usedID:
                return index

    def get_element_by_id(self, id):
        try:
            id = int(id)
        except Exception as e:
            logger.debug("Id nicht nutzbar:",e)
            return

        for element in self.planList:
            if element.id == id:
                return element
        return None
