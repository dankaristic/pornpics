from .core import _PornPicsCore, _PornPicsCoreAsync
from .transport import SyncTransport, AsyncTransport

class AsyncClient(_PornPicsCoreAsync):
    """Asynchronous client for interacting with the PornPics API.

    This class provides a high-level, user-friendly interface for making asynchronous
    requests to the PornPics website. It uses `_PornPicsCoreAsync` internally with an
    `AsyncTransport` for HTTP requests.
    """

    def __init__(self):
        """Initializes the async client with the async transport layer."""
        super().__init__(AsyncTransport())

class Client(_PornPicsCore):
    """Synchronous client for interacting with the PornPics API.

    This class provides a high-level, user-friendly interface for making synchronous
    requests to the PornPics website. It uses `_PornPicsCore` internally with a
    `SyncTransport` for HTTP requests.
    """

    def __init__(self):
        """Initializes the sync client with the sync transport layer."""
        super().__init__(SyncTransport())