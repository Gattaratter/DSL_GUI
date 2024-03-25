from textx import metamodel_from_file, textx_isinstance
def main():
    DSL_meta = metamodel_from_file("camera_grammar.tx")
    DSLPath = "testModell.cam"
    DSLProgramm = DSL_meta.model_from_file(DSLPath)
    PythonPath = "../GeneratedPythonCode/generatedCode.py"

    with open(PythonPath, 'w') as savefile:
        savefile.write(f"#The following code was generated out of DSL-code from the file: {DSLPath}")
        savefile.write(lines_import())


        for command in DSLProgramm.commands:
            print("Main:", type(command))
            if textx_isinstance(command, DSL_meta["CustomEvent"]):
                savefile.write(lines_customEvent(command, DSL_meta))

        savefile.write(lines_setup())

        for command in DSLProgramm.commands:
            if textx_isinstance(command, DSL_meta["CustomEvent"]):
                continue
            savefile.write(lines_programCommand(command, DSL_meta))


def check_semantic(DSLProgramm, DSL_meta):
    # check parameter types
    pass



def lines_import():
    lines = ""
    lines += "\n#from DSLPythonPackage.DSLDevices import*"
    lines += "\nfrom DSLPythonPackage.DSLDevicesMockUp import*"
    lines += "\nfrom DSLPythonPackage.DSLFunctions import*"
    lines += "\n"
    return lines

def lines_setup():
    lines = ""
    lines += "\n\ndevicesList = []"
    return lines

def lines_programCommand(command, DSL_meta, indent = ""):
    lines = "\n\n"
    if textx_isinstance(command, DSL_meta["Variable"]):
        lines += indent + lines_variable(command, DSL_meta)
    elif textx_isinstance(command, DSL_meta["Commentline"]):
        lines += indent + '#' + str(command.text)
    elif textx_isinstance(command, DSL_meta["ControlStructure"]):
        lines += indent + lines_controlStructure(command, DSL_meta, indent)
    elif textx_isinstance(command, DSL_meta["Device"]):
        lines += indent + lines_device(command, DSL_meta)
    elif textx_isinstance(command, DSL_meta["Functions"]):
        lines += indent + lines_function(command, DSL_meta)
    return lines

def lines_eventCommand(command, DSL_meta, indent):
    lines = ""
    if textx_isinstance(command, DSL_meta["Variable"]):
        lines += indent +lines_variable(command, DSL_meta)
    if textx_isinstance(command, DSL_meta["Commentline"]):
        lines += indent +'#' + str(command.text)
    if textx_isinstance(command, DSL_meta["ControlStructure"]):
        lines += indent +lines_controlStructure(command, DSL_meta, indent)
    if textx_isinstance(command, DSL_meta["Device"]):
        lines += indent +lines_device(command, DSL_meta)
    if textx_isinstance(command, DSL_meta["Functions"]):
        lines += indent +lines_function(command, DSL_meta)
    if textx_isinstance(command, DSL_meta["BasicEvent"]):
        lines += indent +lines_basicEvent(command, DSL_meta)
    return lines

def lines_variable(variable, DSL_meta):
    lines = f"{variable.name} = "
    lines += lines_expression(variable.value, DSL_meta)
    return lines

def lines_expression(operand, DSL_meta):
    lines = ""
    if isinstance(operand, str):
        lines += "\""+operand+ "\""
    elif isinstance(operand, bool):
        lines += str(operand)
    elif textx_isinstance(operand, DSL_meta["Functions"]):
        lines += lines_function(operand, DSL_meta)

    elif textx_isinstance(operand, DSL_meta["ArithmeticOperation"]):
        for operand in operand.operand:
            if isinstance(operand, str):
                lines += str(operand)
            elif textx_isinstance(operand.operand, DSL_meta["ArithmeticOperation"]):
                lines += '(' + lines_expression(operand.operand, DSL_meta) + ')'
            else:
                lines += str(operand.operand)
    return lines


def lines_controlStructure(structure, DSL_meta, indent = ""):
    indent += "    "
    lines = ""
    expression = ""
    if textx_isinstance(structure.expression, DSL_meta["ArithmeticOperation"]):
        expression += lines_expression(structure.expression, DSL_meta)
    elif textx_isinstance(structure.expression, DSL_meta["Functions"]):
        expression += lines_function(structure.expression, DSL_meta)
    else:
        expression += str(structure.expression)

    if textx_isinstance(structure, DSL_meta["Condition"]):
        lines += f"if {expression}:"
        for command in structure.commands:
            lines += f"\n{lines_eventCommand(command, DSL_meta, indent)}"

    elif textx_isinstance(structure, DSL_meta["WhileLoop"]):
        lines += f"while {expression}:"
        for command in structure.commands:
            lines += f"\n{lines_eventCommand(command, DSL_meta, indent)}"

    return lines


