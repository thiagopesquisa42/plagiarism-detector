from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase

class SeedingData(EntityBase):
    __tablename__               = 'seeding_data'
    id                  = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    preProcessedDataId  = Column('preProcessedDataId', Integer, ForeignKey('pre_processed_data.id'), nullable=False)
    preProcessedData    = relationship('PreProcessedData', foreign_keys=[preProcessedDataId])
    description         = Column('description', String, nullable=True)

    #unique identifier of the object
    def __repr__(self):
        return "<SeedingData (id='" + id + "'>"
