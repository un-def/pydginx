from __future__ import annotations

import re
from inspect import isclass
from typing import Any


def instantiate[T](cls_or_obj: type[T] | T, *args: Any, **kwargs: Any) -> T:
    if isclass(cls_or_obj):
        return cls_or_obj(*args, **kwargs)  # pyright: ignore[reportReturnType]
    return cls_or_obj


def to_snake_case(string: str) -> str:
    string = re.sub(r'([A-Z]+)([A-Z][a-z0-9])', r'\1_\2', string)
    string = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', string)
    return string.lower()
