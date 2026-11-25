from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from db import Base

class Syllabus(Base):
    __tablename__ = "pdf_documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    page_count = Column(Integer, nullable=False)
    extracted_text = Column(Text, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())