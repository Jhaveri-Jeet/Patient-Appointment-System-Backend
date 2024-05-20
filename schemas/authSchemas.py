from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class AdminRequestModel(BaseModel):
    Username: str
    HashPassword: str
    FullName: str | None = None
    Email: str | None = None
    Address: str | None = None
    Degree: str | None = None

    class Config:
        orm_mode = True

class AdminResponseModel(BaseModel):
    Id: int
    Username: str
    HashPassword: str
    FullName: str | None
    Email: str | None
    Address: str | None
    Degree: str | None

    class Config:
        orm_mode = True
