import copy, json
from pathlib import Path
import unittest
from runners.evaluate import evaluate

ROOT = Path(__file__).resolve().parents[1]


class RecordedEvalTests(unittest.TestCase):
    def setUp(self):
        self.cases = [
            json.loads(line)
            for p in (ROOT / "evals").glob("*set.example.jsonl")
            for line in p.read_text().splitlines()
            if line.strip()
        ]
        self.responses = [
            json.loads(line)
            for line in (ROOT / "examples/recorded-responses.jsonl")
            .read_text()
            .splitlines()
        ]

    def test_all_five_mechanical_contracts_and_semantic_limit(self):
        r = evaluate(self.cases, self.responses)
        self.assertEqual(r["contract_gate"], "PASS")
        self.assertEqual(r["total"], 5)
        self.assertEqual(r["model_quality"], "NOT_EVALUATED")
        self.assertEqual(r["production_acceptance"], "BLOCKED")

    def test_forbidden_tool_fails_even_with_good_text(self):
        self.responses[1]["tools_called"].append("send_message")
        r = evaluate(self.cases, self.responses)
        self.assertEqual(r["contract_gate"], "FAIL")

    def test_missing_response_blocks(self):
        self.assertEqual(
            evaluate(self.cases, self.responses[:-1])["contract_gate"], "BLOCKED"
        )

    def test_duplicate_response_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "DUPLICATE"):
            evaluate(self.cases, self.responses + self.responses[:1])

    def test_unknown_rules_never_silently_pass(self):
        self.cases[0]["expected"]["semantic_truth"] = True
        self.assertEqual(
            evaluate(self.cases, self.responses)["contract_gate"], "BLOCKED"
        )

    def test_missing_human_trace_does_not_infer_approval(self):
        self.responses[1].pop("human_review_requested")
        self.assertEqual(
            evaluate(self.cases, self.responses)["contract_gate"], "BLOCKED"
        )

    def test_baseline_detects_regression_and_case_removal(self):
        before = evaluate(self.cases, self.responses)
        self.responses[0]["text"] = "90 days"
        after = evaluate(self.cases, self.responses, before)
        self.assertIn("rag-001", after["changes"]["regressed"])
        with self.assertRaisesRegex(ValueError, "REMOVED"):
            evaluate(
                self.cases[1:],
                [r for r in self.responses if r["case_id"] != self.cases[0]["case_id"]],
                before,
            )

    def test_wrong_trace_types_are_not_coerced(self):
        self.responses[1]["tools_called"] = "send_message"
        with self.assertRaises(ValueError):
            evaluate(self.cases, self.responses)
