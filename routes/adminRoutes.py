from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import SessionLocal
from schemas.authSchemas import *
from controllers.adminControllers import *
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
    admin: AdminRequestModel, db: AsyncSession = Depends(getDb)
) -> Token:
    admin = await authenticateAdmin(admin, db)
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = createAccessToken({"sub": admin.Username, "id": admin.Id})
    return {"access_token": token, "token_type": "bearer"}


@router.put("/admin/{adminId}", tags=["admin"])
async def updateAdminAsync(
    adminId: int, admin: AdminRequestModel, db: AsyncSession = Depends(getDb)
):
    updatedAdmin = await updateAdmin(adminId, admin, db)
    return updatedAdmin


@router.get("/admin", tags=["admin"])
async def getAdminAsync(db: AsyncSession = Depends(getDb)) -> AdminResponseModel:
    admin = await getAdmin(db)
    return admin
