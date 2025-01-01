from typing import overload

from pydginx.conf.directives import (
    Block, DataClassDirective, DirectiveType, SingletonDirective,
)
from pydginx.conf.modules.http.core import Location, Server


class If(Block):
    condition: str

    pgx_context = Server, Location
    pgx_unique = False
    pgx_repr_pos = ['condition']

    def __init__(self, condition: str, /, *directives: DirectiveType) -> None:
        self.condition = condition
        super().__init__(*directives)

    def render_parameters(self) -> str:
        return f'({self.condition})'


class Break(SingletonDirective):
    pgx_context = Server, Location, If
    pgx_unique = False


class Return(DataClassDirective):
    code: int | None = None
    text: str | None = None
    url: str | None = None

    pgx_context = Server, Location, If
    pgx_unique = False
    pgx_repr_kw = ['code', 'text', 'url']

    @overload
    def __init__(self, __code: int, /) -> None:
        ...

    @overload
    def __init__(self, __code: int, _text_or_url: str, /) -> None:
        ...

    @overload
    def __init__(self, __url: str, /) -> None:
        ...

    def __init__(
        self, __code_or_url: int | str, __text_or_url: str | None = None,
    ) -> None:
        if isinstance(__code_or_url, str):
            if __text_or_url is not None:
                raise TypeError('url must be a sole argument')
            self.url = __code_or_url
        else:
            self.code = __code_or_url
            if __text_or_url is not None:
                if self.code // 100 == 3:
                    self.url = __text_or_url
                else:
                    self.text = __text_or_url

    def render_parameters(self) -> str | None:
        code = self.code
        url = self.url
        if code is not None:
            if url is not None:
                return f'{code} {url}'
            text = self.text
            if text is not None:
                return f'{code} {text}'
            return str(code)
        return url
