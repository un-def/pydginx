import enum
from typing import Literal


class LiteralEnum(enum.StrEnum):

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        enum.global_enum(cls)  # pyright: ignore[reportUnusedCallResult]


class Bool(LiteralEnum):
    OFF = enum.auto()
    ON = enum.auto()


type BoolType = Literal[False, True, Bool.OFF, Bool.ON, 'off', 'on']


class Auto(LiteralEnum):
    AUTO = enum.auto()


OFF = Bool.OFF
ON = Bool.ON
AUTO = Auto.AUTO
