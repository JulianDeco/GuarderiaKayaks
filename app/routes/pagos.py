from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from typing import Optional

from app.schemes.schemes import Embarcacion, Pago
from app.providers.consultas import EmbarcacionesManager, PagosManager
from app.models.models import Base, SessionLocal, engine

from sqlalchemy.orm import Session

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
async def listar_pagos(id: Optional[int] = None, db: Session = Depends(get_db)) -> JSONResponse:   
    consulta = PagosManager(db)
    if id:
        try:
            consulta = consulta.obtener_todos()
            lista_pagos = []
            if not consulta:
                return JSONResponse(content={"estado": "No existen registros"}, status_code=200)
            for pago in consulta:
                lista_pagos.append({
                    'id': pago.id_pago,
                    'monto': pago.monto,
                    'cliente': pago.cliente
                })
            return JSONResponse(content={"resultado": lista_pagos})
        except Exception as error:
            return JSONResponse(content={"error": error.args}, status_code=404)
    consulta = consulta.obtener_uno(id)
    return JSONResponse(content={"resultado": consulta})
