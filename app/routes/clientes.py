from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.models.models import Base, SessionLocal, engine
from app.providers.consultas import ClientesManager
from app.schemes.schemes import Cliente, ClienteModificacion

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

@router.post("/", status_code=201)
async def cargar_cliente(ob_cliente: Cliente, db: Session = Depends(get_db)):
    consulta_cliente = ClientesManager(db)
    consulta_cliente.crear(ob_cliente)
    return JSONResponse(content={"estado":"cliente creado"}, status_code=201)

@router.get("/")
async def listar_clientes(id: Optional[str] = None, db: Session = Depends(get_db)):
    consulta_cliente = ClientesManager(db)
    if not id:
        res = consulta_cliente.obtener_todos()
        lista_res = []
        for res_cliente in res:
            lista_res.append({
                "id": res_cliente.id_cliente,
                "nombre": res_cliente.nombre,
                "apellido": res_cliente.apellido,
                "mail": res_cliente.mail,
                "direccion": res_cliente.direccion,
                "nro_documento": res_cliente.nro_documento,
                "tipo_documento": res_cliente.tipo_documento_rel.descripcion,
                "telefono": res_cliente.telefono,
                "habilitado":res_cliente.habilitado
            })
        return JSONResponse(
            content=lista_res ,
            status_code= 200
        )
    res_cliente = consulta_cliente.obtener_uno(id)
    return JSONResponse(
        content= {
                "id": res_cliente.id_cliente,
                "nombre": res_cliente.nombre,
                "apellido": res_cliente.apellido,
                "mail": res_cliente.mail,
                "direccion": res_cliente.direccion,
                "nro_documento": res_cliente.nro_documento,
                "tipo_documento": res_cliente.tipo_documento_rel.descripcion,
                "telefono": res_cliente.telefono,
                "habilitado":res_cliente.habilitado
            },
        status_code= 200
    )
    
@router.put('/{id_cliente}')
async def modifica_cliente(id_cliente: str, ob_cliente: ClienteModificacion = None, db: Session = Depends(get_db)):
    if not id_cliente:
        raise HTTPException(detail={"estado":"falta parámetro id"}, status_code=400)
    consulta_cliente = ClientesManager(db)
    res_modificacion = consulta_cliente.modificar( id_cliente, ob_cliente)
    return JSONResponse(content={"resultado":{
                                    "cliente": res_modificacion.id_cliente,
                                    "nombre": res_modificacion.nombre,
                                    "apellido": res_modificacion.apellido,
                                    "mail": res_modificacion.mail,
                                    "direccion": res_modificacion.direccion,
                                    "nro_documento": res_modificacion.nro_documento,
                                    "tipo_documento": res_modificacion.tipo_documento_rel.descripcion,
                                    "telefono": res_modificacion.telefono,
                                    "habilitado":res_modificacion.habilitado}}, status_code=200)

@router.delete("/")
async def baja_cliente(id_cliente: str, db: Session = Depends(get_db)):
    if not id_cliente:
        raise HTTPException(detail={"estado":"falta parámetro id"}, status_code=400)
    consulta_cliente = ClientesManager(db)
    consulta_cliente.eliminar(id_cliente)
    return JSONResponse(
        content= {
                "detalle": "cliente eliminado"
            },
        status_code= 200
    )