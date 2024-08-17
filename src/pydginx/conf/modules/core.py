"""
https://nginx.org/en/docs/ngx_core_module.html

[ ] accept_mutex
[ ] accept_mutex_delay
[x] daemon
[ ] debug_connection
[ ] debug_points
[ ] env
[ ] error_log
[x] events
[ ] include
[ ] load_module
[ ] lock_file
[ ] master_process
[ ] multi_accept
[ ] pcre_jit
[x] pid
[ ] ssl_engine
[ ] thread_pool
[ ] timer_resolution
[ ] use
[ ] user
[ ] worker_aio_requests
[x] worker_connections
[ ] worker_cpu_affinity
[ ] worker_priority
[x] worker_processes
[ ] worker_rlimit_core
[ ] worker_rlimit_nofile
[ ] worker_shutdown_timeout
[ ] working_directory
"""
from __future__ import annotations

from pathlib import Path

from pydginx.conf.contexts import MainContext
from pydginx.conf.directives import Block, SingleValueDataClassDirective
from pydginx.conf.literals import AutoType, BoolType


class Events(Block):
    context = MainContext


class Daemon(SingleValueDataClassDirective[BoolType]):
    context = MainContext


class PID(SingleValueDataClassDirective[str | Path]):
    context = MainContext


class WorkerConnections(SingleValueDataClassDirective[int]):
    context = Events


class WorkerProcesses(SingleValueDataClassDirective[int | AutoType]):
    context = MainContext
