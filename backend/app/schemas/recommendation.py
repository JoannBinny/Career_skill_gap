from pydantic import BaseModel


class CourseRecommendationRequest(BaseModel):
    resume_skills: list[str]
    job_role_id: str
    courses_per_skill: int = 3