from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker , Session
import model as models

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Base de datos en SQLite

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def cargar_productos_iniciales(db: Session):
    # Verificar si ya existen productos en la base de datos
    if db.query(models.Producto).count() == 0:
        # Productos por defecto
        producto1 = models.Producto(
            nombre="Adobe Photoshop CC 2022",
            descripcion="Software de edición de fotos",
            precio=850,
            imagen_url="https://images.unsplash.com/photo-1515955656352-a1fa3ffcd111?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"
            
        )
        producto2 = models.Producto(
            nombre="The Hilton Hotel",
            descripcion="Hotel en Lisboa, Portugal",
            precio=850,
            imagen_url="https://images.unsplash.com/photo-1511556532299-8f662fc26c06?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"
        )
        # Añadir productos a la sesión
        db.add(producto1)
        db.add(producto2)
        db.commit()
