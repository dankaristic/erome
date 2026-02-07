from .core import _EromeCore, _EromeCoreAsync
from .transport import SyncTransport, AsyncTransport


class AsyncClient(_EromeCoreAsync):
    def __init__(self):
        super().__init__(AsyncTransport())

class Client(_EromeCore):
    def __init__(self):
        super().__init__(SyncTransport())