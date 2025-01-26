from enum import Enum


class Status(str, Enum):
    do_wykonania = "do wykonania"
    w_trakcie = "w trakcie"
    zakonczone = "zakończone"


class Task:
    def __init__(self, title:str, description:str="", status:Status=Status.do_wykonania):
        self.title = title
        self.description = description
        self.status = status

    @property
    def title(self)->str:
        return self.__title

    @title.setter
    def title(self, title):
        if len(title) >= 3 and len(title) <= 100:
            self.__title = title
        else:
            raise ValueError("Title's length must be between 3 and 100")

    @property
    def description(self)->str:
        return (self.__description)

    @description.setter
    def description(self, description):
        if description:
            if len(description) <= 300:
                self.__description = description
            else:
                raise ValueError("Description must be max 300 long")
        else:
            self.__description = ""

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        if status in Status:
            self.__status = status
        else:
            raise ValueError("Wrong status")


