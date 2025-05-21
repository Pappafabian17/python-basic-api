from fastapi import FastAPI
from routers.movie import routerMovie
from routers.user import routerUser
from fastapi.responses import HTMLResponse

app = FastAPI(
  title='MovApi',
  description='Una api de peliculas',
  version='0.0.1'
)

app.include_router(routerMovie)
app.include_router(routerUser)

@app.get('/',tags=['Inicio'])
def read_root():
  return HTMLResponse('<h2>Noticion de hola mundo</h2>')