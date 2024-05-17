from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class AdminModel(BaseModel):
    Username: str
    HashPassword: str

    class Config:
        orm_mode = True
