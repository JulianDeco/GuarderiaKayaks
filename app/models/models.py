from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Uuid, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.providers.database import BaseDeDatos
import uuid

bbdd = BaseDeDatos()
Base, SessionLocal = bbdd.iniciar_conexion()

class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    descripcion = Column(String)

class TipoEmbarcacion(Base):
    __tablename__ = "tipo_embarcaciones"
    id = Column(Integer, primary_key=True)
    descripcion = Column(String)
    
    embarcaciones = relationship("Embarcaciones", back_populates="tipo_embarcacion")  # Relación uno a muchos

class TipoDocumento(Base):
    __tablename__ = "tipo_documento"
    id = Column(Integer, primary_key=True)
    descripcion = Column(String)

    clientes = relationship("Clientes", back_populates="tipo_documento_rel")  # Relación uno a muchos
    usuarios_sistema = relationship("UsuarioSistema", back_populates="tipo_documento_rel")  # Relación uno a muchos

class UsuarioSistema(Base):
    __tablename__ = "usuario_sistema"
  
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String)
    apellido = Column(String)
    rol = Column(Integer, ForeignKey('roles.id'))  
    mail = Column(String, unique=True)
    contraseña = Column(String)
    tipo_documento_id = Column(Integer, ForeignKey('tipo_documento.id'))
    nro_documento = Column(String)

    rol_rel = relationship("Rol", back_populates="usuarios_sistema")
    tipo_documento_rel = relationship("TipoDocumento", back_populates="usuarios_sistema")

class Clientes(Base):
    __tablename__ = "clientes"

    id_cliente = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String)
    apellido = Column(String)
    mail = Column(String, unique=True, index=True)
    direccion = Column(String)
    tipo_documento_id = Column(Integer, ForeignKey('tipo_documento.id'))
    nro_documento = Column(String)
    telefono = Column(Integer)
    
    pagos = relationship("Pagos", back_populates="cliente")
    embarcaciones = relationship("Embarcaciones", back_populates="cliente")  # Relación uno a muchos
    tipo_documento_rel = relationship("TipoDocumento", back_populates="clientes")

class Embarcaciones(Base):
    __tablename__ = "embarcaciones"

    id_embarcacion = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tipo_id = Column(Integer, ForeignKey('tipo_embarcaciones.id'))
    marca = Column(String)
    modelo = Column(String)
    color = Column(String)
    eslora = Column(Integer)
    manga = Column(Integer) 
    año_de_ingreso = Column(Date)
    percha = Column(Integer)
    id_cliente = Column(UUID(as_uuid=True), ForeignKey('clientes.id_cliente'))  # Clave foránea para la relación

    cliente = relationship("Clientes", back_populates="embarcaciones")  # Relación muchos a uno
    tipo_embarcacion = relationship("TipoEmbarcacion", back_populates="embarcaciones")

class Pagos(Base):
    __tablename__ = "pagos"
    
    id_pago = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    monto = Column(Float)
    fecha_pago = Column(Date)
    id_cliente = Column(UUID(as_uuid=True), ForeignKey('clientes.id_cliente'))

    cliente = relationship("Clientes", back_populates="pagos")  # Relación muchos a uno