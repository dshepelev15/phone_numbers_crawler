from pytest import mark

from crawler.utils import find_phone_numbers


@mark.parametrize('text, expected_values',[
    ("Hello +7-(925)-123-43-56 phone", ["89251234356"]),
    ("Hello 8-(925)-123-43-56 phone", ["89251234356"]),  # +7/8 replace
    ("Hello +7-(925)-123-43-56 phone", ["89251234356"]),  # () replace
    ("Hello 123-43-56 phone", ["84951234356"]),  # default Moscow region
    ("Hello +7-(925)-123-43-56 +7-(925)-123-43-56 phone", ["89251234356"]), # check duplication
    ("", []),
    ("Hello 123-435 phone", []),
    ('content="230186824209892" ', []),
    ('YaMetric2420982" ', []),
    ('Year 2020-2021 ', []),
    ('<html>My phone number is:8915-402-31-21</html>', ["89154023121"]),
])
def test_phone_regex(text, expected_values):
    assert find_phone_numbers(text) == expected_values
