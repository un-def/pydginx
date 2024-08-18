import pytest

from pydginx.conf.contexts import MainContext
from pydginx.conf.directives import Directive

from tests.testlib import dedent


@pytest.fixture
def context() -> MainContext:
    return MainContext()


class SomeDirective(Directive):
    name = 'some_directive'
    context = MainContext
    unique = False


def test_render(context: MainContext) -> None:
    context.add_directives(SomeDirective, SomeDirective)
    assert context.render() == dedent("""
        some_directive;
        some_directive;
    """)
