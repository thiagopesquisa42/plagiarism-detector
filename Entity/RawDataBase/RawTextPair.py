from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase

class RawTextPair(EntityBase):
    __tablename__           = 'raw_text_pair'
    id                      = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    suspiciousRawTextId     = Column(Integer, ForeignKey('raw_text.id'), nullable=False)
    suspiciousRawText       = relationship('RawText', foreign_keys=[suspiciousRawTextId], lazy='joined')
    sourceRawTextId         = Column(Integer, ForeignKey('raw_text.id'), nullable=False)
    sourceRawText           = relationship('RawText', foreign_keys=[sourceRawTextId], lazy='joined')

    #unique identifier of the object
    def __repr__(self):
        return "<RawTextPair (id='" + id + "'>"
