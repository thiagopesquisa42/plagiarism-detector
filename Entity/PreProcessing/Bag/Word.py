from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase

class Word(EntityBase):
    __tablename__           = 'word'
    id                      = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    bagOfWordsId            = Column(Integer, ForeignKey('bag_of_words.id'), nullable=False)
    bagOfWords              = relationship('BagOfWords', foreign_keys=[bagOfWordsId])
    occurence               = Column(Integer, nullable=False)
    text                    = Column(String, nullable=False)

    #unique identifier of the object
    def __repr__(self):
        return "<Word (id='" + id + "'>"