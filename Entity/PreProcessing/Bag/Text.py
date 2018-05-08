from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase

class Text(EntityBase):
    __tablename__           = 'text'
    id                      = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    bagOfTextsId            = Column(Integer, ForeignKey('bag_of_texts.id'), nullable=False)
    bagOfTexts              = relationship('BagOfTexts', foreign_keys=[bagOfTextsId])
    text                    = Column(String, nullable=False)
    rawTextExcerptLocationId     = Column(Integer, ForeignKey('raw_text_excerpt_location.id'), nullable=False)
    rawTextExcerptLocation       = relationship('RawTextExcerptLocation', foreign_keys=[rawTextExcerptLocationId])
    
    #unique identifier of the object
    def __repr__(self):
        return "<Text (id='" + id + "'>"
