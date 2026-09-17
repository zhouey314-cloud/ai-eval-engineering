---
name: eval-engineering
description: Use this skill whenever building, modifying, debugging, comparing, or releasing an AI or probabilistic system involving prompts, RAG, knowledge retrieval, agents, workflows, tool calling, model behavior, semantic outputs, AI-generated content, or AI business logic. Establish a baseline, evaluate outcome and trajectory, analyze failures, and make release decisions with evidence. Do not use the full workflow for purely deterministic software changes unless the user asks for it.
---

# Eval Engineering

Operate AI work as an evidence loop:

`Baseline → Build → Test → Eval → Analyze → Fix → Regression Eval → Release`

The goal is not a high score. The goal is a defensible answer to “does this
version solve the real task safely, and what should be fixed next?”

## 1. Decide whether this skill applies

First classify the requested change and inspect the repository. Use the full
workflow when the change can alter a model's output, retrieval, decision,
tool-use trajectory, generated content, or interpretation of user input. This
includes prompt edits, RAG, agent/workflow changes, tool calling, model changes,
semantic classification, and AI business logic.

Use ordinary project tests only for changes with no meaningful AI-behavior
surface, such as CSS/layout, deterministic calculations, migrations, renames,
static docs, or non-AI CRUD. If the boundary is mixed, evaluate the AI-facing
portion and test the deterministic portion.

Do not create a large template framework before understanding the project.

## 2. Scan and define business success

Before editing behavior, inspect the repository and its runtime context:

- README, AGENTS.md, docs, source, prompts, workflows, agents, tools, RAG,
  knowledge bases, APIs, schemas, sample data, logs, reports, and tests.
- Existing evals, rubrics, human decisions, support tickets, production
  failures, and business policies.
- The executable entry point, model/provider configuration, tool interfaces,
  observability, network requirements, and available credentials.

Write a concise project-specific success contract before writing cases. Capture
the business goal, users, critical user journeys, AI tasks, deterministic
components, probabilistic components, failure definition, high-risk outcomes,
and what evidence is authoritative. Prefer a project `evals/PROJECT_EVAL_SPEC.md`
when the repository is willing to store this asset.

For each task answer:

1. What user outcome counts as success?
2. What must be true in the final answer or action?
3. What must never happen?
4. Which failures are critical even if the overall score is high?
5. Which facts are grounded in repository or business evidence?

Separate software health from AI quality. Traditional tests cover API,
function, database, JSON/schema, tool arguments, deterministic logic,
integration, and E2E mechanics. Evals cover correctness, task success,
relevance, completeness, groundedness, hallucination, instruction following,
business-rule compliance, retrieval, agent behavior, and final-answer quality.

## 3. Choose the smallest useful project architecture

Adapt to the project. A small system may need one JSONL dataset, a rule checker,
and a runner. A high-risk system may need:

```text
evals/
  PROJECT_EVAL_SPEC.md
  datasets/       # golden, edge, regression, review queue
  rubrics/        # versioned scoring definitions
  evaluators/     # deterministic and semantic evaluators
  runners/        # stable local entry point
  baselines/      # immutable run artifacts
  reports/        # machine-readable and human-readable results
```

Keep the runner reproducible. Record commit/version, prompt/model/config
versions, dataset version, timestamps, latency, token usage/cost when available,
raw candidate output, trace/tool events, evaluator version, and human-review
status. Never silently turn an unavailable dependency into PASS.

## 4. Build datasets without inventing authority

Construct cases from real user journeys, existing tests and examples, prompts,
business rules, logs, historical failures, and verified production incidents.
Cover normal high-frequency cases plus:

- edge and boundary values;
- negative and refusal cases;
- ambiguous or underspecified input;
- missing information;
- tool timeout, failure, empty, malformed, or contradictory results;
- retrieval miss, stale knowledge, wrong document, and unsupported claim;
- adversarial or confusing instructions;
- high-risk decisions and irreversible actions;
- historical failures and known regressions.

Use stable case IDs and explicit tags such as `normal`, `edge`, `negative`,
`ambiguous`, `missing_information`, `tool_failure`, `retrieval_failure`,
`adversarial`, `high_risk`, and `historical_failure`.

Never present a model-generated answer as human truth. Every expected answer or
constraint must carry provenance. Use `ground_truth_status` values such as
`human_verified`, `source_verified`, `synthetic_unverified`, or
`needs_human_review`. Put unverified candidate cases in a human review queue and
include the reviewer question: what exactly must be true, what is forbidden,
and which source or policy decides it? Only promote a case into the Golden Set
after the required owner confirms it.

For sensitive domains—HR, legal, medical, financial, customer decisions, or
other high-impact outcomes—do not infer the final business standard from model
intuition. Ask for the minimum human decision needed and retain the decision
provenance.

Maintain separate Golden, Edge, Regression, and Human Review sets when their
governance differs. Add verified production failures to Regression rather than
removing them or changing their expected result to improve a score.

## 5. Design metrics and rubrics

Choose metrics per task. Do not collapse all behavior into Overall Pass Rate.
At minimum, consider Task Success, Correctness, Completeness, Relevance,
Instruction Following, Groundedness, Hallucination/Unsupported Claim Rate,
Business Rule Compliance, latency, and cost.

For RAG, separately measure retrieval and generation:

- retrieval hit rate, recall, precision, correct-document rate, rank/coverage;
- groundedness, citation correctness, supported versus unsupported claims.

A wrong answer after the right document was retrieved is primarily a generation
failure. A right-looking answer without the required document is not evidence of
retrieval success.

For agents and workflows, measure both outcome and trajectory/trace:

