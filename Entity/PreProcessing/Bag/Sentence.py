from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase

class Sentence(EntityBase):
    __tablename__               = 'sentence'
    id                          = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    bagOfSentencesId            = Column(Integer, ForeignKey('bag_of_sentences.id'), nullable=False)
    bagOfSentences              = relationship('BagOfSentences', foreign_keys=[bagOfSentencesId])
    text                        = Column(String, nullable=False)
    rawTextExcerptLocationId    = Column(Integer, ForeignKey('raw_text_excerpt_location.id'), nullable=False)
    rawTextExcerptLocation      = relationship('RawTextExcerptLocation', foreign_keys=[rawTextExcerptLocationId])
    
    #unique identifier of the object
    def __repr__(self):
        return "<Sentence (id='" + id + "'>"
