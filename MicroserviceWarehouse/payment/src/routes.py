####################################################################################################
# Imports                                                                                         ##
####################################################################################################

# Standard modules:
import time

# External modules:
from src import BackgroundTasks
from starlette.requests import Request
import requests


# Internal Modules:
from src import app
from src import redis
from src.models import Order


####################################################################################################
# Code start                                                                                      ##
####################################################################################################

## Get all order ##
@app.get('/order/{id}')
def get(id: str):
    return Order.get(id)

@app.get('/orders')
def get_all():
    return Order.all_pks()
    #return Order.get(id)


## Insert order ##
@app.post('/orders')
async def create(request: Request, bckgrnd_tsk: BackgroundTasks):   #id, quantity
    body = await request.json()

    req = requests.get('http://localhost:8000/products/%s' % body['id'])
    product = req.json()

    order = Order(
        product_id = body['id'],
        price = product['price'],
        fee = 0.2 * product['price'],
        total = 1.2 * product['price'],
        qty = body['qty'],
        status = 'pending'
    )

    order.save()

    # We introduced a 10sec delay in the `order_completed` method.
    # when the request is made, it will wait for 10seconds. 
    # Instead, what we can do is have it run in background with the help of BackgroundTasks
    # here, in the add_task method of BackgroundTasks, 
    # the first is the name of the method, and rest of the parameters are the parameters of the metod passed as first parameter
    bckgrnd_tsk.add_task(order_completed, order)

    return order

def order_completed(order: Order):
    time.sleep(10)
    order.status = 'completed'
    order.save()

    redis.xadd('order_complete', order.dict(), '*') # (stream_name, key-value pairs, id)