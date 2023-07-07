from fastapi import APIRouter, status, HTTPException
#from src.config.db import conn
from src.models.index import UsersModel
from src.schemas.index import User, UserOut

from typing import Optional, List
from src.config.db import SessionLocal


user = APIRouter()
db = SessionLocal()


@user.get('/users',response_model=List[User],status_code=200)
async def read_users():
    items = db.query(UsersModel).all()

    return items


@user.get("/user/{id}", response_model=User, status_code=status.HTTP_200_OK)
async def read_user(id: int):
    item = db.query(UsersModel).filter(UsersModel.id == id).first()
    return item


@user.post("/user", response_model = UserOut, status_code=status.HTTP_200_OK)
async def create_user(user: User):
    db_item = db.query(UsersModel).filter(UsersModel.name == user.name).first()
    if db_item is not None:
        raise HTTPException(status_code = 400, detail="User already exists")

    new_user = UsersModel(
            name = user.name,
            email = user.email,
            address = user.address
        )
    
    db.add(new_user)
    db.commit()
    return new_user    # response model is User; if you need "Success" or "new user added" use `str`


'''
@user.put("/{id}")
async def update_data(id: int, user: User):           # `User` from schema
    conn.execute(users.update().values(
        name =  user.name,
        email = user.email,
        password = user.password
    ).where(users.c.id == id)
    )
    return conn.execute(users.select()).fetchall()

@user.delete("/")
async def delete_data():
    conn.execute(users.delete().where(users.c.id == id))
    return conn.execute(users.select()).fetchall()      # `users` from models
'''

'''
Old code:

@user.get("/")
async def read_data():
    return conn.execute(users.select()).fetchall()      # `users` from models

@user.get("/{id}")
async def read_data(id: int):
    return conn.execute(users.select().where(users.c.id == id)).fetchall()

@user.post("/")
async def write_data(user: User):           # `User` from schema
    conn.execute(users.insert().values(
        name =  user.name,
        email = user.email,
        password = user.password
    )
    )
    return conn.execute(users.select()).fetchall()

@user.put("/{id}")
async def update_data(id: int, user: User):           # `User` from schema
    conn.execute(users.update().values(
        name =  user.name,
        email = user.email,
        password = user.password
    ).where(users.c.id == id)
    )
    return conn.execute(users.select()).fetchall()

@user.delete("/")
async def delete_data():
    conn.execute(users.delete().where(users.c.id == id))
    return conn.execute(users.select()).fetchall()      # `users` from models

# idea
@app.put('/item/{item_id}',response_model=Item,status_code=status.HTTP_200_OK)
def update_an_item(item_id:int,item:Item):
    item_to_update=db.query(models.Item).filter(models.Item.id==item_id).first()
    item_to_update.name=item.name
    item_to_update.price=item.price
    item_to_update.description=item.description
    item_to_update.on_offer=item.on_offer

    db.commit()

    return item_to_update

@app.delete('/item/{item_id}')
def delete_item(item_id:int):
    item_to_delete=db.query(models.Item).filter(models.Item.id==item_id).first()

    if item_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource Not Found")
    
    db.delete(item_to_delete)
    db.commit()

    return item_to_delete
'''
