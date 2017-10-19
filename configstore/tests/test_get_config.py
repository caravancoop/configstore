from unittest import TestCase
from .test_data import DEFAULT_KEY, DEFAULT_VALUE

import configstore


class TestConfigStore(TestCase):

    def test_returns_default(self):
        configstore.enabled_backends = []
        val = configstore.get_config(DEFAULT_KEY, DEFAULT_VALUE)
        self.assertEqual(DEFAULT_VALUE, val)

    def test_raises(self):
        configstore.enable_backends = []
        with self.assertRaises(configstore.exceptions.ConfigNotFoundException):
            configstore.get_config(DEFAULT_KEY)
