from fastapi import APIRouter, HTTPException

from app.schemas.recommendation import CourseRecommendationRequest
from app.services.recommendation_service import generate_course_recommendations


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.post("")
def get_course_recommendations(
    request: CourseRecommendationRequest,
):
    try:
        result = generate_course_recommendations(
            resume_skills=request.resume_skills,
            job_role_id=request.job_role_id,
            courses_per_skill=request.courses_per_skill,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    return result