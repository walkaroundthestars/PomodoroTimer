from fastapi import FastAPI
from fastapi.params import Body
from datetime import datetime
app = FastAPI()


list_of_pomodoro = [{"id":1,
             "task_title":"FastAPI",
             "start_time":datetime,
             "end_time":datetime,
             "completed":True}]

list_of_tasks = [{"id":1,
                  "title":"FastAPI",
                  "description":"opis",
                  "status":"do wykonania"}]
@app.get("/tasks")
async def get_tasks():
    return list_of_tasks

@app.get(f"/get_by_id/{id}")
async def get_by_id(id: int):
    return list_of_pomodoro[id]
@app.post("/start")
async def start_timer():
    return {"message": "Start"}

@app.post("/tasks")
async def add_task():
    pass