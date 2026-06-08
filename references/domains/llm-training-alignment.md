# LLM Training/Alignment Domain Evidence Adapter

## Use Only As Optional Evidence Adapter

Do not use this file to decide paper type, venue, or section order. Use it only to adjust evidence
expectations, metrics, baselines, figures, and reviewer-risk notes.

Load this adapter only when the paper clearly studies LLM training, preference optimization, reward
modeling, safety alignment, data filtering, or alignment-oriented evaluation. If the match is weak,
skip it rather than forcing an adapter label.

## Typical Problem Settings

- Supervised fine-tuning.
- Preference optimization.
- Reward modeling.
- Safety behavior shaping.
- Data filtering or curriculum design.

## Common Evidence

- Task performance across benchmarks.
- Preference or win-rate evaluation.
- Safety and refusal behavior evaluation.
- Data quality analysis.
- Compute and scaling discussion.

## Reviewer Attacks

- Data contamination or leakage.
- Evaluation set too narrow.
- Reward model or preference data bias.
- Safety claims exceed evidence.
- Compute cost makes method impractical.

## Framework Effects

- Require explicit data and evaluation scope.
- Treat safety and alignment claims as high-risk.
- Add compute and data provenance risks to claim/evaluation risks or Open Decisions.
