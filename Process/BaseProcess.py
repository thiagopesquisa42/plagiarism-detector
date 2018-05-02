import util
from constant import LoggerConstant
import logging

class BaseProcess(object):
    @staticmethod
    def SetLogger():
        if(isinstance(BaseProcess.logger, logging.Logger)):
            return
        logFormat = util.LoggerUtil.GetLoggerFormat()
        logger = logging.getLogger(name = LoggerConstant.Name.PROCESS)
        fileHandler = logging.FileHandler(filename = LoggerConstant.File.PROCESS)
        formatter = logging.Formatter(logFormat)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler) 
        logger.setLevel(logging.INFO)
                
        infoLogStruct = "\n ascTime levelName module funcName lineNumber \n message \n"
        logger.info("This log has the struct: " + infoLogStruct)
        BaseProcess.logger = logger
    
    logger = None

    def __init__(self):
        self.logger = BaseProcess.logger

BaseProcess.SetLogger()
