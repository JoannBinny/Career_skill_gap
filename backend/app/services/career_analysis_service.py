from app.ml.skill_extractor import extract_skills
from app.services.recommendation_service import generate_course_recommendations


def analyze_career(
    resume_text: str,
    job_role_id: str,
    courses_per_skill: int = 3,
) -> dict:
    """
    Analyze a resume against a target job role
    and generate course recommendations.
    """

    extracted_skills = extract_skills(resume_text)

    recommendations = generate_course_recommendations(
        resume_skills=extracted_skills,
        job_role_id=job_role_id,
        courses_per_skill=courses_per_skill,
    )

    return {
        "extracted_skills": extracted_skills,
        **recommendations,
    }