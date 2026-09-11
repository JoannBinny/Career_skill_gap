import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "courses.json"


def load_courses() -> list[dict]:
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_all_courses() -> list[dict]:
    return load_courses()


def get_course(course_id: str) -> dict | None:
    courses = load_courses()

    for course in courses:
        if course["id"] == course_id:
            return course

    return None


def get_courses_for_skill(skill: str) -> list[dict]:
    courses = load_courses()

    return [
        course
        for course in courses
        if skill.lower() in [course_skill.lower() for course_skill in course["skills"]]
    ]