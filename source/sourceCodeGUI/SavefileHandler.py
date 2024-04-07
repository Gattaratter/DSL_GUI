import json
from PyQt6.QtWidgets import QPushButton

import logging.config
logging.config.fileConfig('../resources/configurations/logging.conf')
logger = logging.getLogger(__name__)

class SaveFileHandler:
    def __init__(self, filePath):
        self.filePath = filePath


class DevicePlanFileHandler(SaveFileHandler):
    def __init__(self,filePath):
        super().__init__(filePath)

    def load_devicePlan(self):
        with open(self.filePath[0], 'r') as savefile:
            devicePlanList = json.load(savefile)
            savefile.close()
        return devicePlanList


    def save_devicePlan(self, devicePlan):
        devicePlanList = []
        for element in devicePlan.planList:
            devicePlanList.append(element.create_dictionary())
        path = self.filePath[0]
        if path[-5:] != ".json":
            path += ".json"
        with open(path, 'w') as savefile:
            json.dump(devicePlanList, savefile, indent=4)


class DSLEventFileHandler(SaveFileHandler):
    def __init__(self, filePath):
        super().__init__(filePath)

    def load_basic_DSLEventDict(self):
        with open(self.filePath, 'r') as savefile:
            DSLEventDict = json.load(savefile)
            savefile.close()
        return DSLEventDict

    def load_custom_DSLEventDict(self):
        with open(self.filePath, 'r') as savefile:
            DSLEventDict = json.load(savefile)
            savefile.close()
        return DSLEventDict

    def save_custom_DSLEventDict(self, DSLEventDict):
        path = self.filePath
        if path[-5:] != ".json":
            path += ".json"
        with open(path, 'w') as savefile:
            json.dump(DSLEventDict, savefile, indent=4)


class DSLFileHandler(SaveFileHandler):
    def __init__(self,filePath):
        super().__init__(filePath)

    def save_DSLCode(self,  devicePlan, DSLEventListHandler):
        try:
            path = self.filePath
            if path[-4:] != ".cam":
                path += ".cam"

            lines_DSLEvents = ""
            lines_devices = ""

            '''if device Names are not unique adds the id to the name to unsure loading the saved modell is possible'''
            names = []
            for device in devicePlan.planList:
                if device.name in names:
                    device.name = device.name+"_"+str(device.id)
                names.append(device.name)

            for device in devicePlan.planList:
                '''create DSL-Code for DeviceObjects'''
                lines_devices += device.create_DSLline() + "\n"
            '''create DSL-Code for Event logic'''
            lines_DSLEvents += DSLEventListHandler.create_DSLlines() + "\n"
            logger.debug(f"success")
        except Exception as exception:
            logger.debug(f"Error while genereating DSL-Modell:{exception}")

        with open(path, 'w') as savefile:
            savefile.write("#The following lines define all the custom Events which were created" + "\n")
            savefile.write(lines_DSLEvents + "\n")
            savefile.write("\n"+"#The following lines define all the devices which were created" + "\n")
            savefile.write(lines_devices + "\n")
