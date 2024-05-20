from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class AdminRequestModel(BaseModel):
    Username: str
    HashPassword: str
    Email: str | None = None
    Address: str | None = None
    Degree: str | None = None

    class Config:
        orm_mode = True
