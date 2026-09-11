from app.ml.course_ranker import rank_courses_hybrid
from app.services.course_service import get_all_courses
from app.services.skill_gap_service import calculate_skill_gap


def add_course_explanation(
    course: dict,
    missing_skill: str,
) -> dict:
    """Add a human-readable explanation to a course recommendation."""

    if course["explicit_match"]:
        explanation = (
            f"Directly teaches the missing skill '{missing_skill}'. "
            f"Semantic similarity: {course['similarity']:.4f}. "
            f"Hybrid score: {course['final_score']:.4f}."
        )
    else:
        explanation = (
            f"Semantically related to the missing skill '{missing_skill}', "
            f"but does not explicitly list it as a taught skill. "
            f"Semantic similarity: {course['similarity']:.4f}."
        )

    return {
        **course,
        "explanation": explanation,
    }


def generate_course_recommendations(
    resume_skills: list[str],
    job_role_id: str,
    courses_per_skill: int = 3,
) -> dict:
    """
    Generate explainable course recommendations for skills
    missing from a user's target job role.
    """

    skill_gap = calculate_skill_gap(
        user_skills=resume_skills,
        job_role_id=job_role_id,
    )

    missing_skills = skill_gap["missing_skills"]
    courses = get_all_courses()

    recommendations = []

    for skill in missing_skills:
        ranked_courses = rank_courses_hybrid(
            skill=skill,
            courses=courses,
            top_k=len(courses),
        )

        direct_courses = [
            add_course_explanation(course, skill)
            for course in ranked_courses
            if course["explicit_match"]
        ][:courses_per_skill]

        related_courses = [
            add_course_explanation(course, skill)
            for course in ranked_courses
            if not course["explicit_match"]
        ][:courses_per_skill]

        recommendations.append(
            {
                "missing_skill": skill,
                "direct_recommendations": direct_courses,
                "related_recommendations": related_courses,
            }
        )

    return {
        "job_role": skill_gap["job_role"],
        "match_percentage": skill_gap["match_percentage"],
        "matched_skills": skill_gap["matched_skills"],
        "missing_skills": missing_skills,
        "recommendations": recommendations,
    }