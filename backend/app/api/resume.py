import os
import tempfile

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.ml.hybrid_skill_analyzer import analyze_skills
from app.services.resume_parser import extract_resume_text


router = APIRouter(prefix="/resume", tags=["Resume"])


ALLOWED_EXTENSIONS = {".pdf", ".docx"}


@router.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    filename = file.filename or ""
    extension = os.path.splitext(filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported.",
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension,
        ) as temp_file:
            temp_file.write(contents)
            temp_path = temp_file.name

        text = extract_resume_text(temp_path)

        if not text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract any text from the resume.",
            )

        analysis = analyze_skills(text)

        return {        
            "filename": file.filename,
            "text": text,
            "skills": analysis["explicit_skills"],
            "semantic_matches": analysis["semantic_matches"],
            "inferred_skills": analysis["inferred_matches"],
        }
        

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)