####################################################################################################
# Imports                                                                                         ##
####################################################################################################

# Internal modules:
import time

# External modules:
from src import BackgroundTasks
from starlette.requests import Request
import requests


# Internal Modules:
from src import app
from src.models import Order


####################################################################################################
# Code start                                                                                      ##
####################################################################################################

## Get all order ##
@app.get('/order/{id}')
def get(id: str):
    return Order.get(id)



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

    bckgrnd_tsk.add_task(order_completed, order)

    return order

def order_completed(order: Order):
    time.sleep(10)
    order.status = 'completed'
    order.save()