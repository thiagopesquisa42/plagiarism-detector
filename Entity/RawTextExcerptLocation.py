from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase

class RawTextExcerptLocation(EntityBase):
    __tablename__           = 'raw_text_excerpt_location'
    id                      = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    firstCharacterPosition  = Column(Integer, nullable=False)
    stringLength            = Column(Integer, nullable=False)

#    preProcessedDataId      = Column(Integer, ForeignKey('pre_processed_data.id'), nullable=True)
    preProcessedDataId      = Column(Integer, nullable=True)
    rawTextId               = Column(Integer, ForeignKey('raw_text.id'), nullable=False)
    rawText                 = relationship('RawText', foreign_keys=[rawTextId])
    
    #unique identifier of the object
    def __repr__(self):
        return "<RawTextExcerptLocation (id='" + id + "'>"
