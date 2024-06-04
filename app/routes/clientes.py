from fastapi import APIRouter, Depends

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

router = APIRouter(prefix="/clientes")


@router.post("/nuevo")
async def cargar_cliente():
    return

@router.get("/listar")
async def listar_clientes():
    return