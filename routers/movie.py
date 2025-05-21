from fastapi import  Path, Query, Request, HTTPException, Depends, APIRouter
from fastapi.responses import  JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import  validateToken
from bd.database import Session
from models.movie import Movie as ModelMovie
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func


routerMovie = APIRouter()

class Movie(BaseModel):
  id:Optional[int] = None
  title: str = Field( default='Titulo ', min_length=3)
  overview: str =  Field(default='Descripcion de la pelicula ', min_length=15 , max_length=60)
  year : int = Field(default=2025)
  rating : float = Field(ge=1, le=10)
  category : str = Field(default='Categoria', min_length=3 , max_length=15)

class BearerJWT(HTTPBearer):
  async def __call__(self, request : Request):
    auth = await super().__call__(request)
    data = validateToken(auth.credentials)
    if(data['email'] != 'fabian@gmail.com' ):
      raise HTTPException(status_code=403, detail="Credenciales incorrectas ")


@routerMovie.get('/movies',tags=['Movies'], dependencies=[Depends(BearerJWT())])
def get_movies():
  db = Session()
  data = db.query(ModelMovie).all()
  mov = jsonable_encoder(data)
  return JSONResponse(content=mov)

@routerMovie.get('/movies/{id}',tags=['Movies'])
def get_movie(id: int = Path(ge=1, le=100) ) :
  db = Session()
  data  = db.query(ModelMovie).filter(ModelMovie.id == id).first()
  if not data:
    return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
  return JSONResponse(status_code=200, content=jsonable_encoder(data))

@routerMovie.get('/movies/', tags=['Movies'])
def get_movies_by_category(category : str = Query(default='Categoria', min_length=3 , max_length=15)):
  db = Session()
  data = db.query(ModelMovie).filter( func.lower(ModelMovie.category) == category.lower()).all()

  return JSONResponse(status_code=200, content=jsonable_encoder(data))

@routerMovie.post('/movies',tags=['Movies'], status_code=201)
def create_movie(movie:Movie):
  db = Session()
  newMovie = ModelMovie(**dict(movie))
  pelirepetida = db.query(ModelMovie).filter(ModelMovie.id == newMovie.id).first()
  if pelirepetida:
    return JSONResponse(status_code=400, content={'message': 'El id proporcionado ya existe, intenta  con otro diferente'})
  db.add(newMovie)
  print(newMovie)
  db.commit()
  return JSONResponse(status_code=201, content={'message': 'se ha cargado una nueva pelicula', 'movie' :jsonable_encoder(newMovie)})


@routerMovie.put('/movies/{id}', tags=['Movies'],status_code=200)
def update_movie(id : int, movie :Movie ):
  db = Session()
  data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
  if not data:
    return JSONResponse(status_code=404, content={'message':'No se encontro el recurso'})
  data.title = movie.title
  data.overview = movie.overview
  data.year = movie.year
  data.rating = movie.rating
  data.category = movie.category
  db.commit()
  return JSONResponse(content={'message':"se modifico la pelicula correctamente"})

@routerMovie.delete('/movies/{id}', tags=['Movies'],status_code=200)
def delete_movie(id: int):
  db = Session()
  data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
  if not data:
    return JSONResponse(status_code=404, content={'message':'No se encontro el recurso'})
  db.delete(data)
  db.commit()
  return JSONResponse(content={'message':"se ha eliminado la pelicula correctamente", "data" : jsonable_encoder(data)})