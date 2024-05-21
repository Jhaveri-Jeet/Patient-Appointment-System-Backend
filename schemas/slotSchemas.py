from pydantic import BaseModel


class SlotRequestModel(BaseModel):
    Time: str
    Status: str | None = None

    class Config:
        orm_mode = True


class SlotResponseModel(BaseModel):
    Id: int
    Time: str
    Status: str

    class Config:
        orm_mode = True
