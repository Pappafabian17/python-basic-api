from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import createToken, validateToken
from bd.database import Session, engine, Base
from models.movie import Movie as ModelMovie
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func


@app.get('/movies',tags=['Movies'], dependencies=[Depends(BearerJWT())])
def get_movies():
  db = Session()
  data = db.query(ModelMovie).all()
  mov = jsonable_encoder(data)
  return JSONResponse(content=mov)

@app.get('/movies/{id}',tags=['Movies'])
def get_movie(id: int = Path(ge=1, le=100) ) :
  db = Session()
  data  = db.query(ModelMovie).filter(ModelMovie.id == id).first()
  if not data:
    return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
  return JSONResponse(status_code=200, content=jsonable_encoder(data))

@app.get('/movies/', tags=['Movies'])
def get_movies_by_category(category : str = Query(default='Categoria', min_length=3 , max_length=15)):
  db = Session()
  data = db.query(ModelMovie).filter( func.lower(ModelMovie.category) == category.lower()).all()

  return JSONResponse(status_code=200, content=jsonable_encoder(data))

@app.post('/movies',tags=['Movies'], status_code=201)
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


@app.put('/movies/{id}', tags=['Movies'],status_code=200)
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

@app.delete('/movies/{id}', tags=['Movies'],status_code=200)
def delete_movie(id: int):
  db = Session()
  data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
  if not data:
    return JSONResponse(status_code=404, content={'message':'No se encontro el recurso'})
  db.delete(data)
  db.commit()
  return JSONResponse(content={'message':"se ha eliminado la pelicula correctamente", "data" : jsonable_encoder(data)})