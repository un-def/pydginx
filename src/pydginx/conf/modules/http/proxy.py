from __future__ import annotations

from pydginx.conf.directives import TempPathDirective

from .core import HTTP, Location, Server


class ProxyTempPath(TempPathDirective):
    pgx_context = HTTP, Server, Location
