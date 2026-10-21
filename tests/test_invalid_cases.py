import json
from pathlib import Path
import tempfile
import unittest
from runners.validate_cases import validate


class InvalidFixtureTests(unittest.TestCase):
    def check_errors(self, rows):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'cases.jsonl'
            path.write_text('\n'.join(json.dumps(row) for row in rows), encoding='utf-8')
            count, errors = validate(path)
        self.assertTrue(errors, 'invalid fixtures must fail the contract gate')
        return errors

    def test_non_object_rows_are_errors_instead_of_crashes(self):
        for row in [None, [], 'text', 1]:
            with self.subTest(row=row):
                self.assertIn('object', ' '.join(self.check_errors([row])))

    def test_empty_dataset_is_not_a_pass(self):
        self.check_errors([])

    def test_duplicate_or_empty_case_ids_fail(self):
        source = Path(__file__).parents[1] / 'evals/golden_set.example.jsonl'
        case = json.loads(source.read_text().splitlines()[0])
        self.check_errors([case, case])
        self.check_errors([{**case, 'case_id': ''}])
