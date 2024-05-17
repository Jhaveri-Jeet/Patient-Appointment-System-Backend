from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import SessionLocal
from schemas.authSchemas import *
from controllers.adminControllers import *
from fastapi.security import OAuth2PasswordRequestForm
from config.auth import createAccessToken

router = APIRouter()


def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/adminToken", tags=["auth"])
async def loginForAccessToken(
    formData: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(getDb)
) -> Token:
    admin = await authenticateAdmin(formData.username, formData.password, db)
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = createAccessToken({"sub": admin.Username, "id": admin.Id})
    return {"access_token": token, "token_type": "bearer"}


@router.put("/admin", tags=["admin"])
async def updateAdminAsync(admin: AdminRequestModel, db: AsyncSession = Depends(getDb)):
    updatedAdmin = await updateAdmin(admin, db)
    return updatedAdmin
