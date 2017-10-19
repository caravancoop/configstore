from unittest import TestCase
from .test_data import DEFAULT_KEY, DEFAULT_VALUE

import configstore


class TestConfigStore(TestCase):

    def test_returns_default(self):
        backends = []
        store = configstore.Store(backends)
        val = store.get_config(DEFAULT_KEY, DEFAULT_VALUE)
        self.assertEqual(DEFAULT_VALUE, val)

    def test_raises(self):
        backends = []
        store = configstore.Store(backends)
        with self.assertRaises(configstore.exceptions.ConfigNotFoundException):
            store.get_config(DEFAULT_KEY)
