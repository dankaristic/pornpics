# core.py
from .exceptions import NotFound
from .consts import BASE_URL
from .parsers import parse_gallery_item



class _PornPicsCore:
    def __init__(self, transport):
        self._t = transport

    def _get_html(self, url: str) -> str:
        r = self._t.request("GET", url)
        if r.status_code != 200:
            raise NotFound(url)
        return r.text

    def get_gallery(self, slug):
        url = f"{BASE_URL}/galleries/{slug}/"
        html = self._get_html(url)
        return parse_gallery_item(html)



class _PornPicsCoreAsync:
    def __init__(self, transport):
        self._t = transport

    async def _get_html(self, url: str) -> str:
        r = await self._t.request("GET", url)
        if r.status_code != 200:
            raise NotFound(url)
        return r.text

    async def get_gallery(self, slug):
        url = f"{BASE_URL}/galleries/{slug}/"
        html = await self._get_html(url)
        return parse_gallery_item(html)

