from fastapi import APIRouter
from fastapi.responses import  JSONResponse
from pydantic import BaseModel
from user_jwt import createToken
from bd.database import engine, Base
from routers.movie import routerMovie


routerUser = APIRouter()


Base.metadata.create_all(bind=engine)


class User(BaseModel):
  email: str
  password: str

@routerUser.post('/login', tags=["authentication"])
def login(user : User):
  if user.email == 'fabian@gmail.com' and user.password == '123':
    token : str = createToken(dict(user))
    print(token)
    return JSONResponse(content=token)

