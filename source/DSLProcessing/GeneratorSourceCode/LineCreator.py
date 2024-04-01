from textx import metamodel_from_file, textx_isinstance

class LineCreator():
    def __init__(self, DSL_meta):
        self.DSL_meta = DSL_meta

    def lines_import(self):
        lines = ""
        lines += "\nfrom DSLPythonPackage.DSLDevices import*"
        lines += "\nfrom DSLPythonPackage.DSLFunctions import*"
        lines += "\nimport logging"
        lines += "\nlogger = logging.getLogger(__name__)"
        lines += "\nlogging.basicConfig(filename='logfile.log', level=logging.DEBUG, format='%(asctime)s - Func: %(funcName)30s - Line: %(lineno)4d - %(levelname)8s: %(message)s')"
        lines += "\n"
        return lines

    def lines_setup(self):
        lines = ""
        lines += "\n\ndevicesList = []"
        return lines

    def lines_programCommand(self, command, indent=""):
        lines = "\n\n"
        if textx_isinstance(command, self.DSL_meta["Variable"]):
            lines += indent + self.lines_variable(command)
        elif textx_isinstance(command, self.DSL_meta["Commentline"]):
            lines += indent + '#' + str(command.text)
        elif textx_isinstance(command, self.DSL_meta["ControlStructure"]):
            lines += indent + self.lines_controlStructure(command, indent)
        elif textx_isinstance(command, self.DSL_meta["Device"]):
            lines += indent + self.lines_device(command)
        elif textx_isinstance(command, self.DSL_meta["Functions"]):
            lines += indent + self.lines_function(command)
        return lines

    def lines_eventCommand(self, command, indent):
        lines = ""
        if textx_isinstance(command, self.DSL_meta["Variable"]):
            lines += indent + self.lines_variable(command)
        if textx_isinstance(command, self.DSL_meta["Commentline"]):
            lines += indent + '#' + str(command.text)
        if textx_isinstance(command, self.DSL_meta["ControlStructure"]):
            lines += indent + self.lines_controlStructure(command, indent)
        if textx_isinstance(command, self.DSL_meta["Device"]):
            lines += indent + self.lines_device(command)
        if textx_isinstance(command, self.DSL_meta["Functions"]):
            lines += indent + self.lines_function(command)
        if textx_isinstance(command, self.DSL_meta["BasicEvent"]):
            lines += indent + self.lines_basicEvent(command)
        return lines


    def lines_variable(self, variable):
        lines = f"{variable.name} = "
        lines += self.lines_expression(variable.value)
        return lines


    def lines_expression(self, operand):
        lines = ""
        if isinstance(operand, str):
            lines += "\"" + operand + "\""
        elif isinstance(operand, bool):
            lines += str(operand)
        elif textx_isinstance(operand, self.DSL_meta["Functions"]):
            lines += self.lines_function(operand)

        elif textx_isinstance(operand, self.DSL_meta["ArithmeticOperation"]):
            for operand in operand.operand:
                if isinstance(operand, str):
                    lines += str(operand)
                elif textx_isinstance(operand.operand, self.DSL_meta["ArithmeticOperation"]):
                    lines += '(' + self.lines_expression(operand.operand) + ')'
                else:
                    lines += str(operand.operand)
        return lines


    def lines_controlStructure(self, structure, indent=""):
        indent += "    "
        lines = ""
        expression = ""
        if textx_isinstance(structure.expression, self.DSL_meta["ArithmeticOperation"]):
            expression += self.lines_expression(structure.expression)
        elif textx_isinstance(structure.expression, self.DSL_meta["Functions"]):
            expression += self.lines_function(structure.expression)
        else:
            expression += str(structure.expression)

        if textx_isinstance(structure, self.DSL_meta["Condition"]):
            lines += f"if {expression}:"
            for command in structure.commands:
                lines += f"\n{self.lines_eventCommand(command, indent)}"

        elif textx_isinstance(structure, self.DSL_meta["WhileLoop"]):
            lines += f"while {expression}:"
            for command in structure.commands:
                lines += f"\n{self.lines_eventCommand(command, indent)}"

        elif textx_isinstance(structure, self.DSL_meta["Break"]):
            lines += f"break"

        return lines


    def lines_device(self, device):
        lines = ""
        newDevice = ""
        if textx_isinstance(device, self.DSL_meta["Camera"]):
            newDevice = f"Camera(\"{device.name}\", {device.position}, \"{device.ipAddress}\", {device.eventName})"
        elif textx_isinstance(device, self.DSL_meta["Sensor"]):
            newDevice = f"Sensor(\"{device.name}\", {device.position})"
        elif textx_isinstance(device, self.DSL_meta["Connection"]):
            newDevice = f"Connection(\"{device.name}\", {device.firstDevice}, {device.secondDevice}, \"{device.type}\", \"{device.line}\")"
        lines += f"{device.name} = {newDevice}"
        lines += f"\ndevicesList.append({device.name})"
        return lines


    def lines_function(self, function):
        lines = ""
        if textx_isinstance(function, self.DSL_meta["SendData"]):
            lines += f"sendData({function.receiverDevice}, {self.lines_expression(function.data)})"
        if textx_isinstance(function, self.DSL_meta["ReceiveData"]):
            lines += f"receiveData({function.transmitterDevice})"
        if textx_isinstance(function, self.DSL_meta["SendTCP"]):
            lines += f"sendTCP(\"{function.ipAddress}\", {function.port}, \"{function.role}\", {self.lines_expression(function.data)})"
        if textx_isinstance(function, self.DSL_meta["ReceiveTCP"]):
            lines += f"receiveTCP(\"{function.ipAddress}\", {function.port}, \"{function.role}\")"
        if textx_isinstance(function, self.DSL_meta["WriteFile"]):
            lines += f"writeFile(\"{function.filename}\", {self.lines_expression(function.data)})"
        if textx_isinstance(function, self.DSL_meta["ReadFile"]):
            lines += f"readFile(\"{function.filename}\")"
        return lines


    def lines_customEvent(self, event, indent=""):
        indent += "    "
        lines = "\n"
        lines += f"def {event.name}(device):"
        for command in event.commandList:
            lines += f"\n{self.lines_eventCommand(command, indent)}"
        return lines


    def lines_basicEvent(self, event):
        lines = ""
        if textx_isinstance(event, self.DSL_meta["EventWait"]):
            lines += f"device.eventWait({self.lines_expression(event.duration)})"
        elif textx_isinstance(event, self.DSL_meta["EventPhoto"]):
            lines += f"device.eventPhoto()"
        elif textx_isinstance(event, self.DSL_meta["EventPhotos"]):
            lines += f"device.eventPhotos({self.lines_expression(event.count)}, {self.lines_expression(event.delay)})"
        elif textx_isinstance(event, self.DSL_meta["EventVideo"]):
            lines += f"device.eventVideo({self.lines_expression(event.duration)})"
        elif textx_isinstance(event, self.DSL_meta["EventSaveLocation"]):
            lines += f"device.eventSaveLocation({self.lines_expression(event.filepath)})"
        elif textx_isinstance(event, self.DSL_meta["EventTimerTrigger"]):
            lines += f"device.eventTimerTrigger({self.lines_expression(event.duration)}, {event.event})"
        elif textx_isinstance(event, self.DSL_meta["EventSignalTrigger"]):
            lines += f"device.eventSignalTrigger({self.lines_expression(event.inputLine)}, {self.lines_expression(event.value)}, lambda: {event.event}(device=device))"
        elif textx_isinstance(event, self.DSL_meta["EventSendSignal"]):
            lines += f"device.eventSendSignal({self.lines_expression(event.outputLine)}, {self.lines_expression(event.value)})"
        elif textx_isinstance(event, self.DSL_meta["EventSendData"]):
            lines += f"device.eventSendData({self.lines_expression(event.data)})"
        elif textx_isinstance(event, self.DSL_meta["EventReceiveData"]):
            lines += f"{event.variable} = device.eventReceiveData()"
        elif textx_isinstance(event, self.DSL_meta["EventConfiguration"]):
            lines += f"device.eventConfiguration({event.attribute}, {self.lines_expression(event.value)})"
        elif textx_isinstance(event, self.DSL_meta["EventAutomatedSignal"]):
            lines += f"eventAutomatedSignal({event.mode}, {self.lines_expression(event.outputLine)}, {self.lines_expression(event.value)})"
        return lines