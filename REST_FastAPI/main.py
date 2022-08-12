from typing import List
from uuid import uuid4, UUID
from fastapi import FastAPI, HTTPException

from models import User, Gender, Role, UserUpdateRequest

app = FastAPI()

db: List[User] = [
    User(id=uuid4(), 
        first_name = "Varun", 
        last_name = "Rodrigues", 
        gender = Gender.male,
        roles = [Role.admin],
        wallet = 1000
    ),
    User(id=uuid4(), 
        first_name = "Test", 
        last_name = "User1", 
        gender = Gender.female,
        roles = [Role.student, Role.user],
        active = False
    )
]

@app.get("/")
async def root():
    return {"Hello": "mundo"}


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code = 404,
        detail = f"User with user id {user_id} does not exist"
    )


@app.put("/api/v1/users/{user_id}")
async def update_user(user_to_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_to_update.first_name is not None:
                user.first_name = user_to_update.first_name
            if user_to_update.middle_name is not None:
                user.middle_name = user_to_update.middle_name
            if user_to_update.last_name is not None:
                user.last_name = user_to_update.last_name
            if user_to_update.roles is not None:
                user.roles = user_to_update.roles
            return
    raise HTTPException(
        status_code = 404,
        detail = f"User with user id {user_id} does not exist"
    )

'''
PUT Request body:
{
    "middle_name": "Pius",
    "roles": [
      "admin", "student"
    ]
}
'''