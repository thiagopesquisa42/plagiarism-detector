from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase

class _Bag(EntityBase):
    __tablename__               = 'bag'
    id                          = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    preProcessStepChainNodeId   = Column(Integer, ForeignKey('pre_process_step_chain_node.id'), nullable=False)
    preProcessStepChainNode     = relationship('PreProcessStepChainNode', foreign_keys=[preProcessStepChainNodeId])
    bagOfTextsId                = Column(Integer, ForeignKey('bag_of_texts.id'), nullable=True)
    bagOfTexts                  = relationship('BagOfTexts', foreign_keys=[bagOfTextsId])
    bagOfSentencesId            = Column(Integer, ForeignKey('bag_of_sentences.id'), nullable=True)
    bagOfSentences              = relationship('BagOfSentences', foreign_keys=[bagOfSentencesId])
    bagOfWordsId                = Column(Integer, ForeignKey('bag_of_words.id'), nullable=True)
    bagOfWords                  = relationship('BagOfWords', foreign_keys=[bagOfWordsId])
    bagOfNGramId                = Column(Integer, ForeignKey('bag_of_n_grams.id'), nullable=True)
    bagOfNGram                  = relationship('BagOfNGrams', foreign_keys=[bagOfNGramId])

    #unique identifier of the object
    def __repr__(self):
        return "<Bag id='" + id + "'>"
