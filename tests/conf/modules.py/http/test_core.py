from typing import Literal

import pytest

from pydginx.conf.modules.http.core import Location, LocationType


class TestLocation:

    def test_exact(self):
        loc = Location(exact='/some/path')

        assert loc.type is LocationType.EXACT
        assert loc.path == '/some/path'
        # has no meaning for EXACT type
        assert loc.skip_regexes is False
        assert loc.case_sensitive is True

    @pytest.mark.parametrize(
        ['location', 'expected_path'],
        [
            ['=/some/path', '/some/path'],
            ['=\t/some/path ', '/some/path'],
            ['===loc', '==loc'],
        ]
    )
    def test_exact_from_string(self, location: str, expected_path: str):
        loc = Location(location)

        assert loc.type is LocationType.EXACT
        assert loc.path == expected_path
        # has no meaning for EXACT type
        assert loc.skip_regexes is False
        assert loc.case_sensitive is True

    def test_prefix(self):
        loc = Location(prefix='/some/path')

        assert loc.type is LocationType.PREFIX
        assert loc.path == '/some/path'
        assert loc.skip_regexes is False
        # has no meaning for PREFIX type
        assert loc.case_sensitive is True

    @pytest.mark.parametrize("skip_regexes", [False, True])
    def test_prefix_with_skip_regexes(self, skip_regexes: bool):
        loc = Location(prefix='/some/path', skip_regexes=skip_regexes)

        assert loc.type is LocationType.PREFIX
        assert loc.path == '/some/path'
        assert loc.skip_regexes is skip_regexes
        # has no meaning for PREFIX type
        assert loc.case_sensitive is True

    @pytest.mark.parametrize(
        ['location', 'expected_path', 'expected_skip_regexes'],
        [
            ['/some/path', '/some/path', False],
            ['^/some/path ', '^/some/path', False],
            ['^ /some/path', '^ /some/path', False],
            ['^~   /some/path', '/some/path', True],
            ['^~/some/path', '/some/path', True],
        ]
    )
    def test_prefix_from_string(
        self, location: str, expected_path: str, expected_skip_regexes: bool,
    ):
        loc = Location(location)

        assert loc.type is LocationType.PREFIX
        assert loc.path == expected_path
        assert loc.skip_regexes is expected_skip_regexes
        # has no meaning for PREFIX type
        assert loc.case_sensitive is True

    def test_regex(self):
        loc = Location(regex='/some/path')

        assert loc.type is LocationType.REGEX
        assert loc.path == '/some/path'
        assert loc.case_sensitive is True
        # has no meaning for REGEX type
        assert loc.skip_regexes is False

    @pytest.mark.parametrize("case_sensitive", [False, True])
    def test_regex_with_case_sensitive(self, case_sensitive: bool):
        loc = Location(regex='/some/path', case_sensitive=case_sensitive)

        assert loc.type is LocationType.REGEX
        assert loc.path == '/some/path'
        assert loc.case_sensitive is case_sensitive
        # has no meaning for REGEX type
        assert loc.skip_regexes is False

    @pytest.mark.parametrize(
        ['location', 'expected_path', 'expected_case_sensitive'],
        [
            ['~ /some/path', '/some/path', True],
            ['~/some/path', '/some/path', True],
            ['~* /some/path', '/some/path', False],
            ['~*/some/path', '/some/path', False],
        ]
    )
    def test_regex_from_string(
        self, location: str, expected_path: str, expected_case_sensitive: bool,
    ):
        loc = Location(location)

        assert loc.type is LocationType.REGEX
        assert loc.path == expected_path
        assert loc.case_sensitive is expected_case_sensitive
        # has no meaning for REGEX type
        assert loc.skip_regexes is False

    @pytest.mark.parametrize('kwargs', [
        {},
        {'skip_regexes': True},
        {'case_sensitive': True},
    ])
    def test_error_no_args(
        self, kwargs: dict[Literal['skip_regexes', 'case_sensitive'], bool],
    ):
        with pytest.raises(TypeError, match='no required arguments'):
            Location(**kwargs)

    @pytest.mark.parametrize('kwargs', [
        {'exact': '/path'},
        {'prefix': '/path'},
        {'regex': '/path'},
        {'case_sensitive': False},
        {'skip_regexes': False},
    ])
    def test_error_both_pos_and_kw_args(self, kwargs: dict[str, str | bool]):
        with pytest.raises(TypeError, match='mutually exclusive'):
            Location('/path', **kwargs)

    @pytest.mark.parametrize('kwargs', [
        {'exact': '/path', 'prefix': '/path'},
        {'exact': '/path', 'regex': '/path'},
        {'prefix': '/path', 'regex': '/path'},
    ])
    def test_error_multiple_kw_args(
        self, kwargs: dict[Literal['exact', 'prefix', 'regex'], str],
    ):
        with pytest.raises(TypeError, match='multiple arguments'):
            Location(**kwargs)

    @pytest.mark.parametrize('kwargs', [
        {'exact': '/path'},
        {'regex': '/path'},
    ])
    def test_error_skip_regexes_for_prefix_only(self, kwargs: dict[str, str]):
        with pytest.raises(TypeError, match='for prefix path only'):
            Location(**kwargs, skip_regexes=True)

    @pytest.mark.parametrize('kwargs', [
        {'exact': '/path'},
        {'prefix': '/path'},
    ])
    def test_error_case_sensitive_for_regex_only(self, kwargs: dict[str, str]):
        with pytest.raises(TypeError, match='for regex path only'):
            Location(**kwargs, case_sensitive=True)
