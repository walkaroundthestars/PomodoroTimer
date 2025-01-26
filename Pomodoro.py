from datetime import datetime


class Pomodoro:
    def __init__(self, task_title:str, start_time:datetime):
        self.task_title = task_title
        self.start_time = datetime.now()



