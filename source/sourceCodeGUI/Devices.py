import logging.config
logging.config.fileConfig('../resources/configurations/logging.conf')
logger = logging.getLogger(__name__)


'''These classes implement each Device and its needed parameters and how they are saved'''
class Device:
    def __init__(self, id, button, positionX, positionY, positionZ=0, size = 30, name="none"):
        self.id = id
        self.button = button
        self.positionX = positionX
        self.positionY = positionY
        self.positionZ = positionZ
        self.size = size
        self.name = name

class Camera(Device):
    def __init__(self, id, button, positionX, positionY, positionZ = 0, size = 30, name="none", modell = "none", ipAddress = "0.0.0.0", DSLEventId = None):
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
        if self.DSLEventId:
            event = self.DSLEventId.split(':')[1]
        else:
            event = self.DSLEventId
        line = (f"Camera({self.name}, ({self.positionX},{self.positionY},{self.positionZ}), \"{self.ipAddress}\", {event})")
        return line

class Sensor(Device):
    def __init__(self, id, button, positionX, positionY, positionZ = 0, size = 30, name="none"):
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
        line = (f"Sensor({self.name}, ({self.positionX},{self.positionY},{self.positionZ}))")
        return line

class Wire:
    def __init__(self, id, button, firstDevice, secondDevice, size = 20, name = "none"):
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
        line = (f"Connection({self.name},{self.firstDevice.name}, {self.secondDevice.name}, wire, \"Pin1\")")
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
