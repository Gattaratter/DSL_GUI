#The following code was generated out of DSL-code from the file: ../DSLsourcePrograms/simpleCamProgram.cam
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
    device.eventPhotos("sdf", delay)

devicesList = []

#Erstellung der benoetigten Geraete

ip = "192.168.0.0"

KameraOben = Camera("KameraOben", (1,4,0), "<textx:camera_grammar.ArithmeticOperation instance at 0x2283e0fdc40>", PhotoCapture)
devicesList.append(KameraOben)

Lichtschranke = Sensor("Lichtschranke", (0,3,0))
devicesList.append(Lichtschranke)

Kabel_1 = Connection("Kabel_1", KameraOben, Lichtschranke, "wire", "Pin1")
devicesList.append(Kabel_1)

#Logik des ausfuehrenden PCs

geschwindigkeit = 10

distanz_1 = 100

sendData(KameraOben, distanz_1/geschwindigkeit)

sendData(KameraOben, 5)

sendData(KameraOben, 2)
logger.info('Program wurde beendet')