from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase

class PreProcessStepChainNode(EntityBase):
    __tablename__                       = 'pre_process_step_chain_node'
    id                                  = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    preProcessedDataId                  = Column(Integer, ForeignKey('pre_processed_data.id'), nullable=False)
    preProcessedData                    = relationship('PreProcessedData', foreign_keys=[preProcessedDataId])
    preProcessStepId                    = Column(Integer, ForeignKey('pre_process_step.id'), nullable=False)
    preProcessStep                      = relationship('PreProcessStep', foreign_keys=[preProcessStepId])
    stepPosition                        = Column(Integer, nullable=False)
    previousPreProcessStepChainNodeId   = Column(Integer, ForeignKey('pre_process_step_chain_node.id'), nullable=True)
    previousPreProcessStepChainNode     = relationship('PreProcessStepChainNode', foreign_keys=[previousPreProcessStepChainNodeId], uselist=False)

    #unique identifier of the object
    def __repr__(self):
        return "<PreProcessStepChainNode id='" + id + "'>"

