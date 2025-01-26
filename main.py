from datetime import datetime
from enum import Enum

from fastapi import FastAPI
from fastapi.params import Body
app = FastAPI()

class Status(Enum):
    "do wykonania"
    "w trakcie"
    "zakończone"

class Pomodoro:
    def __init__(self, task_title:str, start_time:datetime):
        self.task_title = task_title
        self.start_time = datetime.now()


class Task:
    def __init__(self, title:str, description:str, status:Status):
        self.title = title
        self.description = description
        self.status = status

    @property
    def title(self):
        return self.title

    @title.setter
    def title(self, title):
        if len(self.title) >= 3 and len(self.title) <= 100:
            self.title = title
        else:
            raise ValueError("Title's length must be between 3 and 100")

    @property
    def description(self):
        return self.description

    @description.setter
    def description(self, description):
        if len(self.title) <= 300:
            self.description = description
        else:
            raise ValueError("Description must be max 300 long")

    @property
    def status(self):
        return self.status

    @status.setter
    def status(self, status):
        if status:
            self.title = status
        else:
            raise ValueError("Wrong status")


list_of_pomodoro = [{"id":1,
             "task_title":"FastAPI",
             "start_time":datetime,
             "end_time":datetime,
             "completed":True}]

list_of_tasks = [{"id":1, "title":"FastAPI", "description":"opis", "status":"do wykonania"}]
@app.get("/test")
async def funkcja():
    return {"message": "Hello!"}

@app.get(f"/get_by_id/{id}")
async def get_by_id(id: int):
    return list_of_pomodoro[id]
@app.post("/start")
async def start_timer():
    return {"message": "Start"}

