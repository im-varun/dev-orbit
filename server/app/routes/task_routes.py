from fastapi import APIRouter, HTTPException
from app.schemas import Task
from app.repositories.project_repository import project_repository
from app.repositories.task_repository import task_repository

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])

@task_router.post("/", response_model=Task, status_code=201)
def create_task(task: Task):
    project = project_repository.get_by_id(task.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return task_repository.create(task)

@task_router.patch("/{task_id}", response_model=Task)
def update_task(task_id: str, task_update: dict):
    if not task_repository.get_by_id(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task_repository.update(task_id, task_update)

@task_router.delete("/{task_id}", status_code=204)
def delete_task(task_id: str):
    if not task_repository.get_by_id(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_repository.delete(task_id)

    return None