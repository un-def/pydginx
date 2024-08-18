import shutil
import signal
import subprocess
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from functools import cached_property
from pathlib import Path
from types import FrameType

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
    _process: subprocess.Popen[bytes] | None = None

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
        signal.signal(signal.SIGINT, self.sigint_handler)
        conf = self.conf.render()
        print(conf)
        with self.tempdir() as tempdir:
            conf_path = tempdir / 'nginx.conf'
            with open(conf_path, 'wb') as conf_file:
                conf_file.write(conf.encode())
            process = subprocess.Popen([
                exec, '-e', 'stderr', '-p', tempdir, '-c', conf_file.name])
            self._process = process
            process.wait()

    def sigint_handler(self, signum: int, frame: FrameType | None) -> None:
        if self._process:
            self._process.send_signal(signal.SIGQUIT)

    @contextmanager
    def tempdir(self) -> Iterator[Path]:
        tmpdir = Path(tempfile.mkdtemp())
        try:
            yield tmpdir
        finally:
            shutil.rmtree(tmpdir)


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
