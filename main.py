from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from starlette.responses import JSONResponse
from datetime import datetime, timedelta
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
        if item.title == task.title:
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


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for task in list_of_tasks:
        if task.id == task_id:
            list_of_tasks.remove(task)
            return f"task deleted"
    raise HTTPException(status_code=404, detail="Task not found.")

@app.post("/pomodoro")
async def add_pomodoro(task_id: int):
    is_there_a_task = False
    for task in list_of_tasks:
        if task.id == task_id:
            is_there_a_task = True

    if not is_there_a_task:
        raise HTTPException(status_code=404, detail="Task not found.")

    active_pomodoro_task_ids = []
    for pomo in list_of_pomodoro:
        if not pomo.completed:
            active_pomodoro_task_ids.append(pomo.task_id)

    if task_id in active_pomodoro_task_ids:
        raise HTTPException(status_code=404, detail="There is already active pomodoro for this task.")

    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=25)
    pomodoro = Pomodoro(task_id=task_id, start_time=start_time, end_time=end_time, completed=False)
    list_of_pomodoro.append(pomodoro)
    return pomodoro

@app.post("/pomodoro/{task_id}/stop")
async def stop_pomodoro(task_id: int):
    is_there_a_task = False
    for task in list_of_tasks:
        if task.id == task_id:
            is_there_a_task = True

    if not is_there_a_task:
        raise HTTPException(status_code=404, detail="Task not found.")

    active_pomodoro_task_ids = []
    for pomo in list_of_pomodoro:
        if not pomo.completed:
            active_pomodoro_task_ids.append(pomo.task_id)

    if task_id not in active_pomodoro_task_ids:
        raise HTTPException(status_code=404, detail="There isn't active pomodoro for this task.")

    for pomo in list_of_pomodoro:
        if pomo.task_id == task_id:
            pomo.end_time = datetime.now()
            if pomo.end_time-pomo.start_time >= timedelta(minutes=25):
                pomo.completed = True
            return pomo

@app.get("/pomodoro/stats")
async def get_pomodoro_stats():
    stats = {}
    time = 0

    for pomo in list_of_pomodoro:
        if pomo.completed:
            if pomo.task_id not in stats:
                stats[pomo.task_id] = 1
            else:
                stats[pomo.task_id] += 1
            time += pomo.end_time - pomo.start_time
    return stats, time
