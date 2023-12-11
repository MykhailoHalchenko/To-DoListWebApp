from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Set up the static folder
static_folder = Path(__file__).parent.absolute() / "static"
app.mount("/static", StaticFiles(directory=static_folder), name="static")

tasks = []


class Task:
    def __init__(self, description: str, priority: int, due_date: str):
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.is_complete = False


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})


@app.post("/add_task/")
def add_task(request: Request, description: str = Form(...), priority: int = Form(...), due_date: str = Form(...)):
    new_task = Task(description=description, priority=priority, due_date=due_date)
    tasks.append(new_task)
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})


@app.get("/delete_task/{task_index}")
def delete_task(request: Request, task_index: int):
    if 0 <= task_index < len(tasks):
        del tasks[task_index]
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80, reload=True)
