# CVPR Venue Profile

## Source Status

- Official template/guideline source status: `official source found`; see `../../maintenance/source-provenance.md`.
- Profile guidance source status: `generic cross-venue guidance pending representative-paper analysis`.
- The guidance below is `starter guidance`, not advice extracted from CVPR papers or reviews.

## Reviewer Expectations

- State the visual recognition, generation, geometry, perception, or vision-language problem clearly.
- Make dataset, protocol, and evaluation setup unambiguous.
- Pair quantitative comparisons with visual evidence that reveals behavior.
- Use ablations or analysis to isolate architecture, data, training, or inference choices.

## Typical Story Rhythm

- Visual problem and why current methods fail.
- Key insight about representation, architecture, data, supervision, or inference.
- Method with enough detail for reproduction.
- Dataset/protocol setup and main quantitative results.
- Qualitative comparisons, failure cases, and ablations.
- Limitations across scenes, categories, domains, or deployment conditions.

## Evidence Pressure

- Main metrics should match the visual task and protocol.
- Qualitative examples should be representative, not cherry-picked.
- Ablations should isolate architecture/training/data choices behind the claimed gain.
- Dataset splits, preprocessing, and evaluation code/protocol should be clear enough to audit.

## Claim Strength Preferences

- Use strong claims for improvements shown across relevant datasets and protocols.
- Use moderate claims for gains on one benchmark or constrained visual domain.
- Avoid visual generalization claims without cross-dataset or out-of-domain evidence.

## Common Reviewer Risks

- Dataset or evaluation protocol is unclear or nonstandard without justification.
- Qualitative results do not support the quantitative story.
- Ablations are missing for key architecture or training choices.
- Comparisons omit recent vision or vision-language baselines.
- Failure cases, compute, or ethical concerns are under-discussed.

## Writing Policy Effects

- Fill `Venue constraints`.
- Adjust `Claim Strength Policy`.
- Adjust `Metric And Evidence Policy`.
- Add venue-specific risks to `Reviewer Risk Register`.
