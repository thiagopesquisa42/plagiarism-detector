from sqlalchemy import Column, Integer, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase
from Entity import _PlagiarismClass as PlagiarismClass

class SeedAttributes(EntityBase):
    __tablename__               = 'seed_attributes'
    seedId                      = Column(Integer, ForeignKey('seed.id'), primary_key=True, nullable=False)
    seed                        = relationship('Seed', foreign_keys=[seedId])
    plagiarismClass             = Column(Enum(PlagiarismClass))
    percentualInDetection       = Column(Float)
    cosine                      = Column(Float)
    maxCosine                   = Column(Float)
    dice                        = Column(Float)
    maxDice                     = Column(Float)

    #unique identifier of the object
    def __repr__(self):
        return "<SeedAttributes (seedId='" + seedId + "'>"