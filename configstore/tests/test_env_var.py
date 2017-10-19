from unittest import TestCase
try:
    from unittest import mock
except ImportError:
    import mock
from configstore.backends.env_var import EnvVarBackend
from .test_data import DEFAULT_KEY, DEFAULT_VALUE


class TestEnvVarBackend(TestCase):

    @mock.patch('configstore.backends.env_var.os.environ',
                {DEFAULT_KEY: DEFAULT_VALUE})
    def test_env_var(self):
        b = EnvVarBackend()
        val = b.get_config(DEFAULT_KEY)
        self.assertEqual(DEFAULT_VALUE, val)
