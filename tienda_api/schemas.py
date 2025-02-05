from pydantic import BaseModel 
from typing import Optional, List, Optional

class ProductoBase(BaseModel):
    nombre: str
    descripcion: str
    imagen_url: Optional[str] = None  # URL para la imagen asociada al producto
    precio: float

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int

    class Config:
        from_attributes = True
        

class UserCreate(BaseModel):
    """
    Esquema para la creación de un usuario.
    Contiene los campos básicos requeridos para registrar un usuario.
    """
    username: str  # Nombre de usuario
    password: str  # Contraseña en texto plano
    rol:str

class UserInDB(UserCreate):
    """
    Esquema para representar un usuario almacenado en la base de datos.
    Hereda de UserCreate y añade la contraseña encriptada.
    """
    hashed_password: str  # Contraseña almacenada de forma encriptada


class TokenData(BaseModel):
    """
    Esquema para los datos contenidos en el token.
    Se utiliza para validar la información del usuario.
    """
    username: Optional[str] = None  # Nombre de usuario, puede ser opcional
    
class UserOut(BaseModel):
    username: str
    rol:str
    is_active:bool
    # omite el password en la salida
    class Config:
        from_attributes = True
        #fields = {'password': {'exclude': True}}  # Excluye el campo password
        

class UserOutWithToken(UserOut):
    access_token: str  # Incluye el token de acceso

class Token(BaseModel):
    """
    Esquema para la respuesta de autenticación.
    Contiene el token de acceso y su tipo.
    """
    access_token: str  # El token JWT generado
    token_type: str  # Tipo de token, normalmente "Bearer"
    user: UserOut  # Información adicional del usuario
    
    
class LoginRequest(BaseModel):
    username: str
    password: str



