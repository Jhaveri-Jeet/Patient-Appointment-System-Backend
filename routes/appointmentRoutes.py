from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import SessionLocal
from schemas.appointmentSchemas import *
from controllers.appointmentController import *

router = APIRouter()


def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/appointment", tags=["appointment"])
async def createAppointmentAsync(
    appointment: AppointmentRequestModel, db: AsyncSession = Depends(getDb)
) -> AppointmentResponseModel:
    newAppointment = await createAppointment(appointment, db)
    return newAppointment


@router.get("/appointment/{patientId}", tags=["appointment"])
async def getAllAppointmentAccPatientAsync(
    patientId: int, db: AsyncSession = Depends(getDb)
) -> list[AppointmentResponseModel]:
    appointment = await getAllAppointmentAccPatient(patientId, db)
    return appointment


@router.post("/prescription/{appointmentId}", tags=["appointment"])
async def createPrescriptionAsync(
    appointmentId: int,
    prescription: PrescriptionRequestModel,
    db: AsyncSession = Depends(getDb),
) -> AppointmentResponseModel:
    newPrescription = await createPrescription(appointmentId, prescription, db)
    return newPrescription
