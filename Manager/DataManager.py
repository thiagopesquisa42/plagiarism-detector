from Process import _DataImportationProcess as DataImportationProcess

class DataManager(object):

    def Hello(self):
        print ('Hello, I\'m the DataManager')
        print ('And I manage these processes:')
        self._dataImportationProcess.Hello()

    def ImportPanDataBase(self):
        self._dataImportationProcess.ImportFromPanFiles(1,2)

    _dataImportationProcess = DataImportationProcess()

    def __init__(self):
        pass