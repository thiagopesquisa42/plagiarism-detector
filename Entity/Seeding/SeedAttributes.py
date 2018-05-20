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
    dice                        = Column(Float)
    
    isMaxCosine                 = Column(Float)
    maxCosineDiff               = Column(Float)
    meanMaxCosineDiff           = Column(Float)
    maxCosineNeighbour          = Column(Float)
    verticalCosineMaxDistance   = Column(Float)
    verticalCosineMaxMeasure    = Column(Float)

    isMaxDice                   = Column(Float)
    maxDiceDiff                 = Column(Float)
    meanMaxDiceDiff             = Column(Float)
    maxDiceNeighbour            = Column(Float)
    verticalDiceMaxDistance     = Column(Float)
    verticalDiceMaxMeasure      = Column(Float)

    lengthRatio                 = Column(Float)

    #unique identifier of the object
    def __repr__(self):
        return "<SeedAttributes (seedId='" + seedId + "'>"

    def ToDictionary(self):
        return {
            'seedId':                       self.seedId,
            'plagiarismClass':              self.plagiarismClass.name,
            'percentualInDetection':        self.percentualInDetection,
            'cosine':                       self.cosine,
            'dice':                         self.dice,
            'isMaxCosine':                  self.isMaxCosine,
            'maxCosineDiff':                self.maxCosineDiff,
            'meanMaxCosineDiff':            self.meanMaxCosineDiff,
            'maxCosineNeighbour':           self.maxCosineNeighbour,
            'verticalCosineMaxDistance':    self.verticalCosineMaxDistance,
            'verticalCosineMaxMeasure':     self.verticalCosineMaxMeasure,
            'isMaxDice':                    self.isMaxDice,
            'maxDiceDiff':                  self.maxDiceDiff,
            'meanMaxDiceDiff':              self.meanMaxDiceDiff,
            'maxDiceNeighbour':             self.maxDiceNeighbour,
            'verticalDiceMaxDistance':      self.verticalDiceMaxDistance,
            'verticalDiceMaxMeasure':       self.verticalDiceMaxMeasure,
            'lengthRatio':                  self.lengthRatio
        }
