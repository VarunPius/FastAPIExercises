######################################################################################################################################################
# Code Info                                                                                                                                          #
#                                                                                                                                                    #                                                                                                                                     #
# Author(s): Varun Pius Rodrigues                                                                                                                    #
# About: Database setup and initializer                                                                                                              #
######################################################################################################################################################


# -------------------------------------------------------------------------------------------------------------------------------------------------- #
# Library Imports goes here
# -------------------------------------------------------------------------------------------------------------------------------------------------- #

# Internal imports
from src.config.db import DATABASE_URL
from src.models.index import Base  # Import your SQLAlchemy models


# External librabries
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


# -------------------------------------------------------------------------------------------------------------------------------------------------- #
# Code Here 
# -------------------------------------------------------------------------------------------------------------------------------------------------- #

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def drop_db():
    from src.config.db import DATABASE_URL
    from src.models.index import Base
    
    engine = create_engine(DATABASE_URL)
    
    # This will drop all tables
    Base.metadata.drop_all(bind=engine)
    
    print("All database tables dropped successfully!")


def init_db():
    # Create engine with your connection string
    logger.info("Creating engine")
    engine = create_engine(DATABASE_URL)
    logger.info("Engine created")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    #print("Database tables created successfully!")
    logger.info("Database tables created successfully!")


if __name__ == "__main__":
    init_db()