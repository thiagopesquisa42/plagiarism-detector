from constant import LoggerConstant
import settings
import util
import logging
import pickle
import os

class BaseRepository(object):
    name = 'BaseRepository'
    logger = None
    subFolder = settings.subFolderDefault

    @staticmethod
    def SetLogger():
        if(isinstance(BaseRepository.logger, logging.Logger)):
            return
        logFormat = util.LoggerUtil.GetLoggerFormat()
        logger = logging.getLogger(name = LoggerConstant.Name.REPOSITORY)
        fileHandler = logging.FileHandler(filename = LoggerConstant.File.REPOSITORY)
        formatter = logging.Formatter(logFormat)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler) 
        logger.setLevel(logging.INFO)
                
        infoLogStruct = "\n ascTime levelName module funcName lineNumber \n message \n"
        logger.info("This log has the struct: " + infoLogStruct)
        BaseRepository.logger = logger

    def GetPath(self):
        return os.path.join(self.rootLocation, self.subFolder)

    def CheckPath(self):
        path = self.GetPath()
        if(not os.path.exists(path)):
            os.makedirs(path)

    def GetPickleName(self):
        return os.path.join(self.GetPath(), self.name + '.pickle')

    def GetPickleFileReader(self):
        pickleName = self.GetPickleName()
        return open(pickleName, 'rb')

    def GetPickleFileWriter(self):
        pickleName = self.GetPickleName()
        return open(pickleName, 'wb')

    def Store(self, item):
        try:
            fileWriter = self.GetPickleFileWriter()
            pickle.dump(item, fileWriter)
        except Exception as exception:
            self.logger.info('failure when storing item, error ' + str(exception))
        else:
            self.logger.info('item stored: ' + str(type(item)))
            return fileWriter.name
        
    def Get(self):
        try:
            fileReader = self.GetPickleFileReader()
            item = pickle.load(fileReader)
        except Exception as exception:
            self.logger.info('failure when retrieving item, error ' + str(exception))
        else:
            self.logger.info('item retrieved: ' + str(type(item)))
            return item

    def StoreAndGet(self, item):
        self.Store(item)
        return self.Get()

    def __init__(self):
        self.logger = BaseRepository.logger
        self.rootLocation = settings.rootLocation
        self.CheckPath()

BaseRepository.SetLogger()