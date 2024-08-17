from __future__ import annotations

from pathlib import Path

from pydginx.conf.contexts import MainContext
from pydginx.conf.directives import Block, SingleValueDataClassDirective
from pydginx.conf.literals import AutoType, BoolType


class Events(Block):
    context = MainContext


class AcceptMutex(SingleValueDataClassDirective[BoolType]):
    context = Events
    unique = True


class Daemon(SingleValueDataClassDirective[BoolType]):
    context = MainContext


class PID(SingleValueDataClassDirective[str | Path]):
    context = MainContext


class WorkerConnections(SingleValueDataClassDirective[int]):
    context = Events


class WorkerProcesses(SingleValueDataClassDirective[int | AutoType]):
    context = MainContext
