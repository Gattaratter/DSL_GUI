#The following code was generated out of DSL-code from the file: testModell.cam
#from DSLPythonPackage.DSLDevices import*
from DSLPythonPackage.DSLDevicesMockUp import*
from DSLPythonPackage.DSLFunctions import*

def WaitToPhotos(device):
    a_8 = 5
    while a_8-3:
        a_8 = a_8-1
    device.eventTimerTrigger(4, lambda: print(a_8))
    device.eventWait(a_8)
    device.eventPhotos(5, 9)
def Custumonus(device):
    test0 = 34
    if test0:
        test0 = 1

    duration = receiveData()
    count = receiveData()
    delay = receiveData()
    device.eventWait(duration)
    device.eventPhoto()
    device.eventPhotos(count, delay)
    device.eventVideo(duration)
    device.eventSaveLocation("hierspeichern")
    device.eventTimerTrigger(5, WaitToPhotos)
    device.eventSignalTrigger("pin3", True, lambda: WaitToPhotos(device=device))
    device.eventSendSignal("pin3", True)

devicesList = []

#Variable and Controlstructure tests


test0 = 7

if test0:
    test0 = 1

while test0:
    test0 = 0

test = 33+5*(3-4+test0)

test1 = "hallo1"

#Event tests


#Device tests


KameraOben = Camera("KameraOben", (1,4,0), "192.168.0.0", WaitToPhotos)
devicesList.append(KameraOben)

KameraUnten = Camera("KameraUnten", (4,0,0), "192.168.0.1", WaitToPhotos)
devicesList.append(KameraUnten)

Lichtschranke = Sensor("Lichtschranke", (0,3,0))
devicesList.append(Lichtschranke)

Kabel_1 = Connection("Kabel_1", KameraOben, Lichtschranke, "wire", "Pin1")
devicesList.append(Kabel_1)

#Function tests


sendData(KameraOben, 2)

receiveData(KameraOben)

sendTCP("192.168.0.1", 8080, "client", 5)

receiveTCP("192.168.0.1", 8080, "client")

writeFile("savefile", "HelloUniverse")

writeFile("savefile", True)

readFile("savefile")