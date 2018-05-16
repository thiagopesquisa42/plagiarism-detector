from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, join
from Entity import _EntityBase as EntityBase

class SentenceList(EntityBase):
    __tablename__               = 'sentence_list'
    id                          = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    preProcessStepChainNodeId   = Column(Integer, ForeignKey('pre_process_step_chain_node.id'), nullable=False)
    preProcessStepChainNode     = relationship('PreProcessStepChainNode', foreign_keys=[preProcessStepChainNodeId])
    rawTextId                   = Column(Integer, ForeignKey('raw_text.id'), nullable=True)
    rawText                     = relationship('RawText', foreign_keys=[rawTextId])
    sentences                   = relationship("Sentence", primaryjoin="SentenceList.id==Sentence.sentenceListId")

    #unique identifier of the object
    def __repr__(self):
        return "<SentenceList id='" + id + "'>"
