from sqlalchemy import Column, Integer, String, Float ,Boolean 
from database import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)
    imagen_url = Column(String)
    precio = Column(Float)
    
    
class User(Base):
    """
    Modelo para la tabla 'users' en la base de datos.
    Representa a un usuario con su nombre de usuario, contraseña encriptada y estado.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)  # ID único para cada usuario
    username = Column(String, unique=True, index=True)  # Nombre de usuario único
    hashed_password = Column(String)  # Contraseña almacenada de forma encriptada
    is_active = Column(Boolean, default=True)  # Estado del usuario (activo o no)
    rol=Column(String, index=True)


