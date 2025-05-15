from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional


app = FastAPI(
  title='Aprendiendo FastApi',
  description='Una api en los primero pasos',
  version='0.0.1'
)

class Movie(BaseModel):
  id:Optional[int] = None
  title: str
  overview: str
  year : int
  rating : float
  category : str


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

@app.get('/',tags=['Inicio'])
def read_root():
  return HTMLResponse('<h2>Noticion de hola mundo</h2>')

@app.get('/movies',tags=['Movies'])
def get_movies():
  return movies

@app.get('/movies/{id}',tags=['Movies'])
def get_movie(id: int):
  for item in movies:
    if item['id'] == id:
      return item
  return []

@app.get('/movies/', tags=['Movies'])
def get_movies_by_category(category : str):
  return category

@app.post('/movies',tags=['Movies'])
def create_movie(movie:Movie):
  movies.append(movie)
  print(movies)
  return movie.title


@app.put('/movies/{id}', tags=['Movies'])
def update_movie(
  id: int ,
  title : str = Body(),
  overview : str = Body(), 
  year: int = Body(),
  rating : float = Body(),
  category : str = Body()
):
  for movie in movies:
    if movie['id'] == id:
      movie['title']= title,
      movie['overview']= overview,
      movie['year']= year,
      movie['rating']= rating,
      movie['category']= category
      return movies

@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id: int):
  for item in movies:
    if item['id'] == id:
      movies.remove(item)
      return movies