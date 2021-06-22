import aiohttp
import asyncio
import logging

from .utils import find_phone_numbers


async def crawle_static_pages(urls):
    async with aiohttp.ClientSession() as session:
        htmls = await fetch_all_urls(urls, session)

    return {
        url: find_phone_numbers(html)
        for url, html in zip(urls, htmls)
    }


async def fetch_all_urls(urls, session):
    tasks = [
        asyncio.create_task(fetch_url(url, session))
        for url in urls
    ]
    return await asyncio.gather(*tasks)


async def fetch_url(url, session):
    logging.info("static fetch %s", url)
    async with session.get(url, ssl=False) as response:
        if response.status != 200:
            logging.error("got incorrect status code %d by url %s", response.status, url)
            return ""

        return await response.text()