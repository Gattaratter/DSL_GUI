from PypylonMockup import pylon
#from pypylon import pylon

import time
import timeit
from threading import Thread, Event
import queue

from DSLPythonPackage import Trigger

'''These classes implement the devices and all functions of the Basic-Events'''
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
        if event:
            self.event = lambda: event(device = self)
        else:
            self.event = None
        self.camera = None
        self.savelocation = "."
        self.thread = None
        self.messageQueueReceive = queue.Queue()
        self.messageQueueSend = queue.Queue()
        self.eventStop = Event()
        self.eventStop.clear()
        self.signalMode = None

        self.start_thread()

    def start_thread(self):
        self.thread = Thread(target=self.threadFunction, args = ())
        self.thread.start()

    def threadFunction(self):
        self.openCamera()
        if self.event:
            self.event()

    def openCamera(self):
        selfcamera = None
        tlFactory = pylon.TlFactory.GetInstance()
        devices = tlFactory.EnumerateDevices()

        for cam in devices:
            if cam.GetDeviceInfo().GetIpAddress() == self.ipAddress:
                self.camera = cam
                self.camera.Open()
                return

    def eventPhoto(self):
        img = pylon.PylonImage()
        self.camera.StartGrabbing()
        result = self.camera.GrabOne(1000)
        img.AttachGrabResultBuffer(result)
        ipo = pylon.ImagePersistenceOptions()
        quality = 100
        ipo.SetQuality(quality)

        filename = f"{self.savelocation}.jpeg"
        img.Save("JPEG", filename, ipo)

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
            self.camera.StartGrabbingMax(10000, "pylon.GrabStrategy_LatestImageOnly")
            while self.camera.IsGrabbing():
                endTime = time.time()
                # check if requested Video length is reached
                if endTime - startTime > duration:
                    break
                grabResult = self.camera.RetrieveResult(5000, "pylon.TimeoutHandling_ThrowException")
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

        except Exception as e:
            print("An exception occurred.", e)


    def eventSavelocation(self, filepath):
        self.savelocation = filepath

    def eventTimerTrigger(self, timer, event):
        trigger = Trigger.TimerTrigger(timer, event)
        while not self.eventStop.is_set():
            if trigger.evaluate():
                    print("triggerd Timer")
                    if trigger.event():
                        return
            time.sleep(0.1)

    def eventSignalTrigger(self, inputline, value, event):
        trigger = Trigger.SignalTrigger(inputline, value, event, self.camera)
        while not self.eventStop.is_set():
            if trigger.evaluate():
                    print("triggerd Signal")
                    if trigger.event():
                        return
            time.sleep(0.1)


    def eventSendSignal(self, outputline, value):
        self.camera.LineSelector.Value = outputline
        self.camera.LineSource.Value = "UserOutput1"
        self.camera.UserOutputSelector.Value = "UserOutput1"
        self.camera.UserOutputValue.Value = value

    def eventSendData(self, data):
        self.messageQueueSend.put(data)

    def eventReceiveData(self):
        value = self.messageQueueReceive.get()
        return value

    def eventConfiguration(self, attribute, value):
        try:
            match attribute:
                case "width":
                    self.camera.Width.Value = value
                case "height":
                    self.camera.Height.Value = value
                case "offsetX":
                    self.camera.OffsetX.Value = value
                case "offsetY":
                    self.camera.OffsetY.Value = value
                case "exposuretime":
                    self.camera.ExposuretimeAbs.Value = value
                case "pixelformat":
                    self.camera.Pixelformat.Value = value
                case "position":
                    self.position = value
        except Exception as exception:
            print("Error", exception)

    def eventAutomatedSignal(self, mode, outputLine, value):
        self.signalMode = {"mode": mode,
                           "outputLine": outputLine,
                           "value": value}

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
