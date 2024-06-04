from abc import ABC, abstractmethod

class ManagerGral(ABC):
    def __init__(self, instancia_db, objeto):
        self.instancia_db = instancia_db
        self.objeto = objeto
    
    @abstractmethod    
    def crear(self):
        pass
    
    @abstractmethod 
    def eliminar(self):
        pass
    
    @abstractmethod 
    def modificar(self):
        pass
    
    @abstractmethod 
    def obtener_uno(self, id):
        pass
    
    @abstractmethod 
    def obtener_todos(self):
        pass


class EmbarcacionesManager(ManagerGral):
    def __init__(self, instancia_db, objeto):
        super().__init__(instancia_db, objeto)
        self.instancia_db = instancia_db
        self.objeto = objeto  

    def crear(self):
        pass
    
    def eliminar(self):
        pass
    
    def modificar(self):
        pass
    
    def obtener_uno(self, id):
        pass
    
    def obtener_todos(self):
        pass
    
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