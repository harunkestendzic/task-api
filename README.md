# Task API

A small CRUD API for a to-do list, built with FastAPI. Tasks are stored in memory, so they reset when the server restarts.

## Install and run

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install "fastapi[standard]"
fastapi dev main.py
```

The server runs at http://localhost:8000. Swagger UI is at http://localhost:8000/docs.

## Endpoints

| Method | Path | Description | Success | Errors |
|---|---|---|---|---|
| GET | `/` | API description | 200 | — |
| GET | `/health` | Health check | 200 | — |
| GET | `/tasks` | List all tasks | 200 | — |
| GET | `/tasks/{task_id}` | Get one task | 200 | 404 |
| POST | `/tasks` | Create a task | 201 | 400, 422 |
| PUT | `/tasks/{task_id}` | Update title and/or done | 200 | 400, 404, 422 |
| DELETE | `/tasks/{task_id}` | Delete a task | 204 | 404 |

## Example

```
HTTP/1.1 200 OK
content-type: application/json

[{"id":1,"title":"Buy milk","done":false}, ...]
```

## Swagger UI

![Swagger UI](swagger.png)

## AI vs me

Not done yet. This section is for Stage 7.