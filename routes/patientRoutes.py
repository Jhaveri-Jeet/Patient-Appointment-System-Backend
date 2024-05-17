from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import SessionLocal
from schemas.patientSchemas import *
from controllers.patientControllers import *

router = APIRouter()


def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/patient")
async def createPatientAsync(
    patient: PatientRequestModel, db: AsyncSession = Depends(getDb)
) -> PatientResponseModel:
    newPatient = await createPatient(patient, db)
    return newPatient


@router.post("/authenticatePatient")
async def autheticatePatientAsync(
    patient: PatientAuthModel, db: AsyncSession = Depends(getDb)
) -> PatientResponseModel:
    patient = await authenticatePatient(patient, db)
    return patient


@router.get("/patient/{patientId}")
async def getPatientAsync(
    patientId: int, db: AsyncSession = Depends(getDb)
) -> PatientResponseModel:
    patient = await getPatient(patientId, db)
    return patient


@router.get("/patient")
async def getAllPatientAsync(
    db: AsyncSession = Depends(getDb),
) -> list[PatientResponseModel]:
    patients = await getAllPatient(db)
    return patients


@router.put("/patient/{patientId}")
async def updatePatientAsync(
    patientId: int, newPatient: PatientRequestModel, db: AsyncSession = Depends(getDb)
) -> PatientResponseModel:
    patient = await updatePatient(patientId, newPatient, db)
    return patient


@router.delete("/patient/{patientId}")
async def deletePatientAsync(patientId: int, db: AsyncSession = Depends(getDb)):
    patient = await deletePatient(patientId, db)
    return patient
