#The following code was generated out of DSL-code from the file: ../../savefiles/DSL/TestMinWait.cam
import sys
sys.path.append('../../GeneratedPythonCode')
from DSLPythonPackage.DSLDevices import*
from DSLPythonPackage.DSLFunctions import*
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format='%(asctime)s - Func: %(funcName)30s - Line: %(lineno)4d - %(levelname)8s: %(message)s')

logger.info('Program wurde gestartet')
def none(device):
    device.eventWait(0)

devicesList = []

#The following lines define all the custom Events which were created


#The following lines define all the devices which were created

logger.info('Program wurde beendet')