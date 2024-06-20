from abc import ABC, abstractmethod
from typing import Optional


from app.models.models import Embarcaciones
from app.models.models import Mails
from app.models.models import Pagos




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
    def __init__(self, instancia_db, objeto=None):
        super().__init__(instancia_db, objeto)
        self.tipo = Embarcaciones  # Asegúrate de definir Embarcaciones
    
    def crear(self):
        """Crear una embarcación"""
        pass
    
    def eliminar(self, id=int):
        """Eliminar una embarcación"""
        eliminar_embacaion = self.instancia_db.query(self.tipo).filter(self.tipo.id_embarcacion == id).delete()
        self.instancia_db.commit()
        return eliminar_embacaion
        
    
    def modificar(self, id = int, marca = str, modelo = str, color= str, año_ingreso = None, percha = int, id_cliente = int):
        """Modificar una embarcación"""
        modificar_embarcacion = self.instancia_db.query(self.tipo).filter(self.tipo.id_embarcacion == id).update(
            {
                self.tipo.marca: marca,
                self.tipo.modelo: modelo,
                self.tipo.color: color,
                self.tipo.año_ingreso: año_ingreso,#no se que hiria aca,
                self.tipo.percha: percha,
                self.tipo.id_cliente: id_cliente
            }
        )
        self.instancia_db.commit()
        return modificar_embarcacion
    
    def obtener_uno(self, id=int):
        """Obtener una embarcación por su ID"""
        return self.instancia_db.query(self.tipo).filter(self.tipo.id_embarcacion== id).fist()
    
    def obtener_todos(self):
        """Obtener todas las embarcaciones"""
        return self.instancia_db.query(self.tipo).all()
    
class MailsManager(ManagerGral):
    def __init__(self, instancia_db, objeto):
        super().__init__(instancia_db, objeto)
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
    def __init__(self, instancia_db, objeto: object | None):
        super().__init__(instancia_db, objeto)
        self.instancia_db = instancia_db
        self.pagos = Pagos
    
    def obtener_uno(self, id = int):
        return self.instancia_db.query(self.pagos).filter(self.pagos.id_pago == id).first()
    
    def obtener_todos(self):
        return self.instancia_db.query(self.pagos).all()