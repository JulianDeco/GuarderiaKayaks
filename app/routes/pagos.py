from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from typing import Optional

from app.schemes.schemes import Embarcacion, Pago, PagoRealizado
from app.providers.consultas import EmbarcacionesManager, PagosManager
from app.models.models import Base, SessionLocal, engine

from sqlalchemy.orm import Session

import json

import logging
logger = logging.getLogger(f'{__name__}')

try:
    Base.metadata.create_all(bind=engine)
except Exception as err:
    logger.error(err)
    
def get_db():
    
    try:
        db = SessionLocal()
        yield db
    except Exception as error:
        logger.error(error)
    finally: 
        db.close()

router = APIRouter(prefix="/pagos", tags=["Pagos"])


@router.post("/")
async def crear_pagos(pagos: Pago, db: Session = Depends(get_db)):
    manager = PagosManager(db)
    rta = manager.crear(pagos)
    return rta

@router.get("/")
async def listar_pagos(id: Optional[str] = None, db: Session = Depends(get_db)) -> JSONResponse:   
    consulta = PagosManager(db)
    if not id:
        try:
            consulta = consulta.obtener_todos()
            lista_pagos = []
            if not consulta:
                return JSONResponse(content={"estado": "No existen registros"}, status_code=200)
            for pago in consulta:
                lista_pagos.append({
                    'id': pago.id_pago,
                    'monto': float(pago.monto),
                    'fecha': str(pago.fecha_pago),
                    'cliente': {
                        "id": pago.cliente.id_cliente,
                        "nombre": pago.cliente.nombre,
                        "apellido": pago.cliente.apellido,
                        "mail": pago.cliente.mail,
                        "direccion": pago.cliente.direccion,
                        "nro_documento": pago.cliente.nro_documento,
                        "telefono": pago.cliente.telefono,
                        
                    }
                })
            return JSONResponse(content={"resultado": lista_pagos})
        except Exception as error:
            logger.exception(error)
            return JSONResponse(content={"error": error.args}, status_code=404)
    consulta = consulta.obtener_uno(id)
    return JSONResponse(content={"resultado": {
                    'id': consulta.id_pago,
                    'monto': float(consulta.monto),
                    'fecha': str(consulta.fecha_pago),
                    'cliente': {
                        "id": consulta.cliente.id_cliente,
                        "nombre": consulta.cliente.nombre,
                        "apellido": consulta.cliente.apellido,
                        "mail": consulta.cliente.mail,
                        "direccion": consulta.cliente.direccion,
                        "nro_documento": consulta.cliente.nro_documento,
                        "telefono": consulta.cliente.telefono,
                        
                    }
                }})

@router.put("/{id_pago}")
async def pago_realizado(id_pago: str, body: PagoRealizado, db: Session = Depends(get_db)) -> JSONResponse:
    pago = PagosManager(db)
    pago = pago.modificar(id_pago)
    return JSONResponse(content={"estado":pago})