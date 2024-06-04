from pydantic import BaseModel, UUID4, Field
from uuid import uuid4
import datetime

class Login(BaseModel):
    email: str
    contraseña: str

class Cliente(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    nombre: str
    email: str
    direccion: str
    tipo_documento: int
    nro_documento: str

class Embarcacion(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    tipo_id: int
    marca: str
    modelo: str
    color: str
    año_ingreso: datetime.date
    percha: int
    id_cliente: int
