import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Uuid, Date, Float, DECIMAL, DateTime, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.providers.database import BaseDeDatos
import uuid

bbdd = BaseDeDatos()
Base, SessionLocal, engine = bbdd.iniciar_conexion()
class TipoEmbarcacion(Base):
    __tablename__ = "tipo_embarcaciones"
    id = Column(Integer, primary_key=True)
    descripcion = Column(String(250))

    embarcaciones = relationship("Embarcaciones", back_populates="tipo_embarcacion")

class TipoDocumento(Base):
    __tablename__ = "tipo_documento"
    id = Column(Integer, primary_key=True)
    descripcion = Column(String(250))

    clientes = relationship("Clientes", back_populates="tipo_documento_rel")
    usuarios_sistema = relationship("UsuarioSistema", back_populates="tipo_documento_rel")

class Rol(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    descripcion = Column(String(250))

    usuarios_sistema = relationship("UsuarioSistema", back_populates="rol_rel")

class UsuarioSistema(Base):
    __tablename__ = "usuario_sistema"
  
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = Column(String(250))
    apellido = Column(String(250))
    rol = Column(Integer, ForeignKey('roles.id'))
    mail = Column(String(250), unique=True, index=True)
    contraseña = Column(String(250))
    tipo_documento_id = Column(Integer, ForeignKey('tipo_documento.id'))
    nro_documento = Column(String(250))

    rol_rel = relationship("Rol", back_populates="usuarios_sistema")
    tipo_documento_rel = relationship("TipoDocumento", back_populates="usuarios_sistema")
    tokens = relationship("Usuario_Token", back_populates="usuario_token")

class Clientes(Base):
    __tablename__ = "clientes"

    id_cliente = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = Column(String(250))
    apellido = Column(String(250))
    mail = Column(String(250), unique=True, index=True)
    direccion = Column(String(250))
    tipo_documento_id = Column(Integer, ForeignKey('tipo_documento.id'))
    nro_documento = Column(String(250))
    telefono = Column(String(20))
    fecha_alta_cliente = Column(DateTime, server_default=func.now())
    fecha_baja_cliente = Column(DateTime, default=None)
    habilitado = Column(Integer, default= 1)
    
    pagos = relationship("Pagos", back_populates="cliente")
    embarcaciones = relationship("Embarcaciones", back_populates="cliente")
    tipo_documento_rel = relationship("TipoDocumento", back_populates="clientes")
    mails = relationship("Mails", back_populates="cliente")

class Embarcaciones(Base):
    __tablename__ = "embarcaciones"

    id_embarcacion = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tipo_id = Column(Integer, ForeignKey('tipo_embarcaciones.id'))
    marca = Column(String(250))
    modelo = Column(String(250))
    color = Column(String(250))
    fecha_ingreso = Column(DateTime, server_default=func.now())
    fecha_baja = Column(DateTime, default=None)
    percha = Column(Integer, unique=True)
    id_cliente = Column(String(36), ForeignKey('clientes.id_cliente'))
    habilitado = Column(Integer, default= 1)

    cliente = relationship("Clientes", back_populates="embarcaciones")
    tipo_embarcacion = relationship("TipoEmbarcacion", back_populates="embarcaciones")

class Pagos(Base):
    __tablename__ = "pagos"
    
    id_pago = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    monto = Column(DECIMAL(10, 2))
    fecha_pago = Column(DateTime, server_default=func.now())
    fecha_pago_realizado = Column(DateTime, default=None)
    aviso_mail = Column(Integer, default = 0)
    id_cliente = Column(String(36), ForeignKey('clientes.id_cliente'))

    cliente = relationship("Clientes", back_populates="pagos")
    
class Mails(Base):
    __tablename__ = "mails"
    id_mail = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    mensaje = Column(String(400))
    titulo = Column(String(200))
    receptor_cliente = Column(String(400), ForeignKey('clientes.id_cliente'))
    receptor_mail = Column(String(400))
    fecha_creacion = Column(DateTime, server_default=func.now())
    
    cliente = relationship("Clientes", back_populates="mails")
    
class Parametros(Base):
    __tablename__="parametros"
    id = Column(Integer, primary_key=True)
    descripcion = Column(String(200))
    
    
def fecha_token():
    return str(datetime.datetime.now() + datetime.timedelta(minutes=30))
class Usuario_Token(Base):
    __tablename__ = "usuarios_token"
    id = Column(Integer, primary_key = True, autoincrement= True)
    mail = Column(String(36), ForeignKey('usuario_sistema.mail'))
    token = Column(String(36))
    expira_en = Column(DateTime, default=None)
    
    usuario_token = relationship("UsuarioSistema", back_populates="tokens")