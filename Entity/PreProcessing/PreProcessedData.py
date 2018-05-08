from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase

class PreProcessedData(EntityBase):
    __tablename__                   = 'pre_processed_data'
    id                              = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    topPreProcessStepChainNodeId    = Column(Integer, ForeignKey('pre_process_step_chain_node.id'), nullable=True)
    topPreProcessStepChainNode      = relationship('PreProcessStepChainNode', foreign_keys=[topPreProcessStepChainNodeId])
    
    #unique identifier of the object
    def __repr__(self):
        return "<PreProcessedData (id='" + id + "'>"
