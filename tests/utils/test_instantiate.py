import pytest

from pydginx.utils import instantiate


@pytest.mark.parametrize(['value', 'expected'], [
    ['foo', 'foo'], [str, ''],
    [1, 1], [int, 0],
    [(1, 2, 3), (1, 2, 3)], [tuple, ()],
])
def test[T](value: type[T] | T, expected: T) -> None:
    assert instantiate(value) == expected
