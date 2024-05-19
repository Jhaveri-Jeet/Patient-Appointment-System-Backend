from pydantic import BaseModel


class PatientRequestModel(BaseModel):
    Name: str
    Mobile: str
    Email: str
    Address: str
    Gender: str
    BloodGroup: str

    class Config:
        orm_mode: True


class PatientResponseModel(BaseModel):
    Id: int
    Name: str
    Mobile: str
    Email: str
    Address: str
    Gender: str
    BloodGroup: str

    class Config:
        orm_mode: True