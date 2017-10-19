from unittest import TestCase

import configstore

DEFAULT_KEY = 'FAKE_KEY'
DEFAULT_VALUE = 'FAKE_VALUE'


class TestConfigStore(TestCase):

    def test_returns_default(self):
        configstore.enabled_backends = []
        val = configstore.get_config(DEFAULT_KEY, DEFAULT_VALUE)
        self.assertEqual(DEFAULT_VALUE, val)

    def test_raises(self):
        configstore.enable_backends = []
        with self.assertRaises(configstore.exceptions.ConfigNotFoundException):
            configstore.get_config(DEFAULT_KEY)
