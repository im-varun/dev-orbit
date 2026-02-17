from fastapi import APIRouter, HTTPException
from app.schemas import Project, Task
from app.repositories.project_repository import project_repository
from app.repositories.task_repository import task_repository

project_router = APIRouter(prefix="/projects", tags=["Projects"])

@project_router.get("/", response_model=list[Project])
def get_projects():
    return project_repository.get_all()

@project_router.get("/{project_id}", response_model=Project)
def get_project(project_id: str):
    project = project_repository.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return project

@project_router.get("/{project_id}/tasks", response_model=list[Task])
def get_project_tasks(project_id: str):
    project = project_repository.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    tasks = task_repository.get_by_project(project_id)

    return tasks

@project_router.post("/", response_model=Project, status_code=201)
def create_project(project: Project):
    return project_repository.create(project)

@project_router.patch("/{project_id}", response_model=Project)
def update_project(project_id: str, project_update: dict):
    if not project_repository.get_by_id(project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    
    return project_repository.update(project_id, project_update)

@project_router.delete("/{project_id}", status_code=204)
def delete_project(project_id: str):
    if not project_repository.get_by_id(project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    
    project_repository.delete(project_id)

    return None