import asyncio
import logging
from functools import partial

import cloudscraper
import scrapy


class CloudflareMiddleware(object):

    def __init__(self):
        self.scraper = cloudscraper.create_scraper()

    @classmethod
    def from_crawler(cls, crawler):
        logging.getLogger('websockets').setLevel(logging.INFO)
        return cls()

    async def process_request(self, request, spider):
        # Check if needed by this request
        if not request.meta.get('cloudflare', False):
            return None

        # Forward the request to cloudscraper
        response = await self._cloudscraper_get(request.url, headers={'referer': request.url})

        # Convert requests.Response back to scrapy.http.Response
        response = scrapy.http.HtmlResponse(
            request.url,
            status=response.status_code,
            headers=response.headers,
            body=response.content,
            encoding=response.encoding,
            request=request,
        )
        return response

    async def _cloudscraper_get(self, *args, **kwargs):
        func = partial(self.scraper.get, *args, **kwargs)
        response = await asyncio.get_event_loop().run_in_executor(None, func)
        return response
