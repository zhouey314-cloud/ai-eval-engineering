# Project AI quality policy

- Separate traditional tests from probabilistic evals.
- Mark unverified examples `synthetic_unverified`.
- Never promote a model-generated answer to Golden Set truth without a human
  owner and source provenance.
- Preserve difficult and historical failures in Regression.
- Treat malformed judge output, missing providers and missing evidence as
  `blocked` or `needs_human_review`, not PASS.
