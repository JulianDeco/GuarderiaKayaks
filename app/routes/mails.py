from typing import Optional
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.models.models import Base, SessionLocal, engine
from app.providers.consultas import MailsManager
from app.schemes.schemes import Mail

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

router = APIRouter(prefix="/mails", tags=["Mails"])

@router.post("/", status_code=201)
async def cargar_cliente(ob_mail: Mail, db: Session = Depends(get_db)):
    consulta_mail = MailsManager(db)
    consulta_mail.crear(ob_mail)
    
    return JSONResponse(content={"estado":"mail enviado"}, status_code=201, background=None)
