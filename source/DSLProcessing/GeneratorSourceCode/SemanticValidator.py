from textx import metamodel_from_file, textx_isinstance

class SemanticValidator():
    def __init__(self, DSL_meta):
        self.DSL_meta = DSL_meta
        self.deviceList = []
        self.connectableDeviceList = []
        self.basicEventList = []
        self.customEventList = []
        self.cameraList = []
        self.connectionList = []
        self.receiveDataList = []
        self.sendDataList = []
        self.variableList = []
        self.returnMessage = ""

    def semantic_check(self, command):
        self.add_command(command)


    def add_command(self, command):
        if textx_isinstance(command, self.DSL_meta["Device"]):
            self.deviceList.append(command)
            self.returnMessage += self.rule_unique_deviceNames()
            self.returnMessage += self.rule_unique_positions()
            self.returnMessage += self.rule_deviceEvent_defined()

        if textx_isinstance(command, self.DSL_meta["Camera"]):
            self.cameraList.append(command)
            self.connectableDeviceList.append(command)

            self.returnMessage += self.typecheck_parameter_camera(command)

        if textx_isinstance(command, self.DSL_meta["Sensor"]):
            self.connectableDeviceList.append(command)

        if textx_isinstance(command, self.DSL_meta["Connection"]):
            self.connectionList.append(command)
            self.returnMessage += self.rule_connection_device()

        if textx_isinstance(command, self.DSL_meta["BasicEvent"]):
            self.basicEventList.append(command)

            self.returnMessage += self.typecheck_parameter_basicEvent(command)

        if textx_isinstance(command, self.DSL_meta["CustomEvent"]):
            self.customEventList.append(command)
            self.returnMessage += self.rule_unique_eventNames()

        if textx_isinstance(command, self.DSL_meta["ReceiveData"]):
            self.receiveDataList.append(command)
            self.returnMessage += self.rule_receiveData_device()

        if textx_isinstance(command, self.DSL_meta["SendData"]):
            self.sendDataList.append(command)
            
        if textx_isinstance(command, self.DSL_meta["Variable"]):
            self.variableList.append(command)


    # jede position darf nur einmal genutzt werden
    def rule_unique_positions(self):
        errorCode = ""
        positions = []
        for device in self.deviceList:
            if not textx_isinstance(device, self.DSL_meta["Connection"]):
                if device.position in positions:
                    errorCode += f"\ndevice-position: {device.position} is not unique."
                else:
                    positions.append(device.position)
        return errorCode

    # jeder name von Devices muss einzigartig sein
    def rule_unique_deviceNames(self):
        errorCode = ""
        names = []
        for device in self.deviceList:
            if device.name in names:
                errorCode += f"\ndevice-name: {device.name} is not unique."
            else:
                names.append(device.name)
        return errorCode

    # jeder name von Events muss einzigartig sein
    def rule_unique_eventNames(self):
        errorCode = ""
        names = []
        for event in (self.basicEventList + self.customEventList):
            if event.name in names:
                errorCode += f"\nevent-name: {event.name} is not unique."
            else:
                names.append(event.name)
        return errorCode

    # Das von einer Kamera genutzte Event muss definiert sein
    def rule_deviceEvent_defined(self):
        errorCode = ""
        names = list(map(lambda event: event.name, self.customEventList))
        for camera in self.cameraList:
            if not camera.eventName in names:
                errorCode += f"\ncamera-customEvent: {camera.eventName} is not defined."
        return errorCode

    # Das Gerät, von dem Daten empfangen werden sollen muss definiert sein
    def rule_receiveData_device(self):
        errorCode = ""
        names = list(map(lambda device: device.name, self.deviceList))
        for receiveData in self.receiveDataList:
            if not receiveData.transmitterDevice in names:
                errorCode += f"\nreceiveData-transmitterDevice: {receiveData.transmitterDevice} is not defined."
        return errorCode

    # Die von einer Connection verbundenen Geräte müssen definiert und verschieden sein.
    def rule_connection_device(self):
        errorCode = ""
        names = list(map(lambda device: device.name, self.connectableDeviceList))
        for connection in self.connectionList:
            if connection.firstDevice not in names:
                errorCode += f"\nConnection-firstDevice: {connection.firstDevice} is not defined."
            if connection.secondDevice not in names:
                errorCode += f"\nConnection-secondDevice: {connection.secondDevice} is not defined."
            if connection.firstDevice == connection.secondDevice:
                errorCode += f"\nConnection, connected devices cant't be the same: {connection.firstDevice}."
        return errorCode

    # Check der Parameter, die noch nicht durch die Syntax sichergestellt werden
    def typecheck_parameter_camera(self, camera):
        errorCode = ""
        names = list(map(lambda variable: variable.name, self.variableList))
        if not isinstance(camera.ipAddress, str):
            if textx_isinstance(camera.ipAddress, self.DSL_meta["ArithmeticOperation"]) and camera.ipAddress.operand[0].operand not in names:
                print(type(camera.ipAddress.operand[0].operand))
                errorCode += f"The Ip-Address of the camera {camera.name} needs to be a string."
        return errorCode

    def typecheck_parameter_basicEvent(self, event):
        def typecheck_parameter_eventWait(event):
            errorCode = ""
            if not (isinstance(event.duration, (int, float))):
                errorCode += f"The duration of the EventWait needs to be a number."
            return errorCode
        def typecheck_parameter_eventPhotos(event):
            errorCode = ""
            if not (isinstance(event.count, int)):
                errorCode += f"The number of images of the EventPhotos needs to be an integer number."
            if not (isinstance(event.delay, (int, float))):
                errorCode += f"The delay of the EventPhotos needs to be a number."
            return errorCode

        if textx_isinstance(event, self.DSL_meta["EventWait"]):
            return typecheck_parameter_eventWait(event)
        elif textx_isinstance(event, self.DSL_meta["EventPhotos"]):
            return typecheck_parameter_eventPhotos(event)
        else:
            return ""