- task success and final answer quality;
- tool selection, exact arguments, result usage, step count, unnecessary calls;
- recovery from tool failure, human escalation, policy compliance, and trace
  completeness.

Version rubrics as data. Each scoring dimension needs observable 0–5 or 1–5
anchors, a pass threshold, and critical-failure conditions. Example:

```text
Groundedness 5: every material claim is supported by supplied evidence.
Groundedness 3: the main answer is supported but contains minor unsupported detail.
Groundedness 1: a material decision relies on an invented or contradicted fact.
Pass: score >= 4 and no critical failure.
Critical: fabricated source, unsafe action, protected-attribute decision,
or violation of an explicit business constraint.
```

Avoid labels such as “good,” “professional,” or “high quality” without
observable anchors.

## 6. Implement deterministic rules first

Use code instead of an LLM for checks that are mechanically decidable:

- JSON/schema, required fields, types, URLs, numbers, dates, status values;
- forbidden terms, hard business constraints, formatting contracts;
- tool name and argument shape, allowed transitions, and exact invariants.

Rule evaluators must be deterministic, reproducible, and emit a structured
failure reason with case ID, rule ID, observed value, and expected constraint.
Rule failures are not repaired by asking an LLM to reinterpret the same result.

## 7. Use LLM-as-a-Judge carefully

Use a judge only for semantic dimensions that cannot be reliably coded. The
judge input should include the user task, relevant context, reference or
ground-truth constraints, candidate output, rubric, and business constraints.

Version the judge prompt and configuration. Prefer a stable temperature/config,
record the judge model, save the raw response, require schema validation, and
treat judge errors or uncertainty as `needs_human_review`, never PASS.

Require structured output such as:

```json
{
  "task_success": 4,
  "correctness": 5,
  "completeness": 4,
  "groundedness": 3,
  "instruction_following": 5,
  "critical_failure": false,
  "pass": false,
  "reason": "Main answer is supported; one material claim lacks evidence.",
  "failure_type": "hallucination",
  "confidence": 0.82,
  "human_review_needed": false
}
```

The runner must reject malformed judge output and preserve the candidate and
judge artifacts for audit. Do not use one judge score as the only release gate
for a high-risk decision.

## 8. Build a baseline before changing behavior

Run the smallest meaningful baseline before editing. For broad or high-risk
changes, run the full current set; otherwise run the relevant smoke and
regression sets plus at least one high-risk slice. Record the exact version,
inputs, outputs, traces, metrics, failures, and blocked cases.

If the project has no executable path or credentials, still build offline
infrastructure and run deterministic checks against fixtures, but label the
runtime baseline `blocked` with the exact missing dependency. Do not simulate
model success or fabricate latency/cost.

Report at least total, passed, failed, blocked, pass rate, task success,
high-risk pass rate, hallucination rate, average/p95 latency when measured,
cost when measured, regression count, human-review count, and failure taxonomy.

## 9. Analyze, fix, and compare

Classify every failure with the best evidence-supported root cause:

`Prompt | Retrieval | Knowledge | Parsing | Tool Selection | Tool Arguments |
Tool Failure | Workflow | Hallucination | Instruction Following | Business Rule |
Formatting | Model Capability | Latency | Cost | Unknown`

Do not label every problem “Prompt.” Distinguish retrieval failure from
generation failure and tool failure from tool-selection/argument errors.

Prioritize with:

`Impact × Frequency × Risk × Fixability`

For the highest-value low-risk issue, preserve the old baseline, make the
smallest fix, run traditional tests, rerun the same evals, and compare:

- improved cases;
- regressed cases;
- unchanged cases;
- new failures;
- metric deltas and changed traces.

If the fix changes expected business behavior, obtain human approval and record
why; do not silently rewrite the Golden Set.

## 10. Release gates

Create gates per project risk, not by copying universal numbers. Mark first-pass
thresholds `provisional` when there is not enough verified history, and state
how they will be calibrated.

Consider gates for Overall Pass Rate, high-risk pass rate, hallucination or
unsupported-claim rate, critical failures, regression count, latency, and cost.
Hard safety/business constraints should be zero-tolerance where appropriate.
An unavailable metric is `blocked` or `unknown`, not a pass.

The release decision must say `PASS`, `FAIL`, or `BLOCKED`, show the evidence,
and identify the next action. Never claim “done” when a critical gate fails or
an unacceptable regression is unexplained.

## 11. Offline and production feedback loops

Offline evals are repeatable fixture/dataset runs used before merge and release.
Keep them deterministic where possible and isolate network/provider variance.

Production evals use sampled traces, user feedback, incident data, latency/cost,
retrieval evidence, tool events, and human outcomes. Respect privacy and access
controls; minimize or redact sensitive data. Sample high-risk and failure-prone
paths, not only successful traffic.

Convert production learning into durable assets:

```text
Production Failure
  → Human Verification
  → Regression Case
  → Smallest Fix
  → Tests + Re-Eval
  → Release Decision
```

## 12. Handoff and Definition of Done

For a completed AI-behavior task, report:

1. what changed and why;
2. baseline and new-version metrics;
3. improved, regressed, unchanged, and new-failure cases;
4. failure taxonomy and prioritized next fixes;
5. release-gate decision and any blocked dependency;
6. human-review items and ground-truth provenance;
7. exact commands used so the result is reproducible.

When a project supports it, add one stable runner with focused selectors such
as `--smoke`, `--full`, `--regression`, `--high-risk`, `--case-id`, and
`--baseline`. Adapt names to the project's tooling and document the command in
its eval README. Do not require a complex framework when a smaller executable
check is enough.
