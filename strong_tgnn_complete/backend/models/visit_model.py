from sqlalchemy import Column, Integer, String, Text, ForeignKey
from .database import Base
class Visit(Base):
    __tablename__ = "visits"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"), index=True)
    disease = Column(String, index=True)
    visit_date = Column(String)
    mri_path = Column(String, nullable=True)
    ct_path = Column(String, nullable=True)
    pet_path = Column(String, nullable=True)
    notes_path = Column(String, nullable=True)
    genomics_path = Column(String, nullable=True)
    pathology_path = Column(String, nullable=True)
    file_paths = Column(Text, nullable=True)
    def to_dict(self): return {"id": self.id, "patient_id": self.patient_id, "disease": self.disease, "visit_date": self.visit_date, "file_paths": self.file_paths or '{}'}