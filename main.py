from fastapi import FastAPI
from db.postgres_db import Base, engine
from models.ingestion import Syllabus  # Ensures table is registered
from routes.syllabus_ingestion import router as syllabus_upload

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(syllabus_upload)