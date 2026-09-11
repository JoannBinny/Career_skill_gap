import re

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.ml.skill_taxonomy import SKILL_TAXONOMY


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def get_all_skills() -> list[str]:
    skills = []

    for category_skills in SKILL_TAXONOMY.values():
        skills.extend(category_skills)

    return skills


def split_into_chunks(text: str) -> list[str]:
    """
    Split resume text into meaningful sentence-like chunks.

    Handles both normal sentences and resume bullet points.
    """

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    chunks = []

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        # Split long lines into sentences where appropriate.
        sentences = re.split(r"(?<=[.!?])\s+", line)

        for sentence in sentences:
            sentence = sentence.strip()

            if len(sentence) >= 15:
                chunks.append(sentence)

    return chunks


def calculate_skill_similarity(
    text: str,
    skills: list[str] | None = None,
    top_k: int = 10,
) -> list[dict]:
    """
    Compare individual resume chunks against skill names.

    Returns the strongest semantic evidence for each skill.
    """

    if not text.strip():
        return []

    if skills is None:
        skills = get_all_skills()

    chunks = split_into_chunks(text)

    if not chunks:
        return []

    chunk_embeddings = model.encode(
        chunks,
        normalize_embeddings=True,
    )

    skill_embeddings = model.encode(
        skills,
        normalize_embeddings=True,
    )

    similarity_matrix = cosine_similarity(
        chunk_embeddings,
        skill_embeddings,
    )

    results = []

    for skill_index, skill in enumerate(skills):
        skill_scores = similarity_matrix[:, skill_index]

        best_chunk_index = skill_scores.argmax()
        best_score = float(skill_scores[best_chunk_index])

        results.append(
            {
                "skill": skill,
                "similarity": best_score,
                "evidence": chunks[best_chunk_index],
            }
        )

    results.sort(
        key=lambda result: result["similarity"],
        reverse=True,
    )

    return results[:top_k]