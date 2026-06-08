# Domain Evidence Adapter Index

These files are optional evidence adapters. They help the agent adjust metrics, baselines, figures,
evidence expectations, and reviewer-risk notes for a few common AI/LLM domains.

Do not use this index as a complete research-domain taxonomy. Do not use it to decide paper type,
venue, or section order. Do not force a match. If there is no clear match, use
`none / no matching profile` and continue with the Writing Policy plus the paper type profile.

| Domain evidence adapter | Profile | Typical evidence pressure |
|---|---|---|
| LLM agent | `llm-agent.md` | task success, tool-use robustness, cost, trajectory analysis, failure modes |
| RAG | `rag.md` | retrieval quality, faithfulness, citation grounding, answer quality, corpus freshness |
| LLM training/alignment | `llm-training-alignment.md` | objective design, data quality, preference/safety evaluation, scaling and compute |
