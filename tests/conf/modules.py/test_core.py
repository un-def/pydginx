import pytest

from pydginx.conf.modules.core import Env


class TestEnv:

    def test_only_name(self):
        env = Env('VAR')

        assert env.variable == 'VAR'
        assert env.value is None

    def test_name_value_two_arguments(self):
        env = Env('VAR', 'value')

        assert env.variable == 'VAR'
        assert env.value == 'value'

    def test_name_value_one_argument(self):
        env = Env('VAR=value')

        assert env.variable == 'VAR'
        assert env.value == 'value'

    def test_one_argument_expected(self):
        with pytest.raises(TypeError, match=r'one argument expected'):
            Env('VAR=value1', 'value2')
