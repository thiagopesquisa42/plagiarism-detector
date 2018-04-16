import Repository.DataBaseConfiguration as DataBaseConfiguration
# Import create_engine function
from sqlalchemy import create_engine
# the Session class 
from sqlalchemy.orm import sessionmaker

class DataBaseConnection(object):
    # Create an engine to the census database
    engine = create_engine(DataBaseConfiguration.CONSTANTS_CONFIGURATIONS.
    SQLALCHEMY_CONNECTION_STRING_DATA_BASE)
    session = sessionmaker(bind=engine)()

    def __init__(self):
        pass

