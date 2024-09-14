from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from tienda_api import model as models
from tienda_api import schemas
from database import SessionLocal, engine, get_db , cargar_productos_iniciales

app = FastAPI()

# Configurar CORS para permitir cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Cargar productos por defecto
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    cargar_productos_iniciales(db)
    db.close()

# Obtener todos los productos (asíncrono)
@app.get("/productos/", response_model=list[schemas.Producto])
async def read_productos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    productos = db.query(models.Producto).offset(skip).limit(limit).all()
    return productos

# Crear un nuevo producto (asíncrono)
@app.post("/productos/", response_model=schemas.Producto)
async def create_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    db_producto = models.Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

# Obtener un producto por ID (asíncrono)
@app.get("/productos/{producto_id}", response_model=schemas.Producto)
async def read_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# Actualizar un producto por ID (asíncrono)
@app.put("/productos/{producto_id}", response_model=schemas.Producto)
async def update_producto(producto_id: int, producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    for key, value in producto.dict().items():
        setattr(db_producto, key, value)

    db.commit()
    db.refresh(db_producto)
    return db_producto

# Eliminar un producto por ID (asíncrono)
@app.delete("/productos/{producto_id}", response_model=schemas.Producto)
async def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(db_producto)
    db.commit()
    return db_producto

