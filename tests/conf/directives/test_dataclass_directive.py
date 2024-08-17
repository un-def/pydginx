from dataclasses import FrozenInstanceError

import pytest

from pydginx.conf.directives import DataClassDirective


def test() -> None:
    class SomeDir(DataClassDirective):
        foo: int
        bar: str

    some_dir = SomeDir(foo=3, bar='val')

    assert some_dir.foo == 3
    assert some_dir.bar == 'val'
    with pytest.raises(FrozenInstanceError):
        some_dir.foo = 5  # pyright: ignore[reportAttributeAccessIssue]
