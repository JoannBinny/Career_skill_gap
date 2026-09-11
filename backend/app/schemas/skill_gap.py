from pydantic import BaseModel


class SkillGapRequest(BaseModel):
    resume_text: str
    job_role_id: str