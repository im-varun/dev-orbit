import uuid
from app.database import firebase_db
from app.schemas import Task

class TaskRepository:
    def __init__(self):
        self.ref = firebase_db.reference("tasks")

    def create(self, task: Task):
        task_id = str(uuid.uuid4())
        task.id = task_id

        self.ref.child(task_id).set(task.model_dump())

        return task

    def get_all(self):
        data = self.ref.get()
        if not data or not isinstance(data, dict):
            return []
        
        return [Task(**value) for value in data.values()]
    
    def get_by_id(self, task_id):
        data = self.ref.child(task_id).get()
        if not data or not isinstance(data, dict):
            return None
        
        return Task(**data)
    
    def get_by_project(self, project_id):
        all = self.get_all()
        return [task for task in all if task.project_id == project_id]
    
    def update(self, task_id, update_data):
        self.ref.child(task_id).update(update_data)
        return self.get_by_id(task_id)
    
    def delete(self, task_id):
        self.ref.child(task_id).delete()
        return True
    
task_repository = TaskRepository()