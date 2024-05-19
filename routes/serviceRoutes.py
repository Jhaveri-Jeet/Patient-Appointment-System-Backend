from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import SessionLocal
from schemas.serviceSchemas import *
from controllers.serviceControllers import *


router = APIRouter()


def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/service", tags=["service"])
async def createServiceAsync(
    service: ServiceRequestModel, db: AsyncSession = Depends(getDb)
) -> ServiceResponseModel:
    newService = await createService(service, db)
    return newService


@router.get("/service", tags=["service"])
async def getAllServiceAsync(
    db: AsyncSession = Depends(getDb),
) -> list[ServiceResponseModel]:
    services = await getAllServices(db)
    return services


@router.get("/service/{serviceId}", tags=["service"])
async def getServiceAsync(
    serviceId: int, db: AsyncSession = Depends(getDb)
) -> ServiceResponseModel:
    service = await getService(serviceId, db)
    return service


@router.put("/service/{serviceId}", tags=["service"])
async def updateServiceAsync(
    serviceId: int,
    updatedService: ServiceRequestModel,
    db: AsyncSession = Depends(getDb),
) -> ServiceResponseModel:
    service = await updateService(serviceId, updatedService, db)
    return service


@router.delete("/service/{serviceId}", tags=["service"])
async def deleteSerivceAsync(serviceId: int, db: AsyncSession = Depends(getDb)):
    service = await deleteService(serviceId, db)
    return service
