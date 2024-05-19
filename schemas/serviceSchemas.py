from pydantic import BaseModel


class ServiceRequestModel(BaseModel):
    Name: str
    Description: str
    Price: int

    class Config:
        orm_mode = True


class ServiceResponseModel(BaseModel):
    Id: int
    Name: str
    Description: str
    Price: int

    class Config:
        orm_mode = True
