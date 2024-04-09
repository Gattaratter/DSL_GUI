#The following code was generated out of DSL-code from the file: ../../savefiles/DSL/TestVerwendungsbeispiel.cam
import sys
sys.path.append('../../GeneratedPythonCode')
from DSLPythonPackage.DSLDevices import*
from DSLPythonPackage.DSLFunctions import*
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format='%(asctime)s - Func: %(funcName)30s - Line: %(lineno)4d - %(levelname)8s: %(message)s')

logger.info('Program wurde gestartet')
def KameraOben(device):
    device.eventWait(2)
    device.eventPhotos(2, 8)
def KameraUnten(device):
    device.eventWait(6)
    device.eventPhotos(1, 10)

devicesList = []

#The following lines define all the custom Events which were created

#The following lines define all the devices which were created

KameraOben = Camera("KameraOben", (361,207,0), "0.0.0.0", KameraOben)
devicesList.append(KameraOben)

KameraUnten = Camera("KameraUnten", (564,315,0), "0.0.0.0", KameraUnten)
devicesList.append(KameraUnten)

Lichtschranke = Sensor("Lichtschranke", (265,274,0))
devicesList.append(Lichtschranke)

VerbindungOben = Connection("VerbindungOben", Lichtschranke, KameraOben, "wire", "Pin1")
devicesList.append(VerbindungOben)

VerbindungUnten = Connection("VerbindungUnten", Lichtschranke, KameraUnten, "wire", "Pin1")
devicesList.append(VerbindungUnten)
logger.info('Program wurde beendet')