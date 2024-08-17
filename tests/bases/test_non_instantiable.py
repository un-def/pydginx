import pytest

from pydginx.bases import NonInstantiable


def test() -> None:
    class Cls(NonInstantiable):
        pass

    with pytest.raises(TypeError, match=r'Cls cannot be instantiated'):
        Cls()
