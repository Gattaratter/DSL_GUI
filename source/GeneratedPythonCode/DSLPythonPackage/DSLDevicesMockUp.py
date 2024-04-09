import time
import timeit
from threading import Thread, Event
import queue

from DSLPythonPackage import Trigger

'''These classes were used to test without the pypylon library'''

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
        self.event()

    def openCamera(self):
        print("openCamera")

    def eventPhoto(self):
        print("eventPhoto")

    def eventPhotos(self, count, delay):
        print("eventPhotos")

    def eventVideo(self, duration):
        print("eventVideo")


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
        print("SignalTrigger")

    def eventSendSignal(self, outputline, value):
        print("eventSendSignal")

    def eventSendData(self, data):
        self.messageQueueSend.put(data)

    def eventReceiveData(self):
        value = self.messageQueueSend.get()
        return value

    def eventConfiguration(self, attribute, value):
        print("setConfig", attribute, value)

    def eventAutomatedSignal(self, mode, outputLine, value):
        print("automatedSignal", mode, outputLine, value)
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
