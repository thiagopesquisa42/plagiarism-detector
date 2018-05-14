from sqlalchemy import Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase

class NGramsList(EntityBase):
    __tablename__               = 'n_grams_list'
    id                          = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    sentenceId                  = Column(Integer, ForeignKey('sentence.id'), nullable=False)
    sentence                    = relationship('Sentence', foreign_keys=[sentenceId])
    nGramsOccurenceDictionary   = Column(JSON, nullable=False)

    #unique identifier of the object
    def __repr__(self):
        return "<NGramsList (id='" + id + "'>"
