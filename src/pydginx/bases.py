from __future__ import annotations

from collections.abc import Iterator
from itertools import chain
from typing import ClassVar, Never, Protocol, Self


class Singleton:
    slots = ('_instance',)
    _instance: ClassVar[Self]

    def __new__(cls) -> Self:
        try:
            return cls.__dict__['_instance']
        except KeyError:
            pass
        cls._instance = instance = super().__new__(cls)
        return instance


class NonInstantiable:

    def __new__(cls) -> Never:
        raise TypeError(f'{cls.__name__} cannot be instantiated')


class _NotSet(Singleton):

    def __str__(self) -> str:
        return '<NOTSET>'

    __repr__ = __str__


_NOTSET = _NotSet()


class Representable:
    repr_positional_fields: ClassVar[list[str] | tuple[str, ...] | str] = ()
    repr_keyword_fields: ClassVar[list[str] | tuple[str, ...] | str] = ()

    def __repr__(self) -> str:
        pos_fields = self.repr_positional_fields
        if isinstance(pos_fields, str):
            pos_fields = (pos_fields,)
        kw_fields = self.repr_keyword_fields
        if isinstance(kw_fields, str):
            kw_fields = (kw_fields,)
        name = self.__class__.__name__
        values = ', '.join(chain(
            (repr(getattr(self, f, _NOTSET)) for f in pos_fields),
            (f'{f}={getattr(self, f, _NOTSET)!r}' for f in kw_fields),
        ))
        return f'{name}({values})'


class Renderable(Protocol):
    DEFAULT_INDENT_WIDTH = 4

    def __str__(self) -> str:
        return self.render()

    def render(
        self, *, indent_level: int = 0, indent_width: int | None = None,
    ) -> str:
        return ''.join(self.render_iter(
            indent_level=indent_level,
            indent_width=indent_width,
        ))

    def render_indent(self, level: int = 0, width: int | None = None) -> str:
        if not level:
            return ''
        if width is None:
            width = self.DEFAULT_INDENT_WIDTH
        return ' ' * level * width

    def render_iter(
        self, *, indent_level: int = 0, indent_width: int | None = None,
    ) -> Iterator[str]:
        raise NotImplementedError
