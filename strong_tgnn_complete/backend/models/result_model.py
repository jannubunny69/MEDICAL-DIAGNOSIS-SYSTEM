from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from .database import Base
import datetime
class InferenceResult(Base):
    __tablename__ = "inference_results"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"), index=True)
    disease = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    result_json = Column(Text)
    def to_dict(self): return {"patient_id": self.patient_id, "disease": self.disease, "timestamp": str(self.timestamp), "result": self.result_json}