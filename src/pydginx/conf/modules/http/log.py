"""
https://nginx.org/en/docs/http/ngx_http_log_module.html

[ ] access_log
[ ] log_format
[ ] open_log_file_cache
"""
from __future__ import annotations

from pathlib import Path

from pydginx.conf.directives import SingleValueDataClassDirective
from pydginx.conf.literals import OffType

from .core import HTTP, Server


class AccessLog(SingleValueDataClassDirective[str | Path | OffType]):
    context = HTTP, Server
