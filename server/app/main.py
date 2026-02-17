from fastapi import FastAPI
from app.routes.project_routes import project_router
from app.routes.task_routes import task_router

app = FastAPI(title="Dev Orbit API")

app.include_router(project_router)
app.include_router(task_router)

@app.get("/")
def read_root():
    return {"status": "online"}