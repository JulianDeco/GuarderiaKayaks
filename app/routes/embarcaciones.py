from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from typing import Optional

from app.schemes.schemes import Embarcacion
from app.providers.consultas import EmbarcacionesManager
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

router = APIRouter(prefix="/embarcaciones", tags=["Embarcaciones"])


@router.post("/")
async def cargar_embarcacion(embarcacion: Embarcacion, db: Session = Depends(get_db)):
    manager = EmbarcacionesManager(db, embarcacion)
    rta = manager.crear()
    return rta

@router.get("/")
async def listar_embarcacion(id: Optional[int] = None, db: Session = Depends(get_db)) -> JSONResponse:   
    if id:
        try:
            consulta = EmbarcacionesManager(db)
            consulta = consulta.obtener_uno(id)
            lista_embarcaciones = []
            if not consulta:
                return JSONResponse(content={"estado": "No existen registros"}, status_code=200)
            for embarcacion in consulta:
                lista_embarcaciones.append({
                    'id': embarcacion.id_embarcacion,
                    'modelo':embarcacion.modelo,
                    'color': embarcacion.color
                })
            return JSONResponse(content={"objeto": lista_embarcaciones})
        except Exception as error:
            return JSONResponse(content={"error": error.args}, status_code=404)
    consulta = EmbarcacionesManager(db)
    consulta = consulta.obtener_todos()
    return JSONResponse(content={"objeto": consulta})

@router.delete("/")
async def eliminar_embarcacion(id: int, db: Session = Depends(get_db)):
    return

@router.put("/")
async def modificar_embarcacion(id: int, db: Session = Depends(get_db)):
    return