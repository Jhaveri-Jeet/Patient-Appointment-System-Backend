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
):
    appointment = await getAllAppointmentAccPatient(patientId, db)
    return appointment


@router.get("/todaysAppointments", tags=["appointment"])
async def getAllTodaysAppointmentAsync(
    db: AsyncSession = Depends(getDb),
):
    appointments = await getAllTodaysAppointment(db)
    return appointments


@router.get("/appointment", tags=["appointment"])
async def getAllAppointmentAsync(
    db: AsyncSession = Depends(getDb),
):
    appointment = await getAllAppointment(db)
    return appointment


@router.post("/prescription/{appointmentId}", tags=["appointment"])
async def createPrescriptionAsync(
    appointmentId: int,
    prescription: PrescriptionRequestModel,
    db: AsyncSession = Depends(getDb),
) -> AppointmentResponseModel:
    newPrescription = await createPrescription(appointmentId, prescription, db)
    return newPrescription


@router.get("/totalPendingAppointment", tags=["appointment"])
async def totalPendingAppointmentAsync(db: AsyncSession = Depends(getDb)):
    total = await totalPendingAppointment(db)
    return total


@router.post("/createPaymentLink", tags=["appointment"])
async def createPaymentLinkAsync(payment: PaymentLinkRequestModel):
    paymentLink = await create_payment_link_for_appointment(payment)
    return paymentLink
