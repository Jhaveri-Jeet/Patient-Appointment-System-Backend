from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import SessionLocal
from schemas.slotSchemas import *
from controllers.slotControllers import *


router = APIRouter()


def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/slot", tags=["slot"])
async def createSlotAsync(
    slot: SlotRequestModel, db: AsyncSession = Depends(getDb)
) -> SlotResponseModel:
    newSlot = await createSlot(slot, db)
    return newSlot


@router.get("/slot", tags=["slot"])
async def getAllSlotAsync(
    db: AsyncSession = Depends(getDb),
) -> list[SlotResponseModel]:
    slots = await getAllSlots(db)
    return slots


@router.get("/slot/{slotId}", tags=["slot"])
async def getSlotAsync(
    slotId: int, db: AsyncSession = Depends(getDb)
) -> SlotResponseModel:
    slot = await getSlot(slotId, db)
    return slot


@router.put("/slot/{slotId}", tags=["slot"])
async def updateSlotAsync(
    slotId: int, updatedSlot: SlotRequestModel, db: AsyncSession = Depends(getDb)
) -> SlotResponseModel:
    slot = await updateSlot(slotId, updatedSlot, db)
    return slot


@router.delete("/slot/{slotId}", tags=["slot"])
async def deleteSlotAsync(slotId: int, db: AsyncSession = Depends(getDb)):
    slot = await deleteSlot(slotId, db)
    return slot
