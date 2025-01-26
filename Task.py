from enum import Enum


class Status(Enum):
    "do wykonania"
    "w trakcie"
    "zakończone"


class Task:
    def __init__(self, title:str, description:str, status:Status="do wykonania"):
        self.title = title
        self.description = description
        self.status = status