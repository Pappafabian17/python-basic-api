from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import createToken

app = FastAPI(
  title='Aprendiendo FastApi',
  description='Una api en los primero pasos',
  version='0.0.1'
)

class Movie(BaseModel):
  id:Optional[int] = None
  title: str = Field( default='Titulo ', min_length=3)
  overview: str =  Field(default='Descripcion de la pelicula ', min_length=15 , max_length=60)
  year : int = Field(default=2025)
  rating : float = Field(ge=1, le=10)
  category : str = Field(default='Categoria', min_length=3 , max_length=15)

class User(BaseModel):
  email: str
  password: str


movies = [
  {
    'id' : 1,
    'title' : 'El Padrino',
    'overview' : 'El Padrino es una pelicula de 1972 dirigida por coppola...',
    'year' : '1972',
    'rating' : 9.2,
    'category' : 'Crimen' 
  },
  {
    'id' : 2,
    'title' : 'la Padrina',
    'overview' : 'La Padrina es una pelicula de 1972 dirigida por coppola...',
    'year' : '1976',
    'rating' : 5.2,
    'category' : 'Crimen' 
  }
]

@app.post('/login', tags=["authentication"])
def login(user : User):
  if user.email == 'fabian@gmail.com' and user.password == '123':
    token : str = createToken(dict(user))
    print(token)
    return JSONResponse(content=token)

@app.get('/',tags=['Inicio'])
def read_root():
  return HTMLResponse('<h2>Noticion de hola mundo</h2>')

@app.get('/movies',tags=['Movies'])
def get_movies():
  return JSONResponse(content=movies)

@app.get('/movies/{id}',tags=['Movies'])
def get_movie(id: int = Path(ge=1, le=100) ) :
  for item in movies:
    if item['id'] == id:
      return item
  return []

@app.get('/movies/', tags=['Movies'])
def get_movies_by_category(category : str = Query(default='Categoria', min_length=3 , max_length=15)):
  return category

@app.post('/movies',tags=['Movies'], status_code=201)
def create_movie(movie:Movie):
  movies.append(movie)
  print(movies)
  return JSONResponse(status_code=201, content={'message': 'se ha cargado una nueva pelicula', 'movie' : [dict(movie) for movie in movies]})


@app.put('/movies/{id}', tags=['Movies'],status_code=200)
def update_movie(id : int, movie :Movie ):
  for item in movies:
    if item['id'] == id:
      item['title']= movie.title,
      item['overview']= movie.overview,
      item['year']= movie.year,
      item['rating']= movie.rating,
      item['category']= movie.category
      return JSONResponse(content={'message':"se modifico la pelicula correctamente"})

@app.delete('/movies/{id}', tags=['Movies'],status_code=200)
def delete_movie(id: int):
  for item in movies:
    if item['id'] == id:
      movies.remove(item)
      return JSONResponse(content={'message':"se ha eliminado la pelicula correctamente"})