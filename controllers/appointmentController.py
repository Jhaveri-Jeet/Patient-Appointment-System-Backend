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
