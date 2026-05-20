# core.py
from .exceptions import NotFound
from .consts import BASE_URL
from .parsers import parse_gallery_item, parse_category_item, parse_home_page


class _PornPicsCore:
    """Core synchronous client for interacting with the PornPics API.

    This class provides synchronous methods to fetch and parse gallery and category data
    from the PornPics website using the provided transport layer.
    """

    def __init__(self, transport):
        """Initializes the PornPics core client.

        Args:
            transport: A transport layer for making HTTP requests.
        """
        self._t = transport

    def _get_html(self, url: str) -> str:
        """Fetches the HTML content of a given URL.

        Args:
            url (str): The URL to fetch HTML from.

        Returns:
            str: The HTML content of the page.

        Raises:
            NotFound: If the request returns a non-200 status code.
        """
        r = self._t.request("GET", url)
        if r.status_code != 200:
            raise NotFound(url)
        return r.text

    def get_gallery(self, slug):
        """Fetches and parses a single gallery by its slug.

        Args:
            slug (str): The slug of the gallery to fetch.

        Returns:
            GalleryResponse: A parsed gallery response object.
        """
        url = f"{BASE_URL}/galleries/{slug}/"
        html = self._get_html(url)
        return parse_gallery_item(html)

    def get_category(self, slug, offset: int = 0, limit: int = 20):
        """Fetches and parses a category or tag page.

        Args:
            slug (str): The slug of the category or tag.
            offset (int, optional): The offset for pagination. Defaults to 0.
            limit (int, optional): The limit for pagination. Defaults to 20.

        Returns:
            CategoryResponse: A parsed category response object.
        """
        url = f"{BASE_URL}/{slug}/?offset={offset}&limit={limit}"
        html = self._get_html(url)
        return parse_category_item(html, offset)

    def get_home(self):
        """Fetches and parses the homepage. It returns tags and categories listed on the homepage

        Returns:
            List[HomeMedia]: A list of `HomeMedia` objects representing the featured tags and categories.
                       Each object contains the link, type (tag/category), name, and thumbnail.
        """
        url = f"{BASE_URL}/"
        html = self._get_html(url)
        return parse_home_page(html)

class _PornPicsCoreAsync:
    """Core asynchronous client for interacting with the PornPics API.

    This class provides asynchronous methods to fetch and parse gallery and category data
    from the PornPics website using the provided transport layer.
    """

    def __init__(self, transport):
        """Initializes the PornPics core async client.

        Args:
            transport: A transport layer for making HTTP requests.
        """
        self._t = transport

    async def _get_html(self, url: str) -> str:
        """Asynchronously fetches the HTML content of a given URL.

        Args:
            url (str): The URL to fetch HTML from.

        Returns:
            str: The HTML content of the page.

        Raises:
            NotFound: If the request returns a non-200 status code.
        """
        r = await self._t.request("GET", url)
        if r.status_code != 200:
            raise NotFound(url)
        return r.text

    async def get_gallery(self, slug):
        """Asynchronously fetches and parses a single gallery by its slug.

        Args:
            slug (str): The slug of the gallery to fetch.

        Returns:
            GalleryResponse: A parsed gallery response object.
        """
        url = f"{BASE_URL}/galleries/{slug}/"
        html = await self._get_html(url)
        return parse_gallery_item(html)

    async def get_category(self, slug, offset: int = 0, limit: int = 20):
        """Asynchronously fetches and parses a category or tag page.

        Args:
            slug (str): The slug of the category or tag.
            offset (int, optional): The offset for pagination. Defaults to 0.
            limit (int, optional): The limit for pagination. Defaults to 20.

        Returns:
            CategoryResponse: A parsed category response object.
        """
        url = f"{BASE_URL}/{slug}/?offset={offset}&limit={limit}"
        html = await self._get_html(url)
        return parse_category_item(html, offset)

    async def get_home(self):
        """Asynchronously fetches and parses the homepage. It returns tags and categories listed on the homepage

        Returns:
            List[HomeMedia]: A list of `HomeMedia` objects representing the featured tags and categories.
                       Each object contains the link, type (tag/category), name, and thumbnail.
        """
        url = f"{BASE_URL}/"
        html = await self._get_html(url)
        return parse_home_page(html)