######################################################################################################################################################
# Code Info                                                                                                                                          #
#                                                                                                                                                    #                                                                                                                                     #
# Author(s): Varun Pius Rodrigues                                                                                                                    #
# About: Module setup and initializer                                                                                                                #
######################################################################################################################################################


# -------------------------------------------------------------------------------------------------------------------------------------------------- #
# Library Imports goes here
# -------------------------------------------------------------------------------------------------------------------------------------------------- #

# System Libraries
import os

# Internal imports
from src.routes.index import user

# External librabries
from fastapi import FastAPI


# -------------------------------------------------------------------------------------------------------------------------------------------------- #
# Configurations goes here
# -------------------------------------------------------------------------------------------------------------------------------------------------- #

# FastAPI
# -------------------------------------------------------------------------------------------------------------------------------------------------- #
app = FastAPI()
app.include_router(user)    # `user` from routes APIRouter


# Directory setups
# -------------------------------------------------------------------------------------------------------------------------------------------------- #
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
confdir = os.path.join(basedir, 'resources')
#datadir = os.path.join(basedir, 'data')


# Home page
# -------------------------------------------------------------------------------------------------------------------------------------------------- #

import logging
from fastapi import FastAPI
from src.config.db_init import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting database initialization...")
    try:
        init_db()
        logger.info("Database initialization complete")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")


@app.get("/")
async def root():
    return {"Hello": "mundo"}


