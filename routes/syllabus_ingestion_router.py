from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from db.postgres_db import get_db
from services.syllabus_ingestion_service import get_all_syllabi, process_and_save_syllabus

router = APIRouter(tags=["Syllabus"])


@router.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    try:
        pdf_record = process_and_save_syllabus(file, db)
    except FileExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "id": pdf_record.id,
        "filename": pdf_record.filename,
        "file_path": pdf_record.file_path,
        "page_count": pdf_record.page_count,
        "text_preview": pdf_record.extracted_text,
    }

@router.get("/pdfs")
def list_pdfs(db: Session = Depends(get_db)):
    return get_all_syllabi(db)