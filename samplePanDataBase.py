from Util import _LoggerUtil as LoggerUtil
from constant  import PanDataBaseLocation
from Process import _DataImportationProcess as DataImportationProcess
_dataImportationProcess = DataImportationProcess()

_dataImportationProcess.DecreasePanDataBaseInNewFolder(
    decreasePercentage = 0.8,
    folderCompletePath = PanDataBaseLocation.fullSamples.FOLDER_PATH_2013_TRAIN_JANUARY)