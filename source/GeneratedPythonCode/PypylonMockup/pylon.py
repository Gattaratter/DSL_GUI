class TlFactory():

    __instance = None

    @staticmethod
    def GetInstance():
        if TlFactory.__instance == None:
            TlFactory()
        return TlFactory.__instance

    def __init__(self):
        if TlFactory.__instance != None:
            raise Exception("Singleton object already created!")
        else:
            TlFactory.__instance = self

    def EnumerateDevices(self):
        devices = []

        testDevice = Device()
        testDevice.deviceInfo.ipAddress = "192.168.0.0"
        devices.append(testDevice)

        testDevice = Device()
        testDevice.deviceInfo.ipAddress = "192.168.0.1"
        devices.append(testDevice)

        testDevice = Device()
        testDevice.deviceInfo.ipAddress = "0.0.0.0"
        devices.append(testDevice)

        return devices



class Device():
    def __init__(self):
        self.deviceInfo = DeviceInfo()
        self.open = False
        self.grabbing = False
        self.LineSelector = LineSelector()
        self.LineSource = LineSource()
        self.UserOutputSelector = UserOutputSelector()
        self.UserOutputValue = UserOutputValue()
        self.LineMode = LineMode()

    def GetDeviceInfo(self):
        return self.deviceInfo

    def Open(self):
        self.open = True

    def StartGrabbing(self):
        if self.open:
            self.grabbing = True

    def StopGrabbing(self):
        self.grabbing = False

    def GrabOne(self, timeout):
        self.grabbing = True
        #Take one picture
        self.grabbing = False

    def StartGrabbingMax(self, timeout, grabStrategy):
        if self.open:
            self.grabbing = True

    def IsGrabbing(self):
        return self.grabbing

    def RetrieveResult(self, timeout, exeption):
        result = GrabResult()
        return result


class DeviceInfo:
    def __init__(self):
        self.ipAddress = "0.0.0.0"

    def GetIpAddress(self):
        return self.ipAddress


class PylonImage():
    def __init__(self):
        pass

    def AttachGrabResultBuffer(self, result):
        pass

    def Save(self, format, filename, ipo):
        pass

    def Release(self):
        pass


class ImagePersistenceOptions():
    def __init__(self):
        pass

    def SetQuality(self, quality):
        pass


class PylonImageWindow():
    def __init__(self):
        self.visible = True

    def Create(self, parameter):
        pass

    def SetImage(self, grabResult):
        pass

    def Show(self):
        pass

    def IsVisible(self):
        return self.visible

    def Close(self):
        self.visible = False


class GrabResult():
    def __init__(self):
        self.status = True

    def GrabSucceeded(self):
        return self.status

    def Release(self):
        pass

class LineSelector():
    def __init__(self):
        self.Value = None

class LineSource():
    def __init__(self):
        self.Value = None

class UserOutputSelector():
    def __init__(self):
        self.Value = None

class UserOutputValue():
    def __init__(self):
        self.Value = None

class LineMode():
    def __init__(self):
        self.Value = None
