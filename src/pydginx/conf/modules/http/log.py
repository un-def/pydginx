from __future__ import annotations

from pathlib import Path

from pydginx.conf.directives import SingleValueDataClassDirective
from pydginx.conf.literals import OffType

from .core import HTTP, Server


class AccessLog(SingleValueDataClassDirective[str | Path | OffType]):
    context = HTTP, Server
