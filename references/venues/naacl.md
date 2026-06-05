# NAACL Venue Profile

## Source Status

- Official template/guideline source status: `needs source verification`; shared *ACL formatting source is recorded in `../../maintenance/source-provenance.md`.
- Profile guidance source status: `generic cross-venue guidance pending representative-paper analysis`.
- The guidance below is `starter guidance`, not advice extracted from NAACL papers or reviews.

## Reviewer Expectations

- Frame the contribution for NLP and computational linguistics readers.
- Make task, dataset, language, domain, and annotation assumptions explicit.
- Connect method or resource claims to measurable language/task behavior.
- Address reproducibility, data governance, and ethical concerns where relevant.

## Typical Story Rhythm

- NLP problem, linguistic phenomenon, or application gap.
- Gap in existing resources, methods, or evaluation.
- Core contribution: model, dataset, analysis, benchmark, or system.
- Experimental or analytical evidence.
- Error analysis, qualitative examples, and language/domain breakdowns.
- Limitations and applicability boundaries.

## Evidence Pressure

- Metrics should match the task and be interpreted with language-specific context.
- Dataset claims need provenance, annotation quality, and licensing/access clarity.
- Error analysis should expose linguistic or domain-specific failure modes.
- Reproducibility details should cover preprocessing, splits, prompts/settings, and evaluation tooling.

## Claim Strength Preferences

- Use strong claims only for directly tested languages, domains, and tasks.
- Use moderate claims when evidence is constrained to a specific benchmark or resource.
- Avoid broad NLP-general claims from narrow dataset coverage.

## Common Reviewer Risks

- Linguistic or task motivation is underspecified.
- Dataset construction, annotation, or evaluation protocol is unclear.
- Results lack error analysis or robustness checks.
- Claims exceed language/domain coverage.
- Ethical, privacy, data licensing, or bias concerns are missing.

## Writing Policy Effects

- Fill `Venue constraints`.
- Adjust `Claim Strength Policy`.
- Adjust `Metric And Evidence Policy`.
- Add venue-specific risks to `Reviewer Risk Register`.
