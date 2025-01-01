from __future__ import annotations

from pydginx.conf.directives import TempPathDirective

from .core import HTTP, Location, Server


class ScgiTempPath(TempPathDirective):
    pgx_context = HTTP, Server, Location
