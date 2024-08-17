from typing import Any

import pytest

from pydginx.conf.directives import Directive, is_directive


def test_is_directive() -> None:
    class Dir(Directive):
        pass

    assert is_directive(Dir) is True
    assert is_directive(Dir()) is True


@pytest.mark.parametrize('value', [1, 'foo', True, ()])
def test_is_not_directive(value: Any) -> None:
    assert is_directive(value) is False
