# RAG Domain Evidence Adapter

## Use Only As Optional Evidence Adapter

Do not use this file to decide paper type, venue, or section order. Use it only to adjust evidence
expectations, metrics, baselines, figures, and reviewer-risk notes.

Load this adapter only when the paper clearly studies retrieval-augmented generation, retrieval
quality, citation-grounded generation, or corpus-grounded answering. If the match is weak, skip it
rather than forcing an adapter label.

## Typical Problem Settings

- Retrieval-augmented question answering.
- Knowledge-intensive generation.
- Citation-grounded answers.
- Long-context or hybrid retrieval comparisons.

## Common Baselines

- No-retrieval generation.
- BM25 or sparse retrieval.
- Dense retrieval.
- Reranking or hybrid retrieval.
- Long-context model baseline when relevant.

## Common Metrics

- Retrieval recall or nDCG.
- Answer exact match, F1, or task-specific quality.
- Faithfulness and citation support.
- Hallucination rate.
- Latency and retrieval cost.

## Reviewer Attacks

- Retrieval metric improves but answer quality does not.
- Answer quality improves but grounding is not verified.
- Corpus freshness or leakage is unclear.
- Long-context baselines are missing.

## Framework Effects

- Separate retrieval evidence from generation evidence.
- Require citation-grounding checks for factual claims.
- Add faithfulness and corpus limitations to claim/evaluation risks or Open Decisions.
