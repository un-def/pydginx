import shutil
from functools import cached_property
from pathlib import Path
from subprocess import Popen
from tempfile import NamedTemporaryFile

from pydginx.conf.contexts import MainContext
from pydginx.conf.literals import AUTO, OFF
from pydginx.conf.modules.core import (
    PID, Daemon, Events, WorkerConnections, WorkerProcesses,
)
from pydginx.conf.modules.http.core import HTTP, Server
from pydginx.conf.modules.http.log import AccessLog


class Conf(MainContext):

    @cached_property
    def events(self) -> Events:
        events = Events()
        self.add_directive(events)
        return events

    @cached_property
    def http(self) -> HTTP:
        http = HTTP()
        self.add_directive(http)
        return http


class Nginx:

    @cached_property
    def conf(self) -> Conf:
        return Conf()

    @cached_property
    def executable(self) -> Path | None:
        for exec in ['nginx', 'openresty']:
            exec_path = shutil.which(exec)
            if exec_path is not None:
                return Path(exec_path)
        return None

    def run(self):
        exec = self.executable
        if not exec:
            raise RuntimeError('nginx executable not found')
        with NamedTemporaryFile(mode='wb', suffix='.nginx.conf') as conf_file:
            conf_file.write(self.conf.render().encode())
            conf_file.flush()
            process = Popen([
                exec, '-e', 'stderr', '-p', '.', '-c', conf_file.name])
            process.wait()


nginx = Nginx()
nginx.conf <<= [
    Daemon(OFF),
    PID('./nginx.pid'),
    WorkerProcesses(AUTO),
]
nginx.conf.events <<= WorkerConnections(100)
nginx.conf.http <<= [
    Server(),
    AccessLog(OFF),
]

nginx.run()
