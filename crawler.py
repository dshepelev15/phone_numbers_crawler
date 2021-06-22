import asyncio
import argparse
import logging

logging.basicConfig(level=logging.INFO)

from crawler import crawle_phone_numbers
from crawler.utils import dump_data

parser = argparse.ArgumentParser()
parser.add_argument('--urls', help="Desired urls for crawling", nargs='*', required=True)


async def main():
    args = parser.parse_args()
    data = await crawle_phone_numbers(args.urls)
    dump_data(data, output_file='result.json')


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
