from datetime import datetime
from pydantic import BaseModel

class Pomodoro(BaseModel):
    task_id: int
    start_time: datetime
    end_time: datetime
    completed: bool



