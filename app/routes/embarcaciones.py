from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from typing import Optional

from app.schemes.schemes import Embarcacion, EmbarcacionModificacion
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

router = APIRouter(prefix="/embarcaciones", tags=["Embarcaciones"])


@router.post("/")
async def cargar_embarcacion(embarcacion: Embarcacion, db: Session = Depends(get_db)):
    manager = EmbarcacionesManager(db)
    rta = manager.crear(embarcacion)
    return rta

@router.get("/")
async def listar_embarcacion(id: Optional[str] = None, db: Session = Depends(get_db)) -> JSONResponse:   
    consulta = EmbarcacionesManager(db)
    if not id:
        try:
            consulta = consulta.obtener_todos()
            lista_embarcaciones = []
            if not consulta:
                return JSONResponse(content={"estado": "No existen registros"}, status_code=200)
            for embarcacion in consulta:
                lista_embarcaciones.append({
                    'id': embarcacion.id_embarcacion,
                    'modelo':embarcacion.modelo,
                    'marca':embarcacion.marca,
                    'fecha_ingreso': str(embarcacion.fecha_ingreso),
                    'fecha_baja': str(embarcacion.fecha_baja),
                    'percha' : embarcacion.percha,
                    'habilitado': embarcacion.habilitado,
                    'tipo_kayak': embarcacion.tipo_embarcacion.descripcion,
                    'color': embarcacion.color,
                    'cliente': {
                        "id": embarcacion.cliente.id_cliente,
                        "nombre": embarcacion.cliente.nombre,
                        "apellido": embarcacion.cliente.apellido,
                        "mail": embarcacion.cliente.mail,
                        "direccion": embarcacion.cliente.direccion,
                        "nro_documento": embarcacion.cliente.nro_documento,
                        "telefono": embarcacion.cliente.telefono,
                        
                    }
                })
            return JSONResponse(content={"resultado": lista_embarcaciones})
        except Exception as error:
            return JSONResponse(content={"error": error.args}, status_code=404)
    consulta = consulta.obtener_uno(id)
    return JSONResponse(content={"resultado": {
                    'id': consulta.id_embarcacion,
                    'modelo':consulta.modelo,
                    'marca':consulta.marca,
                    'fecha_ingreso': str(consulta.fecha_ingreso),
                    'fecha_baja': str(consulta.fecha_baja),
                    'percha' : consulta.percha,
                    'habilitado': consulta.habilitado,
                    'tipo_kayak': consulta.tipo_embarcacion.descripcion,
                    'color': consulta.color,
                    'cliente': {
                        "id": consulta.cliente.id_cliente,
                        "nombre": consulta.cliente.nombre,
                        "apellido": consulta.cliente.apellido,
                        "mail": consulta.cliente.mail,
                        "direccion": consulta.cliente.direccion,
                        "nro_documento": consulta.cliente.nro_documento,
                        "telefono": consulta.cliente.telefono,
                        
                    }
                }})

@router.delete("/")
async def eliminar_embarcacion(id: str, db: Session = Depends(get_db)):
    consulta_embarcacion = EmbarcacionesManager(db)
    consulta_embarcacion.eliminar(id)
    return JSONResponse(
        content={
            "detalle": "embarcacion eliminado"
        },
    status_code=200
    )

@router.put("/{id_embarcacion}")
async def modificar_embarcacion(id_embarcacion: str, embarcacion: EmbarcacionModificacion, db: Session = Depends(get_db)):
    embarcacion_db = EmbarcacionesManager(db)
    embarcacion_db = embarcacion_db.modificar(id_embarcacion, embarcacion)
    return {"message": "Embarcación actualizada", "embarcacion": {
                    'id': embarcacion_db.id_embarcacion,
                    'modelo':embarcacion_db.modelo,
                    'marca':embarcacion_db.marca,
                    'fecha_ingreso': str(embarcacion_db.fecha_ingreso),
                    'fecha_baja': str(embarcacion_db.fecha_baja),
                    'percha' :embarcacion_db.percha,
                    'habilitado': embarcacion_db.habilitado,
                    'tipo_kayak': embarcacion_db.tipo_embarcacion.descripcion,
                    'color': embarcacion_db.color,
                    'cliente': {
                        "id": embarcacion_db.cliente.id_cliente,
                        "nombre": embarcacion_db.cliente.nombre,
                        "apellido": embarcacion_db.cliente.apellido,
                        "mail":embarcacion_db.cliente.mail,
                        "direccion":embarcacion_db.cliente.direccion,
                        "nro_documento": embarcacion_db.cliente.nro_documento,
                        "telefono":embarcacion_db.cliente.telefono,
                        
                    }
                }}