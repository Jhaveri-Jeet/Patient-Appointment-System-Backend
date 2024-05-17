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


async def updateAdmin(admin: AdminRequestModel, db: AsyncSession):
    result = await db.execute(select(Admin).filter(Admin.Username == admin.Username))
    adminCheck = result.scalars().first()
    if adminCheck is None:
        raise HTTPException(status_code=400, detail="Admin not found")

    adminCheck.Username = admin.Username
    adminCheck.HashPassword = passwordHash.hash(admin.HashPassword)
    await db.commit()
    await db.refresh(adminCheck)
    return adminCheck


async def createDefaultUser(db: AsyncSession):
    result = await db.execute(select(Admin).filter(Admin.Username == "admin"))
    admin_exists = result.scalars().first()

    if admin_exists is None:
        hashed_password = passwordHash.hash("admin")
        default_admin = Admin(Username="admin", HashPassword=hashed_password)
        db.add(default_admin)
        await db.commit()
        await db.refresh(default_admin)
