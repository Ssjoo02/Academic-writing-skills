# Systems / Implementation Engineering Paper Type

Use this profile for papers whose main contribution is a working system, software/hardware module,
platform, runtime, deployment pipeline, engineering framework, or implementation strategy.

## Use Only As Section Planning Reference

This file is only a section and page-budget reference for building a Paper Framework. It is not a
fixed paper template and does not prescribe writing style, reviewer strategy, claims, experiments,
or citations.

Adapt sections and page budgets to the actual paper, venue, evidence, and user request. Do not copy
this structure mechanically. Merge, rename, split, shrink, or remove sections when the confirmed
venue, contribution, evidence package, or page budget requires it.

## Section And Page-Budget Reference

When no venue-specific budget is known, use the workflow's soft 6-8 main-text-page drafting budget
and treat 8 pages as an upper bound, not a venue limit.

| Order | Candidate section | Typical budget | Section role |
|---|---:|---:|---|
| Front | Abstract | 0.15-0.25 page | Summarize the engineering problem, system approach, achieved capability, and practical value. |
| 1 | Introduction | 1.0-1.5 pages | Motivate the real-world problem, requirements, gap in existing systems, target users, and contributions. |
| 2 | Related Work | 0.75-1.25 pages | Compare relevant systems, architectures, tools, or implementation strategies by capability and limitation. |
| 3 | System Design and Implementation | 2.0-3.0 pages | Describe architecture, module boundaries, interfaces, data/control flow, technical choices, and key implementation details. |
| 4 | Experimental Setup | 0.5-0.75 page | Define evaluation goals, environment, workloads, test cases, baselines, metrics, and configuration. |
| 5 | Results and Analysis | 1.5-2.25 pages | Evaluate functionality, reliability, efficiency, scalability, stability, resource use, and goal satisfaction. |
| 6 | Conclusion | 0.25-0.5 page | Summarize the system contribution and practical implications. |
| End | Limitations | venue-dependent | State deployment boundaries, assumptions, engineering tradeoffs, evaluation scope, and unsupported settings. |
| Back | Appendix | outside main budget when allowed | Put extended configuration, API details, extra experiments, logs, screenshots, and implementation notes here. |

## Flexible Adjustment Notes

- If the system design is the core contribution, protect architecture diagrams and implementation space.
- If deployment evidence is central, reserve more space for workload design, operational constraints, and case studies.
- If the venue is short, combine Experimental Setup with Results and keep only the essential system internals in the main text.
