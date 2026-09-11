from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.api.resume import router as resume_router
from app.api.health import router as health_router
from app.core.config import settings
from app.api.jobs import router as jobs_router
from app.api.courses import router as courses_router
from app.api.recommendations import router as recommendations_router
from app.api.career_analysis import router as career_analysis_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for the AI Career Skill Gap & Course Recommendation System.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(resume_router, prefix="/api")
app.include_router(jobs_router, prefix="/api")
app.include_router(courses_router, prefix="/api")
app.include_router(recommendations_router, prefix="/api")
app.include_router(career_analysis_router, prefix="/api")

@app.get("/", tags=["Root"])
def root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/api/health",
    }
