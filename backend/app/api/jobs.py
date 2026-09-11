from fastapi import APIRouter, HTTPException
from app.services.skill_gap_service import calculate_skill_gap

from app.schemas.skill_gap import SkillGapRequest
from app.ml.skill_extractor import extract_skills

from app.services.job_role_service import (
    get_all_job_roles,
    get_job_role,
)


router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("")
def list_job_roles():
    """Return all available job roles."""

    return {
        "job_roles": get_all_job_roles()
    }


@router.get("/{job_role_id}")
def get_job_role_details(job_role_id: str):
    """Return details and required skills for a job role."""

    job_role = get_job_role(job_role_id)

    if job_role is None:
        raise HTTPException(
            status_code=404,
            detail="Job role not found",
        )

    return job_role

@router.post("/skill-gap")
def analyze_resume_skill_gap(request: SkillGapRequest):
    user_skills = extract_skills(request.resume_text)

    try:
        result = calculate_skill_gap(
            user_skills=user_skills,
            job_role_id=request.job_role_id,
        )
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

    result["extracted_skills"] = user_skills

    return result

@router.post("/{job_role_id}/skill-gap")
def analyze_skill_gap(job_role_id: str, user_skills: list[str]):
    try:
        return calculate_skill_gap(user_skills, job_role_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

