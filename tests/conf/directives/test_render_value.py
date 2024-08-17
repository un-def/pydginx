from pathlib import Path

import pytest

from pydginx.conf.directives import ValueType, render_value
from pydginx.conf.literals import AUTO, OFF, ON


@pytest.mark.parametrize(['value', 'expected'], [
    ['foo', 'foo'],
    [23, '23'],
    [False, 'off'], [True, 'on'],
    [OFF, 'off'], [ON, 'on'],
    [AUTO, 'auto'],
    [Path('/path/to/file'), '/path/to/file'], [Path('file'), 'file'],
])
def test(value: ValueType, expected: str) -> None:
    assert render_value(value) == expected
