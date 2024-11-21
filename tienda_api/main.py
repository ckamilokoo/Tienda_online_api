from fastapi import FastAPI, Depends, HTTPException , status
from typing import Annotated
from typing import Optional, List
from datetime import datetime, timedelta, timezone
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from model import Producto , User
from schemas import ProductoCreate, Producto as ProductoSchema , Token , UserCreate ,UserInDB ,TokenData ,UserOut

from database import SessionLocal, engine, get_db, cargar_productos_iniciales
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt  # Manejo de JWT para la autenticación
from passlib.context import CryptContext  # Encriptación de contraseñas
from pydantic import BaseModel


SECRET_KEY = "your_secret_key"  # Clave secreta para firmar los tokens JWT
ALGORITHM = "HS256"  # Algoritmo de encriptación usado
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Duración del token en minutos

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


# Contexto para manejar la encriptación de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema OAuth2 para manejar autenticación mediante tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependencia para inyectar la base de datos en las funciones
db_dependency = Annotated[Session, Depends(get_db)]

def get_current_user(db: db_dependency, token: str = Depends(oauth2_scheme)):
    """
    Obtiene el usuario actual autenticado a partir de un token JWT.
    - Decodifica el token.
    - Valida los datos contenidos en el token.
    - Recupera al usuario de la base de datos.
    """
    # Excepción para credenciales inválidas
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodifica el token JWT utilizando la clave secreta y el algoritmo configurado
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # Obtiene el nombre de usuario del token
        if username is None:  # Si no hay nombre de usuario, lanza una excepción
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:  # Si ocurre un error al decodificar el token, lanza una excepción
        raise credentials_exception
    
    # Recupera el usuario de la base de datos
    user = get_user(db, username=token_data.username)
    if user is None:  # Si no encuentra al usuario, lanza una excepción
        raise credentials_exception
    
    return user  # Devuelve el usuario autenticado

# Dependencia para inyectar el usuario actual autenticado en las funciones
user_dependency = Annotated[dict, Depends(get_current_user)]

def verify_password(plain_password, hashed_password):
    """
    Verifica que una contraseña en texto plano coincida con una encriptada.
    Utiliza el contexto de encriptación configurado para comparar ambas.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Genera un hash encriptado a partir de una contraseña en texto plano.
    Esto asegura que las contraseñas no se almacenen directamente en la base de datos.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Crea un token de acceso (JWT) con una fecha de expiración opcional.
    - `data`: Información que se codificará dentro del token.
    - `expires_delta`: Tiempo adicional para configurar la expiración del token.
    """
    to_encode = data.copy()  # Copia los datos originales para no modificarlos directamente
    if expires_delta:
        # Si se proporciona un tiempo de expiración, se calcula la fecha de vencimiento
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Si no se proporciona, el token expira en 15 minutos por defecto
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})  # Agrega la fecha de expiración al token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Codifica el token
    return encoded_jwt  # Retorna el token codificado

def get_user(db, username: str):
    """
    Recupera un usuario de la base de datos a partir del nombre de usuario.
    - `db`: Sesión de base de datos.
    - `username`: Nombre de usuario que se busca.
    """
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db, username: str, password: str):
    """
    Autentica a un usuario verificando su existencia y su contraseña.
    - `db`: Sesión de base de datos.
    - `username`: Nombre de usuario.
    - `password`: Contraseña proporcionada por el usuario.
    """
    user = get_user(db, username)  # Busca al usuario en la base de datos
    if not user:  # Si el usuario no existe, retorna False
        return False
    if not verify_password(password, user.hashed_password):  # Verifica la contraseña
        return False
    return user  # Si todo es válido, retorna al usuario

@app.post("/register", response_model=Token)
def register(user: UserCreate, db: db_dependency):
    """
    Registra un nuevo usuario en el sistema.
    - Verifica que el nombre de usuario no esté ya registrado.
    - Encripta la contraseña antes de guardarla.
    - Genera un token JWT de acceso tras el registro exitoso.
    """
    db_user = get_user(db, user.username)  # Verifica si el usuario ya existe
    if db_user:
        # Lanza una excepción si el nombre de usuario ya está registrado
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)  # Encripta la contraseña
    # Crea un nuevo objeto de usuario con los datos proporcionados
    db_user = User(username=user.username, hashed_password=hashed_password ,rol="user")
    db.add(db_user)  # Agrega el usuario a la base de datos
    db.commit()  # Confirma los cambios
    db.refresh(db_user)  # Refresca el objeto usuario para obtener el ID asignado
    access_token = create_access_token(data={"sub": db_user.username})  # Genera un token de acceso
    return {"access_token": access_token, "token_type": "bearer"}  # Retorna el token

@app.post("/token", response_model=Token)
def login_for_access_token(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint para iniciar sesión y obtener un token de acceso.
    - Verifica las credenciales proporcionadas.
    - Genera y retorna un token JWT si la autenticación es exitosa.
    """
    user = authenticate_user(db, form_data.username, form_data.password)  # Autentica al usuario
    if not user:
        # Lanza una excepción si las credenciales son incorrectas
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})  # Genera un token de acceso
    return {"access_token": access_token, "token_type": "bearer"}  # Retorna el token


@app.get("/users/me/", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Devuelve la información del usuario actualmente autenticado.
    - `current_user`: Obtenido a través de la dependencia `user_dependency`, que valida el token JWT.
    - Responde con el modelo `UserCreate`, mostrando detalles como el nombre de usuario.
    """
    return current_user


