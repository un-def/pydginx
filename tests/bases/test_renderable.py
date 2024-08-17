from __future__ import annotations

import textwrap
from collections.abc import Iterator

import pytest

from pydginx.bases import Renderable


def dedent(text: str) -> str:
    return textwrap.dedent(text.lstrip('\n'))


def reindent(prefix: str, text: str) -> str:
    return textwrap.indent(dedent(text), prefix)


class Node(Renderable):

    def __init__(self, name: str, children: list[Node] | None = None) -> None:
        self.name = name
        self.children = children

    def render_iter(
        self, *, indent_level: int = 0, indent_width: int | None = None,
    ) -> Iterator[str]:
        yield self.render_indent(indent_level, indent_width)
        yield self.name
        yield '\n'
        if self.children:
            for child in self.children:
                yield from child.render_iter(
                    indent_level=indent_level + 1,
                    indent_width=indent_width,
                )


@pytest.fixture
def node() -> Node:
    return Node('lvl1', [
        Node('lvl2_1', ), Node('lvl2_2', [
            Node('lvl3'),
        ]),
        Node('lvl2_3'),
    ])


def test_str_method(node: Node) -> None:
    assert str(node) == dedent("""
        lvl1
            lvl2_1
            lvl2_2
                lvl3
            lvl2_3
        """)


def test_render_defaults(node: Node) -> None:
    assert node.render() == dedent("""
        lvl1
            lvl2_1
            lvl2_2
                lvl3
            lvl2_3
        """)


def test_render_custom_width_and_level(node: Node) -> None:
    assert node.render(indent_width=8, indent_level=2) == reindent(
        ' ' * 16,
        """
            lvl1
                    lvl2_1
                    lvl2_2
                            lvl3
                    lvl2_3
        """)
