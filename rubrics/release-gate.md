# Release gate template

Record one decision per version:

```text
Version:
Commit:
Dataset versions:
Model/provider/config:
Total / passed / failed / blocked:
High-risk pass rate:
Unsupported-claim rate:
Regression count:
Human-review count:
Latency/cost: measured | unavailable
Decision: PASS | FAIL | BLOCKED
Next action:
```

Thresholds are provisional until human-verified history exists. An unavailable
metric is not a pass.
