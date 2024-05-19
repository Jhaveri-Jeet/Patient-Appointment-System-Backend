from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.appointmentSchemas import *
from config.models import Appointment, Patient, Slot, Service
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException


async def createAppointment(appointment: AppointmentRequestModel, db: AsyncSession):
    # Exsisting Patient Check
    patientResult = await db.execute(
        select(Patient).filter(Patient.Id == appointment.PatientId)
    )
    patientCheck = patientResult.scalars().first()

    if patientCheck is None:
        raise HTTPException(status_code=400, detail="Patient not found")

    # Exsisting Slot Check
    slotResult = await db.execute(select(Slot).filter(Slot.Id == appointment.SlotId))
    slotCheck = slotResult.scalars().first()

    if slotCheck is None:
        raise HTTPException(status_code=400, detail="Slot not found")

    # Exsisting Service Check
    serviceResult = await db.execute(
        select(Service).filter(Service.Id == appointment.ServiceId)
    )
    serviceCheck = serviceResult.scalars().first()

    if serviceCheck is None:
        raise HTTPException(status_code=400, detail="Service not found")

    newAppointment = Appointment(
        Problem=appointment.Problem,
        Date=appointment.Date,
        PatientId=appointment.PatientId,
        ServiceId=appointment.ServiceId,
        SlotId=appointment.SlotId,
    )
    db.add(newAppointment)
    await db.commit()
    await db.refresh(newAppointment)

    return newAppointment


async def getAllAppointment(db: AsyncSession):
    smt = (
        select(Appointment)
        .options(joinedload(Appointment.patient))
        .options(joinedload(Appointment.service))
        .options(joinedload(Appointment.slot))
        .filter(Appointment.Status == "Pending")
        .order_by(Appointment.Id.desc())
    )

    result = await db.execute(smt)
    appointments = result.scalars().all()
    return appointments


async def getAllTodaysAppointment(db: AsyncSession):
    result = await db.execute(
        select(Appointment)
        .options(joinedload(Appointment.patient))
        .options(joinedload(Appointment.service))
        .options(joinedload(Appointment.slot))
        .filter(
            Appointment.Date == datetime.now().date(), Appointment.Status == "Pending"
        )
        .order_by(Appointment.Id.desc())
    )
    appointments = result.scalars().all()
    if appointments is None:
        raise HTTPException(status_code=404, detail="Appointments not found")
    return appointments


async def getAllAppointmentAccPatient(patientId: int, db: AsyncSession):
    result = await db.execute(
        select(Appointment)
        .options(joinedload(Appointment.patient))
        .options(joinedload(Appointment.service))
        .options(joinedload(Appointment.slot))
        .filter(Appointment.PatientId == patientId)
        .order_by(Appointment.Id.desc())
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
    appointmentCheck.Status = "Completed"
    await db.commit()
    await db.refresh(appointmentCheck)

    return appointmentCheck


async def totalPendingAppointment(db: AsyncSession):
    result = await db.execute(
        select(Appointment).filter(Appointment.Status == "Pending")
    )
    appointments = result.scalars().all()
    if appointments is None:
        raise HTTPException(status_code=404, detail="Appointments not found")

    return len(appointments)
