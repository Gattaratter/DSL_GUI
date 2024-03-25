from pypylon import pylon
from pypylon import genicam
import time
import timeit
from threading import Thread, Event
import queue

from DSLPythonPackage import Trigger

class Device:
    def __init__(self):
        pass

    def eventWait(self, duration):
        time.sleep(duration)

    def eventTimerTrigger(self, duration):
        pass


class Camera(Device):
    def __init__(self, name, position, ipAddress, event):
        self.name = name
        self.position = position
        self.ipAddress = ipAddress
        self.event = lambda : event(device = self)
        self.camera = None
        self.savelocation = "."
        self.thread = None
        self.messageQueueReceive = queue.Queue
        self.messageQueueSend = queue.Queue
        self.eventStop = Event()
        self.eventStop.clear()

        self.start_thread()

    def start_thread(self):
        self.thread = Thread(target=self.threadFunction, args = ())
        self.thread.start()

    def threadFunction(self):
        self.openCamera()
        self.event()

    def openCamera(self):
        selfcamera = None
        tlFactory = pylon.TlFactory.GetInstance()
        devices = tlFactory.EnumerateDevices()
        for cam in devices:
            if cam.GetDeviceInfo().GetIpAddress == self.ipAddress:
                selfcamera = cam
                selfcamera.Open()
                return

    def eventPhoto(self):
        img = pylon.PylonImage()
        self.camera.StartGrabbing()
        result = self.camera.GrabOne(1000)
        img.AttachGrabResultBuffer(result)
        ipo = pylon.ImagePersistenceOptions()
        quality = 100
        ipo.SetQuality(quality)

        filename = f"{self.savelocation}.jpeg" % quality
        img.Save(pylon.ImageFileFormat_Jpeg, filename, ipo)

        img.Release()
        self.camera.StopGrabbing()

    def eventPhotos(self, count, delay):
        savelocation = self.savelocation
        for index in range(count):
            timeStart = timeit.default_timer()
            self.savelocation = savelocation+f"_{index}"
            self.eventPhoto()
            timeEnd = timeit.default_timer()
            time.sleep(delay - (timeEnd-timeStart))

    def eventVideo(self, duration):
        try:
            startTime = time.time()
            imageWindow = pylon.PylonImageWindow()
            imageWindow.Create(1)
            self.camera.StartGrabbingMax(10000, pylon.GrabStrategy_LatestImageOnly)
            while self.camera.IsGrabbing():
                endTime = time.time()
                # check if requested Video length is reached
                if endTime - startTime > duration:
                    break
                grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                if grabResult.GrabSucceeded():
                    imageWindow.SetImage(grabResult)
                    imageWindow.Show()
                else:
                    print("Error: ", grabResult.ErrorCode)
                grabResult.Release()
                time.sleep(0.05)
                if not imageWindow.IsVisible():
                    self.camera.StopGrabbing()
            imageWindow.Close()

        except genicam.GenericException as e:
            print("An exception occurred.", e)


    def eventSavelocation(self, filepath):
        self.savelocation = filepath

    def eventTimerTrigger(self, timer, event):
        trigger = Trigger.TimerTrigger(timer, event)
        while not self.eventStop.is_set():
            if trigger.evaluate():
                    print("triggerd Timer")
                    trigger.event()
            time.sleep(0.1)

    def eventSignalTrigger(self, inputline, value, event):
        trigger = Trigger.SignalTrigger(inputline, value, event, self.camera)
        while not self.eventStop.is_set():
            if trigger.evaluate():
                    print("triggerd Signal")
                    trigger.event()
            time.sleep(0.1)


    def eventSendSignal(self, outputline, value):
        self.camera.LineSelector.Value = outputline
        self.camera.LineSource.Value = "UserOutput1"
        self.camera.UserOutputSelector.Value = "UserOutput1"
        self.camera.UserOutputValue.Value = value

    def eventSendData(self, data):
        self.messageQueueSend.put(data)

    def eventReceiveData(self):
        value = self.messageQueueSend.get()
        return value


class Sensor:
    def __init__(self, name, position):
        self.name = name
        self.position = position


class Connection:
    def __init__(self, name, firstDevice, secondDevice, type, pin):
        self.name = name
        self.firstDevice = firstDevice
        self.secondDevice = secondDevice
        self.type = type
        self.pin = pin
