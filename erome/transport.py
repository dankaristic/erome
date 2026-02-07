import httpx

from erome.types import ResponseLike

DEFAULT_HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://www.erome.com/"
        }


class AsyncTransport:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=15, headers=DEFAULT_HEADERS)

    async def request(self, method, url, **kwargs):
        resp = await self.client.request(method, url, **kwargs)
        resp.raise_for_status()
        return resp

class SyncTransport:
    def __init__(self):
        self.client = httpx.Client(timeout=15, headers=DEFAULT_HEADERS)

    def request(self, method, url, **kwargs):
        resp = self.client.request(method, url, **kwargs)
        resp.raise_for_status()
        return resp

