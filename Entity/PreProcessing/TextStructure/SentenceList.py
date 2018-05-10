from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase

class SentenceList(EntityBase):
    __tablename__               = 'sentence_list'
    id                          = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    preProcessStepChainNodeId   = Column(Integer, ForeignKey('pre_process_step_chain_node.id'), nullable=False)
    preProcessStepChainNode     = relationship('PreProcessStepChainNode', foreign_keys=[preProcessStepChainNodeId])
    rawTextExcerptLocationId    = Column(Integer, ForeignKey('raw_text_excerpt_location.id'), nullable=False)
    rawTextExcerptLocation      = relationship('RawTextExcerptLocation', foreign_keys=[rawTextExcerptLocationId])
    
    #unique identifier of the object
    def __repr__(self):
        return "<SentenceList id='" + id + "'>"
