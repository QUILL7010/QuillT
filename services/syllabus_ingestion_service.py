import pymupdf
from fastapi import UploadFile
from sqlalchemy.orm import Session

from helpers.syllabus_ingestion_helper import clean_pdf_text, remove_file_safely, save_file_to_disk
from models.syllabus import Syllabus

UPLOAD_DIR = "uploads"


def process_and_save_syllabus(file: UploadFile, db: Session) -> Syllabus:
    file_path = save_file_to_disk(UPLOAD_DIR, file.filename, file.file)

    try:
        with pymupdf.open(file_path) as doc:
            page_count = len(doc)
            raw_text = "\n".join(page.get_text() for page in doc)
            extracted_text = clean_pdf_text(raw_text)
    except Exception as e:
        remove_file_safely(file_path)
        raise ValueError(f"Could not read PDF: {str(e)}")

    pdf_record = Syllabus(
        filename=file.filename,
        file_path=file_path,
        page_count=page_count,
        extracted_text=extracted_text,
    )
    db.add(pdf_record)
    db.commit()
    db.refresh(pdf_record)
    return pdf_record


def get_all_syllabi(db: Session) -> list[Syllabus]:
    return db.query(Syllabus).all()