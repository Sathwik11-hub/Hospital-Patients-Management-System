from pydantic import BaseModel
from typing import Optional


class PatientBase(BaseModel):
    name: str
    age: int
    gender: str
    phone: int
    address: Optional[str] = None
    disease: str
    admission_days: int


class PatientCreate(PatientBase):
    pass


class PatientResponse(PatientBase):
    id: int

    class Config:
        from_attributes = True
