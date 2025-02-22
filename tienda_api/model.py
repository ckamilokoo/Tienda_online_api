from sqlalchemy import Column, Integer, String, Float ,Boolean 


class Producto():
    __tablename__ = "productos"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)
    imagen_url = Column(String)
    precio = Column(Float)
    
    
class User():
    """
    Modelo para la tabla 'users' en la base de datos.
    Representa a un usuario con su nombre de usuario, contraseña encriptada y estado.
    """
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)  # ID único para cada usuario
    username = Column(String, unique=True, index=True)  # Nombre de usuario único
    hashed_password = Column(String)  # Contraseña almacenada de forma encriptada
    is_active = Column(Boolean, default=True)  # Estado del usuario (activo o no)
    rol=Column(String, index=True)


