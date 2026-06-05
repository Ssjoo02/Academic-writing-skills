# RAG Domain Profile

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

## Policy Effects

- Separate retrieval evidence from generation evidence.
- Require citation-grounding checks for factual claims.
- Add faithfulness and corpus limitations to claim/evaluation risks or Open Decisions.
