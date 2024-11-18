from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Define Base en un módulo separado
Base = declarative_base()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Base de datos en SQLite

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def cargar_productos_iniciales(db: Session):
    from model import Producto  # Import local para evitar importación circular

    # Verificar si ya existen productos en la base de datos
    if db.query(Producto).count() == 0:
        # Productos por defecto
        producto1 = Producto(
            nombre="Adobe Photoshop CC 2022",
            descripcion="Software de edición de fotos",
            precio=850,
            imagen_url="https://images.unsplash.com/photo-1515955656352-a1fa3ffcd111?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"
        )
        producto2 = Producto(
            nombre="The Hilton Hotel",
            descripcion="Hotel en Lisboa, Portugal",
            precio=850,
            imagen_url="https://images.unsplash.com/photo-1511556532299-8f662fc26c06?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"
        )
        producto3 = Producto(
            nombre="The Hilton Hotel",
            descripcion="Hotel en Lisboa, Portugal",
            precio=850,
            imagen_url="https://images.unsplash.com/photo-1511556532299-8f662fc26c06?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"
        )
        producto4 = Producto(
            nombre="The Hilton Hotel",
            descripcion="Hotel en Lisboa, Portugal",
            precio=850,
            imagen_url="https://images.unsplash.com/photo-1511556532299-8f662fc26c06?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"
        )
        producto5 = Producto(
            nombre="The Hilton Hotel",
            descripcion="Hotel en Lisboa, Portugal",
            precio=850,
            imagen_url="https://images.unsplash.com/photo-1511556532299-8f662fc26c06?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"
        )
        producto6 = Producto(
            nombre="The Hilton Hotel",
            descripcion="Hotel en Lisboa, Portugal",
            precio=850,
            imagen_url="https://images.unsplash.com/photo-1511556532299-8f662fc26c06?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"
        )
        producto7 = Producto(
            nombre="The Hilton Hotel",
            descripcion="Hotel en Lisboa, Portugal",
            precio=850,
            imagen_url="https://images.unsplash.com/photo-1511556532299-8f662fc26c06?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"
        )
        producto8 = Producto(
            nombre="The Hilton Hotel",
            descripcion="Hotel en Lisboa, Portugal",
            precio=850,
            imagen_url="https://images.unsplash.com/photo-1511556532299-8f662fc26c06?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"
        )
        producto9 = Producto(
            nombre="The Hilton Hotel",
            descripcion="Hotel en Lisboa, Portugal",
            precio=850,
            imagen_url="https://images.unsplash.com/photo-1511556532299-8f662fc26c06?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"
        )
        producto10 = Producto(
            nombre="The Hilton Hotel",
            descripcion="Hotel en Lisboa, Portugal",
            precio=850,
            imagen_url="https://images.unsplash.com/photo-1511556532299-8f662fc26c06?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"
        )
        producto11 = Producto(
            nombre="The Hilton Hotel",
            descripcion="Hotel en Lisboa, Portugal",
            precio=850,
            imagen_url="https://images.unsplash.com/photo-1511556532299-8f662fc26c06?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"
        )
        producto12 = Producto(
            nombre="The Hilton Hotel",
            descripcion="Hotel en Lisboa, Portugal",
            precio=850,
            imagen_url="https://images.unsplash.com/photo-1511556532299-8f662fc26c06?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"
        )
        producto13 = Producto(
            nombre="The Hilton Hotel",
            descripcion="Hotel en Lisboa, Portugal",
            precio=850,
            imagen_url="https://images.unsplash.com/photo-1511556532299-8f662fc26c06?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"
        )
        # Añadir productos a la sesión
        db.add(producto1)
        db.add(producto2)
        db.add(producto3)
        db.add(producto4)
        db.add(producto5)
        db.add(producto6)
        db.add(producto7)
        db.add(producto8)
        db.add(producto9)
        db.add(producto10)
        db.add(producto11)
        db.add(producto12)
        db.add(producto13)
        db.commit()

