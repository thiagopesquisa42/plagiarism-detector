from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase
from Entity import _PlagiarismObfuscation as PlagiarismObfuscation
from Entity import _PlagiarismType as PlagiarismType
from Entity import _EnumYesNo as EnumYesNo

class Detection(EntityBase):
    __tablename__           = 'detection'
    id                      = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name                    = Column(String)
    obfuscation             = Column(Enum(PlagiarismObfuscation))
    _type                   = Column('type', Enum(PlagiarismType))
    obfuscationDegree       = Column(Float)
    isGiven                 = Column(Enum(EnumYesNo), nullable=False)
    isDetected              = Column(Enum(EnumYesNo), nullable=False)

    rawTextSuspiciousLocationId     = Column(Integer, ForeignKey('raw_text_excerpt_location.id'), nullable=False)
    rawTextSuspiciousLocation       = relationship('RawTextExcerptLocation', foreign_keys=[rawTextSuspiciousLocationId], lazy='joined')
    rawTextSourceLocationId         = Column(Integer, ForeignKey('raw_text_excerpt_location.id'), nullable=False)
    rawTextSourceLocation       = relationship('RawTextExcerptLocation', foreign_keys=[rawTextSourceLocationId], lazy='joined')
    
    textCollectionMetaId         = Column(Integer, ForeignKey('text_collection_meta.id'), nullable=False)
    textCollectionMeta           = relationship('TextCollectionMeta', foreign_keys=[textCollectionMetaId])

    rawTextPairId         = Column(Integer, ForeignKey('raw_text_pair.id'), nullable=False)
    rawTextPair           = relationship('RawTextPair', foreign_keys=[rawTextPairId])

    #unique identifier of the object
    def __repr__(self):
        return "<RawTextExcerptLocation (id='" + id + "'>"
