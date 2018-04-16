from sqlalchemy import Column, Integer, String
from Entity.EntityBase import EntityBase

class Token(EntityBase):
    __tablename__ = 'token'

    id          =   Column(Integer, primary_key=True)
    text        =   Column(String(1000), unique=False, nullable=False)
    occurence   =   Column(Integer, default=0)
    
    #unique identifier of the object
    def __repr__(self):
        return "<Token (id='" + id + "'>"