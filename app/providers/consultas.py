from abc import ABC, abstractmethod
from typing import Optional

from app.models.models import Embarcaciones


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
    
    def eliminar(self):
        """Eliminar una embarcación"""
        pass
    
    def modificar(self):
        """Modificar una embarcación"""
        pass
    
    def obtener_uno(self, id):
        """Obtener una embarcación por su ID"""
        pass
    
    def obtener_todos(self):
        """Obtener todas las embarcaciones"""
        return self.instancia_db.query(self.tipo).all()
class MailsManager(ManagerGral):
    def __init__(self, instancia_db, objeto):
        super().__init__(instancia_db, objeto)
        self.instancia_db = instancia_db
        self.objeto = objeto  

    def crear(self):
        pass
    
    def obtener_uno(self, id):
        pass
    
    def obtener_todos(self):
        pass
    
    def enviar_mail(self):
        pass