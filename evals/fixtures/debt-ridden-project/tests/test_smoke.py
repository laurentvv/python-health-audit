"""Excluded decoy: tests/ must be skipped by every audit step.

The unused import below must NOT appear in the report.
"""

import collections  # planted: must stay invisible (tests/ is excluded)
import unittest


class TestSmoke(unittest.TestCase):
    def test_nothing(self):
        self.assertTrue(True)


if __name__ == "__main__":
    _ = collections
    unittest.main()
