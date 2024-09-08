from fastapi import FastAPI, Request, Depends, Response, BackgroundTasks
from starlette.background import BackgroundTask
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi_utils.tasks import repeat_every

from app.middlewares.middleware import RateLimitingMiddleware
from app.providers.aviso_mail import envio_mail
from app.providers.consultas import PagosManager
from app.routes.autenticacion import router as autenticacion
from app.routes.embarcaciones import router as embarcaciones
from app.routes.clientes import router as clientes
from app.routes.pagos import router as pagos

from app.models.models import Base, Pagos, SessionLocal, engine

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
    },
    {
        "name": "Mails",
        "description": "Endpoints relacionados a los mails." 
    }
]

security = JWTBearer()

app = FastAPI(title = titulo, 
              description=descripcion , 
              openapi_tags=tags_metadata,
              )

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

responses = {
    403: {
        "description": "Not authenticated",
        "content": {
            "application/json": {
                "examples": {
                    "default": {"summary": "Default", "value": {"detail": "Not authenticated"}},
                    "invalid_token": {"summary": "Invalid or expired token", "value": {"detail": "Invalid token or expired token."}},
                    "invalid_scheme": {"summary": "Invalid authentication scheme", "value": {"detail": "Invalid authentication scheme."}},
                }
            }
        }
    }
}

app.include_router(autenticacion, prefix="/v1", responses= responses)
app.include_router(embarcaciones, dependencies= [Depends(security)], prefix="/v1", responses= responses)
app.include_router(clientes, dependencies= [Depends(security)], prefix="/v1", responses= responses)
app.include_router(pagos, dependencies= [Depends(security)], prefix="/v1", responses= responses)


@app.on_event("startup")
@repeat_every(seconds=60, raise_exceptions = True)  # 24 horas
def background_tasks() -> None:
    try:
        instancia_db = next(get_db())
        pagos = PagosManager(instancia_db)
        lista_pagos_vencidos = pagos.obtener_vencidos()
        logger.info(lista_pagos_vencidos)
        
        if lista_pagos_vencidos:
            for pago_vencido in lista_pagos_vencidos:
                try:
                    envio_mail( 
                        [pago_vencido.cliente.mail], 
                        "Aviso pago", 
                        f"{pago_vencido.cliente.nombre} {pago_vencido.cliente.apellido}", 
                        pago_vencido.fecha_pago
                    )
                    logger.info(f"Correo enviado para el pago {pago_vencido.id_pago}")
                    
                    # Modificar el estado de aviso_mail a 1
                    pagos.modificar(pago_vencido.id_pago, 1)
                    logger.info('FIN BUCLE')
                except Exception as e:
                    logger.error(f"Error enviando mail o modificando el pago {pago_vencido.id_pago}: {e}")
    except Exception as error:
        logger.error(f"Error en la tarea de background: {error}")