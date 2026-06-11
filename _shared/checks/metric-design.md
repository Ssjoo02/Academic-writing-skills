# Metric Design Check

Metrics must validate research questions. A paper with many metrics can still fail if the
metrics do not support the core claim.

## Mapping Rule

For each research question, create:

| Research question | Metric / experiment | Required evidence | Why this metric matters | Failure if missing |
|---|---|---|---|---|

## Checks

- Does the metric directly measure the claimed capability?
- Is it only a proxy metric?
- Are strong and fair baselines included?
- Are cost, latency, or compute needed?
- Is robustness or generalization needed?
- Is human evaluation needed?
- Is failure analysis needed?
- Are only favorable results shown?

## Common Metric Risks

- Proxy metric improves but task outcome does not.
- Average score hides severe failure modes.
- Main metric ignores cost.
- Benchmark is too easy or saturated.
- Ablation does not isolate the claimed mechanism.
