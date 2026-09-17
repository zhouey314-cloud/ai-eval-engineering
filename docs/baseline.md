# Baseline

Run the smallest meaningful fixture slice before changing prompts, retrieval,
tools or workflow behavior. Record version, dataset, provider/config, outputs,
trace evidence, metrics and blocked dependencies. A fixture-schema pass is not
a model baseline; if no provider is configured, report model quality as
`BLOCKED`.
