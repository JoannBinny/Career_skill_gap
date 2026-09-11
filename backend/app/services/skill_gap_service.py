from app.services.job_role_service import get_job_role


def calculate_skill_gap(
    user_skills: list[str],
    job_role_id: str,
) -> dict:
    job_role = get_job_role(job_role_id)

    if job_role is None:
        raise ValueError("Job role not found")

    required_skills = job_role["skills"]

    user_skill_set = {skill.lower() for skill in user_skills}

    matched_skills = []
    missing_skills = []

    for skill in required_skills:
        if skill.lower() in user_skill_set:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    total_required = len(required_skills)
    matched_count = len(matched_skills)

    match_percentage = (
        (matched_count / total_required) * 100
        if total_required > 0
        else 0
    )

    return {
        "job_role": {
            "id": job_role["id"],
            "title": job_role["title"],
        },
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": round(match_percentage, 2),
    }
