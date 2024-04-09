from PypylonMockup import pylon
#from pypylon import pylon

import timeit

'''This class manages activation of events'''
class Trigger:
    def __init__(self):
        pass

'''Trigger which react to a set timer'''
class TimerTrigger(Trigger):
    def __init__(self, duration, event):
        self.duration = duration
        self.event = event
        self.startTime = timeit.default_timer()
        self.nextTime = self.startTime + self.duration

    def evaluate(self):
        timeNow = timeit.default_timer()
        if timeNow > self.nextTime:
            self.nextTime = self.startTime + ((timeNow-self.startTime)//self.duration+1)*self.duration
            return True
        else:
            return False

'''Trigger which react to a signal'''
class SignalTrigger(Trigger):
    def __init__(self, inputLine, value, event, camera):
        self.inputLine = inputLine
        self.value = value
        self.event = event
        self.camera = camera

    def evaluate(self):
        currentValue = None
        try:
            self.camera.LineSelector.Value = self.inputLine
            self.camera.LineMode.Value = "Input"
            currentValue = self.camera.LineMode.Value
        except Exception as exception:
            print("error", exception)

        if currentValue == self.value:
            return True
        else:
            return False
