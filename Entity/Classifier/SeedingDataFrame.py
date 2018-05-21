from sqlalchemy import Column, Integer, ForeignKey, BLOB, JSON
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase
import pickle

class SeedingDataFrame(EntityBase):
    __tablename__               = 'seeding_data_frame'
    id                      = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    seedingDataId           = Column(Integer, ForeignKey('seeding_data.id'), nullable=True)
    seedingData             = relationship('SeedingData', foreign_keys=[seedingDataId])
    pickleDataFrame         = Column(BLOB, nullable=False)
    descriptionDictionary   = Column(JSON, nullable=True)

    #unique identifier of the object
    def __repr__(self):
        return "<SeedingDataFrame (id='" + id + "'>"

    def GetDataFrame(self):
        return pickle.loads(self.pickleDataFrame)

    def SetPickleDataFrame(self, dataFrame):
        self.pickleDataFrame = pickle.dumps(dataFrame)