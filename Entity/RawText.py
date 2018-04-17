from sqlalchemy import Column, Integer, String, Enum
from Entity import _EntityBase as EntityBase
import enum

class RawTextType(enum.Enum):
    suspicious = 1000
    source = 2000

class RawText(EntityBase):
    __tablename__ = 'raw_text'
    id          =   Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    text        =   Column(String, nullable=False)
    fileName   =   Column(Integer, nullable=False)
    _type       =  Column('type', Enum(RawTextType), nullable=True )
    
    #unique identifier of the object
    def __repr__(self):
        return "<RawText (id='" + id + "'>"