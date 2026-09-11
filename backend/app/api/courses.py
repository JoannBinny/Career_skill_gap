from fastapi import APIRouter, HTTPException

from app.services.course_service import (
    get_all_courses,
    get_course,
    get_courses_for_skill,
)


router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("")
def list_courses():
    return {"courses": get_all_courses()}


@router.get("/skill/{skill}")
def list_courses_for_skill(skill: str):
    return {
        "skill": skill,
        "courses": get_courses_for_skill(skill),
    }


@router.get("/{course_id}")
def get_course_details(course_id: str):
    course = get_course(course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    return course