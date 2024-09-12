from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.models.models import Base, SessionLocal, engine
from app.providers.consultas import ParametrosManager

from sqlalchemy.orm import Session

import logging

from app.schemes.schemes import ParametroModificacion
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

router = APIRouter(prefix="/parametros", tags=["Parametros"])

@router.get("/")
async def obtener_parametros(db: Session = Depends(get_db)):
    consulta_parametros = ParametrosManager(db)
    consulta_parametros = consulta_parametros.obtener_todos()
    lista_parametros = []
    for params in consulta_parametros:
        lista_parametros.append({
            'id': params.id,
            'descripcion': params.descripcion
        })
    return JSONResponse(content={'parametros': lista_parametros})

@router.put("/{id_parametro}")
async def modificar_parametros(id_parametro: int, parametro: ParametroModificacion, db: Session = Depends(get_db)):
    if not id_parametro:
        raise HTTPException(detail={"estado":"falta parámetro id"}, status_code=400)
    consulta_parametros = ParametrosManager(db)
    resultado = consulta_parametros.modificar(id_parametro, parametro)
    return JSONResponse(content={'resultado': {
        'id': resultado.id,
        'descripcion': resultado.descripcion
    }})