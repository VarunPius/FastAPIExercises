####################################################################################################
# Imports                                                                                         ##
####################################################################################################

# External modules:


# Internal Modules:
from src import app
from src.models import Product


####################################################################################################
# Code start                                                                                      ##
####################################################################################################

## Home page ##
@app.get("/")
async def root():
    return {"hello": "world"}


## Get all products ##
@app.get("/products")
def fetch_all():
    #return Product.all_pks()   #only fetches Primary keys
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)
    
    return {
        'id':product.pk,
        'name': product.name,
        'price': product.price,
        'Quantity': product.qty
    }

## Insert new product ##
'''
You can run this directly in Postman/Thunder Client. In the POST request body write the following:
{
  "name": "pd1",
  "price": 500,
  "qty": 100
}
'''
@app.post("/product")
def add_prod(product: Product):
    return product.save()

## Get specific product
@app.get("/products/{pk}")
def get_prod(pk: str):
    return Product.get(pk)

## Deleting specific product ##
@app.delete("/products/{pk}")
def delete_prod(pk: str):
    return Product.delete(pk)
