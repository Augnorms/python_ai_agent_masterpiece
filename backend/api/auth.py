from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from database.database import create_auth_user, get_auth_user_by_username
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

router = APIRouter()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(BASE_DIR, ".env"))
load_dotenv()

secret_key = os.getenv("JWT_SECRET") or "aquasync_super_secret_jwt_key_2026_industrial_scada"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days

def hash_password(password: str) -> str:
    pwd_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        pwd_bytes = plain_password.encode("utf-8")[:72]
        return bcrypt.checkpw(pwd_bytes, hashed_password.encode("utf-8"))
    except Exception:
        return False


# --- Schemas ---
class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)


# --- Endpoints ---
@router.post("/api/auth/register")
async def register(user: UserRegister):
    # 1. Hash the password
    hashed_pw = hash_password(user.password)
    
    # 2. Save to database
    user_id = create_auth_user(user.username, user.email, hashed_pw)
    
    if not user_id:
        raise HTTPException(status_code=400, detail="Username or email already registered")
        
    return {"status": "success", "message": "User registered successfully"}



@router.post("/api/auth/login")
async def login(user: UserLogin):
    # 1. Find user
    db_user = get_auth_user_by_username(user.username)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    # 2. Verify password
    if not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    # 3. Generate JWT
    token = create_access_token({"sub": db_user["username"], "id": db_user["id"]})
    
    return {
        "status": "success",
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": db_user["id"], "username": db_user["username"], "email": db_user["email"]}
    }



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        email: str = payload.get("email")

        if username is None or user_id is None:
            raise credentials_exception
        return {"username": username, "user_id": user_id, "email":email}
    except JWTError:
        raise credentials_exception