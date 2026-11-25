from fastapi import FastAPI
from db.postgres_db import Base, engine
from models.syllabus import Syllabus  # Ensures table is registered
from routes.syllabus_ingestion_router import router as syllabus_upload

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(syllabus_upload)