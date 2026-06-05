# ICLR Venue Profile

## Source Status

- Official template/guideline source status: `official source found`; see `../../maintenance/source-provenance.md`.
- Profile guidance source status: `generic cross-venue guidance pending representative-paper analysis`.
- The guidance below is `starter guidance`, not advice extracted from ICLR papers or reviews.

## Reviewer Expectations

- Frame the learning problem, representation question, or capability gap early.
- Explain the core modeling or optimization insight, not only the implementation.
- Tie empirical claims to controlled comparisons, ablations, and analysis.
- Clarify when a contribution is methodological, empirical, theoretical, or a combination.

## Typical Story Rhythm

- Learning gap or limitation in current approaches.
- Core insight about model behavior, objective design, data, or training.
- Method or framework.
- Experimental setup and primary result.
- Ablations, sensitivity analysis, or representation/behavior analysis.
- Limitations, failure modes, and scope.

## Evidence Pressure

- Main result should support the headline learning or representation claim.
- Ablations should isolate the proposed mechanism or design choice.
- Analysis should explain when and why the method works.
- Baselines should be recent, relevant, and tuned fairly.

## Claim Strength Preferences

- Use strong claims only when direct multi-setting evidence exists.
- Use moderate claims for improvements shown on limited tasks or model scales.
- Avoid broad generalization claims without evidence across datasets, models, or regimes.

## Common Reviewer Risks

- Novelty is only an engineering combination.
- Ablations do not isolate the proposed insight.
- Baselines are weak, outdated, or undertuned.
- Results are sensitive to one dataset, seed, model size, or implementation detail.
- The method's limitations are hidden in appendices or not discussed.

## Writing Policy Effects

- Fill `Venue constraints`.
- Adjust `Claim Strength Policy`.
- Adjust `Metric And Evidence Policy`.
- Add venue-specific risks to `Reviewer Risk Register`.
