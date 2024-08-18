from collections.abc import Iterable

import pytest

from pydginx.conf.contexts import Context
from pydginx.conf.directives import Directive
from pydginx.conf.exceptions import Duplicate


class SomeContext(Context):
    pass


class SomeDirective(Directive):
    name = 'some_directive'
    context = SomeContext
    unique = False


@pytest.fixture
def context() -> SomeContext:
    return SomeContext()


def test_bool_false(context: SomeContext) -> None:
    assert bool(context) is False


def test_bool_true(context: SomeContext) -> None:
    context.add_directive(SomeDirective)
    assert bool(context) is True


def test_add_directive(context: SomeContext) -> None:
    directive = SomeDirective()

    context.add_directive(directive)
    context.add_directive(SomeDirective)

    assert len(context.directives) == 2
    assert context.directives[0] is directive
    assert isinstance(context.directives[1], SomeDirective)


def test_add_directives_varargs(context: SomeContext) -> None:
    directive = SomeDirective()

    context.add_directives(directive, SomeDirective)

    assert len(context.directives) == 2
    assert context.directives[0] is directive
    assert isinstance(context.directives[1], SomeDirective)


@pytest.mark.parametrize('iterable', [
    [SomeDirective(), SomeDirective],
    (SomeDirective(), SomeDirective),
    (SomeDirective for _ in range(2)),
])
def test_add_directives_iterable(
    context: SomeContext, iterable: Iterable[Directive | type[Directive]],
) -> None:
    context.add_directives(iterable)

    assert len(context.directives) == 2
    assert isinstance(context.directives[0], SomeDirective)
    assert isinstance(context.directives[1], SomeDirective)


def test_lshift(context: SomeContext) -> None:
    context << SomeDirective  # pyright: ignore[reportUnusedExpression]
    context << [
        SomeDirective(), SomeDirective,
    ]  # pyright: ignore[reportUnusedExpression]
    context << (
        SomeDirective(), SomeDirective,
    )  # pyright: ignore[reportUnusedExpression]
    context << (
        SomeDirective for _ in range(2)
    )  # pyright: ignore[reportUnusedExpression]

    assert len(context.directives) == 7
    assert all(isinstance(d, SomeDirective) for d in context.directives)


def test_ilshift(context: SomeContext) -> None:
    context <<= SomeDirective
    context <<= [SomeDirective(), SomeDirective]
    context <<= (SomeDirective(), SomeDirective)
    context <<= (SomeDirective for _ in range(2))

    assert len(context.directives) == 7
    assert all(isinstance(d, SomeDirective) for d in context.directives)


def test_one_unique_directive(context: SomeContext) -> None:
    class NotUniqueDirective(Directive):
        context = SomeContext
        unique = False

    class UniqueDirective(Directive):
        context = SomeContext

    context <<= NotUniqueDirective
    context <<= UniqueDirective
    context <<= NotUniqueDirective()


def test_two_same_unique_is_error(context: SomeContext) -> None:
    class UniqueDirective1(Directive):
        context = SomeContext
        unique = True

    class UniqueDirective2(Directive):
        context = SomeContext
        unique = True

    context <<= UniqueDirective1
    context <<= UniqueDirective2()

    with pytest.raises(Duplicate, match=r'duplicate'):
        context <<= UniqueDirective1()
