from __future__ import annotations

from pathlib import Path

from pydginx.conf.contexts import AnyContext, MainContext
from pydginx.conf.directives import (
    Block, DataClassDirective, SingleValueDataClassDirective,
    maybe_escape_string,
)
from pydginx.conf.literals import AutoType, BoolType


class Events(Block):
    pgx_context = MainContext


class AcceptMutex(SingleValueDataClassDirective[BoolType]):
    pgx_context = Events


class Daemon(SingleValueDataClassDirective[BoolType]):
    pgx_context = MainContext


class Env(DataClassDirective):
    name: str
    value: str | None = None

    pgx_context = MainContext
    pgx_unique = False
    pgx_repr_pos = ['_repr']

    def __post_init__(self) -> None:
        variable, sep, value = self.name.partition('=')
        if sep:
            if self.value is not None:
                raise TypeError(
                    'one argument expected when VARIABLE=value syntax is used')
            self.name = variable
            self.value = value

    def render_parameters(self) -> str:
        if self.value is None:
            return self.name
        return f'{self.name}={maybe_escape_string(self.value)}'

    @property
    def _repr(self) -> str:
        return self.render_parameters()


class Include(SingleValueDataClassDirective[str | Path]):
    pgx_context = AnyContext
    pgx_unique = False


class PID(SingleValueDataClassDirective[str | Path]):
    pgx_context = MainContext


class WorkerConnections(SingleValueDataClassDirective[int]):
    pgx_context = Events


class WorkerProcesses(SingleValueDataClassDirective[int | AutoType]):
    pgx_context = MainContext
