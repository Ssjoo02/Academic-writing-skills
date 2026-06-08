# Venue Profiles Index

Use venue profiles only after the Writing Policy has been confirmed and the workflow is building a
Paper Framework, drafting under a confirmed venue, or running a final submission-readiness check.
Do not load these files during Workspace Discovery or Writing Policy generation.

Venue profiles are dated constraint cards, not paper-story sources and not substitutes for the
current official call for papers. They may influence template choice, page-budget arithmetic,
anonymity, citation command style, required statements, figure/table planning, claim-strength
calibration, and final checklist risks. They must not invent claims, results, citations, or paper
identity.

The schema is strict; the facts are allowed to be incomplete. Prefer `not verified` or `verify
current official page` over filling a field from memory, old calls, search snippets, or another
venue's pattern. If a target venue is unavailable, choose the closest profile only for approximate
planning and mark the fit as approximate in the Paper Framework. If a venue fact affects compilation,
page counting, post-main section order, anonymity, or submission readiness and the profile does not
record a current verified value, record it as an Open Decision and verify against the official venue
page or a user-provided guideline before calling the draft submission-ready.

## Required Profile Schema

Every venue profile should use these sections. If a value is unknown, keep the field and write
`not verified`.

```text
## Source Status
- Official sources:
- Access date:
- Verified for:
- Drift risk:

## Scope
- Applies to:
- Submission version:

## Length And Counting
- Main text limit:
- References count:
- Appendix count:
- Checklist count:
- Ethics/limitations count:
- Supplementary material count:

## Post-Main Order
- Required order:
- Optional sections:
- Not verified:

## Drafting Implications
- Main paper self-contained:
- Appendix/supplement use:
- Anonymity checks:

## Final Gate
- Before submission-ready:

## Do Not Infer
- 
```

## Supported Venue Fact Cards

| Venue family | Profile file | Use for |
|---|---|---|
| ICLR | `iclr.md` | ML representation learning, deep learning, general ML method papers |
| NeurIPS | `neurips.md` | broad ML, theory-to-systems ML, empirical ML |
| ICML | `icml.md` | ML methods, theory, empirical learning systems |
| ACL | `acl.md` | NLP and computational linguistics |
| EMNLP | `emnlp.md` | empirical NLP |
| NAACL | `naacl.md` | NLP and computational linguistics |
| CVPR | `cvpr.md` | computer vision and vision-language |
| ICCV/ECCV | `iccv-eccv.md` | computer vision and vision-language |
| AAAI/IJCAI | `aaai-ijcai.md` | broad AI |
| KDD/WWW/SIGIR | `kdd-www-sigir.md` | data mining, web, search, recommender, IR |
| CHI/UIST | `chi-uist.md` | HCI, interaction, user studies, systems for people |
