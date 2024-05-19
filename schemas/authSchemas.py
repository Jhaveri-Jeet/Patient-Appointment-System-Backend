from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class AdminRequestModel(BaseModel):
    Username: str
    HashPassword: str
    Email: str
    Address: str
    Degree: str

    class Config:
        orm_mode = True