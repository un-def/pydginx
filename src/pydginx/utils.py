from __future__ import annotations

import re
from inspect import isclass
from typing import Any, Self, overload


class ReadOnlyProxy[T]:

    def __set_name__(self, owner: type, name: str) -> None:
        self._private_name = f'_{name}'

    @overload
    def __get__[O](self, instance: None, owner: type[O] | None = None) -> Self:
        ...

    @overload
    def __get__[O](self, instance: O, owner: type[O] | None = None) -> T:
        ...

    def __get__[O](
        self, instance: O | None, owner: type[O] | None = None,
    ) -> T | Self:
        if instance is None:
            return self
        return getattr(instance, self._private_name)


def instantiate[T](cls_or_obj: type[T] | T, *args: Any, **kwargs: Any) -> T:
    if isclass(cls_or_obj):
        return cls_or_obj(*args, **kwargs)  # pyright: ignore[reportReturnType]
    return cls_or_obj


def to_snake_case(string: str) -> str:
    string = re.sub(r'([A-Z]+)([A-Z][a-z0-9])', r'\1_\2', string)
    string = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', string)
    return string.lower()
