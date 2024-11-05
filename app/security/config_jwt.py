import datetime
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from typing import Dict, Optional
from sqlalchemy import Engine
from typing_extensions import Annotated, Doc

from app.models.models import Base, SessionLocal, Usuario_Token, UsuarioSistema
from app.security.handler_jwt import decodeJWT


try:
    Base.metadata.create_all(bind=Engine)
except Exception as err:
    print(err.args)
    
def get_db():
    
    try:
        db = SessionLocal()
        yield db
    except Exception as error:
        print(error.args)
    finally: 
        db.close()

ROLES_PERMITIDOS = ['ADMIN']
class TokenBearer(HTTPBearer):
    def __init__(self, description: Annotated[
            Optional[str],
            Doc(
                """
                Security scheme description.

                HTTPBearer (_type_): token obtenido luego de la autenticación
                """
            ),
        ] = None,auto_error: bool = True):
        super(TokenBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(TokenBearer, self).__call__(request)
        metodo_http = request.method
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if len(credentials.credentials) <= 32:
                if not self.verificar_token(credentials.credentials, metodo_http):
                    raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            else:
                if not self.verify_jwt(credentials.credentials, metodo_http):
                    raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str, metodo_http) -> bool:
        isTokenValid: bool = False

        payload = decodeJWT(jwtoken)
        rol_user = payload.get("rol")
        if rol_user.upper() not in ROLES_PERMITIDOS and metodo_http != 'GET':
            raise HTTPException(status_code=401, detail="Usuario no autorizado.")
        payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
    
    def verificar_token(self, token, metodo_http):
        session_bbdd = next(get_db())
        resultado = session_bbdd.query(Usuario_Token).filter(Usuario_Token.token == token,
                                                 Usuario_Token.expira_en >= str(datetime.datetime.now())).first()
        if not resultado:
            False
        resultado_usuario = session_bbdd.query(UsuarioSistema).filter(UsuarioSistema.mail == resultado.mail).first()
        if resultado_usuario.rol_rel.descripcion.upper() not in ROLES_PERMITIDOS and metodo_http != 'GET':
            raise HTTPException(status_code=401, detail="Usuario no autorizado.")
        return resultado