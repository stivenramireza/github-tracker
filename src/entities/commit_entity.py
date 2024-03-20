from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Commit:
    id: Optional[str]
    repo_name: str
    commit_id: str
    commit_message: str
    author_username: str
    author_email: str
    payload: str
    created_at: datetime
    updated_at: datetime
