import os
from sqlmodel import create_engine, Session, SQLModel, select
from Pomodoro import Pomodoro
from Task import Task, Status
from datetime import datetime, timedelta
from typing import Annotated, Optional
from fastapi import Depends, HTTPException


if os.getenv("ENVIRONMENT") == "development":
    DATABASE_URL = "sqlite:///./database.db"
else:
    DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

sessionDependency = Annotated[Session, Depends(get_session)]

class StorageHandler:
    def __init__(self, session: Session):
        self.session = session

    def db_get_tasks(self):
        tasks = self.session.exec(select(Task)).all()
        return list(tasks)

    def db_add_task(self, task: Task):
        task_with_same_title = self.session.exec(select(Task).where(Task.title == task.title)).first()
        if task_with_same_title:
            raise HTTPException(status_code=400, detail="Task with this title already exists." )

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def db_get_task_by_id(self, task_id: int):
        task = self.session.exec(select(Task).where(Task.id == task_id)).first()
        if task:
            return task
        else:
            raise HTTPException(status_code=404, detail="Task not found.")

    def db_update_task(self, task_id: int, new_task : Task):
        titles = list(self.session.exec(select(Task.title)).all())

        task = self.db_get_task_by_id(task_id)
        if new_task.title != task.title and new_task.title not in titles and len(new_task.title) >= 3 and len(new_task.title) <= 100:
            task.title = new_task.title
        elif new_task.title in titles:
            raise HTTPException(status_code=400, detail="Title must be unique.")
        if new_task.description != task.description and len(new_task.description) < 300:
            task.description = new_task.description
        if new_task.status in Status:
            task.status = new_task.status
        self.session.commit()
        self.session.refresh(task)
        return task

    def db_delete_task(self, task_id: int):
        task = self.db_get_task_by_id(task_id)
        self.session.delete(task)
        self.session.commit()
        return "task deleted"

    def db_get_active_pomodoros(self):
        active_pomodoros = list(self.session.exec(select(Pomodoro).where(Pomodoro.completed == False)).all())
        return active_pomodoros

    def db_add_pomodoro(self, task_id: int):
        task = self.db_get_task_by_id(task_id)

        active_pomodoros = self.db_get_active_pomodoros()

        if task_id in active_pomodoros:
            raise HTTPException(status_code=400, detail="There is already active pomodoro for this task.")

        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=25)
        pomodoro = Pomodoro(task_id=task_id, start_time=start_time, end_time=end_time, completed=False)

        self.session.add(pomodoro)
        self.session.commit()
        return pomodoro

    def db_stop_pomodoro(self, task_id: int):
        task = self.db_get_task_by_id(task_id)
        active_pomodoros = self.db_get_active_pomodoros()

        if task_id not in active_pomodoros:
            raise HTTPException(status_code=400, detail="There isn't active pomodoro for this task.")

        for pomo in active_pomodoros:
            if pomo.task_id == task_id:
                pomo.end_time = datetime.now()
                if pomo.end_time - pomo.start_time >= timedelta(minutes=25):
                    pomo.completed = True
                return pomo

    def db_get_pomodoro_stats(self):
        stats = {}
        time = 0

        completed_pomodoros = list(self.session.exec(select(Pomodoro).where(Pomodoro.completed == True)).all())

        for pomo in completed_pomodoros:
            if pomo.task_id not in stats:
                stats[pomo.task_id] = 1
            else:
                stats[pomo.task_id] += 1
            time += pomo.end_time - pomo.start_time
        return stats, time

def get_DB_handler(session: Session = Depends(get_session)):
    return StorageHandler(session)

StorageHandlerDependency = Annotated[StorageHandler, Depends(get_DB_handler)]