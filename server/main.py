from fastapi import FastAPI, HTTPException
from schemas import Project, Task
from repository import project_repository, task_repository

app = FastAPI(title="Dev Orbit API")

@app.get("/", tags=["Health"])
def read_root():
    return {"status": "Dev Orbit API is online"}

@app.get("/projects", response_model=list[Project], tags=["Projects"])
def get_projects():
    return project_repository.get_all()

@app.get("/projects/{project_id}", response_model=Project, tags=["Projects"])
def get_project(project_id: str):
    project = project_repository.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return project

@app.post("/projects", response_model=Project, status_code=201, tags=["Projects"])
def create_project(project: Project):
    return project_repository.create(project)

@app.get("/projects/{project_id}/tasks", response_model=list[Task], tags=["Tasks"])
def get_project_tasks(project_id: str):
    project = project_repository.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    tasks = task_repository.get_by_project(project_id)

    return tasks

@app.post("/tasks", response_model=Task, status_code=201, tags=["Tasks"])
def create_task(task: Task):
    project = project_repository.get_by_id(task.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return task_repository.create(task)