#!/usr/bin/env python3
"""Validate the offline case contract; never grades model quality."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASETS = {
    "smoke": [ROOT / "evals/golden_set.example.jsonl"],
    "full": [
        ROOT / "evals/golden_set.example.jsonl",
        ROOT / "evals/regression_set.example.jsonl",
        ROOT / "evals/high_risk_set.example.jsonl",
    ],
    "regression": [ROOT / "evals/regression_set.example.jsonl"],
    "high-risk": [ROOT / "evals/high_risk_set.example.jsonl"],
}


def validate(path: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    count = 0
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        count += 1
        try:
            case = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"{path.name}:{line_no}: invalid JSON: {exc.msg}")
            continue
        required = {"case_id", "task_type", "tags", "input", "expected", "ground_truth_status", "provenance"}
        missing = sorted(required - case.keys())
        if missing:
            errors.append(f"{path.name}:{line_no}: missing {', '.join(missing)}")
        if case.get("ground_truth_status") != "synthetic_unverified":
            errors.append(f"{path.name}:{line_no}: example status must be synthetic_unverified")
        if not isinstance(case.get("tags"), list) or not case["tags"]:
            errors.append(f"{path.name}:{line_no}: tags must be a non-empty list")
        if not isinstance(case.get("expected"), dict):
            errors.append(f"{path.name}:{line_no}: expected must be an object")
    return count, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    for name in DATASETS:
        group.add_argument(f"--{name}", action="store_true")
    args = parser.parse_args()
    selector = next((name for name in DATASETS if getattr(args, name.replace("-", "_"))), "smoke")

    total = 0
    errors: list[str] = []
    for path in DATASETS[selector]:
        count, path_errors = validate(path)
        total += count
        errors.extend(path_errors)
    if errors:
        print("BLOCKED")
        print("\n".join(errors))
        return 1
    print(f"FIXTURE_SCHEMA_PASS selector={selector} cases={total}")
    print("MODEL_QUALITY=NOT_RUN provider=offline")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
