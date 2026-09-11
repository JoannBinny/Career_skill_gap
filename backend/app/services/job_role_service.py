import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "job_roles.json"


def load_job_roles() -> list[dict]:
    """Load job roles from the development dataset."""
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_all_job_roles() -> list[dict]:
    """Return all available job roles."""

    return load_job_roles()


def get_job_role(job_role_id: str) -> dict | None:
    """Return a job role by its ID."""

    job_roles = load_job_roles()

    for job_role in job_roles:
        if job_role["id"] == job_role_id:
            return job_role

    return None
