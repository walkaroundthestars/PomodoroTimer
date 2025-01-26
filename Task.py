from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

class Status(str, Enum):
    do_wykonania = "do wykonania"
    w_trakcie = "w trakcie"
    zakonczone = "zakończone"


class Task(BaseModel):
    id: int
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=300)
    status: Status = Status.do_wykonania

