from sqlalchemy.ext.asyncio import AsyncSession
from schemas.patientSchemas import *
from config.models import Patient
from sqlalchemy.future import select
from fastapi import HTTPException
import bcrypt


async def createPatient(patient: PatientRequestModel, db: AsyncSession):
    result = await db.execute(select(Patient).filter(Patient.Email == patient.Email))
    emailCheck = result.scalars().first()

    if emailCheck is not None:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = bcrypt.hashpw(patient.Password.encode("utf-8"), bcrypt.gensalt())

    newPatient = Patient(
        Name=patient.Name,
        Mobile=patient.Mobile,
        Email=patient.Email,
        Password=hashed_password.decode("utf-8"),
        Address=patient.Address,
        Gender=patient.Gender,
    )
    db.add(newPatient)
    await db.commit()
    await db.refresh(newPatient)
    return newPatient


async def authenticatePatient(patient: PatientAuthModel, db: AsyncSession):
    result = await db.execute(select(Patient).filter(Patient.Email == patient.Email))
    authPatient = result.scalars().first()
    if authPatient is None:
        raise HTTPException(status_code=401, detail="Invalid email")

    if not bcrypt.checkpw(
        patient.Password.encode("utf-8"), authPatient.Password.encode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="Invalid password")

    return authPatient


async def getPatient(id: int, db: AsyncSession):
    result = await db.execute(select(Patient).filter(Patient.Id == id))
    patient = result.scalars().first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patient


async def getAllPatient(db: AsyncSession):
    results = await db.execute(select(Patient))
    patients = results.scalars().all()
    if patients is None:
        raise HTTPException(status_code=404, detail="Patients not found")

    return patients


async def updatePatient(id: int, newPatient: PatientRequestModel, db: AsyncSession):
    result = await db.execute(select(Patient).filter(Patient.Id == id))
    patient = result.scalars().first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    hashed_password = bcrypt.hashpw(newPatient.Password.encode("utf-8"), bcrypt.gensalt())

    patient.Name = newPatient.Name
    patient.Mobile = newPatient.Mobile
    patient.Email = newPatient.Email
    patient.Password = hashed_password.decode("utf-8"),
    patient.Address = newPatient.Address
    patient.Gender = newPatient.Gender
    await db.commit()
    await db.refresh(patient)
    return patient


async def deletePatient(id: int, db: AsyncSession):
    result = await db.execute(select(Patient).filter(Patient.Id == id))
    patient = result.scalars().first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    await db.delete(patient)
    await db.commit()
    return {"message": "Patient deleted successfully"}
