import logging

from .static import crawle_static_pages
from .dynamic import crawle_dynamic_pages


async def crawle_phone_numbers(urls):
    """
    Crawle all passed urls and return dict[url, unique phone numbers]

    1. Static page crawling via aiohttp
    2. Dynamic page crawling via selenium (if any phone numbers are not found via static crawling)
    """
    logging.info("start crawling urls")

    urls = list(set(urls))  # drop duplicates

    static_data = await crawle_static_pages(urls)
    dynamic_data = await crawle_dynamic_pages(urls)

    logging.info("end crawling urls")

    return {
        url: list(set(static_data[url] + dynamic_data[url]))
        for url in urls
    }