def lines_device(device, DSL_meta):
    lines = ""
    newDevice = ""
    if textx_isinstance(device, DSL_meta["Camera"]):
        newDevice = f"Camera(\"{device.name}\", {device.position}, \"{device.ipAddress}\", {device.eventName})"
    elif textx_isinstance(device, DSL_meta["Sensor"]):
        newDevice = f"Sensor(\"{device.name}\", {device.position})"
    elif textx_isinstance(device, DSL_meta["Connection"]):
        newDevice = f"Connection(\"{device.name}\", {device.firstDevice}, {device.secondDevice}, \"{device.type}\", \"{device.line}\")"
    lines += f"{device.name} = {newDevice}"
    lines += f"\ndevicesList.append({device.name})"

    return lines

def lines_function(function, DSL_meta):
    lines = ""
    if textx_isinstance(function, DSL_meta["SendData"]):
        lines += f"sendData({function.receiverDevice}, {lines_expression(function.data, DSL_meta)})"
    if textx_isinstance(function, DSL_meta["ReceiveData"]):
        lines += f"receiveData({function.transmitterDevice})"
    if textx_isinstance(function, DSL_meta["SendTCP"]):
        lines += f"sendTCP(\"{function.ipAddress}\", {function.port}, \"{function.role}\", {lines_expression(function.data, DSL_meta)})"
    if textx_isinstance(function, DSL_meta["ReceiveTCP"]):
        lines += f"receiveTCP(\"{function.ipAddress}\", {function.port}, \"{function.role}\")"
    if textx_isinstance(function, DSL_meta["WriteFile"]):
        lines += f"writeFile(\"{function.filename}\", {lines_expression(function.data, DSL_meta)})"
    if textx_isinstance(function, DSL_meta["ReadFile"]):
        lines += f"readFile(\"{function.filename}\")"
    return lines


def lines_customEvent(event, DSL_meta, indent = ""):
    indent += "    "
    lines = "\n"
    lines += f"def {event.name}(device):"
    for command in event.commandList:
        lines += f"\n{lines_eventCommand(command, DSL_meta, indent)}"
    return lines


def lines_basicEvent(event, DSL_meta):
    lines = ""
    if textx_isinstance(event, DSL_meta["EventWait"]):
        lines += f"device.eventWait({lines_expression(event.duration, DSL_meta)})"
    elif textx_isinstance(event, DSL_meta["EventPhoto"]):
        lines += f"device.eventPhoto()"
    elif textx_isinstance(event, DSL_meta["EventPhotos"]):
        lines += f"device.eventPhotos({lines_expression(event.count, DSL_meta)}, {lines_expression(event.delay, DSL_meta)})"
    elif textx_isinstance(event, DSL_meta["EventVideo"]):
        lines += f"device.eventVideo({lines_expression(event.duration, DSL_meta)})"
    elif textx_isinstance(event, DSL_meta["EventSaveLocation"]):
        lines += f"device.eventSaveLocation({lines_expression(event.filepath, DSL_meta)})"
    elif textx_isinstance(event, DSL_meta["EventTimerTrigger"]):
        lines += f"device.eventTimerTrigger({lines_expression(event.duration, DSL_meta)}, {event.event})"
    elif textx_isinstance(event, DSL_meta["EventSignalTrigger"]):
        lines += f"device.eventSignalTrigger({lines_expression(event.inputLine, DSL_meta)}, {lines_expression(event.value, DSL_meta)}, lambda: {event.event}(device=device))"
    elif textx_isinstance(event, DSL_meta["EventSendSignal"]):
        lines += f"device.eventSendSignal({lines_expression(event.outputLine, DSL_meta)}, {lines_expression(event.value, DSL_meta)})"
    elif textx_isinstance(event, DSL_meta["EventSendData"]):
        lines += f"device.eventSendData({lines_expression(event.data, DSL_meta)})"

    return lines


def lines_from(object, DSL_meta):
    lines = ""
    return lines








if __name__=="__main__":
    main()