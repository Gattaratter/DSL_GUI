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

        self.variableList = []
        self.variableNameList = []
        self.returnMessage = ""

    def semantic_check(self, command):
        self.add_command(command)


    def add_command(self, command):
        print("addCommand", type(command))

        if textx_isinstance(command, self.DSL_meta["Device"]):
            self.returnMessage += self.typecheck_parameter_devices(command)
            self.deviceList.append(command)

        if textx_isinstance(command, self.DSL_meta["BasicEvent"]):
            self.returnMessage += self.typecheck_parameter_basicEvent(command)
            self.basicEventList.append(command)

        if textx_isinstance(command, self.DSL_meta["CustomEvent"]):
            self.customEventList.append(command)
            for eventCommand in command.commandList:
                self.add_command(eventCommand)

        if textx_isinstance(command, self.DSL_meta["Functions"]):
            self.returnMessage += self.typecheck_parameter_functions(command)

        if textx_isinstance(command, self.DSL_meta["Variable"]):
            self.variableList.append(command)
            self.variableNameList.append(command.name)

    # Methode, um den Namen ein Benutzerdefiniertes Event zu registrieren, das durch eine andere Instanz ausgewertet wird
    def rule_unique_eventNames(self, event):
        errorCode = ""
        names = list(map(lambda event: event.name, self.customEventList))
        if event.name in names:
            errorCode += f"The name of the 'Event': {event.name} is not unique."
        self.returnMessage += errorCode
        self.customEventList.append(event)


    # Das Gerät, von dem Daten empfangen werden sollen muss definiert sein
    def is_device_defined(self, name):
        errorCode = ""
        names = list(map(lambda device: device.name, self.deviceList))
        if name in names:
            return True
        else:
            return False


    def typecheck_parameter_devices(self, device):
        def typecheck_parameter_camera(device):
            errorCode = ""
            self.cameraList.append(device)
            self.connectableDeviceList.append(device)
            errorCode += rule_unique_positions(device)
            errorCode += rule_deviceEvent_defined(device)
            if not self.typecheck_expression(device.ipAddress, (str)):
                errorCode += f"The ipAddress of the 'Device': {device.name} needs to be a String."
            return errorCode

        def typecheck_parameter_Sensor(device):
            errorCode = ""
            self.connectableDeviceList.append(device)
            errorCode += rule_unique_positions(device)
            return errorCode

        def typecheck_parameter_Connection(device):
            errorCode = ""
            if not self.typecheck_expression(device.line, (str)):
                print(type(device.line), device)
                errorCode += f"The line of the 'Device': {device.name} needs to be a String."

            # Die von einer Connection verbundenen Geräte müssen definiert und verschieden sein.
            names = list(map(lambda existingDevice: existingDevice.name, self.connectableDeviceList))
            if device.firstDevice not in names:
                errorCode += f"Connection-firstDevice: {device.firstDevice} is not defined."
            if device.secondDevice not in names:
                errorCode += f"Connection-secondDevice: {device.secondDevice} is not defined."
            if device.firstDevice == device.secondDevice:
                errorCode += f"Connection, connected devices cant't be the same: {device.firstDevice}."

            return errorCode

        # Die Position von Geräten muss einzigartig sein
        def rule_unique_positions(device):
            errorCode = ""
            positions = []
            for existingDevice in self.deviceList:
                if not textx_isinstance(device, self.DSL_meta["Connection"]):
                    positions.append(existingDevice.position)
            if device.position in positions:
                errorCode += f"The postion: {device.position} of the 'Device': {device.name} is not unique."
            return errorCode

        # Der Name von Geräten muss einzigartig sein
        def rule_unique_deviceNames(device):
            errorCode = ""
            names = []
            for existingDevice in self.deviceList:
                names.append(existingDevice.name)
            if device.name in names:
                errorCode += f"The name of the 'Device': {device.name} is not unique."
            return errorCode

        # Das von Geräten genutzte Event muss definiert sein
        def rule_deviceEvent_defined(device):
            errorCode = ""
            names = list(map(lambda event: event.name, self.customEventList))
            names.append("None")
            if not device.eventName in names:
               errorCode += f"The referenced 'Event': {device.eventName} is not defined."
            return errorCode

        errorCode = ""
        errorCode += rule_unique_deviceNames(device)

        if textx_isinstance(device, self.DSL_meta["Camera"]):
            errorCode += typecheck_parameter_camera(device)
        elif textx_isinstance(device, self.DSL_meta["Sensor"]):
            errorCode += typecheck_parameter_Sensor(device)
        elif textx_isinstance(device, self.DSL_meta["Connection"]):
            errorCode += typecheck_parameter_Connection(device)

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

        errorCode = ""

        # Check für spezifisches Event
        if textx_isinstance(event, self.DSL_meta["EventWait"]):
            errorCode += typecheck_parameter_eventWait(event)
        elif textx_isinstance(event, self.DSL_meta["EventPhotos"]):
            errorCode += typecheck_parameter_eventPhotos(event)
        elif textx_isinstance(event, self.DSL_meta["EventVideo"]):
            errorCode += typecheck_parameter_eventVideo(event)
        elif textx_isinstance(event, self.DSL_meta["EventSaveLocation"]):
            errorCode += typecheck_parameter_eventSaveLocation(event)
        elif textx_isinstance(event, self.DSL_meta["EventTimerTrigger"]):
            errorCode += typecheck_parameter_eventTimerTrigger(event)
        elif textx_isinstance(event, self.DSL_meta["EventSignalTrigger"]):
            errorCode += typecheck_parameter_eventSignalTrigger(event)
        elif textx_isinstance(event, self.DSL_meta["EventSendSignal"]):
            errorCode += typecheck_parameter_eventSendSignal(event)
        elif textx_isinstance(event, self.DSL_meta["EventSendData"]):
            errorCode += typecheck_parameter_eventSendData(event)
        elif textx_isinstance(event, self.DSL_meta["EventReceiveData"]):
            errorCode += typecheck_parameter_eventReceiveData(event)
        elif textx_isinstance(event, self.DSL_meta["EventConfiguration"]):
            errorCode += typecheck_parameter_eventConfiguration(event)
        elif textx_isinstance(event, self.DSL_meta["EventAutomatedSignal"]):
            errorCode += typecheck_parameter_eventAutomatedSignal(event)

        return errorCode


    def typecheck_parameter_functions(self, function):
        def typecheck_parameter_sendData(function):
            errorCode = ""
            if not self.is_device_defined(function.receiverDevice):
                errorCode += f"The receiverDevice: {function.receiverDevice} in the function 'SendData' is not defined."
            return errorCode

        def typecheck_parameter_receiveData(function):
            errorCode = ""
            if not self.is_device_defined(function.transmitterDevice):
                errorCode += f"The transmitterDevice: {function.transmitterDevice} in the function 'ReceiveData' is not defined."
            return errorCode

        def typecheck_parameter_sendTCP(function):
            errorCode = ""
            if not self.typecheck_expression(function.ipAddress, (str)):
                errorCode += f"The ipAddress of the function 'SendTCP' needs to be a String."
            if not self.typecheck_expression(function.port, (int)):
                errorCode += f"The port of the function 'SendTCP' needs to be a Integer."
            return errorCode

        def typecheck_parameter_receiveTCP(function):
            errorCode = ""
            if not self.typecheck_expression(function.ipAddress, (str)):
                errorCode += f"The ipAddress of the function 'ReceiveTCP' needs to be a String."
            if not self.typecheck_expression(function.port, (int)):
                errorCode += f"The port of the function 'ReceiveTCP' needs to be a Integer."
            return errorCode

        def typecheck_parameter_writeFile(function):
            errorCode = ""
            if not self.typecheck_expression(function.filename, (str)):
                errorCode += f"The filename of the function 'WriteFile' needs to be a String."
            return errorCode

        def typecheck_parameter_readFile(function):
            errorCode = ""
            if not self.typecheck_expression(function.filename, (str)):
                errorCode += f"The filename of the function 'ReadFile' needs to be a String."
            return errorCode

        def typecheck_parameter_trigger(function):
            errorCode = ""
            if not self.is_device_defined(function.device):
                errorCode += f"The device of the function 'Trigger' needs to be defined."
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
        if textx_isinstance(expression, self.DSL_meta["ArithmeticOperation"]):
            for operand in expression.operand:
                if not textx_isinstance(operand, self.DSL_meta["Symbol"]) and not self.typecheck_expression(operand, demandedTypes):
                    print("hierr", expression.operand[0].operand)
                    return False
            return True
        elif textx_isinstance(expression, self.DSL_meta["Functions"]):
            print("Function need implementation")
            return True
        elif textx_isinstance(expression, self.DSL_meta["Operand"]):
            if isinstance(expression.operand, demandedTypes):
                return True
            elif expression.operand in self.variableNameList:
                return True
            elif isinstance(True, demandedTypes) and expression.operand in ["True", "False"]:
                return True
        # Fall Parameter expliziter String ist, wird dieser noch nicht als Operand gewertet 
        elif isinstance(expression, demandedTypes):
            return True
        else:
            return False
