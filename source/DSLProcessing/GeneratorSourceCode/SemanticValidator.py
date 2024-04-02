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

        self.variableList = []
        self.variableNameList = []
        self.returnMessage = ""

    def semantic_check(self, command):
        self.add_command(command)


    def add_command(self, command):
        print("addCommand", type(command))

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
            for evetnCommand in command.commandList:
                self.add_command(evetnCommand)

        if textx_isinstance(command, self.DSL_meta["Functions"]):
            self.returnMessage += self.typecheck_parameter_functions(command)

        if textx_isinstance(command, self.DSL_meta["Variable"]):
            self.variableList.append(command)
            self.variableNameList.append(command.name)


    # jede position darf nur einmal genutzt werden
    def rule_unique_positions(self):
        errorCode = ""
        positions = []
        for device in self.deviceList:
            if not textx_isinstance(device, self.DSL_meta["Connection"]):
                if device.position in positions:
                    errorCode += f"device-position: {device.position} is not unique."
                else:
                    positions.append(device.position)
        return errorCode

    # jeder name von Devices muss einzigartig sein
    def rule_unique_deviceNames(self):
        errorCode = ""
        names = []
        for device in self.deviceList:
            if device.name in names:
                errorCode += f"device-name: {device.name} is not unique."
            else:
                names.append(device.name)
        return errorCode

    # jeder name von Events muss einzigartig sein
    def rule_unique_eventNames(self):
        errorCode = ""
        names = []
        for event in (self.basicEventList + self.customEventList):
            if event.name in names:
                errorCode += f"event-name: {event.name} is not unique."
            else:
                names.append(event.name)
        return errorCode

    # Das von einer Kamera genutzte Event muss definiert sein
    def rule_deviceEvent_defined(self):
        errorCode = ""
        names = list(map(lambda event: event.name, self.customEventList))
        for camera in self.cameraList:
            if not camera.eventName in names:
                errorCode += f"camera-customEvent: {camera.eventName} is not defined."
        return errorCode

    # Das Gerät, von dem Daten empfangen werden sollen muss definiert sein
    def rule_receiveData_device(self):
        errorCode = ""
        names = list(map(lambda device: device.name, self.deviceList))
        for receiveData in self.receiveDataList:
            if not receiveData.transmitterDevice in names:
                errorCode += f"The transmitterDevice: {receiveData.transmitterDevice} in the Funktion 'ReceiveData' is not defined."
        return errorCode

    # Die von einer Connection verbundenen Geräte müssen definiert und verschieden sein.
    def rule_connection_device(self):
        errorCode = ""
        names = list(map(lambda device: device.name, self.connectableDeviceList))
        for connection in self.connectionList:
            if connection.firstDevice not in names:
                errorCode += f"Connection-firstDevice: {connection.firstDevice} is not defined."
            if connection.secondDevice not in names:
                errorCode += f"Connection-secondDevice: {connection.secondDevice} is not defined."
            if connection.firstDevice == connection.secondDevice:
                errorCode += f"Connection, connected devices cant't be the same: {connection.firstDevice}."
        return errorCode

    # Check der Parameter, die noch nicht durch die Syntax sichergestellt werden
    def typecheck_parameter_camera(self, camera):
        errorCode = ""
        if not isinstance(camera.ipAddress, str):
            if textx_isinstance(camera.ipAddress, self.DSL_meta["ArithmeticOperation"]) and camera.ipAddress.operand[0].operand not in self.variableNameList:
                print(type(camera.ipAddress.operand[0].operand))
                errorCode += f"The Ip-Address of the camera {camera.name} needs to be a string."
        return errorCode


    #überprüft erste welche Art von BasisEvent vorliegt und prüft im Anschluss mit der entsprechenden Funktion die Paramter
    def typecheck_parameter_basicEvent(self, event):
        def typecheck_parameter_eventWait(event):
            errorCode = ""
            if not self.typecheck_expression(event.duration, (int, float)):
                errorCode += f"The duration of the Event 'Wait' needs to be a number."
            return errorCode
        def typecheck_parameter_eventPhotos(event):
            errorCode = ""
            if not self.typecheck_expression(event.count, (int)):
                errorCode += f"The number of images of the Event 'Photos' needs to be an integer number."
            if not self.typecheck_expression(event.delay, (int, float)):
                errorCode += f"The delay of the Event 'Photos' needs to be a number."
            return errorCode

        def typecheck_parameter_eventVideo(event):
            errorCode = ""
            if not self.typecheck_expression(event.duration, (int, float)):
                errorCode += f"The duration of the Event 'Video' needs to be a number."
            return errorCode

        def typecheck_parameter_eventSaveLocation(event):
            errorCode = ""
            if not self.typecheck_expression(event.filepath, (str)):
                errorCode += f"The filepath of the Event 'SaveLocation' needs to be a string."
            return errorCode

        def typecheck_parameter_eventTimerTrigger(event):
            errorCode = ""
            if not self.typecheck_expression(event.duration, (int, float)):
                errorCode += f"The duration of the Event 'TimerTrigger' needs to be a string."
            return errorCode

        def typecheck_parameter_eventSignalTrigger(event):
            errorCode = ""
            if not self.typecheck_expression(event.inputLine, (str)):
                errorCode += f"The inputLine of the Event 'SignalTrigger' needs to be a string, like 'Pin2'"
            if not self.typecheck_expression(event.value, (bool)):
                errorCode += f"The value of the Event 'SignalTrigger' needs to be Boolean, like True/False."
            return errorCode

        def typecheck_parameter_eventSendSignal(event):
            errorCode = ""
            if not self.typecheck_expression(event.outputLine, (str)):
                errorCode += f"The outputLine of the Event 'SendSignal' needs to be a string, like 'Pin2'"
            if not self.typecheck_expression(event.value, (bool)):
                errorCode += f"The value of the Event 'SendSignal' needs to be Boolean, like True/False."
            return errorCode

        def typecheck_parameter_eventSendData(event):
            return ""

        def typecheck_parameter_eventReceiveData(event):
            self.variableNameList.append(event.variable)
            return ""

        def typecheck_parameter_eventConfiguration(event):
            errorCode = ""
            if event.attribute in ['width', 'height', 'offsetX', 'offsetY', 'exposuretime']:
                if not self.typecheck_expression(event.value, (int, float)):
                    errorCode += f"The value of the attribute {event.attribute} in Event 'EventConfiguration' needs to be a number."
            elif event.attribute in ['pixelformat']:
                if not self.typecheck_expression(event.value, (str)):
                    errorCode += f"The value of the attribute {event.attribute} in Event 'EventConfiguration' needs to be a String."
            return errorCode

        def typecheck_parameter_eventAutomatedSignal(event):
            errorCode = ""
            if not self.typecheck_expression(event.outputLine, (str)):
                errorCode += f"The outputLine of the Event 'AutomatedSignal' needs to be a string, like 'Pin2'"
            if not self.typecheck_expression(event.value, (bool)):
                errorCode += f"The value of the Event 'AutomatedSignal' needs to be Boolean, like True/False."
            return errorCode


        if textx_isinstance(event, self.DSL_meta["EventWait"]):
            return typecheck_parameter_eventWait(event)
        elif textx_isinstance(event, self.DSL_meta["EventPhotos"]):
            return typecheck_parameter_eventPhotos(event)
        elif textx_isinstance(event, self.DSL_meta["EventVideo"]):
            return typecheck_parameter_eventVideo(event)
        elif textx_isinstance(event, self.DSL_meta["EventSaveLocation"]):
            return typecheck_parameter_eventSaveLocation(event)
        elif textx_isinstance(event, self.DSL_meta["EventTimerTrigger"]):
            return typecheck_parameter_eventTimerTrigger(event)
        elif textx_isinstance(event, self.DSL_meta["EventSignalTrigger"]):
            return typecheck_parameter_eventSignalTrigger(event)
        elif textx_isinstance(event, self.DSL_meta["EventSendSignal"]):
            return typecheck_parameter_eventSendSignal(event)
        elif textx_isinstance(event, self.DSL_meta["EventSendData"]):
            return typecheck_parameter_eventSendData(event)
        elif textx_isinstance(event, self.DSL_meta["EventReceiveData"]):
            return typecheck_parameter_eventReceiveData(event)
        elif textx_isinstance(event, self.DSL_meta["EventConfiguration"]):
            return typecheck_parameter_eventConfiguration(event)
        elif textx_isinstance(event, self.DSL_meta["AutomatedSignal"]):
            return typecheck_parameter_eventAutomatedSignal(event)
        else:
            return ""


    def typecheck_parameter_functions(self, function):
        def typecheck_parameter_sendData(function):
            return ""

        def typecheck_parameter_receiveData(function):
            errorCode = ""
            self.receiveDataList.append(function)
            errorCode += self.rule_receiveData_device()
            return errorCode

        def typecheck_parameter_sendTCP(function):
            errorCode = ""
            if not self.typecheck_expression(function.ipAddress, (str)):
                errorCode += f"The ipAddress of the Function 'SendTCP' needs to be a String."
            if not self.typecheck_expression(function.port, (int)):
                errorCode += f"The port of the Function 'SendTCP' needs to be a Integer."
            return errorCode

        def typecheck_parameter_receiveTCP(function):
            errorCode = ""
            if not self.typecheck_expression(function.ipAddress, (str)):
                errorCode += f"The ipAddress of the Function 'ReceiveTCP' needs to be a String."
            if not self.typecheck_expression(function.port, (int)):
                errorCode += f"The port of the Function 'ReceiveTCP' needs to be a Integer."
            return errorCode

        def typecheck_parameter_writeFile(function):
            errorCode = ""
            if not self.typecheck_expression(function.filename, (str)):
                errorCode += f"The filename of the Function 'WriteFile' needs to be a String."
            return errorCode

        def typecheck_parameter_readFile(function):
            errorCode = ""
            if not self.typecheck_expression(function.filename, (str)):
                errorCode += f"The filename of the Function 'ReadFile' needs to be a String."
            return errorCode

        def typecheck_parameter_trigger(function):
            errorCode = ""
            if not self.typecheck_expression(function.filename, ()):
                errorCode += f"The device of the Function 'Trigger' needs to be defined."
            return errorCode

        if textx_isinstance(function, self.DSL_meta["SendData"]):
            return typecheck_parameter_sendData(function)
        elif textx_isinstance(function, self.DSL_meta["ReceiveData"]):
            return typecheck_parameter_receiveData(function)
        elif textx_isinstance(function, self.DSL_meta["SendTCP"]):
            return typecheck_parameter_sendTCP(function)
        elif textx_isinstance(function, self.DSL_meta["ReceiveTCP"]):
            return typecheck_parameter_receiveTCP(function)
        elif textx_isinstance(function, self.DSL_meta["WriteFile"]):
            return typecheck_parameter_writeFile(function)
        elif textx_isinstance(function, self.DSL_meta["ReadFile"]):
            return typecheck_parameter_readFile(function)
        elif textx_isinstance(function, self.DSL_meta["Trigger"]):
            return typecheck_parameter_trigger(function)
        else:
            return ""

    def typecheck_expression(self, expression, demandedTypes):
        errorCode = ""
        if textx_isinstance(expression, self.DSL_meta["ArithmeticOperation"]):
            for operand in expression.operand:
                if not textx_isinstance(operand, self.DSL_meta["Symbol"]) and not self.typecheck_expression(operand, demandedTypes):
                    return False
            return True
        elif textx_isinstance(expression, self.DSL_meta["Functions"]):
            print("Funktion need implementation")
            return True
        elif textx_isinstance(expression, self.DSL_meta["Operand"]):
            if isinstance(expression.operand, demandedTypes):
                return True
            elif expression.operand in self.variableNameList:
                return True
        else:
            return False
