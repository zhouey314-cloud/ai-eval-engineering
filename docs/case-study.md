# Case Study — AI Eval Engineering Starter Kit

## Problem
Teams often mistake passing API or schema tests for evidence that an AI feature answers correctly.

## Context
This is a reusable offline starter kit, not an evaluation of a deployed model.

## Constraints
No public provider credentials, no customer examples and no human-verified business ground truth in this repository.

## My Role
Designed the public JSONL case structure, fixture runner, rubric/release-gate templates and failure-analysis guidance.

## Architecture
Datasets in `evals/`, scoring anchors in `rubrics/`, deterministic validation in `runners/`, and baseline/regression/release guidance in `docs/` form a repeatable loop.

## Key Decisions
The runner reports `FIXTURE_SCHEMA_PASS` separately from `MODEL_QUALITY=NOT_RUN`. Cases are labelled `synthetic_unverified`; high-risk failures cannot be waived by a cosmetic aggregate score.

## Hardest Problem
Making the evidence boundary obvious so that a well-shaped synthetic dataset does not become a false model-quality claim.

## Failure/Tradeoff
The portable offline kit is easy to reuse, but without a connected provider, traces and approved expected answers it cannot estimate real-world task success.

## Testing
Run the four selectors in the README and `python3 -m unittest discover -s tests -p 'test_*.py'`; inspect the emitted selector and case count.

## Eval
The included runs validate fixture shape and provenance. A real model eval remains `NOT_RUN` and requires independently reviewed cases.

## Current Evidence
The documented `--full` example reports five synthetic cases passing schema validation. The repository includes a visual release gate and example report.

## Limitations
No measured model correctness, latency, cost or production outcome.

## What I Would Do in Production
Capture traces, get domain-owner review on expected answers, preserve baseline and historical failures, run relevant and high-risk regression sets, then gate release on critical failures.

## What I Learned
An honest `NOT_RUN` is more useful than a score created by the same system that authored its own answers.
