from .core import _PornPicsCore, _PornPicsCoreAsync
from .transport import SyncTransport, AsyncTransport


class AsyncClient(_PornPicsCoreAsync):
    def __init__(self):
        super().__init__(AsyncTransport())

class Client(_PornPicsCore):
    def __init__(self):
        super().__init__(SyncTransport())