"""In-memory storage for users and jobs."""

from datetime import datetime
from typing import Dict, Optional

from app.models.user import User
from app.models.job import Job, JobStatus


class Storage:
    """In-memory storage implementation."""

    def __init__(self):
        self._jobs: Dict[str, Job] = {}
        self._users: Dict[str, User] = {}
        self._initialize_default_data()

    def _initialize_default_data(self):
        """Initialize storage with default test data."""
        self._jobs["test_job"] = Job(
            created_at=datetime.now(), status=JobStatus.SUCCESS
        )
        self._users["user_1"] = User(
            phone_number="+79001234567", email="ivan@gmail.com", name="Ivan"
        )
        self._users["user_2"] = User(telegram_id="987654321", name="Divan")

    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self._users.get(user_id)

    def user_exists(self, user_id: str) -> bool:
        """Check if user exists."""
        return user_id in self._users

    def get_job(self, job_id: str) -> Optional[Job]:
        """Get job by ID."""
        return self._jobs.get(job_id)

    def create_job(self, job_id: str, job: Job) -> None:
        """Create a new job."""
        self._jobs[job_id] = job

    def update_job_status(self, job_id: str, status: JobStatus) -> None:
        """Update job status."""
        if job_id in self._jobs:
            self._jobs[job_id].status = status


# Global storage instance
storage = Storage()
