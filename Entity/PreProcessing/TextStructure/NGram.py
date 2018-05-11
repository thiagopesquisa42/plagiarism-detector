from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase

class NGram(EntityBase):
    __tablename__           = 'n_gram'
    id                      = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    nGramsListId            = Column(Integer, ForeignKey('n_grams_list.id'), nullable=False)
    nGramsList              = relationship('NGramsList', foreign_keys=[nGramsListId])
    occurence               = Column(Integer, nullable=False)
    commaSeparatedGrams     = Column(String, nullable=False)

    #unique identifier of the object
    def __repr__(self):
        return "<NGram (id='" + id + "'>"