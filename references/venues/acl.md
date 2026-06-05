# ACL Venue Profile

## Source Status

- Official template/guideline source status: `official source found`; see `../../maintenance/source-provenance.md`.
- Profile guidance source status: `generic cross-venue guidance pending representative-paper analysis`.
- The guidance below is `starter guidance`, not advice extracted from ACL papers or reviews.

## Reviewer Expectations

- Frame the contribution in terms of language, tasks, data, evaluation, or linguistic insight.
- Define datasets, annotation choices, languages, domains, and task assumptions clearly.
- Connect model or system claims to linguistic/task behavior, not only aggregate scores.
- Address reproducibility, data rights, bias, and ethical concerns where relevant.

## Typical Story Rhythm

- NLP or computational linguistics problem.
- Dataset, task, or modeling gap.
- Core method, resource, analysis, or linguistic hypothesis.
- Evaluation setup and primary findings.
- Error analysis, qualitative examples, or linguistic/task breakdowns.
- Limitations across languages, domains, data sources, and use cases.

## Evidence Pressure

- Metrics should match the task and be supplemented with analysis when aggregate scores hide behavior.
- Dataset claims need clear provenance, annotation protocol, and quality checks.
- Error analysis should explain what the system fails to capture.
- Reproducibility details should cover data splits, prompts/settings, preprocessing, and evaluation scripts where applicable.

## Claim Strength Preferences

- Use strong claims only for task, language, and domain scopes directly tested.
- Use moderate claims when evidence is limited to selected datasets or languages.
- Avoid language-general or human-language claims from English-only or narrow-domain evidence.

## Common Reviewer Risks

- Task framing is unclear or mismatched to the evaluation.
- Dataset construction or annotation quality is under-specified.
- Results rely on weak baselines or opaque prompting/evaluation details.
- Error analysis is missing or too shallow.
- Ethical, privacy, licensing, or bias concerns are ignored.

## Writing Policy Effects

- Fill `Venue constraints`.
- Adjust `Claim Strength Policy`.
- Adjust `Metric And Evidence Policy`.
- Add venue-specific risks to `Reviewer Risk Register`.
