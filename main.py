from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from starlette.responses import JSONResponse
from datetime import datetime
from Task import Task, Status
from Pomodoro import Pomodoro
app = FastAPI()


list_of_pomodoro = []

list_of_tasks = []

#@app.get("/tasks")
#async def create_task(task : Task):
  #  pass
@app.get("/tasks")
async def get_tasks():
    return list_of_tasks

@app.get("/tasks/{task_status}")
async def get_task_by_status(task_status:str):
    for task in list_of_tasks:
        if task.status == task_status:
            return JSONResponse({Task:task})
    return None

@app.post("/tasks")
async def add_task(task : Task):
    for item in list_of_tasks:
        if item["title"] == task.title:
            raise HTTPException(status_code=400, detail="Title must be unique.")
    list_of_tasks.append(task)
    return list_of_tasks


@app.get("/tasks/{task_id}")
async def get_by_id(task_id: int):
    for task in list_of_tasks:
        if task_id == task.id:
            return list_of_tasks[task_id]
    raise HTTPException(status_code=404, detail="Task not found.")



###########################################
@app.post("/start")
async def start_timer():
    return {"message": "Start"}