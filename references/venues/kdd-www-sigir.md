# KDD/WWW/SIGIR Venue Profile

## Source Status

- Official template/guideline source status: `official source found`; see `../../maintenance/source-provenance.md`.
- Profile guidance source status: `generic cross-venue guidance pending representative-paper analysis`.
- The guidance below is `starter guidance`, not advice extracted from KDD/WWW/SIGIR papers or reviews.

## Reviewer Expectations

- Frame the contribution around data mining, web systems, search, recommendation, or information retrieval.
- Make dataset scale, sampling, logging, and temporal or user-interaction context clear.
- Align offline metrics, online metrics, and user/system impact claims.
- Address leakage, bias, feedback loops, privacy, and deployment constraints where relevant.

## Typical Story Rhythm

- Data/web/search/recommender/IR problem and stakeholder impact.
- Gap in current modeling, ranking, retrieval, mining, or web-scale practice.
- Core method, dataset, system, or analysis.
- Experimental setup with datasets, splits, metrics, and baselines.
- Validity analysis: leakage, bias, robustness, efficiency, or online/offline gap.
- Limitations and operational implications.

## Evidence Pressure

- Dataset scale and construction should support the claimed real-world relevance.
- Metrics should reflect the retrieval, ranking, recommendation, mining, or web objective.
- Offline gains need careful interpretation if user or system impact is claimed.
- Leakage checks, temporal splits, bias analysis, or counterfactual concerns may be needed.

## Claim Strength Preferences

- Use strong claims when results hold across datasets, time splits, or realistic traffic/user settings.
- Use moderate claims for offline improvements without online or user-facing validation.
- Avoid impact claims when only proxy metrics are measured.

## Common Reviewer Risks

- Dataset leakage, sampling bias, or temporal contamination is not addressed.
- Offline metrics are treated as direct user-impact evidence.
- Baselines are weak for the relevant IR/recommender/data-mining community.
- Scalability, latency, or systems constraints are ignored.
- Privacy, fairness, or feedback-loop risks are missing.

## Writing Policy Effects

- Fill `Venue constraints`.
- Adjust `Claim Strength Policy`.
- Adjust `Metric And Evidence Policy`.
- Add venue-specific risks to `Reviewer Risk Register`.
