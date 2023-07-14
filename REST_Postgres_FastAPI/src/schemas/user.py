from pydantic import BaseModel

class User(BaseModel):
    # no need for id as it's autoincremented
    #id: int
    name: str
    email: str
    address: str
    
    #class Config:
    #    orm_mode = True
    
class UserOut(BaseModel):
    # Schema for output
    id: int
    name: str
    email: str
    address: str
    
    class Config:
        orm_mode = True
