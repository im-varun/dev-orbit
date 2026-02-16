from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Project(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    created_at: int = Field(default_factory=lambda: int(datetime.now().timestamp()))

class Task(BaseModel):
    id: Optional[str] = None
    project_id: str
    title: str
    status: str = "todo"