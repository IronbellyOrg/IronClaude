# Merge Log

Base: Variant 3 (reviewer-3, refactorer). Merge date: 2026-11-13. Output: merged-output.md.

Finding ids in the merged output map to plan changes as follows: M1 = Change 1, M2 = Change 2 plus base F2, M3 = Change 9, M4 = base F4 + F5 (Variant 2 F4 not merged), M5 = Change 4, M6 = Change 3, M7 = Change 7, M8 = Change 6, M9 = Change 5, M10 = Change 8.

| Change | Status | Before (base) | After (merged) | Provenance tag | Validation |
|---|---|---|---|---|---|
| 1 | applied | V3 F1 MAJOR, category missing-requirement | M1 MAJOR, category unpassable-check, vacuous head check (`target_sha=read.head_sha`) added, spec amendment recommended | Base (original, modified) | Citations plan:70, plan:77, spec:107-109, spec:166 copied from the V3 and V1 cards; paths exist |
| 2 | applied | V3 F2 placement only (MINOR) | M2 MINOR contradiction: V1 F2 wording ambiguity (spec:241 vs plan:137/140, plan:138 narrower) plus placement after the head-binding bullet | Variant 1 F2 per Change #2, plus Base (modified) | Citations plan:137, plan:140, spec:241 copied from the cards |
| 3 | applied | not in base | M6 MAJOR missing-requirement (FR-16 retry has no bound or test body) | Variant 2 F2 per Change #3 | Citations copied from the V2 card |
| 4 | applied | not in base | M5 MINOR (not MAJOR) missing-requirement: cycle-id equality has no test | Variant 2 F1 per Change #4 | Citations copied from the V2 card; severity per the debate (C-007) |
| 5 | applied | not in base | M9 MINOR missing-requirement: crash boundaries narrower than spec section 7 | Variant 2 F3 per Change #5 | Citations copied from the V2 card |
| 6 | applied | not in base | M8 MINOR missing-requirement: `guard_status` has no halt reason | Variant 1 F3 per Change #6 | Citations copied from the V1 card |
| 7 | applied | V3 F3 protected two Wave 6 sentences | M7 MINOR other: every existing Wave bullet line (Wave 6 line and head-binding bullet) is a classification key | Base (original, modified) | Citations plan:150, plan:154, spec:255 copied from the V3 card; test_worker_contract.py:1166, :1186 taken from the debate transcript |
| 8 | applied | not in base | M10 MINOR missing-requirement: exit paths after engage need a held-report test | Invariant probe INV-012/INV-013 per Change #8 | Citations spec:69, spec:275, spec:313, plan:166, plan:169 verified by Read of the spec and plan; no base SKILL line number cited (probe names halts only) |
| 9 | applied | V3 F6 (git write verbs) and V2 F5 separate | M3 MINOR other: one finding, `WRITE_VERB_RE` wording | Base (modified) plus Variant 2 F5 per Change #9 | Citations plan:22, 108, 124, 182, spec:28, spec:255 copied from the cards |
| M10 note | applied | | see Change 8 | | |

Also applied: base F4 and F5 are folded into M4 as the plan's "Changes NOT Being Made" row C-004 requires (Variant 2 F4 not kept stand-alone). Not made: S-001 (layout), A-001/A-002 (all findings stay blocking:false), INV-001 and INV-009 (probe only).

Validation (post-merge):
- Heading hierarchy: H1 title, H2 Summary, Findings, Rows checked and found sound, Findings block; H3 M1 to M10 under Findings. No gaps.
- Every id M1 to M10 in the findings-v2 block appears in a prose heading.
- Cited paths: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` and `.../source.md` both exist (listed with ls). Both were read for the lines cited in M10.
- Not verified here: the base-commit line numbers inside prose (SKILL.md, test_worker_contract.py, `__init__.py` and similar) are copied from the cards as written; the base copy is not in this directory.
