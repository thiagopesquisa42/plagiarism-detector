from Util import _LoggerUtil as LoggerUtil
from Util import  _ContextManager as ContextManager
from constant import LoggerConstant, Contexts
import logging
import pickle
import os

class BaseRepository(object):
    logger = None

    @staticmethod
    def SetLogger():
        if(isinstance(BaseRepository.logger, logging.Logger)):
            return
        logFormat = LoggerUtil.GetLoggerFormat()
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
        return ContextManager.GetContextLocation(self.context)

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
            self.logger.exception('failure when storing item, error ' + str(exception))
            raise exception
        else:
            self.logger.info('item stored: ' + str(type(item)))
            return fileWriter.name
        
    def Get(self):
        try:
            fileReader = self.GetPickleFileReader()
            item = pickle.load(fileReader)
        except Exception as exception:
            self.logger.exception('failure when retrieving item, error ' + str(exception))
            raise exception
        else:
            self.logger.info('item retrieved: ' + str(type(item)))
            return item

    def StoreAndGet(self, item):
        self.Store(item)
        return self.Get()

    def __init__(self, context, name):
        self.context = context
        self.name = name
        self.logger = BaseRepository.logger
        self.CheckPath()

BaseRepository.SetLogger()