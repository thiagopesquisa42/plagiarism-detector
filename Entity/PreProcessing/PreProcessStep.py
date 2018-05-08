from sqlalchemy import Column, Integer, ForeignKey, Enum, String
from Entity import _EntityBase as EntityBase
from Entity import _PreProcessName as PreProcessName
from Entity import _TokenizeType as TokenizeType
from Entity import _StemmingType as StemmingType
from Entity import _NGramType as NGramType

class PreProcessStep(EntityBase):
    __tablename__                   = 'pre_process_step'
    id                              = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name                            = Column(Enum(PreProcessName), nullable=False)
    tokenizeType                    = Column(Enum(TokenizeType), nullable=True) 
    stemmingType                    = Column(Enum(StemmingType), nullable=True)
    nGramType                       = Column(Enum(NGramType), nullable=True)
    nGramParameterN                 = Column(Integer, nullable=True)
    nGramParameterSkip              = Column(Integer, nullable=True)
    regexRule                       = Column(String, nullable=True)
    description                     = Column(String, nullable=True)

    #unique identifier of the object
    def __repr__(self):
        return "<PreProcessStep id='" + id + "'>"

