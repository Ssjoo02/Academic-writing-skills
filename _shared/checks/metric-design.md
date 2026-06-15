# Metric Design Check

Metrics must validate research questions. A paper with many metrics can still fail if the
metrics do not support the core claim.

## Mapping Rule

For each research question, create:

| Research question | Metric / experiment | Required evidence | Why this metric matters | Failure if missing |
|---|---|---|---|---|

## Outcome Semantics Rule

Define outcome labels before naming metrics. A metric may not split or group labels in a way that
hides the paper's actual success/failure semantics.

- **Outcome semantics first**: list each label (`defended`, `executed`, `partial`, `stalled`,
  `run_failed`, etc.), whether it counts as success, compromise, unresolved, or infrastructure
  failure, and why.
- If `partial` means the injected instruction was partly followed, it belongs in the safety
  failure bucket. Report a **compromise rate** such as `(executed + partial) / denominator`, not only
  execution rate.
- State every **denominator**: all assigned tasks, scorable tasks, completed tasks, or another
  declared base. Do not compare metrics with different denominators without saying so.
- Keep residual buckets honest. `Other` may group stalled or infrastructure-failed runs, but it must
  not hide compromised outcomes.

## Checks

- Does the metric directly measure the claimed capability?
- Is it only a proxy metric?
- Are outcome labels mapped to success, compromise, unresolved, and infrastructure failure before
  rates are named?
- Do any residual buckets hide partially compromised runs or other safety-relevant failures?
- Are denominators explicit and consistent across the table, figure, caption, and prose?
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
