from Util import _LoggerUtil as LoggerUtil
from Util import _ContextManager as ContextManager
from constant  import PanDataBaseLocation
from Process import _DataImportationProcess as DataImportationProcess

def SamplePanDataBase(): 
    _dataImportationProcess = DataImportationProcess(context = Contexts.TRAIN)
    _dataImportationProcess.DecreasePanDataBaseInNewFolder(
        decreasePercentage = 0.8,
        folderCompletePath = PanDataBaseLocation.fullSamples.FOLDER_PATH_2013_TRAIN_JANUARY)