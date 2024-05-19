from pydantic import BaseModel
from datetime import date


class AppointmentRequestModel(BaseModel):
    Problem: str
    Date: date
    PatientId: int
    ServiceId: int
    SlotId: int

    class Config:
        orm_mode = True


class AppointmentResponseModel(BaseModel):
    Id: int
    Problem: str
    Date: date
    Prescription: str | None
    PatientId: int
    ServiceId: int
    SlotId: int

    class Config:
        orm_mode = True


class PrescriptionRequestModel(BaseModel):
    Prescription: str

    class Config:
        orm_mode = True
