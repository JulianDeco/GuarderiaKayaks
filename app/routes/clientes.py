from typing import Optional
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.models.models import Base, SessionLocal, engine
from app.providers.consultas import ClientesManager
from app.schemes.schemes import Cliente

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

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("/nuevo", status_code=201)
async def cargar_cliente(ob_cliente: Cliente, db: Session = Depends(get_db)):
    consulta_cliente = ClientesManager(db)
    consulta_cliente.crear(ob_cliente)
    return

@router.get("/listar")
async def listar_clientes(id: Optional[int], db: Session = Depends(get_db)):
    consulta_cliente = ClientesManager(db)
    if not id:
        res = consulta_cliente.obtener_todos()
        lista_res = []
        for res_cliente in res:
            lista_res.append({
                "id": res_cliente.id,
                "nombre": res_cliente.nombre,
                "apellido": res_cliente.apellido,
                "mail": res_cliente.mail,
                "direccion": res_cliente.direccion,
                "nro_documento": res_cliente.nro_documento,
                "telefono": res_cliente.telefono
            })
        return JSONResponse(
            content=lista_res,
            status_code= 200
        )
    res_cliente = consulta_cliente.obtener_uno()
    return JSONResponse(
        content= {
                "id": res_cliente.id,
                "nombre": res_cliente.nombre,
                "apellido": res_cliente.apellido,
                "mail": res_cliente.mail,
                "direccion": res_cliente.direccion,
                "nro_documento": res_cliente.nro_documento,
                "telefono": res_cliente.telefono
            },
        status_code= 200
    )