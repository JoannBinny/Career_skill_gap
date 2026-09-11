import re

from app.ml.skill_taxonomy import SKILL_TAXONOMY, SKILL_ALIASES


def normalize_text(text: str) -> str:
    """Normalize text for matching without changing the original text."""

    text = text.lower()

    # Normalize common separators
    text = text.replace("&", " and ")
    text = re.sub(r"[/|]", " ", text)

    # Collapse whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def build_skill_lookup() -> dict[str, str]:
    """Create a lookup from normalized skill names to canonical names."""

    lookup = {}

    for skills in SKILL_TAXONOMY.values():
        for skill in skills:
            lookup[normalize_text(skill)] = skill

    for alias, canonical_skill in SKILL_ALIASES.items():
        lookup[normalize_text(alias)] = canonical_skill

    return lookup


SKILL_LOOKUP = build_skill_lookup()


def extract_skills(text: str) -> list[str]:
    """
    Extract recognized skills from resume text.

    Returns canonical skill names with duplicates removed.
    """

    normalized_text = normalize_text(text)

    found_skills = set()

    # Check longer phrases first so that:
    # "Data Structures and Algorithms"
    # is matched before smaller components.
    sorted_skills = sorted(
        SKILL_LOOKUP.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    )

    for normalized_skill, canonical_skill in sorted_skills:
        pattern = rf"(?<!\w){re.escape(normalized_skill)}(?!\w)"

        if re.search(pattern, normalized_text):
            found_skills.add(canonical_skill)

    return sorted(found_skills)