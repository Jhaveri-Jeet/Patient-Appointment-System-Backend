from schemas.serviceSchemas import *
from sqlalchemy.ext.asyncio import AsyncSession
from config.models import Service
from sqlalchemy.future import select
from fastapi import HTTPException


async def createService(service: ServiceRequestModel, db: AsyncSession):
    service = Service(
        Name=service.Name, Description=service.Description, Price=service.Price
    )
    db.add(service)
    await db.commit()
    await db.refresh(service)
    return service


async def getAllServices(db: AsyncSession):
    result = await db.execute(select(Service))
    services = result.scalars().all()
    if services is None:
        raise HTTPException(status_code=404, detail="Services not found")
    return services


async def getService(id: int, db: AsyncSession):
    result = await db.execute(select(Service).filter(Service.Id == id))
    service = result.scalars().first()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


async def updateService(id: int, newService: ServiceRequestModel, db: AsyncSession):
    result = await db.execute(select(Service).filter(Service.Id == id))
    service = result.scalars().first()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    service.Name = newService.Name
    service.Description = newService.Description
    service.Price = newService.Price
    await db.commit()
    await db.refresh(service)
    return service


async def deleteService(id: int, db: AsyncSession):
    result = await db.execute(select(Service).filter(Service.Id == id))
    service = result.scalars().first()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    await db.delete(service)
    await db.commit()
    return {"message": "Service deleted successfully"}
