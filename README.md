# scrapy-async-cloudflare
Asynchronous Cloudflare scraper middleware for Scrapy.

## Requirements
* Scrapy >= 2.0 (needed for async support)
* cloudscraper (needed for bypassing Cloudflare)

Run the following command to install packages needed .
```sh
pip install cloudscraper
```

## Usages

**Enable the middleware in scrapy's settings**

_If you want to know more about the `TWISTED_REACTOR` setting, see Scrapy's [document](https://docs.scrapy.org/en/latest/topics/asyncio.html#installing-the-asyncio-reactor)._

```python
DOWNLOADER_MIDDLEWARES = {
    # ...
    'your.scrapy.project.middlewares.CloudflareMiddleware': 543,
    # ...
}
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
```

**Enable the middleware in your requests**

```python
def start_requests(self):
    ...
    return scrapy.Request(url, meta={'cloudflare': True})
```

**Enable the middleware in pipeline requests (if needed)**

```python
class CustomImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        requests = super().get_media_requests(item, info)
        for req in requests:
            req.meta['cloudflare'] = True
        return requests
```

## Extension

Please refer to [VeNoMouS/cloudscraper](https://github.com/VeNoMouS/cloudscraper) for more usages of `cloudscraper`.

To pass more arguments to cloudscraper, change [this line](middlewares.py#L25) to:

```python
response = await self._cloudscraper_get(request.url, *your_args, **your_kwargs)
```

