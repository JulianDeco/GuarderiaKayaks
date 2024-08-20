from abc import ABC, abstractmethod
from typing import Optional


from app.models.models import Embarcaciones, Mails, Pagos, Clientes
from app.schemes.schemes import Cliente


class ManagerGral(ABC):
    def __init__(self, instancia_db, objeto: Optional[object]):
        self.instancia_db = instancia_db
        self.objeto = objeto
    
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
        self.tipo = Embarcaciones  # Asegúrate de definir Embarcaciones
    
    def crear(self):
        """Crear una embarcación"""
        pass
    
    def eliminar(self, id=int):
        """Eliminar una embarcación, en realidad es una baja lógica y no eliminación real"""
        eliminar_embacaion = self.instancia_db.query(self.tipo).filter(self.tipo.id_embarcacion == id).delete()
        self.instancia_db.commit()
        return eliminar_embacaion
        
    
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
        
    def crear():
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
            mail = obj_cliente.email,
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
    
    def baja_cliente(self, cliente: Clientes):
        cliente.habilitado = 0
        return self.instancia_db.commit()
        