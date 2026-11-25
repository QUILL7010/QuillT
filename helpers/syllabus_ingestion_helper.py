import os
import shutil
import uuid
from typing import BinaryIO


def save_file_to_disk(upload_dir: str, original_filename: str, file_obj: BinaryIO) -> str:
    os.makedirs(upload_dir, exist_ok=True)

    for existing_file in os.listdir(upload_dir):
        if existing_file.lower().endswith(f"_{original_filename.lower()}"):
            raise FileExistsError(f"File '{original_filename}' already exists in uploads.")

    unique_filename = f"{str(uuid.uuid4())[:8]}_{original_filename}"
    file_path = os.path.join(upload_dir, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file_obj, buffer)

    return file_path


def remove_file_safely(file_path: str) -> None:
    if os.path.exists(file_path):
        os.remove(file_path)


def clean_pdf_text(raw_text: str) -> str:
    return raw_text.replace("\x00", "").strip()