# Example fixture report

Command: `python3 runners/validate_cases.py --full`

```text
FIXTURE_SCHEMA_PASS selector=full cases=5
MODEL_QUALITY=NOT_RUN provider=offline
```

The first line validates fixture shape and provenance. The second line makes
clear that no provider-backed answer quality, latency or cost was measured.
All cases are `synthetic_unverified` until reviewed by a domain owner.
