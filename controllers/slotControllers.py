from schemas.slotSchemas import *
from sqlalchemy.ext.asyncio import AsyncSession
from config.models import Slot
from sqlalchemy.future import select
from fastapi import HTTPException


async def createSlot(slot: SlotRequestModel, db: AsyncSession):
    newSlot = Slot(
        Time=slot.Time,
        Status="Available",
    )
    db.add(newSlot)
    await db.commit()
    await db.refresh(newSlot)
    return newSlot


async def getAllSlots(db: AsyncSession):
    result = await db.execute(select(Slot))
    slots = result.scalars().all()
    if slots is None:
        raise HTTPException(status_code=404, detail="Slots not found")
    return slots


async def getSlot(id: int, db: AsyncSession):
    result = await db.execute(select(Slot).filter(Slot.Id == id))
    slot = result.scalars().first()
    if slot is None:
        raise HTTPException(status_code=404, detail="Slot not found")
    return slot


async def updateSlot(id: int, updatedSlot: SlotRequestModel, db: AsyncSession):
    result = await db.execute(select(Slot).filter(Slot.Id == id))
    slot = result.scalars().first()
    if slot is None:
        raise HTTPException(status_code=404, detail="Slot not found")

    slot.Time = updatedSlot.Time
    slot.Status = updatedSlot.Status
    await db.commit()
    await db.refresh(slot)
    return updatedSlot


async def deleteSlot(id: int, db: AsyncSession):
    result = await db.execute(select(Slot).filter(Slot.Id == id))
    slot = result.scalars().first()
    if slot is None:
        raise HTTPException(status_code=404, detail="Slot not found")

    await db.delete(slot)
    await db.commit()
    return {"message": "Slot deleted successfully"}
