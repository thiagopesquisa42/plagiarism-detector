from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase

class Seed(EntityBase):
    __tablename__               = 'seed'
    id                          = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    seedingDataId               = Column(Integer, ForeignKey('seeding_data.id'), nullable=False)
    seedingData                 = relationship('SeedingData', foreign_keys=[seedingDataId])
    suspiciousSentenceId        = Column(Integer, ForeignKey('sentence.id'), nullable=False)
    suspiciousSentence          = relationship('Sentence', foreign_keys=[suspiciousSentenceId])
    sourceSentenceId            = Column(Integer, ForeignKey('sentence.id'), nullable=False)
    sourceSentence              = relationship('Sentence', foreign_keys=[sourceSentenceId])
    rawTextPairId               = Column(Integer, ForeignKey('raw_text_pair.id'), nullable=False)
    rawTextPair                 = relationship('RawTextPair', foreign_keys=[rawTextPairId])
    attributes                  = relationship("SeedAttributes", primaryjoin="Seed.id==SeedAttributes.seedId", uselist=False, lazy='joined')

    #unique identifier of the object
    def __repr__(self):
        return "<Seed (id='" + id + "'>"
