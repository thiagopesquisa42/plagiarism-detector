import logging

class BaseProcess(object):
    @staticmethod
    def setLogger():
        if(isinstance(BaseProcess.logger, logging.Logger)):
            return
        init = "\n"
        ascTime = "%(asctime)s ";
        levelName = "%(levelname)s ";
        #pathName = "%(pathname)s \n";
        module = "%(module)s ";
        functionName = "%(funcName)s ";
        lineNumber = "%(lineno)d \n";
        message = "%(message)s \n";

        logFormat = init + ascTime + levelName + module + functionName + lineNumber + message
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

BaseProcess.setLogger()
