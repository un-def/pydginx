import enum

from pydginx.conf.literals import LiteralEnum


THIS_MODULE = __name__.rpartition('.')[2]


def test() -> None:
    class Animal(LiteralEnum):
        CAT = enum.auto()
        DOG = enum.auto()
        RAT = enum.auto()

    assert repr(Animal.CAT) == f'{THIS_MODULE}.CAT'
    assert str(Animal.DOG) == 'dog'
    assert Animal.RAT == 'rat'
