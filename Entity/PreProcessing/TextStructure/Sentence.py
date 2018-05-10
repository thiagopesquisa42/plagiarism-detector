from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase

class Sentence(EntityBase):
    __tablename__               = 'sentence'
    id                          = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    sentenceListId              = Column(Integer, ForeignKey('sentence_list.id'), nullable=False)
    sentenceList                = relationship('SentenceList', foreign_keys=[sentenceListId])
    text                        = Column(String, nullable=False)
    rawTextExcerptLocationId    = Column(Integer, ForeignKey('raw_text_excerpt_location.id'), nullable=False)
    rawTextExcerptLocation      = relationship('RawTextExcerptLocation', foreign_keys=[rawTextExcerptLocationId])
    bagOfWordsId                = Column(Integer, ForeignKey('bag_of_words.id'), nullable=True)
    bagOfWords                  = relationship('BagOfWords', foreign_keys=[bagOfWordsId])
    nGramsListId                = Column(Integer, ForeignKey('n_grams_list.id'), nullable=True)
    nGramsList                  = relationship('NGramsList', foreign_keys=[nGramsListId])

    #unique identifier of the object
    def __repr__(self):
        return "<Sentence (id='" + id + "'>"
