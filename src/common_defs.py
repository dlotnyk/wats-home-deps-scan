from enum import Enum


class ResponseStatus(Enum):
    paid = 0
    unpaid = 1
    unable_to_check = 2
    in_check_progress = 3


class StatusInfo:
    def __init__(self, status: ResponseStatus, info: str):
        self.status = status
        self.info = info

    @property
    def is_ok(self) -> bool:
        return self.status == ResponseStatus.paid
