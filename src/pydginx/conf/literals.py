from enum import StrEnum
from enum import auto as enum_auto
from enum import global_enum
from typing import Literal


class LiteralEnum(StrEnum):

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        global_enum(cls)


class Bool(LiteralEnum):
    OFF = enum_auto()
    ON = enum_auto()


type OffType = Literal[False, Bool.OFF, 'off']
type BoolType = Literal[False, True, Bool.OFF, Bool.ON, 'off', 'on']


class Auto(LiteralEnum):
    AUTO = enum_auto()


type AutoType = Literal[Auto.AUTO, 'auto']


class LogLevel(LiteralEnum):
    DEBUG = enum_auto()
    INFO = enum_auto()
    NOTICE = enum_auto()
    WARN = enum_auto()
    ERROR = enum_auto()
    CRIT = enum_auto()
    ALERT = enum_auto()
    EMERG = enum_auto()


class StandardStream(LiteralEnum):
    STDERR = 'stderr'


type StderrType = Literal[StandardStream.STDERR, 'stderr']


OFF = Bool.OFF
ON = Bool.ON
AUTO = Auto.AUTO
STDERR = StandardStream.STDERR
