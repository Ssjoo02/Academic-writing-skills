# ICCV/ECCV Venue Profile

## Source Status

- Official template/guideline source status: `official source found`; see `../../maintenance/source-provenance.md`.
- Profile guidance source status: `generic cross-venue guidance pending representative-paper analysis`.
- The guidance below is `starter guidance`, not advice extracted from ICCV/ECCV papers or reviews.

## Reviewer Expectations

- Frame the contribution around a clear computer vision or vision-language problem.
- Define datasets, visual domains, protocols, and evaluation settings precisely.
- Support the method story with both quantitative results and qualitative visual evidence.
- Explain architecture, supervision, data, or training choices through ablations where applicable.

## Typical Story Rhythm

- Vision problem, benchmark gap, or deployment limitation.
- Why existing visual methods are insufficient.
- Core insight and method.
- Evaluation protocol and main results.
- Qualitative examples, ablations, and failure analysis.
- Scope across categories, scenes, domains, and compute conditions.

## Evidence Pressure

- Quantitative comparisons should use accepted protocols or justify deviations.
- Visual examples should demonstrate strengths and limits of the method.
- Ablations should test the major architecture, training, and data decisions.
- Cross-dataset or cross-domain evidence is needed for broad generalization claims.

## Claim Strength Preferences

- Use strong claims only when multiple protocols or datasets support them.
- Use moderate claims for benchmark-specific improvements.
- Avoid claims about real-world robustness without stress tests or deployment-relevant evidence.

## Common Reviewer Risks

- Protocol details or data preprocessing are hard to audit.
- The method is an incremental architecture variant without analysis.
- Qualitative evidence is selective or disconnected from metrics.
- Comparisons miss recent vision baselines.
- Failure modes, bias, safety, or compute costs are ignored.

## Writing Policy Effects

- Fill `Venue constraints`.
- Adjust `Claim Strength Policy`.
- Adjust `Metric And Evidence Policy`.
- Add venue-specific risks to `Reviewer Risk Register`.
