from Util import _LoggerUtil as LoggerUtil
from Util import  _ContextManager as ContextManager
from constant import LoggerConstant, Contexts
import logging
import pickle
from datetime import datetime
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
            fileWriter.close()
            storedLength = BaseRepository.HumanizeBytes(bytes = os.path.getsize(fileWriter.name))
            self.logger.info('item stored: ' + str(type(item)) +\
            ' ' + storedLength + ' ' + fileWriter.name)
            return fileWriter.name
        
    def Get(self):
        try:
            fileReader = self.GetPickleFileReader()
            item = pickle.load(fileReader)
        except Exception as exception:
            self.logger.exception('failure when retrieving item, error ' + str(exception))
            raise exception
        else:
            readLength = BaseRepository.HumanizeBytes(bytes = os.path.getsize(fileReader.name))
            self.logger.info(
                'item retrieved: ' + str(type(item)) +\
                ' ' + readLength + ' ' + fileReader.name)
            return item

    def StoreAndGet(self, item):
        self.Store(item)
        return self.Get()

    def HumanizeBytes(bytes, precision=1):
        abbreviations = [
            (1 << 50, 'PB'),
            (1 << 40, 'TB'),
            (1 << 30, 'GB'),
            (1 << 20, 'MB'),
            (1 << 10, 'kB'),
            (2, 'bytes'),
            (1, 'byte')
        ]
        for factor, suffix in abbreviations:
            if bytes >= factor:
                break
        else:
            factor = 1
            suffix = 'byte'
        stringFormatter = '{:0.0'+str(precision)+'f}'
        bytesShift = bytes / factor
        return stringFormatter.format(bytesShift) + ' ' + suffix
    
    def GetUniqueFolderPath(self, nickname = None):
        if(nickname is None):
            nickname = ''
        dateTimeString = datetime.now().strftime('%Y%m%d_%H%M%S')
        folderPath = os.path.join(self.GetPath(), self.name + dateTimeString + nickname)
        os.makedirs(folderPath, exist_ok=True)
        return folderPath

    def __init__(self, context, name):
        self.context = context
        self.name = name
        self.logger = BaseRepository.logger
        self.CheckPath()

BaseRepository.SetLogger()