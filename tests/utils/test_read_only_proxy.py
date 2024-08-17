from pydginx.utils import ReadOnlyProxy


def test() -> None:
    class Cls:
        foo = ReadOnlyProxy[int]()

        def __init__(self, foo: int) -> None:
            self._foo = foo

    obj = Cls(foo=3)

    assert isinstance(Cls.foo, ReadOnlyProxy)
    assert isinstance(obj.foo, int)
    assert obj.foo == 3
