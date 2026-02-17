import uuid
from app.database import firebase_db
from app.schemas import Project

class ProjectRepository:
    def __init__(self):
        self.ref = firebase_db.reference("projects")

    def create(self, project: Project):
        project_id = str(uuid.uuid4())
        project.id = project_id

        self.ref.child(project_id).set(project.model_dump())

        return project

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
    
    def update(self, project_id, update_data):
        self.ref.child(project_id).update(update_data)
        return self.get_by_id(project_id)
    
    def delete(self, project_id):
        from task_repository import task_repository

        related_tasks = task_repository.get_by_project(project_id)
        for task in related_tasks:
            task_repository.delete(task.id)
        
        self.ref.child(project_id).delete()
        
        return True
    
project_repository = ProjectRepository()