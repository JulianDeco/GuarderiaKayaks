from pydantic import BaseModel, UUID4, Field
from uuid import uuid4

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

class Kayak(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
