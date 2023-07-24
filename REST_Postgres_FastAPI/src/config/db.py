######################################################################################################################################################
# Code Info                                                                                                                                          #
#                                                                                                                                                    #                                                                                                                                     #
# Author(s): Varun Pius Rodrigues                                                                                                                    #
# About: Database setup and initializer                                                                                                              #
######################################################################################################################################################


# -------------------------------------------------------------------------------------------------------------------------------------------------- #
# Library Imports goes here
# -------------------------------------------------------------------------------------------------------------------------------------------------- #

# External librabries
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


# -------------------------------------------------------------------------------------------------------------------------------------------------- #
# Configurations goes here
# -------------------------------------------------------------------------------------------------------------------------------------------------- #

# engine=create_engine("postgresql://<user>:<pwd>@<host>/<db>",
conn_url = 'postgresql+psycopg2://vpiusr:Seatt!3@postgres_db/postgres'
engine = create_engine(conn_url, echo=True)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


# -------------------------------------------------------------------------------------------------------------------------------------------------- #
# Appendix
# -------------------------------------------------------------------------------------------------------------------------------------------------- #

'''
Old Code:
from sqlalchemy import  MetaData
from sqlalchemy.engine import URL
url = URL.create(
    drivername="vpiusr",
    username="coderpad",
    host="/tmp/postgresql/socket",
    database="postgres"
)
engine = create_engine(url)
# or 
engine = create_engine(conn_url)

conn = engine.connect()

meta = MetaData()       # meta is used in models if creating object using `Table`
'''