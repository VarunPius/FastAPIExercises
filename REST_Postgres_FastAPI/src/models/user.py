######################################################################################################################################################
# Code Info                                                                                                                                          #
#                                                                                                                                                    #                                                                                                                                     #
# Author(s): Varun Pius Rodrigues                                                                                                                    #
# About: Model Index file                                                                                                                            #
######################################################################################################################################################


# -------------------------------------------------------------------------------------------------------------------------------------------------- #
# Library Imports goes here
# -------------------------------------------------------------------------------------------------------------------------------------------------- #

# External librabries
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, Text

# Internal imports
from src.config.db import Base


# -------------------------------------------------------------------------------------------------------------------------------------------------- #
# Models 
# -------------------------------------------------------------------------------------------------------------------------------------------------- #

class UsersModel(Base):
    __tablename__='users'
    id = Column(Integer, primary_key = True)
    name = Column(String(255), nullable = False)
    email = Column(Text, unique = True)
    address = Column(Text)

    def __repr__(self):
        return f"<User name = {self.name} |-> email = {self.email}>"



# -------------------------------------------------------------------------------------------------------------------------------------------------- #
# Appendix
# -------------------------------------------------------------------------------------------------------------------------------------------------- #

'''
Old code:
from sqlalchemy.sql.expression import null
from database import Base
from src.config.db import meta
from sqlalchemy import String,Boolean,Integer,Column,Text


users = Table(
    'users', meta,
    Column('id', Integer, primary_key = True),
    Column('name', String(255)),
    Column('email', String(255)),
    Column('password', String(255))
)

'''