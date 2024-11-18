from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_mentor: Optional[bool] = False

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_mentor: bool

    class Config:
        orm_mode = True

class AppointmentCreate(BaseModel):
    mentor_id: int
    start_time: datetime
    end_time: datetime

class AppointmentOut(BaseModel):
    id: int
    user_id: int
    mentor_id: int
    start_time: datetime
    end_time: datetime
    video_link: Optional[str]

    class Config:
        orm_mode = True

class AvailabilityCreate(BaseModel):
    start_time: datetime
    end_time: datetime

class AvailabilityOut(BaseModel):
    id: int
    mentor_id: int
    start_time: datetime
    end_time: datetime

    class Config:
        orm_mode = True
