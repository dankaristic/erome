# core.py
from erome.parsers import (
    parse_albums,
    parse_album,
    parse_profile,
    parse_search,
)
from erome.exceptions import NotFound


class _EromeCore:
    def __init__(self, transport):
        self._t = transport

    def _get_html(self, url: str) -> str:
        r = self._t.request("GET", url)
        if r.status_code != 200:
            raise NotFound(url)
        return r.text

    def get_explore(self, page: int = 1):
        html = self._get_html(f"https://www.erome.com/explore?page={page}")
        return parse_albums(html)

    def get_album(self, album_id: str):
        html = self._get_html(f"https://www.erome.com/a/{album_id}")
        return parse_album(html, album_id)

    def get_related_albums(self, album_id: str):
        html = self._get_html(f"https://www.erome.com/a/{album_id}")
        return parse_albums(html)

    def get_search(self, query: str, page: int = 1):
        html = self._get_html(
            f"https://www.erome.com/search?q={query}&page={page}"
        )
        return parse_search(html)

    def get_profile(self, username: str, page: int = 1):
        url = f"https://www.erome.com/{username}?t=posts&page={page}"
        html = self._get_html(url)
        return parse_profile(html, page)


class _EromeCoreAsync:
    def __init__(self, transport):
        self._t = transport

    async def _get_html(self, url: str) -> str:
        r = await self._t.request("GET", url)
        if r.status_code != 200:
            raise NotFound(url)
        return r.text

    async def get_explore(self, page: int = 1):
        html = await self._get_html(f"https://www.erome.com/explore?page={page}")
        return parse_albums(html)

    async def get_album(self, album_id: str):
        html = await self._get_html(f"https://www.erome.com/a/{album_id}")
        return parse_album(html, album_id)

    async def get_related_albums(self, album_id: str):
        html = await self._get_html(f"https://www.erome.com/a/{album_id}")
        return parse_albums(html)

    async def get_search(self, query: str, page: int = 1):
        html = await self._get_html(
            f"https://www.erome.com/search?q={query}&page={page}"
        )
        return parse_search(html)

    async def get_profile(self, username: str, page: int = 1):
        url = f"https://www.erome.com/{username}?t=posts&page={page}"
        html = await self._get_html(url)
        return parse_profile(html, page)
