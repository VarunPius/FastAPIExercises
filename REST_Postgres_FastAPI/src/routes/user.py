from fastapi import APIRouter
#from src.config.db import conn
from src.models.index import UsersModel
from src.schemas.index import User

from typing import Optional, List
from src.config.db import SessionLocal


user = APIRouter()
db = SessionLocal()

'''
@user.get("/", response_model=List[User], status_code=200)
async def read_data():
    return conn.execute(users.select()).fetchall()      # `users` from models
'''

@user.get('/',response_model=List[User],status_code=200)
def get_all_items():
    items = db.query(UsersModel).all()

    return items


'''
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
'''