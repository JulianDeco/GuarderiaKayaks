from multimethod import multimethod
import os
from abc import ABC, abstractmethod
import datetime
import secrets
from typing import Optional
from fastapi import HTTPException
from sqlalchemy import extract

from passlib.context import CryptContext

from app.models.models import Embarcaciones, Mails, Pagos, Clientes, Parametros, Usuario_Token, UsuarioSistema
from app.schemes.schemes import Cliente, CrearUsuario, Embarcacion, Pago, ClienteModificacion

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
            embarcacion.percha = None
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
    def crear(self, mensaje, titulo, receptor_cliente, receptor_mail):
        nuevo_mail = Mails(
            mensaje = mensaje,
            titulo = titulo,
            receptor_cliente = receptor_cliente,
            receptor_mail = receptor_mail
        )
        self.instancia_db.add(nuevo_mail)
        self.commit()
        pass 

    def eliminar(self, id_mail):
        pass  

    def modificar(self, id_mail, mail: Mails):
        pass 

    def obtener_uno(self, id_mail):
        return self.instancia_db.query(Mails).filter(Mails.id == id_mail).first()

    def obtener_todos(self):
        return self.instancia_db.query(Mails).all()

class PagosManager(ManagerGral):
    def crear(self, pago: Pago):
        self.instancia_db.add(Pagos(monto = pago.monto, id_cliente = pago.id_cliente))
        self.commit()
        pass

    def eliminar(self, id_pago):
        pass  # Implementar según sea necesario

    def modificar(self, id_pago, aviso_mail: bool):
        pago = self.obtener_uno(id_pago)
        if pago:
            pago.aviso_mail = aviso_mail
            self.commit()
        else:
            raise HTTPException(status_code=404, detail="Pago no encontrado")

    def realizar_pago(self, id_pago, fecha_pago_realizado):
        pago = self.obtener_uno(id_pago)
        if pago:
            pago.fecha_pago_realizado = fecha_pago_realizado
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

    def obtener_uno(self):
        pass
    
    def obtener_todos(self):
        pass

    @multimethod
    def obtener(self, id_cliente: str):
            return self.instancia_db.query(Clientes).filter(Clientes.id_cliente == id_cliente).first()

    @multimethod
    def obtener(self):
            return self.instancia_db.query(Clientes).all()

class UsuariosManager(ManagerGral):
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def verificar_contraseña(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)


    def obtener_hash_contraseña(self, password):
        return self.pwd_context.hash(password)
    
    def autenticar_usuario(self, mail: str, password: str):
        user = self.obtener_uno(mail)
        print(user)
        if not user:
            return False
        if not self.verificar_contraseña(password, user.contraseña):
            return False
        
        token = secrets.token_hex(16)
        token_usuario = Usuario_Token(mail =user.mail, token = token, expira_en = str(datetime.datetime.now() + datetime.timedelta(minutes=30)))        
        self.instancia_db.add(token_usuario)
        self.instancia_db.commit()

        return token
    
    def crear(self, objeto: CrearUsuario):
        
        objeto.contraseña = self.pwd_context.hash(objeto.contraseña)
        
        nuevo_usuario = UsuarioSistema(
            nombre = objeto.nombre,
            apellido = objeto.apellido,
            rol = objeto.rol,
            mail = objeto.mail,
            contraseña = objeto.contraseña,
            tipo_documento_id = objeto.tipo_documento_id,
            nro_documento = objeto.nro_documento
            )
        self.instancia_db.add(nuevo_usuario)
        self.commit()
        return
    
    def eliminar(self):
        pass
    
    def modificar(self):
        pass
    
    def obtener_uno(self, mail):
        return self.instancia_db.query(UsuarioSistema).filter(UsuarioSistema.mail == mail).first()
    
    
    def obtener_todos(self):
        pass

class ParametrosManager(ManagerGral):
    def crear(self):
        pass 

    def eliminar(self, id_parametro):
        pass  

    def modificar(self, id_parametro, obj_parametro):
        parametro_actual = self.obtener_uno(id_parametro)
        if parametro_actual:
            for key, value in obj_parametro.dict(exclude_unset=True).items():
                setattr(parametro_actual, key, value)
            self.commit()
            self.instancia_db.refresh(parametro_actual)
            return parametro_actual
        raise HTTPException(status_code=404, detail="Parametro no encontrado")
        pass 

    def obtener_uno(self, id_parametro):
        return self.instancia_db.query(Parametros).filter(Parametros.id == id_parametro).first()

    def obtener_todos(self):
        return self.instancia_db.query(Parametros).all()