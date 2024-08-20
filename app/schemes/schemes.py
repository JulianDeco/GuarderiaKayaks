from pydantic import BaseModel, UUID4, Field
from uuid import uuid4
import datetime

class Login(BaseModel):
    email: str
    contraseña: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@example.com",
                "contraseña": "contraseña"
            }
        }

class Cliente(BaseModel):
    nombre: str
    apellido: str
    email: str
    direccion: str
    tipo_documento_id: int
    nro_documento: str
    telefono: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": str(uuid4()),
                "nombre": "Juan Pérez",
                "email": "juan.perez@example.com",
                "direccion": "Calle Falsa 123, Ciudad, País",
                "tipo_documento": 1,  # Ejemplo: 1 para DNI, 2 para Pasaporte, etc.
                "nro_documento": "12345678"
            }
        }

class Embarcacion(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    tipo_id: int
    marca: str
    modelo: str
    color: str
    año_ingreso: datetime.date
    percha: int
    id_cliente: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": str(uuid4()),
                "tipo_id": 1,  # Ejemplo: 1 para Velero, 2 para Yate, etc.
                "marca": "MarcaEjemplo",
                "modelo": "ModeloEjemplo",
                "color": "Azul",
                "año_ingreso": datetime.date(2023, 1, 1).isoformat(),
                "percha": 5,
                "id_cliente": 123  # Suponiendo que el ID del cliente es un entero
            }
        }