#defining shape of data coming in and going out from my API
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

#User schemas

#when the user registers for the first time
class UserCreate(BaseModel):
    username : str
    email : str
    password : str

#when user just logins
class UserLogin(BaseModel):
    email : str
    password : str

#sending complete user information to cliend
class UserOut(BaseModel):
    id : int 
    username : str
    email : str
    created_at : datetime

    model_config = ConfigDict(from_attributes=True)


#Task schemas

#when a task is created for the first time
class TaskCreate(BaseModel):
    title : str
    description : str

#used when a task is updated
class TaskUpdate(BaseModel):
    #every field is optional
    title : Optional[str] = None
    description : Optional[str] = None
    is_done: Optional[bool] = None


#giving complete info about a task
class TaskOut(BaseModel):
    id : int
    title : str
    description : str
    is_done : bool
    created_at : datetime
    owner_id : int

    model_config = ConfigDict(from_attributes=True)

    

#Token schemas -> for JWT authentication

#response shape after login
class Token(BaseModel):
    access_token : str
    token_type : str

#that parameter which is unique to each user in JWT
class TokenData(BaseModel):
    user_id : int


#model config tells pydantic that you may get python objects not only dictionary
