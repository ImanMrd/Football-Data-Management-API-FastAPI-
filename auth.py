## standard authorization mechanism

# calling the necessary libraries

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta

# -----------------------------
# JWT Configuration
# -----------------------------
SECRET_KEY = "hdhfh5jdnb7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # Using a secure key
ALGORITHM = "HS256"             # Encryption algorithm for the token
ACCESS_TOKEN_EXPIRE_MINUTES = 30  #  Token expiration time

# -----------------------------
# Password hashing config
# -----------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -----------------------------
# OAuth2 configuration
# -----------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# -----------------------------
# In-memory users "database"
# -----------------------------
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "hashed_password": pwd_context.hash("admin12345"),
        "disabled": False,
        "role": "admin"
    },
    "basicuser": {
        "username": "basicuser",
        "full_name": "Basic User",
        "hashed_password": pwd_context.hash("basicuser12345"),
        "disabled": False,
        "role": "basic"
    }
}

# -----------------------------
# Data Models
# -----------------------------

# Response model for /token
class Token(BaseModel):
    access_token: str
    token_type: str

# Data extracted from the token
class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

# Public user model (password not included)
class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    role: str

# Internal user model (includes hashed password)
class UserInDB(User):
    hashed_password: str

# -----------------------------
# Utility Functions
# -----------------------------

# Verify a plain password against a hashed one
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Return a hashed version of a plain password (for manual creation)
def get_password_hash(password):
    return pwd_context.hash(password)

# Get a user from the database
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

# Authenticate user with username and password
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Create a JWT access token for the user
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# -----------------------------
# Auth Dependencies
# -----------------------------

# Validate and decode the JWT token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
        token_data = TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception

    user = get_user(fake_users_db, token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Only allow access to users with role == "admin"
async def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user

# -----------------------------
# Login Endpoint (/token)
# -----------------------------
router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
