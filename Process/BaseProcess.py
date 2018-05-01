import util
import logging

class BaseProcess(object):
    @staticmethod
    def SetLogger():
        if(isinstance(BaseProcess.logger, logging.Logger)):
            return
        logFormat = util.GetLoggerFormat()
        logger = logging.getLogger(name = 'process')
        fileHandler = logging.FileHandler('logging.process.log')
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
