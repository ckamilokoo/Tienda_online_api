from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Define Base en un módulo separado
Base = declarative_base()

# Usa la variable de entorno DATABASE_URL para obtener la URL de conexión
SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')

# Configuración del motor de la base de datos con PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=1800)

# Crear una sesión local
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
            nombre="Mvp Zapatillas Jordan Hombre Gris",
            descripcion="Unas Zapatillas muy bonitas",
            precio=900,
            imagen_url="https://api-prd.ynk.cl/medias/BOLD-NIDZ4475026-VIEW1.jpg-515Wx515H?context=bWFzdGVyfGltYWdlc3wxNTI5OHxpbWFnZS9qcGVnfGFESmpMMmhsTWk4NU5UY3pNemc0TmpFMU56RXdMMEpQVEVSZlRrbEVXalEwTnpVd01qWmZWa2xGVnpFdWFuQm5YelV4TlZkNE5URTFTQXwzNDI1ZTk0NjcxNzIxNzk5YjJhMjZkNGFjYTMwMzQ0MGYxODY2MTExNzQyY2E2MDQ0ZmZmMmU4N2UwNWNjYjIz"
        )
        producto4 = Producto(
            nombre="JORDAN ZAPATILLA JORDAN AIR JORDAN 1 MID HOMBRE",
            descripcion="Unas zapatillas muy a la moda 2024",
            precio=1200,
            imagen_url="https://thelinegroupcl.vtexassets.com/arquivos/ids/192384/23024.jpg?v=638480764126630000"
        )
        producto5 = Producto(
            nombre="JORDAN STAY LOYAL 3",
            descripcion="Para saltar como MIKE",
            precio=920,
            imagen_url="https://nikeclprod.vtexassets.com/arquivos/ids/1031573/DZ4475_600_A_PREM.jpg?v=638548415742930000"
        )
        producto6 = Producto(
            nombre="AIR FOR 1 / 3",
            descripcion="Unas zapatillas muy a la moda 2024",
            precio=850,
            imagen_url="https://www.dimarsa.cl/media/catalog/product/m/a/marcasnikedc9836-160-blanco1jpeg_0.jpg"
        )
        producto7 = Producto(
            nombre="AIR FOR 1 / 4",
            descripcion="Unas zapatillas muy a la moda 2024",
            precio=850,
            imagen_url="https://cdnx.jumpseller.com/bendita-bodega/image/44224924/AR3762-100.png?1704812694"
        )
        producto8 = Producto(
            nombre="AIR FOR 1 / 74",
            descripcion="Unas zapatillas muy a la moda 2024",
            precio=850,
            imagen_url="https://thelinegroupcl.vtexassets.com/arquivos/ids/202871-800-450?v=638481032356600000&width=800&height=450&aspect=true"
        )
        producto9 = Producto(
            nombre="AIR FOR 1 / 23",
            descripcion="Unas zapatillas muy a la moda 2024",
            precio=850,
            imagen_url="https://i5.walmartimages.com/seo/NIKE-AIR-FORCE-1-07-MENS-SNEAKERS-315122-001_04fd782a-466a-4e7d-8028-abfd27a21db5_1.d84956ef0fd4d07e9d25b1b34b264567.jpeg"
        )
        producto10 = Producto(
            nombre="AIR FOR 1 / 12",
            descripcion="Unas zapatillas muy a la moda 2024",
            precio=850,
            imagen_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSPa_5OLIstJouz6Bgkz5-yMpItuErknZm0EQ&s"
        )
        producto11 = Producto(
            nombre="AIR FOR 1 / 98",
            descripcion="Unas zapatillas muy a la moda 2024",
            precio=850,
            imagen_url="https://http2.mlstatic.com/D_NQ_NP_635658-MLC52924096862_122022-O.webp"
        )
        producto12 = Producto(
            nombre="AIR FOR 1 / 09",
            descripcion="Unas zapatillas muy a la moda 2024",
            precio=850,
            imagen_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3b8J-5xJYslShCLZGMGHRjkE6z0BYjIb6tg&s"
        )
        producto13 = Producto(
            nombre="AIR FOR 1 / 34",
            descripcion="Unas zapatillas muy a la moda 2024",
            precio=1100,
            imagen_url="https://www.lockeroutlet.cl/wp-content/uploads/2024/05/LOCKER_NIDZ2554100_VIEW1.jpg"
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

