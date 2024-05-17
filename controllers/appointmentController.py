from sqlalchemy.ext.asyncio import AsyncSession
from schemas.appointmentSchemas import *
from config.models import Appointment, Patient
from sqlalchemy.future import select
from fastapi import HTTPException


async def createAppointment(appointment: AppointmentRequestModel, db: AsyncSession):
    result = await db.execute(
        select(Patient).filter(Patient.Id == appointment.PatientId)
    )

    patientCheck = result.scalars().first()
    if patientCheck is None:
        raise HTTPException(status_code=400, detail="Patient not found")

    newAppointment = Appointment(
        Problem=appointment.Problem,
        Date=appointment.Date,
        PatientId=appointment.PatientId,
    )
    db.add(newAppointment)
    await db.commit()
    await db.refresh(newAppointment)

    return newAppointment


async def getAllAppointmentAccPatient(patientId: int, db: AsyncSession):
    result = await db.execute(
        select(Appointment).filter(Appointment.PatientId == patientId)
    )
    appointments = result.scalars().all()
    if appointments is None:
        raise HTTPException(status_code=404, detail="Appointments not found")

    return appointments


async def createPrescription(
    appoinmentId: int, prescription: PrescriptionRequestModel, db: AsyncSession
):
    result = await db.execute(
        select(Appointment).filter(Appointment.Id == appoinmentId)
    )
    appointmentCheck = result.scalars().first()
    if appointmentCheck is None:
        raise HTTPException(status_code=400, detail="Appointment not found")

    appointmentCheck.Prescription = prescription.Prescription
    await db.commit()
    await db.refresh(appointmentCheck)

    return appointmentCheck
