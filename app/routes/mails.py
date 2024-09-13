from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.models.models import Base, SessionLocal, engine
from app.providers.consultas import MailsManager

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

@router.get("/")
async def obtener_mails(db: Session = Depends(get_db)):
    try:
        consulta_mails = MailsManager(db)
        lista_mails = []
        for mail in consulta_mails.obtener_todos():
            lista_mails.append({
                'id_mail': str(mail.id_mail),
                'mensaje': mail.mensaje,
                'titulo': mail.titulo,
                'id_receptor': str(mail.receptor_cliente),
                'mail_receptor': str(mail.receptor_mail),
                'fecha_creacion':str(mail.fecha_creacion)
            })
        logger.info(lista_mails)
    except Exception as error:
        logger.exception("Error inesperado")
        raise HTTPException(detail={"estado": "error durante consulta"}, status_code=500)
    
    return JSONResponse(content={"resultado": lista_mails})