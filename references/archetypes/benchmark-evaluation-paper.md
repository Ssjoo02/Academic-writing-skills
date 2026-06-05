# Benchmark/Evaluation Paper Archetype

## Story Logic

- Start from a measurement gap that affects research conclusions or deployment decisions.
- Explain why existing benchmarks, metrics, or protocols miss the target construct.
- Define the benchmark's intended use, excluded use, and validity argument.
- Show how tasks, data, metrics, and protocols expose meaningful differences between systems.
- Use findings to revise understanding, not just to rank models.

## Framework Effects

- Abstract: measurement problem, benchmark/protocol contribution, headline findings, scoped use.
- Introduction: motivate why current evaluation gives incomplete or misleading signals.
- Benchmark Design: define construct validity, data sources, task format, and annotation or scoring rules.
- Evaluation Protocol: specify baselines, prompts/training access, splits, leakage controls, and fairness constraints.
- Findings: report rankings only alongside diagnostic patterns, uncertainty, and failure modes.
- Related Work: compare against prior benchmarks by construct, coverage, and protocol assumptions.
- Conclusion: state what the benchmark can and cannot support.

## Reviewer Risks

- Benchmark does not validly measure the claimed capability.
- Data leakage or benchmark contamination undermines conclusions.
- Task is already saturated or too easy to reveal useful differences.
- Protocol gives unfair advantages to some systems or baselines.
- Metrics have weak construct validity or reward superficial behavior.
