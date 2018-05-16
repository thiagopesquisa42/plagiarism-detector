from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase

class RawTextExcerptLocation(EntityBase):
    __tablename__           = 'raw_text_excerpt_location'
    id                      = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    firstCharacterPosition  = Column(Integer, nullable=False)
    lastCharacterPosition   = Column(Integer, nullable=True)
    stringLength            = Column(Integer, nullable=False)
    rawTextId               = Column(Integer, ForeignKey('raw_text.id'), nullable=False)
    rawText                 = relationship('RawText', foreign_keys=[rawTextId])
    
    #unique identifier of the object
    def __repr__(self):
        return "<RawTextExcerptLocation (id='" + id + "'>"
