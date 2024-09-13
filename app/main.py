from datetime import datetime
from fastapi import FastAPI, HTTPException, Request, Depends, Response, BackgroundTasks
from sqlalchemy import and_, extract, not_
from starlette.background import BackgroundTask
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi_utils.tasks import repeat_every

from app.middlewares.middleware import RateLimitingMiddleware

from app.providers.aviso_mail import envio_mail

from app.providers.consultas import PagosManager, ParametrosManager, MailsManager

from app.routes.autenticacion import router as autenticacion_router
from app.routes.embarcaciones import router as embarcaciones_router
from app.routes.clientes import router as clientes_router
from app.routes.pagos import router as pagos_router
from app.routes.mails import router as mails_router
from app.routes.parametros import router as parametros_router

from app.models.models import Base, Clientes, Embarcaciones, Pagos, SessionLocal, engine

from app.schemes.schemes import Pago
from app.security.config_jwt import JWTBearer

from app.custom_logging import CustomizeLogger

from sqlalchemy.orm import Session, joinedload

import logging
from pathlib import Path
#127.0.0.1/docs

titulo = "Refugio del Remo"
descripcion =   "Sistema para carga de clientes y kayaks de clientes, además de login de los operarios del sistema con autenticación JWT"
tags_metadata = [
    {
        "name": "Clientes",
        "description": "Endpoints relacionados a clientes.",
    },
    {
        "name": "Embarcaciones",
        "description": "Endpoints relacionados a embarcaciones.",
    },
    {
        "name": "Pagos",
        "description": "Endpoints relacionados a los pagos." 
    },
    {
        "name": "Mails",
        "description": "Endpoints relacionados a los mails." 
    },
    {
        "name": "Parametros",
        "description": "Endpoints relacionados a obtención y modificación de parámetros." 
    },
    {
        "name": "Autenticación",
        "description": "Endpoints relacionados a la autenticación y seguridad del sistema." 
    },
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

app.include_router(autenticacion_router, prefix="/v1", responses= responses)
app.include_router(embarcaciones_router, dependencies= [Depends(security)], prefix="/v1", responses= responses)
app.include_router(clientes_router, dependencies= [Depends(security)], prefix="/v1", responses= responses)
app.include_router(pagos_router, dependencies= [Depends(security)], prefix="/v1", responses= responses)
app.include_router(mails_router, dependencies= [Depends(security)], prefix="/v1", responses= responses)
app.include_router(parametros_router, dependencies= [Depends(security)], prefix="/v1", responses= responses)


def envio_mails_pagos_vencidos(instancia_db):
    pagos = PagosManager(instancia_db)
    mails = MailsManager(instancia_db)
    
    lista_pagos_vencidos = pagos.obtener_vencidos()
    logger.info(lista_pagos_vencidos)
        
    if lista_pagos_vencidos:
        for pago_vencido in lista_pagos_vencidos:
            envio_mail( 
                    [pago_vencido.cliente.mail], 
                    "Aviso pago", 
                    f"{pago_vencido.cliente.nombre} {pago_vencido.cliente.apellido}", 
                    pago_vencido.fecha_pago
            )
            logger.info(f"Correo enviado para el pago {pago_vencido.id_pago}")
                    
            pagos.modificar(pago_vencido.id_pago, 1)
            
            mails.crear('Aviso Pago', 'Aviso Pago', pago_vencido.cliente.id_cliente, pago_vencido.cliente.mail)
            logger.info('FIN BUCLE')
            
def creacion_pago(instancia_db):
    mes_actual = datetime.now().month
    año_actual = datetime.now().year
    
    pagos = PagosManager(instancia_db)
    consulta_pagos_mes = pagos.obtener_pagos_mes()
    lista_pagos_mes = []
    if consulta_pagos_mes:
        lista_pagos_mes = [pago[0] for pago in consulta_pagos_mes]
    consulta_cliente = (
    instancia_db.query(Clientes)
    .options(joinedload(Clientes.embarcaciones))
    .filter(extract('month', Clientes.fecha_alta_cliente) == mes_actual)
    .filter(extract('year', Clientes.fecha_alta_cliente) == año_actual)
    .filter(
        and_(        
            not_(Clientes.id_cliente.in_(lista_pagos_mes)),            
            Embarcaciones.habilitado == 1,                       
            Embarcaciones.percha.isnot(None)                     
        )
    )
    .join(Embarcaciones)  
    .all()
    )
    logger.info(consulta_cliente)
    if not consulta_cliente:
        return
    consulta_parametros = ParametrosManager(instancia_db)
    precio_cuota = float(consulta_parametros.obtener_uno(2).descripcion)
    for cliente in consulta_cliente:
        logger.info(cliente.__dict__)
        acum_cuota = 0
        for embarcacion in cliente.embarcaciones:
            if embarcacion.tipo_embarcacion.descripcion == 'DOBLE':
                acum_cuota += (precio_cuota * 1.15)
            else:
                acum_cuota += precio_cuota
        pagos.crear(Pago(monto=acum_cuota, id_cliente=cliente.id_cliente))

@app.exception_handler(500)
async def HTTPException_exception_handler(request: Request, exc: HTTPException):
    logger.info(exc.args)
    return JSONResponse(content={"estado":"error durante consulta a bbdd"}, status_code=500)

@app.on_event("startup")
@repeat_every(seconds=60, raise_exceptions = True)  # 24 horas
def background_tasks() -> None:
    try:
        instancia_db = next(get_db())
        creacion_pago(instancia_db)
        envio_mails_pagos_vencidos(instancia_db)
    except Exception as error:
        logger.exception(f"Error en la tarea de background: {error}")