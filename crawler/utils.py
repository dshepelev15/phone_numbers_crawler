import json
import logging
import re

from typing import List

PATTERN = r"[\s>:,](8|\+7)?[\- ]?(\(?(\d{3})\)?[\- ]?)?(\d{3}[\- ]?\d{2}[\- ]?\d{2})[\s<,]"
regexp = re.compile(PATTERN)


def find_phone_numbers(text) -> List[str]:
    """
    Find and normalize phone numbers format
    """
    found_groups = regexp.findall(text)
    numbers = []
    for country_code, _, region, number in found_groups:
        country_code = country_code.replace('+7', '8') if country_code else "8"  # all numbers will start with 8
        region = region or "495"  # Moscow region
        number = number.replace(' ', '').replace('-', '')
        numbers.append(f"{country_code}{region}{number}")

    return list(set(numbers))


def dump_data(data, output_file):
    logging.info("dump processed result")

    with open(output_file, 'w') as fd:
        json.dump(data, fd)
