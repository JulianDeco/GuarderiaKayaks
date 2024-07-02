from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes.autenticacion import router as autenticacion
from app.routes.embarcaciones import router as embarcaciones
from app.routes.clientes import router as clientes

from app.models.models import Base, SessionLocal, engine

from app.security.config_jwt import JWTBearer

from sqlalchemy.orm import Session

#127.0.0.1/docs

titulo = "Refugio del Remo"
descripcion =   "Sistema para carga de clientes y kayaks de clientes, además de login de los operarios del sistema con autenticación JWT"
tags_metadata = [
    {
        "name": "Embarcaciones",
        "description": "Endpoints relacionados a embarcaciones.",
    },
    {
        "name": "Clientes",
        "description": "Endpoints relacionados a clientes.",
    },
    {
        "name": "Autenticación",
        "description": "Endpoints relacionados a la autenticación y seguridad del sistema." 
    },
    {
        "name": "Pagos",
        "description": "Endpoints relacionados a los pagos." 
    },
    {
        "name": "Endpoints Billetera",
        "description": "Endpoints a consumir de billetera.",
        "externalDocs": {
            "description" : "Endpoints",
            "url": " https://{URL_BASE}/AvisoMovimientoEnEntidad.com"
        },
    },    
]

security = JWTBearer()

app = FastAPI(title = titulo, 
              description=descripcion , 
              openapi_tags=tags_metadata)



try:
    Base.metadata.create_all(bind=engine)
except Exception as err:
    print(err.args)
    
def get_db():
    
    try:
        db = SessionLocal()
        yield db
    except Exception as error:
        print(error.args)
    finally: 
        db.close()

@app.get("/ping")
async def pong():
    return {"estado":"pong"}


app.include_router(autenticacion)
app.include_router(embarcaciones, dependencies= [Depends(security)])
app.include_router(clientes, dependencies= [Depends(security)])