from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from starlette.responses import JSONResponse
from datetime import datetime
from Task import Task, Status
from Pomodoro import Pomodoro
app = FastAPI()


list_of_pomodoro = []

list_of_tasks = []
@app.get("/tasks")
async def get_tasks():
    return list_of_tasks

@app.post("/tasks")
async def add_task(task : Task):
    for item in list_of_tasks:
        if item["title"] == task.title:
            raise HTTPException(status_code=400, detail="Title must be unique.")
    list_of_tasks.append(task)
    return task

@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int):
    for task in list_of_tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found.")

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, new_task : Task):
    titles = []
    for task in list_of_tasks:
        titles.append(task.title)

    for task in list_of_tasks:
        if task.id == task_id:
            if new_task.title != task.title and new_task.title not in titles and len(new_task.title) >= 3 and len(new_task.title) <= 100:
                task.title = new_task.title
            elif new_task.title in titles:
                raise HTTPException(status_code=400, detail="Title must be unique.")
            if new_task.description != task.description and len(new_task.description) < 300:
                task.description = new_task.description
            if new_task.status in Status:
                task.status = new_task.status
            return task
        raise HTTPException(status_code=404, detail="Task not found.")


###########################################
@app.post("/start")
async def start_timer():
    return {"message": "Start"}