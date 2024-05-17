from jose import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def createAccessToken(data: dict):
    encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp": expire})
    encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verifyPassword(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
