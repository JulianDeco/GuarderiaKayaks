from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from typing import Optional

from app.schemes.schemes import Embarcacion, Pagos  
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
async def cargar_embarcacion(embarcacion: Embarcacion, db: Session = Depends(get_db)):
    manager = PagosManager(db)
    rta = manager.crear()
    return rta
