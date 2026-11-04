from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Write report", "done": False},
    {"id": 3, "title": "Call mom", "done": True},
]

next_id = 4


class TaskCreate(BaseModel):
    title: str


@app.get("/")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"],
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"},
    )


@app.post("/tasks")
def create_task(body: TaskCreate):
    global next_id
    title = body.title.strip()
    if not title:
        return JSONResponse(
            status_code=400,
            content={"error": "title must not be empty"},
        )
    task = {"id": next_id, "title": title, "done": False}
    next_id += 1
    tasks.append(task)
    return JSONResponse(status_code=201, content=task)