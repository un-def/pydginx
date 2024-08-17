from __future__ import annotations

from collections.abc import Iterable, Iterator
from functools import cached_property
from typing import TYPE_CHECKING, Self, final, overload

from pydginx.bases import NonInstantiable, Renderable
from pydginx.utils import instantiate

from .exceptions import Duplicate, NotAllowedHere


if TYPE_CHECKING:
    from .directives import Directive, DirectiveType


class Context:
    _unique_directives: set[type[Directive]]

    def __init__(self) -> None:
        self._unique_directives = set()

    @property
    def directives(self) -> tuple[Directive, ...]:
        return tuple(self._directives)

    def __bool__(self) -> bool:
        return bool(self._directives)

    def _add_directives_and_return_self(
        self, __directives: Iterable[DirectiveType] | DirectiveType, /,
    ) -> Self:
        self.add_directives(__directives)
        return self

    __lshift__ = _add_directives_and_return_self
    __ilshift__ = _add_directives_and_return_self

    def add_directive(self, directive: DirectiveType) -> None:
        self._add_directives((directive,))

    @overload
    def add_directives(self, __directives: Iterable[DirectiveType], /) -> None:
        ...

    @overload
    def add_directives(
        self, __directieves: DirectiveType, /, *directives: DirectiveType,
    ) -> None:
        ...

    def add_directives(
        self, __directives: Iterable[DirectiveType] | DirectiveType, /,
        *directives: DirectiveType,
    ) -> None:
        from .directives import is_directive

        _directives: Iterable[DirectiveType]
        if is_directive(__directives):
            _directives = (__directives,) + directives
        else:
            if directives:
                raise TypeError(
                    'extra arguments are not allowed '
                    'if the first argument is an Iterable'
                )
            _directives = __directives  # pyright: ignore[reportAssignmentType]
        self._add_directives(_directives)

    def _add_directives(self, directives: Iterable[DirectiveType]) -> None:
        cls = type(self)
        if issubclass(cls, MainContext):
            # allow MainContext subclassing
            cls = MainContext
        for directive in directives:
            directive = instantiate(directive)
            if directive.unique:
                directive_cls = type(directive)
                if directive_cls in self._unique_directives:
                    raise Duplicate(directive, self)
                self._unique_directives.add(directive_cls)
            allowed_context = directive.allowed_context
            if allowed_context is AnyContext or cls in allowed_context:
                self._directives.append(directive)
            else:
                raise NotAllowedHere(directive=directive, context=self)

    @cached_property
    def _directives(self) -> list[Directive]:
        return []


class SpecialContext(Context):
    pass


@final
class AnyContext(NonInstantiable, SpecialContext):
    pass


@final
class SelfContext(NonInstantiable, SpecialContext):
    pass


class MainContext(Renderable, SpecialContext):

    def render_iter(
        self, *, indent_level: int = 0, indent_width: int | None = None,
    ) -> Iterator[str]:
        for directive in self._directives:
            yield from directive.render_iter(
                indent_level=indent_level, indent_width=indent_width)
