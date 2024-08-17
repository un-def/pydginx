from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .contexts import Context
    from .directives import Directive


class ConfError(Exception):
    pass


class _ContextDirectiveError(ConfError):
    directive: Directive
    context: Context

    def __init__(self, directive: Directive, context: Context) -> None:
        self.directive = directive
        self.context = context


class NotAllowedHere(_ContextDirectiveError):

    def __str__(self) -> str:
        # nginx error example: "default_type" directive is not allowed
        # here in ./nginx.conf:4
        return f'{self.directive!r} is not allowed in {self.context!r}'


class Duplicate(_ContextDirectiveError):

    def __str__(self) -> str:
        # ngix error example "directive is duplicate in nginx.conf:7
        return f'{self.directive!r} is duplicate in {self.context!r}'
