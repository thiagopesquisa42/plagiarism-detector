import Repository.DataBaseConfiguration as DataBaseConfiguration
from constant import LoggerConstant
# Import create_engine function
from sqlalchemy import create_engine
# the Session class 
from sqlalchemy.orm import sessionmaker
import logging

class BaseRepository(object):
    session = None
    
    @staticmethod
    def InitSession():
        # Create an engine to the census database
        engine = create_engine(DataBaseConfiguration.CONSTANTS_CONFIGURATIONS.
            SQLALCHEMY_CONNECTION_STRING_DATA_BASE)
        BaseRepository.session = sessionmaker(bind=engine)()

    @staticmethod
    def SetLogger():
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

    def Insert(self, item):
        if(item == None):
            return
        self.session.add(item)
        self.session.commit()

    def InsertList(self, itemList):
        if(itemList == None or len(itemList) == 0):
            return
        for item in itemList:
            self.session.add(item)
        self.session.commit()

    def Update(self, item):
        self.Insert(item)
    
    def UpdateList(self, itemList):
        self.InsertList(itemList)

    def __init__(self):
        self.session = BaseRepository.session

BaseRepository.SetLogger()
BaseRepository.InitSession()