from fastapi import FastAPI, Request, Depends, Response
from starlette.background import BackgroundTask
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes.autenticacion import router as autenticacion
from app.routes.embarcaciones import router as embarcaciones
from app.routes.clientes import router as clientes

from app.models.models import Base, SessionLocal, engine

from app.security.config_jwt import JWTBearer

from app.custom_logging import CustomizeLogger

from sqlalchemy.orm import Session

import logging
from pathlib import Path
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
    }
]

security = JWTBearer()

app = FastAPI(title = titulo, 
              description=descripcion , 
              openapi_tags=tags_metadata)

logger = logging.getLogger(f'{__name__}')

config_path=Path(__file__).with_name("logging_config.json")
logger = CustomizeLogger.make_logger(config_path)
print(config_path)

def log_info(req_body, res_body):
    logging.info(req_body)
    logging.info(res_body)

@app.middleware('http')
async def some_middleware(request: Request, call_next):
    req_body = await request.body()
    response = await call_next(request)
    logging.info(request.headers)
    res_body = b''
    async for chunk in response.body_iterator:
        res_body += chunk
    
    task = BackgroundTask(log_info, req_body, res_body)
    return Response(content=res_body, status_code=response.status_code, 
        headers=dict(response.headers), media_type=response.media_type, background=task)


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