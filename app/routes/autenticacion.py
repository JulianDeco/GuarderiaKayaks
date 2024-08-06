from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPAuthorizationCredentials

from app.models.models import Base, SessionLocal, engine

from sqlalchemy.orm import Session

from typing import Annotated
import logging

from app.security.handler_jwt import signJWT

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

router = APIRouter(prefix="/auth", tags=["Autenticación"])

security = HTTPBasic()

@router.post("/login")
async def login(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    signJWT(2, 'admin')
    return signJWT(2, 'admin')


# @router.post("/register")
# async def register():
#     return

