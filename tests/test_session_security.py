import importlib.util
import os
from pathlib import Path
import unittest
from unittest.mock import patch


# Load the pure configuration helper without opening the application's database.
spec = importlib.util.spec_from_file_location(
    'session_security',
    Path(__file__).resolve().parents[1] / 'app' / 'session_security.py',
)
security = importlib.util.module_from_spec(spec)
spec.loader.exec_module(security)


class SessionSecretTests(unittest.TestCase):
    def test_missing_key_is_unpredictable_and_differs_between_starts(self):
        with patch.dict(os.environ, {}, clear=True):
            first = security.session_secret()
            second = security.session_secret()
        self.assertGreaterEqual(len(first), 64)
        self.assertNotEqual(first, second)
        self.assertNotEqual(first, 'dev')

    def test_deployment_key_is_preserved_for_shared_workers(self):
        key = 'a-private-deployment-key-with-32-plus-bytes'
        with patch.dict(os.environ, {'SECRET_KEY': key}, clear=True):
            self.assertEqual(security.session_secret(), key)

    def test_empty_and_short_configured_keys_are_rejected(self):
        for key in ('', 'dev', 'a' * 31):
            with self.subTest(key_length=len(key)):
                with patch.dict(os.environ, {'SECRET_KEY': key}, clear=True):
                    with self.assertRaises(ValueError):
                        security.session_secret()


if __name__ == '__main__':
    unittest.main()
