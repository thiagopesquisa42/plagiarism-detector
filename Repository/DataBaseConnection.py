import Repository.DataBaseConfiguration as DataBaseConfiguration
from constant import LoggerConstant
# Import create_engine function
from sqlalchemy import create_engine
# the Session class 
from sqlalchemy.orm import sessionmaker
import logging

class DataBaseConnection(object):
    session = None
    
    def setLogger(self):
        init = "\n"
        ascTime = "%(asctime)s ";
        levelName = "%(levelname)s ";
        pathName = "%(pathname)s \n";
        module = "%(module)s ";
        functionName = "%(funcName)s ";
        lineNumber = "%(lineno)d \n";
        message = "%(message)s \n";

        logFormat = init + ascTime + levelName + pathName + module + functionName + lineNumber + message
        logging.basicConfig(filename = LoggerConstant.File.REPOSITORY_SQLALCHEMY, format = logFormat)
        logger = logging.getLogger(name = LoggerConstant.Name.REPOSITORY_SQLALCHEMY)
        logger.setLevel(logging.INFO)
                
        infoLogStruct = "\n ascTime levelName pathName \n module funcName lineNumber \n message \n"
        logger.info("This log has the struct: " + infoLogStruct)

    def __init__(self):
        self.setLogger()
        # Create an engine to the census database
        engine = create_engine(DataBaseConfiguration.CONSTANTS_CONFIGURATIONS.
            SQLALCHEMY_CONNECTION_STRING_DATA_BASE)
        self.session = sessionmaker(bind=engine)()

