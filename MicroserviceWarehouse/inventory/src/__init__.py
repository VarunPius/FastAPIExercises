####################################################################################################
# Imports                                                                                         ##
####################################################################################################

# Standard Modules:
import os
import yaml

# External modules:
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection


####################################################################################################
# Configurations                                                                                  ##
####################################################################################################

# Project structure configurations
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
#servicedir = os.path.join(basedir, 'inventory')
confdir = os.path.join(basedir, 'docs')


# Service configurations
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=['*'],
    allow_headers=['*']
)


# Database configurations
conffile = os.path.join(confdir, 'conf.yaml')
with open(conffile, "r") as ymlconf:
    try:
        conf = yaml.safe_load(ymlconf)
    except yaml.YAMLError as exc:
        print(exc)


host = conf['Redis']['host']
port = conf['Redis']['port']
password = conf['Redis']['password']

redis = get_redis_connection(
    host = host,
    port = port,
    password = password,
    decode_responses = True
)


####################################################################################################
# All circular imports here:                                                                      ##
####################################################################################################

from src import routes
