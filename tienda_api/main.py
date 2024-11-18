from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from model import Producto
from schemas import ProductoCreate, Producto as ProductoSchema
from database import SessionLocal, engine, get_db, cargar_productos_iniciales

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear las tablas en la base de datos
Producto.metadata.create_all(bind=engine)

# Cargar productos por defecto
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    cargar_productos_iniciales(db)
    db.close()

# Rutas
@app.get("/productos/", response_model=list[ProductoSchema])
async def read_productos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    productos = db.query(Producto).offset(skip).limit(limit).all()
    return productos

@app.post("/productos/", response_model=ProductoSchema)
async def create_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    db_producto = Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@app.get("/productos/{producto_id}", response_model=ProductoSchema)
async def read_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.put("/productos/{producto_id}", response_model=ProductoSchema)
async def update_producto(producto_id: int, producto: ProductoCreate, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    for key, value in producto.dict().items():
        setattr(db_producto, key, value)

    db.commit()
    db.refresh(db_producto)
    return db_producto

@app.delete("/productos/{producto_id}", response_model=ProductoSchema)
async def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(db_producto)
    db.commit()
    return db_producto


