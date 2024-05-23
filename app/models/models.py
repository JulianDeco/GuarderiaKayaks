from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import relationship

from app.providers.database import BaseDeDatos

bbdd = BaseDeDatos()
Base, SessionLocal = bbdd.iniciar_conexion()

class TipoDocumento(Base):
    __tablename__ = "tipo_documento"

    id = Column(Integer, primary_key=True, unique=True)
    descripcion = Column(String)

class Usuarios(Base):
    __tablename__ = "usuarios"

    id = Column(Uuid, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    clientes_cargados = relationship("clientes", back_populates="id")

class Clientes(Base):
    __tablename__ = "clientes"

    id = Column(Uuid, primary_key=True)
    email = Column(String, unique=True, index=True)
    nombre = Column(String)
    direccion = Column(String)
    nro_documento = Column(String)
    tipo_documento = Column(Integer, ForeignKey=TipoDocumento.id)

    kayaks = relationship("kayaks", back_populates="id")

class TipoKayak(Base):
    __tablename__ = "tipo_kayak"

    id = Column(Integer, primary_key=True, unique=True)
    descripcion = Column(String)


class Kayak(Base):
    __tablename__ = "kayaks"

    id = Column(Uuid, primary_key=True)
    modelo = Column(String)
    tipo = Column(Integer, ForeignKey=TipoKayak.id)
    color = Column(String)

