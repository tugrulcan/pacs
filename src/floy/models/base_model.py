from pydantic import Extra
from sqlmodel import SQLModel


class BaseModel(SQLModel):
    __abstract__ = True

    class Config:
        extra = Extra.forbid
