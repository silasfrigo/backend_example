from pydantic import BaseModel
from pydantic import constr


class Base(BaseModel):
    id: int


class Clinic(Base):
    pass


class Patient(Base):
    pass


class Physician(Base):
    pass


class CreatePrescription(BaseModel):
    clinic: Clinic
    physician: Physician
    patient: Patient
    text: constr(min_length=1, max_length=255)

    class Config:
        orm_mode = True


class ReadPrescription(CreatePrescription):
    id: int

    class Config:
        orm_mode = True
