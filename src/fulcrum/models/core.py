from typing import Optional
from datetime import datetime

from fulcrum.db.utils import PyObjectId
from pydantic import BaseModel, validator, Field, root_validator


class CoreModel(BaseModel):
    """
    Any common logic to be shared by all models goes here
    """
    pass


class DateTimeModelMixin(BaseModel):
    created_at: datetime
    updated_at: Optional[datetime]

    @validator("created_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.now()

    @root_validator
    def number_validator(cls, values) -> datetime:
        if values["updated_at"]:
            values["updated_at"] = datetime.now()
        else:
            values["updated_at"] = values["created_at"]
        return values


class IDModelMixin(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
