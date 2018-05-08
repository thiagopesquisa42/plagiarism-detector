from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase

class NGramLocations(EntityBase):
    __tablename__               = 'n_gram_locations'
    nGramId                     = Column(Integer, ForeignKey('n_gram.id'), primary_key=True, nullable=False)
    nGram                       = relationship('NGram', foreign_keys=[nGramId])
    rawTextExcerptLocationId    = Column(Integer, ForeignKey('raw_text_excerpt_location.id'), primary_key=True, nullable=False)
    rawTextExcerptLocation      = relationship('RawTextExcerptLocation', foreign_keys=[rawTextExcerptLocationId])
    
    #unique identifier of the object
    def __repr__(self):
        return "<WordLocations (id='" + id + "'>"
