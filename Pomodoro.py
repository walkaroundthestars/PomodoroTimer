from datetime import datetime


class Pomodoro:
    def __init__(self, task_title:str, start_time:datetime):
        self.task_title = task_title
        self.start_time = datetime.now()

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
