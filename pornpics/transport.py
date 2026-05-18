import httpx

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://www.pornpics.com/"
}
"""Default headers for HTTP requests to the PornPics website.

These headers mimic a standard browser request to avoid being blocked or flagged as a bot.
"""

class AsyncTransport:
    """Asynchronous HTTP transport client for making requests to the PornPics API.

    Uses `httpx.AsyncClient` for async HTTP requests with a default timeout and headers.
    """

    def __init__(self):
        """Initializes the async HTTP transport client."""
        self.client = httpx.AsyncClient(timeout=15, headers=DEFAULT_HEADERS)

    async def request(self, method: str, url: str, **kwargs):
        """Sends an asynchronous HTTP request to the specified URL.

        Args:
            method (str): The HTTP method (e.g., "GET", "POST").
            url (str): The URL to send the request to.
            **kwargs: Additional arguments to pass to `httpx.AsyncClient.request`.

        Returns:
            httpx.Response: The HTTP response object.

        Raises:
            httpx.HTTPStatusError: If the request returns a non-200 status code.
        """
        resp = await self.client.request(method, url, **kwargs)
        resp.raise_for_status()
        return resp

class SyncTransport:
    """Synchronous HTTP transport client for making requests to the PornPics API.

    Uses `httpx.Client` for synchronous HTTP requests with a default timeout and headers.
    """

    def __init__(self):
        """Initializes the sync HTTP transport client."""
        self.client = httpx.Client(timeout=15, headers=DEFAULT_HEADERS)

    def request(self, method: str, url: str, **kwargs):
        """Sends a synchronous HTTP request to the specified URL.

        Args:
            method (str): The HTTP method (e.g., "GET", "POST").
            url (str): The URL to send the request to.
            **kwargs: Additional arguments to pass to `httpx.Client.request`.

        Returns:
            httpx.Response: The HTTP response object.

        Raises:
            httpx.HTTPStatusError: If the request returns a non-200 status code.
        """
        resp = self.client.request(method, url, **kwargs)
        resp.raise_for_status()
        return resp