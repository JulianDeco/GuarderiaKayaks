from abc import ABC, abstractmethod
import datetime
from typing import Optional
from fastapi import HTTPException
from sqlalchemy import extract

from app.models.models import Embarcaciones, Mails, Pagos, Clientes
from app.schemes.schemes import Cliente, Embarcacion, Pago, ClienteModificacion

class ManagerGral(ABC):
    """Gestión general para todas las entidades"""

    def __init__(self, instancia_db):
        self.instancia_db = instancia_db
    
    @abstractmethod
    def crear(self):
        pass
    
    @abstractmethod
    def eliminar(self, id):
        pass
    
    @abstractmethod
    def modificar(self, id, obj):
        pass
    
    @abstractmethod
    def obtener_uno(self, id):
        pass
    
    @abstractmethod
    def obtener_todos(self):
        pass
    
    def commit(self):
        """Realizar commit de la sesión"""
        try:
            self.instancia_db.commit()
        except Exception as e:
            self.instancia_db.rollback()
            raise HTTPException(status_code=500, detail=f"Error al guardar cambios: {e}")

class EmbarcacionesManager(ManagerGral):
    
    def crear(self, embarcacion: Embarcacion):
        nueva_embarcacion = Embarcaciones(
            tipo_id=embarcacion.tipo_id,
            marca=embarcacion.marca,
            modelo=embarcacion.modelo,
            color=embarcacion.color,
            percha=embarcacion.percha,
            id_cliente=embarcacion.id_cliente
        )
        self.instancia_db.add(nueva_embarcacion)
        self.commit()
    
    def eliminar(self, id_embarcacion):
        embarcacion = self.obtener_uno(id_embarcacion)
        if embarcacion:
            embarcacion.fecha_baja = datetime.datetime.now()
            embarcacion.habilitado = 0
            self.commit()
        else:
            raise HTTPException(status_code=404, detail="Embarcación no encontrada")

    def modificar(self, id_embarcacion, embarcacion: Embarcacion):
        objeto_actual = self.obtener_uno(id_embarcacion)
        if objeto_actual:
            for key, value in embarcacion.dict(exclude_unset=True).items():
                setattr(objeto_actual, key, value)
            self.commit()
            self.instancia_db.refresh(objeto_actual)
            return objeto_actual
        raise HTTPException(status_code=404, detail="Embarcación no encontrada")

    def obtener_uno(self, id_embarcacion):
        return self.instancia_db.query(Embarcaciones).filter(Embarcaciones.id_embarcacion == id_embarcacion).first()

    def obtener_todos(self):
        return self.instancia_db.query(Embarcaciones).all()

class MailsManager(ManagerGral):
    def crear(self):
        pass  # Implementar según sea necesario

    def eliminar(self, id_mail):
        pass  # Implementar según sea necesario

    def modificar(self, id_mail, mail: Mails):
        pass  # Implementar según sea necesario

    def obtener_uno(self, id_mail):
        return self.instancia_db.query(Mails).filter(Mails.id == id_mail).first()

    def obtener_todos(self):
        return self.instancia_db.query(Mails).all()

class PagosManager(ManagerGral):
    def crear(self, pago: Pago):
        nuevo_pago = Pagos(
            monto=pago.monto,
            id_cliente=pago.id_cliente
        )
        self.instancia_db.add(nuevo_pago)
        self.commit()

    def eliminar(self, id_pago):
        pass  # Implementar según sea necesario

    def modificar(self, id_pago, aviso_mail: bool):
        pago = self.obtener_uno(id_pago)
        if pago:
            pago.aviso_mail = aviso_mail
            self.commit()
        else:
            raise HTTPException(status_code=404, detail="Pago no encontrado")

    def obtener_uno(self, id_pago):
        return self.instancia_db.query(Pagos).filter(Pagos.id_pago == id_pago).first()

    def obtener_todos(self):
        return self.instancia_db.query(Pagos).all()

    def obtener_pagos_mes(self):
        mes_actual = datetime.datetime.now().month
        año_actual = datetime.datetime.now().year

        # Realizar la consulta con SQLAlchemy usando extract
        return (
            self.instancia_db.query(Pagos.id_cliente)
            .filter(extract('month', Pagos.fecha_pago) == mes_actual)
            .filter(extract('year', Pagos.fecha_pago) == año_actual)
            .all()
        )

    def obtener_vencidos(self):
        return (
            self.instancia_db.query(Pagos)
            .filter(
                Pagos.fecha_pago <= datetime.datetime.now(),
                Pagos.fecha_pago_realizado.is_(None),
                Pagos.aviso_mail != 1
            )
            .all()
        )

class ClientesManager(ManagerGral):
    def crear(self, cliente: Cliente):
        nuevo_cliente = Clientes(
            nombre=cliente.nombre,
            apellido=cliente.apellido,
            mail=cliente.mail,
            direccion=cliente.direccion,
            tipo_documento_id=cliente.tipo_documento_id,
            nro_documento=cliente.nro_documento,
            telefono=cliente.telefono
        )
        self.instancia_db.add(nuevo_cliente)
        self.commit()

    def eliminar(self, id_cliente):
        cliente = self.obtener_uno(id_cliente)
        if cliente:
            cliente.habilitado = 0
            cliente.fecha_baja = datetime.datetime.now()
            self.commit()
        else:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

    def modificar(self, id_cliente, cliente: ClienteModificacion):
        cliente_actual = self.obtener_uno(id_cliente)
        if cliente_actual:
            for key, value in cliente.dict(exclude_unset=True).items():
                setattr(cliente_actual, key, value)
            self.commit()
            self.instancia_db.refresh(cliente_actual)
            return cliente_actual
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    def obtener_uno(self, id_cliente):
        return self.instancia_db.query(Clientes).filter(Clientes.id_cliente == id_cliente).first()

    def obtener_todos(self):
        return self.instancia_db.query(Clientes).all()