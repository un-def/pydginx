from __future__ import annotations

from pydginx.conf.directives import SingleValueDataClassDirective
from pydginx.conf.literals import OffType
from pydginx.conf.types import PathOrStr

from .core import HTTP, Server


class AccessLog(SingleValueDataClassDirective[PathOrStr | OffType]):
    pgx_context = HTTP, Server
