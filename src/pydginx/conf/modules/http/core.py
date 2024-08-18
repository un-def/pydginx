from __future__ import annotations

from pydginx.conf.contexts import MainContext
from pydginx.conf.directives import Block


class HTTP(Block):
    context = MainContext


class Server(Block):
    context = HTTP
    unique = False
