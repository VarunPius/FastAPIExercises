####################################################################################################
# Imports                                                                                         ##
####################################################################################################

# External Modules:
from redis_om import HashModel

# Internal Modules:
from src import redis


####################################################################################################
# Database object models                                                                          ##
####################################################################################################

class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    qty: int
    status: str     # pending, completed, refunded
    
    class Meta:
        database = redis