from __future__ import annotations

import enum
from typing import overload

from pydginx.conf.contexts import MainContext, SelfContext
from pydginx.conf.directives import (
    Block, DataClassDirective, SingletonDirective,
    SingleValueDataClassDirective,
)


class HTTP(Block):
    pgx_context = MainContext


class Server(Block):
    pgx_context = HTTP
    pgx_unique = False


class LocationType(enum.Enum):
    EXACT = enum.auto()
    PREFIX = enum.auto()
    REGEX = enum.auto()


class Location(Block, DataClassDirective):
    type: LocationType
    path: str
    skip_regexes: bool
    case_sensitive: bool

    pgx_context = Server, SelfContext
    pgx_unique = False
    pgx_repr_kw = ['type', 'path', 'skip_regexes', 'case_sensitive']

    @overload
    def __init__(self, __str: str, /) -> None:
        ...

    @overload
    def __init__(self, /, *, exact: str) -> None:
        ...

    @overload
    def __init__(
        self, /, *, prefix: str, skip_regexes: bool | None = None,
    ) -> None:
        ...

    @overload
    def __init__(
        self, /, *, regex: str | None = None,
        case_sensitive: bool | None = None,
    ) -> None:
        ...

    def __init__(
        self, __str: str | None = None, /, *, exact: str | None = None,
        prefix: str | None = None, skip_regexes: bool | None = None,
        regex: str | None = None, case_sensitive: bool | None = None,
    ) -> None:
        super().__init__()
        # defaults; may be overridden later
        self.skip_regexes = False
        self.case_sensitive = True
        types: list[LocationType] = []
        path: str | None = None
        if exact is not None:
            types.append(LocationType.EXACT)
            path = exact
        if prefix is not None:
            types.append(LocationType.PREFIX)
            path = prefix
        if regex is not None:
            types.append(LocationType.REGEX)
            path = regex
        if __str is not None:
            if types or skip_regexes is not None or case_sensitive is not None:
                raise TypeError(
                    'positional argument and keyword arguments '
                    'are mutually exclusive'
                )
            self._parse_location_string(__str)
            return
        elif not types:
            raise TypeError('no required arguments specified')
        elif len(types) > 1:
            raise TypeError('multiple arguments specified')
        self.type = types[0]
        assert path is not None
        self.path = path
        if skip_regexes is not None:
            if self.type is not LocationType.PREFIX:
                raise TypeError(
                    'skip_regexes argument is for prefix path only')
            self.skip_regexes = skip_regexes
        if case_sensitive is not None:
            if self.type is not LocationType.REGEX:
                raise TypeError(
                    'case_sensitive argument is for regex path only')
            self.case_sensitive = case_sensitive

    def _parse_location_string(self, location: str) -> None:
        if not location:
            raise ValueError('empty location')
        match location[0]:
            case '=':
                self.type = LocationType.EXACT
                self.path = location[1:].strip()
            case '^':
                self.type = LocationType.PREFIX
                if location.startswith('^~'):
                    self.path = location[2:].strip()
                    self.skip_regexes = True
                else:
                    self.path = location.strip()
            case '~':
                self.type = LocationType.REGEX
                if location.startswith('~*'):
                    self.case_sensitive = False
                    self.path = location[2:].strip()
                else:
                    self.path = location[1:].strip()
            case _:
                self.type = LocationType.PREFIX
                self.path = location.strip()

    def render_parameters(self) -> str:
        match self.type:
            case LocationType.EXACT:
                return f'= {self.path}'
            case LocationType.PREFIX:
                if self.skip_regexes:
                    return f'^~ {self.path}'
                return self.path
            case LocationType.REGEX:
                if self.case_sensitive:
                    return f'~ {self.path}'
                return f'~* {self.path}'
        assert False, 'should not reach here'


class Alias(SingleValueDataClassDirective[str]):
    pgx_context = Location


class DefaultType(SingleValueDataClassDirective[str]):
    pgx_context = HTTP, Server, Location


class Internal(SingletonDirective):
    pgx_context = Location
