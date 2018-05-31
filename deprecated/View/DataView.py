from Manager import _DataManager as DataManager

class DataView(object):

    def Hello(self):
        print ('Hello, I\'m the DataView')
        print ('And I shows the output of these managers:')
        self._dataManager.Hello()

    def Import(self):
        self._dataManager.ImportPanDataBase()

    _dataManager = DataManager()

    def __init__(self):
        pass
