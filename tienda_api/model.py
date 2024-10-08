from sqlalchemy import Column, Integer, String, Float
from tienda_api.database import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)
    imagen_url = Column(String)
    precio = Column(Float)


