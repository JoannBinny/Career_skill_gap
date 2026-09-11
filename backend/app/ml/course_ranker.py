from app.ml.semantic_skill_matcher import model
from sklearn.metrics.pairwise import cosine_similarity


def rank_courses_for_skill(
    skill: str,
    courses: list[dict],
    top_k: int = 5,
) -> list[dict]:
    if not skill.strip() or not courses:
        return []

    course_texts = [
        f"{course['title']}. {course['description']}"
        for course in courses
    ]

    skill_embedding = model.encode(
        [skill],
        normalize_embeddings=True,
    )

    course_embeddings = model.encode(
        course_texts,
        normalize_embeddings=True,
    )

    similarities = cosine_similarity(
        skill_embedding,
        course_embeddings,
    )[0]

    results = []

    for course, similarity in zip(courses, similarities):
        results.append({
            "course_id": course["id"],
            "title": course["title"],
            "provider": course["provider"],
            "description": course["description"],
            "skills": course["skills"],
            "url": course["url"],
            "similarity": round(float(similarity), 4),
        })

    results.sort(
        key=lambda result: result["similarity"],
        reverse=True,
    )

    return results[:top_k]

def rank_courses_hybrid(
    skill: str,
    courses: list[dict],
    top_k: int = 5,
    explicit_weight: float = 0.7,
    semantic_weight: float = 0.3,
) -> list[dict]:
    semantic_results = rank_courses_for_skill(
        skill=skill,
        courses=courses,
        top_k=len(courses),
    )

    for result in semantic_results:
        explicit_match = any(
            course_skill.lower() == skill.lower()
            for course_skill in result["skills"]
        )

        explicit_score = 1.0 if explicit_match else 0.0

        final_score = (
            explicit_weight * explicit_score
            + semantic_weight * result["similarity"]
        )

        result["explicit_match"] = explicit_match
        result["explicit_score"] = explicit_score
        result["final_score"] = round(final_score, 4)

    semantic_results.sort(
        key=lambda result: result["final_score"],
        reverse=True,
    )

    return semantic_results[:top_k]