from sqlalchemy import Column, Integer, String
from connections import Base


class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    clinic_id = Column(Integer, nullable=False)
    physician_id = Column(Integer, nullable=False)
    patient_id = Column(Integer, nullable=False)
    text = Column(String(255), nullable=False)
