from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Write report", "done": False},
    {"id": 3, "title": "Call mom", "done": True},
    {"id": 4, "title": "Buy milk", "done": False},
]

next_id = 5


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


def find_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


@app.get("/")
def read_root():
    """Describe the API: its name, version, and endpoints."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"],
    }


@app.get("/health")
def health():
    """Check that the server is running."""
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    """Return all tasks."""
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Return one task by id, or 404 if it doesn't exist."""
    task = find_task(task_id)
    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"},
        )
    return task


@app.post("/tasks")
def create_task(body: TaskCreate):
    """Create a new task. Title is required and must not be empty."""
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


@app.put("/tasks/{task_id}")
def update_task(task_id: int, body: TaskUpdate):
    """Update a task's title and/or done flag. Send at least one field."""
    task = find_task(task_id)
    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"},
        )
    if body.title is None and body.done is None:
        return JSONResponse(
            status_code=400,
            content={"error": "send at least one of: title, done"},
        )
    if body.title is not None:
        title = body.title.strip()
        if not title:
            return JSONResponse(
                status_code=400,
                content={"error": "title must not be empty"},
            )
        task["title"] = title
    if body.done is not None:
        task["done"] = body.done
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Delete a task by id. Returns 204 on success, 404 if not found."""
    task = find_task(task_id)
    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"},
        )
    tasks.remove(task)
    return Response(status_code=204)