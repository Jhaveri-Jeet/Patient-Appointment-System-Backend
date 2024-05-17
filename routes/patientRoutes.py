from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import SessionLocal
from schemas.patientSchemas import *
from schemas.authSchemas import *
from controllers.patientControllers import *
from fastapi.security import OAuth2PasswordRequestForm
from config.auth import createAccessToken

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


@router.post("/token")
async def loginForAccessToken(
    formData: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(getDb)
) -> Token:
    patient = await authenticatePatient(formData.username, formData.password, db)
    if not patient:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = createAccessToken({"sub": patient.Email, "id": patient.Id})
    return {"access_token": token, "token_type": "bearer"}


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
