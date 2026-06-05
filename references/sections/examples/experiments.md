# Experiments Examples Skeleton

## Example Slot: Main Comparison

- Source:
- Use when: direct baselines or adapted baselines are available.
- Structure to learn: setup -> fair comparison -> metric table -> main result -> caveat.
- Transferable move: state why the comparison is fair before interpreting numbers.
- Do not copy: metric interpretation, table layout, or baseline claims without verification.

## Example Slot: Ablation Package

- Source:
- Use when: the paper has multiple modules or design choices.
- Structure to learn: full model -> remove/replace variants -> delta -> claim status.
- Transferable move: tie each ablation row to one Method Tree node.
- Do not copy: row naming, highlight style, or unsupported causal language.

## Example Slot: Demo Or Stress Test

- Source:
- Use when: the paper claims practical value, robustness, or upper bound.
- Structure to learn: challenging setting -> qualitative/quantitative evidence -> limitation.
- Transferable move: use the demo to reveal capability or boundary, not replace main evidence.
- Do not copy: demo scenario or cherry-picked claim framing.
