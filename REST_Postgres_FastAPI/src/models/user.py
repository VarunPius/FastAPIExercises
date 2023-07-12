from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, Text
#from src.config.db import meta
from src.config.db import Base

'''
users = Table(
    'users', meta,
    Column('id', Integer, primary_key = True),
    Column('name', String(255)),
    Column('email', String(255)),
    Column('password', String(255))
)
'''

class UsersModel(Base):
    __tablename__='users'
    id = Column(Integer, primary_key = True)
    name = Column(String(255),nullable = False,unique = True)
    email = Column(Text)
    address = Column(Text)

    def __repr__(self):
        return f"<Item name = {self.name} |->email = {self.email}>"


'''
from sqlalchemy.sql.expression import null
from database import Base
from sqlalchemy import String,Boolean,Integer,Column,Text


class Item(Base):
    __tablename__='items'
    id=Column(Integer,primary_key=True)
    name=Column(String(255),nullable=False,unique=True)
    description=Column(Text)
    price=Column(Integer,nullable=False)
    on_offer=Column(Boolean,default=False)


    def __repr__(self):
        return f"<Item name={self.name} price={self.price}>"
'''