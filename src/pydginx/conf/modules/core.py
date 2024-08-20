from __future__ import annotations

from pathlib import Path

from pydginx.conf.contexts import AnyContext, MainContext
from pydginx.conf.directives import (
    Block, DataClassDirective, SingleValueDataClassDirective,
    maybe_escape_string,
)
from pydginx.conf.literals import AutoType, BoolType


class Events(Block):
    context = MainContext


class AcceptMutex(SingleValueDataClassDirective[BoolType]):
    context = Events


class Daemon(SingleValueDataClassDirective[BoolType]):
    context = MainContext


class Env(DataClassDirective):
    context = MainContext
    unique = False

    repr_positional_fields = ['_repr']

    variable: str
    value: str | None = None

    def __post_init__(self) -> None:
        variable, sep, value = self.variable.partition('=')
        if sep:
            if self.value is not None:
                raise TypeError(
                    'one argument expected when VARIABLE=value syntax is used')
            self.variable = variable
            self.value = value

    def render_parameters(self) -> str:
        if self.value is None:
            return self.variable
        return f'{self.variable}={maybe_escape_string(self.value)}'

    @property
    def _repr(self) -> str:
        return self.render_parameters()


class Include(SingleValueDataClassDirective[str | Path]):
    context = AnyContext
    unique = False


class PID(SingleValueDataClassDirective[str | Path]):
    context = MainContext


class WorkerConnections(SingleValueDataClassDirective[int]):
    context = Events


class WorkerProcesses(SingleValueDataClassDirective[int | AutoType]):
    context = MainContext
