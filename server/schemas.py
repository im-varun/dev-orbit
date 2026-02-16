from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    status: str = "todo"
    project_id: str

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: str

    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: str
    created_at: int = Field(default_factory=lambda: int(datetime.now().timestamp()))

    class Config:
        from_attributes = True