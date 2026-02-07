from typing import Protocol

class ResponseLike(Protocol):
    status_code: int
    text: str
