from sqlalchemy.ext.asyncio import AsyncSession
from schemas.authSchemas import *
from config.models import Admin
from sqlalchemy.future import select
from fastapi import HTTPException
from passlib.context import CryptContext

passwordHash = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticateAdmin(username: str, password: str, db: AsyncSession):
    result = await db.execute(select(Admin).filter(Admin.Username == username))
    authAdmin = result.scalars().first()
    if authAdmin is None:
        raise HTTPException(status_code=401, detail="Invalid email")

    if not passwordHash.verify(password, authAdmin.HashPassword):
        raise HTTPException(status_code=401, detail="Invalid password")

    return authAdmin
