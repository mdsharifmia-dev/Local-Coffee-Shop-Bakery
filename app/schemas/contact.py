from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ContactCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    subject: str = Field(..., min_length=2, max_length=200)
    message: str = Field(..., min_length=5, max_length=2000)


class ContactResponse(BaseModel):
    id: int
    name: str
    email: str
    subject: str
    message: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ContactSuccessResponse(BaseModel):
    success: bool = True
    message: str = "Thank you! Your message has been received. We will get back to you shortly."
