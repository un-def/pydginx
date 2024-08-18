import pytest

from pydginx.conf.directives import Block, Directive

from tests.testlib import dedent


class SomeBlock(Block):
    pass


class SomeDirective(Directive):
    context = SomeBlock
    unique = False


@pytest.fixture
def block() -> SomeBlock:
    return SomeBlock()


def test_bool_false(block: SomeBlock) -> None:
    assert bool(block) is False


def test_bool_true(block: SomeBlock) -> None:
    block <<= SomeDirective
    assert bool(block) is True


def test_render_no_children(block: SomeBlock) -> None:
    assert block.render() == 'some_block {}\n'


def test_render_with_children(block: SomeBlock) -> None:
    block <<= SomeDirective
    block <<= SomeDirective()
    assert block.render() == dedent("""
        some_block {
            some_directive;
            some_directive;
        }
    """)
