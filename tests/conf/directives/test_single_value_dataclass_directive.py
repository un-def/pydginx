from pydginx.conf.directives import SingleValueDataClassDirective


def test_bool_no_name() -> None:
    class SomeDir(SingleValueDataClassDirective[bool]):
        pass

    assert SomeDir(True).render() == 'some_dir on;\n'


def test_int_with_name() -> None:
    class SomeDir(SingleValueDataClassDirective[int]):
        name = 'foo'

    assert SomeDir(33).render() == 'foo 33;\n'
