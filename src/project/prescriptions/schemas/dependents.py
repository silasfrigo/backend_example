from pydantic import BaseModel
from pydantic import root_validator, EmailStr


class Base(BaseModel):
    id: int
    name: str


class Clinic(Base):

    @root_validator
    def place_attr_name(cls, values):
        prefix = 'clinic_'
        return {prefix + str(key): val for key, val in values.items()}


class Patient(Base):
    email: EmailStr
    phone: str

    @root_validator
    def place_attr_name(cls, values):
        prefix = 'patient_'
        return {prefix + str(key): val for key, val in values.items()}


class Physician(Base):
    crm: str

    @root_validator
    def place_attr_name(cls, values):
        prefix = 'physician_'
        return {prefix + str(key): val for key, val in values.items()}
