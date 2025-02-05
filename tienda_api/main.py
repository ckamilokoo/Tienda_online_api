from fastapi import FastAPI, Depends, HTTPException , status ,UploadFile, File
from typing import Annotated
from typing import Optional, List
from datetime import datetime, timedelta, timezone
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from model import Producto , User
from schemas import ProductoCreate, Producto as ProductoSchema , Token , UserCreate ,UserInDB ,TokenData ,UserOut , LoginRequest , UserOutWithToken

from database import SessionLocal, engine, get_db, cargar_productos_iniciales
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt  # Manejo de JWT para la autenticación
from passlib.context import CryptContext  # Encriptación de contraseñas
from pydantic import BaseModel
import os
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
from supabase import create_client, Client

UPLOAD_FOLDER = "./uploaded_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


SUPABASE_URL = "https://kasavcuflkptbqewqrmv.supabase.co"  # Reemplaza con tu URL de Supabase
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imthc2F2Y3VmbGtwdGJxZXdxcm12Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzIwMDI1NTMsImV4cCI6MjA0NzU3ODU1M30.KL5OefuVJ8az1gfTkGV3gVda__OIUhPDjxAw7tlUQsA"  # Usa la clave secreta correcta de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# Esquema OAuth2 para manejar autenticación mediante tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configuración de seguridad
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
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

# Contexto para manejar la encriptación de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



# Dependencia para inyectar la base de datos en las funciones
# Función para crear token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Función para encriptar contraseñas
def get_password_hash(password: str):
    return pwd_context.hash(password)


@app.post("/register", response_model=Token)
async def register_user(user: UserCreate):
    # Verificar si el usuario ya existe
    existing_user = supabase.table("users").select("username").eq("username", user.username).execute()
    if existing_user.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre de usuario ya está en uso.")

    # Hashear la contraseña y crear usuario en Supabase
    hashed_password = get_password_hash(user.password)
    response = supabase.table("users").insert({
        "username": user.username,
        "hashed_password": hashed_password,
        "rol": user.rol,
        "is_active": True
    }).execute()
    
    print(response)  # Para depuración
    
    # ⚠️ Validación corregida: Verificar si `data` está vacío
    if not response.data:
        raise HTTPException(status_code=500, detail="Error al crear el usuario.")

    # Generar token
    access_token = create_access_token({"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer","user": {  # Agregar los datos del usuario aquí
            "id": response.data[0]["id"],
            "username": response.data[0]["username"],
            "is_active": response.data[0]["is_active"],
            "rol": response.data[0]["rol"]
        }}



# Login de usuario
@app.post("/token", response_model=Token)
async def login_for_access_token(login_request: LoginRequest):
    print(login_request.username)
    response = supabase.table("users").select("*").eq("username", login_request.username).execute()
    print(response)
    if not response.data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado.")

    user = response.data[0]
    if not pwd_context.verify(login_request.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Contraseña incorrecta.")

    access_token = create_access_token({"sub": user["username"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "username": user["username"],
            "rol": user["rol"],
            "is_active": user["is_active"],
        }
    }

@app.get("/users/me/")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido."
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError:  # ✅ Se usa JWTError en vez de PyJWTError
        raise credentials_exception

    response = supabase.table("users").select("*").eq("username", username).execute()
    if not response.data:
        raise credentials_exception

    user = response.data[0]
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "username": user["username"],
            "rol": user["rol"],
            "is_active": user["is_active"],
        }
    }






