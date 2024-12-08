from pydginx.bases import Representable


def test_no_fields() -> None:
    class Cls(Representable):
        pass

    assert repr(Cls()) == 'Cls()'


def test_single_positional_field() -> None:
    class Cls(Representable):
        field: str
        pgx_repr_pos = 'field'

    obj = Cls()
    obj.field = 'val'

    assert repr(obj) == "Cls('val')"


def test_multiple_positional_fields() -> None:
    class Cls(Representable):
        field_1: int
        field_2: bool
        field_3: list[str]
        pgx_repr_pos = ('field_1', 'field_3')

    obj = Cls()
    obj.field_1 = 3
    obj.field_3 = ['foo', 'bar']

    assert repr(obj) == "Cls(3, ['foo', 'bar'])"


def test_single_keyword_field() -> None:
    class Cls(Representable):
        field: str
        pgx_repr_kw = 'field'

    obj = Cls()
    obj.field = 'val'

    assert repr(obj) == "Cls(field='val')"


def test_multiple_keyword_fields() -> None:
    class Cls(Representable):
        field_1: int
        field_2: bool
        field_3: list[str]
        pgx_repr_kw = ('field_1', 'field_3')

    obj = Cls()
    obj.field_1 = 3
    obj.field_3 = ['foo', 'bar']

    assert repr(obj) == "Cls(field_1=3, field_3=['foo', 'bar'])"


def test_both_positional_and_keyword_fields() -> None:
    class Cls(Representable):
        field_1: int
        field_2: bool
        field_3: list[str]
        pgx_repr_kw = ['field_3', 'field_1']
        pgx_repr_pos = ['field_2']

    obj = Cls()
    obj.field_1 = 3
    obj.field_2 = True
    obj.field_3 = ['foo', 'bar']

    assert repr(obj) == "Cls(True, field_3=['foo', 'bar'], field_1=3)"


def test_missing_positional_field() -> None:
    class Cls(Representable):
        pgx_repr_pos = 'field'
        field: str

    obj = Cls()

    assert repr(obj) == 'Cls(<NOTSET>)'


def test_missing_keyword_field() -> None:
    class Cls(Representable):
        field: str
        pgx_repr_kw = 'field'

    obj = Cls()

    assert repr(obj) == 'Cls(field=<NOTSET>)'
