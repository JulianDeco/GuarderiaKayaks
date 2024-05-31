from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Uuid, Date
from sqlalchemy.orm import relationship

from app.providers.database import BaseDeDatos

bbdd = BaseDeDatos()
Base, SessionLocal = bbdd.iniciar_conexion()

class usuario_sistema(Base):
    __tablename__ = "usuario_sistema"
  
    id = Column(Integer, primary_key=True, unique=True)
    nombre = Column(String)
    apellido = Column(String)
    rol = Column(String) #no se que tipo de dato puedo ir aca 
    mail = Column(String)
    contrseña = Column(String)
    tipo_documento = Column(String)
    nro_documento = Column(int)
    
class Usuarios(Base): #esta tabla se va a tener que borrar
    __tablename__ = "usuarios"

    id = Column(Uuid, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    clientes_cargados = relationship("clientes", back_populates="id")

class Clientes(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Uuid, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    mail= Column(String, unique=True, index=True)
    direccion = Column(String)
    tipo_documento = Column(String) 
    nro_documento = Column(String)
    telefono = Column(int)
    
    pagos = relationship("Pagos", back_populates="cliente") # esta relacion em la hizo carlitos(chatgpt)
    
class Embarcaciones(Base):
    __tablename__ = "embarcaciones"

    id_embarcacion = Column(Integer, primary_key=True, unique=True)
    tipo = Column(String) #creo que poniendo el tipo de embarcacion aca nos ahorramos la tabla tipo_embarcaciones
    marca = Column(String)
    modelo = Column(String)
    color = Column(String)
    eslora = Column(int) #creo que va un int 
    manga = Column(int) #busque y es el ancho de una embarcacion y ya que tenemos el largo ¿porque no el ancho?
    año_de_ingreso = Column(Date)
    percha = Column(int) 

class Pagos(Base):
    __tablename__ = "pagos"
    
    id_pago = Column(int, primary_key=True, unique=True)
    monto = Column(float)
    fecha_pago = Column(Date)
    id_cliente = Column(int, ForeignKey('id_cliente')) # vas a tener que hacer las relaciones porque no se que onda como hacerlas y

    cliente = relationship("Clientes", back_populates="pagos") # esta relacion em la hizo carlitos(chatgpt)
     
    
class clientes_embarcaciones(Base):
    __tablename__ = "clientes_embarcaciones"
    
    id_cliente = Column(int, ForeignKey('id_cliente'))
    id_embarcion = Column(int, ForeignKey('id_ embarcacion'))
    
