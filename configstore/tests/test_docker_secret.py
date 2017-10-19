from unittest import TestCase
try:
    from unittest import mock
except ImportError:
    import mock

from configstore.backends.docker_secret import DockerSecretBackend
from .test_data import DEFAULT_KEY, DEFAULT_VALUE, CUSTOM_PATH


class TestDockerSecretBackend(TestCase):

    @mock.patch('configstore.backends.docker_secret.os.path.exists',
                return_value=True)
    def test_get_secret(self, mocked_exists):
        mocked_open = mock.mock_open(read_data=DEFAULT_VALUE)
        with mock.patch('configstore.backends.docker_secret.open',
                        mocked_open,
                        create=True):
            d = DockerSecretBackend()
            val = d.get_config(DEFAULT_KEY)
            self.assertEqual(DEFAULT_VALUE, val)

    @mock.patch('configstore.backends.docker_secret.os.path.exists',
                return_value=False)
    def test_secrets_path(self, mocked_exists):
        mocked_open = mock.MagicMock()
        with mock.patch('configstore.backends.docker_secret.open',
                        mocked_open,
                        create=True):
            d = DockerSecretBackend(CUSTOM_PATH)
            val = d.get_config(DEFAULT_KEY)
            self.assertIsNone(val)
