from pydantic import BaseModel


class CareerAnalysisRequest(BaseModel):
    resume_text: str
    job_role_id: str
    courses_per_skill: int = 3