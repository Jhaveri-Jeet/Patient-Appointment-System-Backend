from pydantic import BaseModel
from datetime import date


class AppointmentRequestModel(BaseModel):
    Problem: str
    Date: date
    PatientId: int

    class Config:
        orm_mode = True


class AppointmentResponseModel(BaseModel):
    Id: int
    Problem: str
    Date: date
    PatientId: int

    class Config:
        orm_mode = True
