#The following code was generated out of DSL-code from the file: ../DSLsourcePrograms/modell.cam
from DSLPythonPackage.DSLDevices import*
from DSLPythonPackage.DSLFunctions import*
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format='%(asctime)s - Func: %(funcName)30s - Line: %(lineno)4d - %(levelname)8s: %(message)s')

logger.info('Program wurde gestartet')
def PhotoCapture(device):
    duration = device.eventReceiveData()
    count = device.eventReceiveData()
    delay = device.eventReceiveData()
    device.eventWait(duration)
    device.eventPhotos(count, delay)
def EventKameraOben(device):
    device.eventSignalTrigger("Pin1", True, lambda: PhotoCapture(device=device))
    device.eventSendData("KameraOben hat die Bildaufnahme abgeschlossen")
def EventKameraUnten(device):
    device.eventSignalTrigger("Pin1", True, lambda: PhotoCapture(device=device))
    device.eventSendData("KameraUnten hat die Bildaufnahme abgeschlossen")

devicesList = []

#Erstellung der benoetigten Geraete

KameraOben = Camera("KameraOben", (1,4,0), "192.168.0.0", EventKameraOben)
devicesList.append(KameraOben)

KameraUnten = Camera("KameraUnten", (4,0,0), "192.168.0.1", EventKameraUnten)
devicesList.append(KameraUnten)

Lichtschranke = Sensor("Lichtschranke", (0,3,0))
devicesList.append(Lichtschranke)

Kabel_1 = Connection("Kabel_1", KameraOben, Lichtschranke, "wire", "Pin1")
devicesList.append(Kabel_1)

Kabel_2 = Connection("Kabel_2", KameraUnten, Lichtschranke, "wire", "Pin1")
devicesList.append(Kabel_2)

#Logik des ausfuehrenden PCs

geschwindigkeit = 10

distanz_1 = 100

distanz_2 = 300

sendData(KameraOben, distanz_1/geschwindigkeit)

sendData(KameraOben, 5)

sendData(KameraOben, 2)

sendData(KameraUnten, distanz_2/geschwindigkeit)

sendData(KameraUnten, 10)

sendData(KameraUnten, 1)
logger.info('Program wurde beendet')