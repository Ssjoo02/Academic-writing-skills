# LLM Agent Domain Profile

## Typical Problem Settings

- Multi-step task completion.
- Tool use and API interaction.
- Planning, memory, reflection, or coordination.
- Robustness under long-horizon or noisy environments.

## Common Baselines

- Strong prompted LLM baseline.
- ReAct-style agent baseline when relevant.
- Planner/executor or tool-use frameworks relevant to the task.
- Domain-specific prior systems.

## Common Metrics

- Task success rate.
- Step-level accuracy or trajectory quality.
- Cost and latency.
- Tool-call validity.
- Robustness under perturbation.
- Human preference or qualitative failure categories when appropriate.

## Common Figures And Tables

- System or agent loop diagram.
- Main result table by task/environment.
- Ablation table for planning, memory, tool use, or reflection modules.
- Failure taxonomy table.
- Cost/performance tradeoff figure.

## Reviewer Attacks

- Evaluation tasks are too simple or saturated.
- Baselines are weak prompting setups.
- Gains come from more tokens, tools, or compute rather than method insight.
- Success metric hides failure modes.
- Method is brittle across environments.

## Policy Effects

- Require metric/evidence mapping for success, robustness, and cost.
- Require clear distinction between method insight and prompt engineering.
- Add failure analysis needs to claim/evaluation risks or Open Decisions.
