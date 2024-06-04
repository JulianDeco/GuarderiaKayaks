from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from typing import Optional

from app.models.models_swagger import Embarcacion
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

router = APIRouter(prefix="/kayaks")


@router.post("/")
async def cargar_kayak(embarcacion: Embarcacion, db: Session = Depends(get_db)):
    manager = EmbarcacionesManager(db, embarcacion)
    rta = manager.crear()
    return rta

@router.get("/")
async def listar_kayak(id: Optional[int] = None, db: Session = Depends(get_db)) -> JSONResponse:   
    if id:
        return
    return

@router.delete("/")
async def eliminar_kayak(id: int, db: Session = Depends(get_db)):
    return

@router.put("/")
async def modificar_kayak(id: int, db: Session = Depends(get_db)):
    return