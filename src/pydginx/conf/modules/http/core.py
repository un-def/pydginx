from __future__ import annotations

from pydginx.conf.contexts import MainContext
from pydginx.conf.directives import Block


class HTTP(Block):
    pgx_context = MainContext


class Server(Block):
    pgx_context = HTTP
    pgx_unique = False
