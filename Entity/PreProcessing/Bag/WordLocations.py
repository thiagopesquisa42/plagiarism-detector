from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase

class WordLocations(EntityBase):
    __tablename__               = 'word_locations'
    wordId                      = Column(Integer, ForeignKey('word.id'), primary_key=True, nullable=False)
    word                        = relationship('Word', foreign_keys=[wordId])
    rawTextExcerptLocationId    = Column(Integer, ForeignKey('raw_text_excerpt_location.id'), primary_key=True, nullable=False)
    rawTextExcerptLocation      = relationship('RawTextExcerptLocation', foreign_keys=[rawTextExcerptLocationId])
    
    #unique identifier of the object
    def __repr__(self):
        return "<WordLocations (id='" + id + "'>"
