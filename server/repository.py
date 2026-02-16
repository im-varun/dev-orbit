import uuid
import time
from database import firebase_db
from schemas import Project, Task

class ProjectRepository:
    def __init__(self):
        self.ref = firebase_db.reference("projects")

    def get_all(self):
        data = self.ref.get()
        if not data or not isinstance(data, dict):
            return []
        
        return [Project(**value) for value in data.values()]
    
    def get_by_id(self, project_id):
        data = self.ref.child(project_id).get()
        if not data or not isinstance(data, dict):
            return None
        
        return Project(**data)
    
    def create(self, project: Project):
        project_id = str(uuid.uuid4())
        project.id = project_id

        self.ref.child(project_id).set(project.model_dump())

        return project
    
class TaskRepository:
    def __init__(self):
        self.ref = firebase_db.reference("tasks")

    def get_all(self):
        data = self.ref.get()
        if not data or not isinstance(data, dict):
            return []
        
        return [Task(**value) for value in data.values()]
    
    def get_by_project(self, project_id):
        all = self.get_all()
        return [task for task in all if task.project_id == project_id]
    
    def create(self, task: Task):
        task_id = str(uuid.uuid4())
        task.id = task_id

        self.ref.child(task_id).set(task.model_dump())

        return task
    
project_repository = ProjectRepository()
task_repository = TaskRepository()