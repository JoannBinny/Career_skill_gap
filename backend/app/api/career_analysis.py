from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import tempfile
import os

from app.services.resume_parser import extract_resume_text

from app.schemas.career_analysis import CareerAnalysisRequest
from app.services.career_analysis_service import analyze_career


router = APIRouter(
    prefix="/career-analysis",
    tags=["Career Analysis"],
)


@router.post("")
def run_career_analysis(request: CareerAnalysisRequest):
    try:
        result = analyze_career(
            resume_text=request.resume_text,
            job_role_id=request.job_role_id,
            courses_per_skill=request.courses_per_skill,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    return result

@router.post("/upload")
async def run_career_analysis_upload(
    resume: UploadFile = File(...),
    job_role_id: str = Form(...),
    courses_per_skill: int = Form(3),
):
    extension = os.path.splitext(resume.filename or "")[1].lower()

    if extension not in {".pdf", ".docx"}:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported.",
        )

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension,
        ) as temp_file:
            temp_path = temp_file.name
            temp_file.write(await resume.read())

        resume_text = extract_resume_text(temp_path)

        result = analyze_career(
            resume_text=resume_text,
            job_role_id=job_role_id,
            courses_per_skill=courses_per_skill,
        )

        result["filename"] = resume.filename

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)