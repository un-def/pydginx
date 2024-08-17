from __future__ import annotations

import dataclasses
from collections.abc import Callable, Iterator
from inspect import isclass
from pathlib import Path
from typing import Any, ClassVar, Final, TypeGuard, dataclass_transform

from pydginx.bases import Renderable, Representable, Singleton
from pydginx.utils import to_snake_case

from .contexts import AnyContext, Context, SelfContext
from .literals import OFF, ON, LiteralEnum


type ValueType = str | int | bool | LiteralEnum | Path


def render_value(value: ValueType) -> str:
    if isinstance(value, bool):
        value = ON if value else OFF
    return str(value)


def is_directive(__obj_or_cls: Any, /) -> TypeGuard[DirectiveType]:
    if isclass(__obj_or_cls):
        return issubclass(__obj_or_cls, Directive)
    return isinstance(__obj_or_cls, Directive)


class Directive(Renderable, Representable):
    name: ClassVar[str]
    context: ClassVar[
        type[Context] | list[type[Context]] | tuple[type[Context], ...]] = ()
    unique: ClassVar[bool] = False

    # computed automatically from context class variable
    allowed_context: ClassVar[frozenset[type[Context]] | type[AnyContext]]

    def __init_subclass__(cls) -> None:
        # see: https://github.com/python/cpython/issues/114326
        super().__init_subclass__()
        try:
            name = cls.__dict__['name']
        except KeyError:
            name = to_snake_case(cls.__name__)
            cls.name = name
        context = cls.context
        if context is AnyContext:
            cls.allowed_context = AnyContext
        else:
            if isclass(context):
                context = (context,)
            allowed_context: set[type[Context]] = set()
            for ctx in context:
                if ctx is SelfContext:
                    if not issubclass(cls, Context):
                        raise ValueError(
                            f'{cls.__name__} cannot use SelfContext '
                            'since it is not a Context'
                        )
                    ctx = cls
                allowed_context.add(ctx)
            cls.allowed_context = frozenset(allowed_context)

    def render_directive(self) -> str:
        return self.name

    def render_parameters(self) -> str | None:
        return None

    def render_iter(
        self, *, indent_level: int = 0, indent_width: int | None = None,
    ) -> Iterator[str]:
        yield self.render_indent(indent_level, indent_width)
        yield self.render_directive()
        parameters = self.render_parameters()
        if parameters:
            yield f' {parameters}'
        yield ';\n'


type DirectiveType = Directive | type[Directive]


class SingletonDirective(Singleton, Directive):
    pass


@dataclasses.dataclass(eq=False, frozen=True, repr=False, match_args=False)
class SingleValueDataClassDirective[T: ValueType](Directive):
    value: T

    repr_positional_fields = 'value'

    def render_parameters(self) -> str:
        return render_value(self.value)


@dataclass_transform(
    kw_only_default=True, eq_default=False, frozen_default=True)
class DataClassDirective(Directive):
    _transform: Final[Callable[[type[Directive]], type[Directive]]]
    _transform = dataclasses.dataclass(
        kw_only=True, eq=False, frozen=True, repr=False, match_args=False)

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls._transform(cls)


class Block(Context, Directive):

    def __init__(self, *directives: DirectiveType) -> None:
        super().__init__()
        self.add_directives(directives)

    def render_iter(
        self, *, indent_level: int = 0, indent_width: int | None = None,
    ) -> Iterator[str]:
        yield self.render_indent(indent_level, indent_width)
        yield self.render_directive()
        parameters = self.render_parameters()
        if parameters:
            yield f' {parameters}'
        if self._directives:
            yield ' {\n'
            next_indent_level = indent_level + 1
            for directive in self._directives:
                yield from directive.render_iter(
                    indent_level=next_indent_level, indent_width=indent_width)
            yield self.render_indent(indent_level, indent_width)
            yield '}\n'
        else:
            yield ' {}\n'
