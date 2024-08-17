import pytest

from pydginx.conf.contexts import AnyContext, Context, SelfContext
from pydginx.conf.directives import Directive


def test_context_none_by_default() -> None:
    class Dir(Directive):
        pass

    assert isinstance(Dir.allowed_context, frozenset)
    assert Dir.allowed_context == set()


def test_context_one_item() -> None:
    class Ctx(Context):
        pass

    class Dir(Directive):
        context = Ctx

    assert isinstance(Dir.allowed_context, frozenset)
    assert Dir.allowed_context == {Ctx}


def test_context_two_items() -> None:
    class Ctx1(Context):
        pass

    class Ctx2(Context):
        pass

    class Dir(Directive):
        context = Ctx1, Ctx2

    assert isinstance(Dir.allowed_context, frozenset)
    assert Dir.allowed_context == {Ctx1, Ctx2}


def test_context_any() -> None:
    class Dir(Directive):
        context = AnyContext

    assert Dir.allowed_context is AnyContext


def test_context_self() -> None:
    class Ctx(Context):
        pass

    class Dir(Directive, Context):
        context = Ctx, SelfContext

    assert isinstance(Dir.allowed_context, frozenset)
    assert Dir.allowed_context == {Ctx, Dir}


def test_context_self_error_if_is_not_context() -> None:
    with pytest.raises(ValueError, match=r'it is not a Context'):
        class Dir(Directive):  # pyright: ignore[reportUnusedClass]
            context = SelfContext


def test_name_auto() -> None:
    class SomeDirective(Directive):
        pass

    assert SomeDirective.name == 'some_directive'


def test_name_provided() -> None:
    class SomeDirective(Directive):
        name = 'foo'

    assert SomeDirective.name == 'foo'


def test_render_no_parameters_no_name() -> None:
    class SomeDirective(Directive):
        pass

    assert SomeDirective().render() == 'some_directive;\n'


def test_render_witn_parameters_and_name() -> None:
    class SomeDirective(Directive):
        name = 'foo'

        def render_parameters(self) -> str:
            return 'bar baz'

    assert SomeDirective().render() == 'foo bar baz;\n'
