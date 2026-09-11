from app.ml.skill_extractor import extract_skills
from app.ml.semantic_skill_matcher import calculate_skill_similarity


def analyze_skills(text: str, semantic_top_k: int = 10) -> dict:
    """
    Analyze resume text using both:
    1. Explicit keyword/phrase-based skill extraction
    2. Semantic similarity using sentence embeddings

    Semantic matches are evidence of relevance, not confirmed skills.
    """

    explicit_skills = extract_skills(text)

    semantic_matches = calculate_skill_similarity(text)[:semantic_top_k]

    # Remove skills that were already explicitly detected.
    inferred_matches = [
        match
        for match in semantic_matches
        if match["skill"] not in explicit_skills
    ]

    return {
        "explicit_skills": explicit_skills,
        "semantic_matches": semantic_matches,
        "inferred_matches": inferred_matches,
    }