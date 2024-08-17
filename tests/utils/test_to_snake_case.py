import pytest

from pydginx.utils import to_snake_case


@pytest.mark.parametrize(['value', 'expected'], [
    ['Word', 'word'],
    ['word', 'word'],
    ['CamelCase', 'camel_case'],
    ['HTTPError', 'http_error'],
    ['BaseHTTPError', 'base_http_error'],
    # XXX: the following cases fail
    # ['HTTP11Error', 'http_11_error'],
])
def test(value: str, expected: str) -> None:
    assert to_snake_case(value) == expected
