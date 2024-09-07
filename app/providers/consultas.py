from abc import ABC, abstractmethod
import datetime
from typing import Optional

from fastapi import HTTPException


from app.models.models import Embarcaciones, Mails, Pagos, Clientes
from app.schemes.schemes import Cliente, Embarcacion, Pago, ClienteModificacion


class ManagerGral(ABC):
    """
    AAAAAA te asesino amigo
    """
    def __init__(self, instancia_db):
        self.instancia_db = instancia_db
    
    @abstractmethod    
    def crear(self):
        """Crear un objeto"""
        pass
    
    @abstractmethod 
    def eliminar(self):
        """Eliminar un objeto"""
        pass
    
    @abstractmethod 
    def modificar(self):
        """Modificar un objeto"""
        pass
    
    @abstractmethod 
    def obtener_uno(self, id):
        """Obtener un objeto por su ID"""
        pass
    
    @abstractmethod 
    def obtener_todos(self):
        """Obtener todos los objetos"""
        pass


class EmbarcacionesManager(ManagerGral):
    def __init__(self, instancia_db):
        super().__init__(instancia_db)
        self.tipo = Embarcaciones
    
    def crear(self, embarcacion: Embarcacion):
        """Crear una embarcación"""
        crear_embarcacion = Embarcaciones(
            tipo_id = embarcacion.tipo_id,
            marca = embarcacion.marca,
            modelo = embarcacion.modelo,
            color = embarcacion.color,
            percha = embarcacion.percha,
            id_cliente = embarcacion.id_cliente
        )
        self.instancia_db.add(crear_embarcacion)
        self.instancia_db.commit()
        pass
    
    def eliminar(self, embarcion_id):
        busqueda_embarcacion = self.obtener_uno(embarcion_id)
        if busqueda_embarcacion:
            busqueda_embarcacion.fecha_baja = datetime.datetime.now()
            busqueda_embarcacion.habilitado = 0
            self.instancia_db.commit()
            return
        raise HTTPException(content={"detalle":"embarcacion no encontrado"}, status_code=404)
        
    
    def modificar(self, objeto):
        
        """Modificar una embarcación"""
        modificar_embarcacion = self.instancia_db.query(self.tipo).filter(self.tipo.id_embarcacion == id).update(
            {
                self.tipo.marca: objeto.marca,
                self.tipo.modelo: objeto.modelo,
                self.tipo.color: objeto.color,
                self.tipo.percha: objeto.percha,
                self.tipo.id_cliente: objeto.id_cliente
            }
        )
        self.instancia_db.commit()
        return modificar_embarcacion
    
    def obtener_uno(self, id=int):
        """Obtener una embarcación por su ID"""
        return self.instancia_db.query(self.tipo).filter(self.tipo.id_embarcacion== id).first()
    
    def obtener_todos(self):
        """Obtener todas las embarcaciones"""
        return self.instancia_db.query(self.tipo).all()
    
class MailsManager(ManagerGral):
    def __init__(self, instancia_db):
        super().__init__(instancia_db)
        self.instancia_db = instancia_db
        self.mail =  Mails

    def crear(self):
        
        return
    
    def obtener_uno(self, id = int):
        return self.instancia_db.query(self.mail).filter(self.mail.id_pago == id).first()
    
    def obtener_todos(self):
        return self.instancia_db.query(self.mail).all()
    
    def enviar_mail(self):
        pass
    
    
class PagosManager(ManagerGral):
    def __init__(self, instancia_db):
        super().__init__(instancia_db)
        self.instancia_db = instancia_db
        self.pagos = Pagos
        
    def crear(self, pagos: Pago):
        nuego_pago = Pagos(
            monto = pagos.monto,
            id_cliente = pagos.id_cliente
        )
        self.instancia_db.add(nuego_pago)
        self.instancia_db.commit()
        pass
    
    def obtener_uno(self, id = int):
        return self.instancia_db.query(self.pagos).filter(self.pagos.id_pago == id).first()
    
    def obtener_todos(self):
        return self.instancia_db.query(self.pagos).all()
    
class ClientesManager(ManagerGral):
    def __init__(self, instancia_db):
        super().__init__(instancia_db)
        self.instancia_db = instancia_db
        self.clientes = Clientes
        
    def crear(self, obj_cliente: Cliente):
        cliente_nuevo = Clientes(
            nombre = obj_cliente.nombre,
            apellido = obj_cliente.apellido,
            mail = obj_cliente.mail,
            direccion = obj_cliente.direccion,
            tipo_documento_id = obj_cliente.tipo_documento_id,
            nro_documento = obj_cliente.nro_documento,
            telefono = obj_cliente.telefono ,
        
        )
        self.instancia_db.add(cliente_nuevo)
        self.instancia_db.commit()
        pass
    
    def obtener_uno(self, id = int):
        return self.instancia_db.query(self.clientes).filter(self.clientes.id_cliente == id).first()
    
    def obtener_todos(self):
        return self.instancia_db.query(self.clientes).all()
    
    def eliminar(self, cliente_id):
        busqueda_cliente = self.obtener_uno(cliente_id)
        if busqueda_cliente:
            busqueda_cliente.fecha_baja_cliente = datetime.datetime.now()
            busqueda_cliente.habilitado = 0
            self.instancia_db.commit()
            return
        raise HTTPException(content={"detalle":"cliente no encontrado"}, status_code=404)
        
    def modificar(self, cliente: ClienteModificacion, id_cliente):
        self.instancia_db.query(self.clientes).filter(self.clientes.id_cliente == id_cliente).update(cliente.model_dump())
        self.instancia_db.commit()
