from sqlalchemy import Column, String, Integer
from .database import Base
class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    sex = Column(String, nullable=True)
    def to_dict(self): return {"patient_id": self.patient_id, "name": self.name, "age": self.age, "sex": self.sex}