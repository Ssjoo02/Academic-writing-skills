# EMNLP Venue Profile

## Source Status

- Official template/guideline source status: `official source found`; see `../../maintenance/source-provenance.md`.
- Profile guidance source status: `generic cross-venue guidance pending representative-paper analysis`.
- The guidance below is `starter guidance`, not advice extracted from EMNLP papers or reviews.

## Reviewer Expectations

- Emphasize empirical NLP contribution, task definition, and evaluation validity.
- Make dataset composition, preprocessing, annotation, and splits transparent.
- Show what model behavior changes, not only whether the headline score improves.
- Discuss reproducibility, limitations, and ethical/data concerns where relevant.

## Typical Story Rhythm

- Empirical NLP problem or capability gap.
- Why current datasets, methods, or evaluations are insufficient.
- Proposed method, resource, benchmark, or analysis.
- Experimental design and main results.
- Error analysis, robustness checks, domain/language breakdowns, or qualitative examples.
- Limitations and responsible-use boundaries.

## Evidence Pressure

- Main result should be supported by appropriate task metrics and statistical or robustness checks where useful.
- Error analysis should identify linguistic, domain, or data conditions behind failures.
- Dataset/resource papers need documentation of collection, filtering, annotation, and intended use.
- Reproducibility details should make training, prompting, evaluation, and data access clear.

## Claim Strength Preferences

- Use strong claims for empirically demonstrated task improvements in the tested settings.
- Use moderate claims when results depend on specific datasets, prompts, languages, or model families.
- Avoid claims about general language understanding without broad evidence.

## Common Reviewer Risks

- Evaluation metric does not reflect the NLP phenomenon or user-facing task.
- Data leakage, contamination, or split construction is not ruled out.
- Dataset or annotation details are insufficient.
- Error analysis is missing despite nuanced language behavior.
- Ethical, privacy, licensing, or social-impact concerns are under-discussed.

## Writing Policy Effects

- Fill `Venue constraints`.
- Adjust `Claim Strength Policy`.
- Adjust `Metric And Evidence Policy`.
- Add venue-specific risks to `Reviewer Risk Register`.
