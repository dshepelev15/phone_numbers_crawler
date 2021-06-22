import asyncio
import logging
import os

from concurrent.futures import ProcessPoolExecutor

from selenium import webdriver
from selenium.webdriver import ActionChains

from .utils import find_phone_numbers

STOP_WORDS = {'show', 'показать', 'отобразить', 'подробнее'}


async def crawle_dynamic_pages(urls):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor(max_workers=os.cpu_count() - 1) as pool:
        tasks = [
            loop.run_in_executor(pool, run_selenium, url) for url in urls
        ]
        urls_numbers = await asyncio.gather(*tasks)

    return {
        url: url_numbers
        for url, url_numbers in zip(urls, urls_numbers)
    }


def run_selenium(url):
    """
    Open dynamic site via selenium and click on multiple divs with small words count that contain stop word
    """
    logging.info("dynamic fetch %s", url)
    driver = get_selenium_driver()
    numbers = []
    try:
        driver.get(url)
        already_clicked_div_text = set()
        last_div_is_processed = False

        while not last_div_is_processed:
            div_elements = driver.find_elements_by_tag_name("div")

            for i, div_element in enumerate(div_elements, start=1):
                div_text = div_element.text.lower()
                words = div_text.split(' ') # if words count in div small and it has stop word then try to click
                if len(words) <= 3 and \
                    div_text not in already_clicked_div_text and \
                    any(stop_word in div_text for stop_word in STOP_WORDS):
                        ActionChains(driver).click(div_element).perform()
                        already_clicked_div_text.add(div_text)
                        numbers.extend(find_phone_numbers(driver.find_element_by_tag_name("body").text))
                        break

                last_div_is_processed = len(div_elements) == i  # check div is last or not
    except Exception as exp:
        logging.error(exp)
    finally:
        driver.close()

    return numbers


def get_selenium_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=chrome_options)
    return driver