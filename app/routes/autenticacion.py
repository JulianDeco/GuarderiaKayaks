from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPAuthorizationCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.models.models import Base, SessionLocal, UsuarioSistema, engine

from sqlalchemy.orm import Session

from typing import Annotated
import logging

from app.providers.consultas import UsuariosManager
from app.schemes.schemes import CrearUsuario
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

@router.post("/login")
async def login(credentials: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    consulta = UsuariosManager(db)
    token = consulta.autenticar_usuario(credentials.username, credentials.password)
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrecta",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return JSONResponse(content={"access_token": token, "token_type": "Bearer"}, status_code = 200)

@router.post("/register")
async def register(usuario: CrearUsuario, db: Session = Depends(get_db)):
    consulta = UsuariosManager(db)
    consulta.crear(usuario)
    return usuario


