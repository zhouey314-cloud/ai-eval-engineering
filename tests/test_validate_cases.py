import unittest

from runners.validate_cases import validate


class FixtureContractTests(unittest.TestCase):
    def test_golden_fixtures_are_well_formed(self):
        from pathlib import Path

        count, errors = validate(Path(__file__).parents[1] / "evals/golden_set.example.jsonl")
        self.assertGreaterEqual(count, 2)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
