from unittest import TestCase
try:
    from unittest import mock
except ImportError:
    import mock

from configstore.backends.docker_secret import DockerSecretBackend
from .test_data import DEFAULT_KEY, DEFAULT_VALUE, CUSTOM_PATH


class TestDockerSecretBackend(TestCase):

    def test_get_secret(self):
        mocked_open = mock.mock_open(read_data=DEFAULT_VALUE)
        with mock.patch('configstore.backends.docker_secret.open',
                        mocked_open,
                        create=True):
            d = DockerSecretBackend()
            val = d.get_config(DEFAULT_KEY)
            self.assertEqual(DEFAULT_VALUE, val)

    def test_secrets_path(self):
        def open_raises(filename):
            raise FileNotFoundError

        with mock.patch('configstore.backends.docker_secret.open',
                        side_effect=open_raises,
                        create=True):
            d = DockerSecretBackend(CUSTOM_PATH)
            val = d.get_config(DEFAULT_KEY)
            self.assertIsNone(val)
