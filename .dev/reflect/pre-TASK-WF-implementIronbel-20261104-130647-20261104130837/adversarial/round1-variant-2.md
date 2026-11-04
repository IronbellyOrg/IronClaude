# Round 1 — Variant 2 advocate (qa, haiku alias glm-5.3)

## Position summary
V2 is the smallest card but dense in verified, decision-changing findings; both blockers confirmed by all three variants; its C-001 fix is the only one preserving a positive going-forward invariant. Weakness: coverage breadth (0.60); tokenizer surface belongs to V3, plan-integrity points to V1.

## Steelman
- V1: best-balanced (11 findings, 10 verified), both blockers, three tokenizer gaps, plan-integrity set, Goal-wording catch with template 02 line 965 evidence (re-verified: tells agents to run `python -m` via Bash); minor grades for fail-closed over-blocks defensible; highest C 0.75.
- V3: owns the tokenizer surface (U-001, C-003, C-005, C-006, C-016), the only operational-safety finding (C-011) and the plan-internal contradiction (C-015, L20 vs L120-134); risk-surface 0.90 earned; right against V1 on C-006.

## Strengths claimed
1. R2-F1: test lines 102-105 re-read; plan L73 adds `matcher: "Bash"`; L95 runs tests/cli only. Fix keeps a positive invariant ("the only Bash-matcher registration is block-bare-python.sh") rather than deleting the pin.
2. R2-F2: L64 vs L56/L58; plan fails its own criterion.
3. R2-F3 (unique): L21 mandates fail-open when jq missing; L60 fail-open table has no such case.
4. R2-F4: 39 python3 occurrences across 11 files under src/superclaude/skills; Goal false as wording, right as scope.
5. 5 of 6 findings calibrator-verified.

## Weaknesses identified in others
1. V3 grades documented ceilings blocking (R3-F2 vs L40); inconsistent F3/F10 grading; the apostrophe half is the genuine defect.
2. V1 R1-F5 conflates mention with execution; L56 blocks the unquoted spelling with identical semantics.
3. V1 and V3 C-001 fixes leave no Bash-matcher guard at all.
4. V3 missed C-002 and the jq-missing gap.

## Concessions
1. Coverage breadth weakest; missed C-004, C-005, C-006, C-011, C-015, C-016, C-012/13/14/18.
2. R2-F5 unverifiable; drop or re-evidence.
3. R2-F6 generic; R1-F4 names the concrete mechanism (`sudo -u bob python3` makes `-u` the command word).
4. R2-F2's one case is thinner than R1-F2's three.

## Per-point positions
| Point | Superior | Reason |
|---|---|---|
| C-001 | V2 (assertion) + V3 (run scope) | positive invariant + broad run |
| C-002 | V1 | three cases |
| C-003 | V3 defect / V1 severity | apostrophe FN real; text FP documented at L40 |
| C-004 | V3 | unique, untested |
| C-005 | V1 severity | fail-closed, workaround |
| C-006 | V3 | execution not mention |
| C-007 | V1 | names concrete FN mechanism |
| C-008 | Equivalent | complementary; V3 fix subsumes most |
| C-009 | V1 | extra evidence |
| C-010 | V3 | superset |
| C-011 | V3 | unique, real |
| C-012 | V1 | unique |
| C-013 | V1 | unique |
| C-014 | V1 | unique |
| C-015 | V3 | verified |
| C-016 | V3 | unique, minor |
| C-017 | V2 (low value) | unverifiable |
| C-018 | V1 | refinement classification |
| X-001 | V1 | minor right |
| X-002 | V3 | Done-when violated |
| X-003 | V1 severity / V3 substance | documented ceiling vs quote corruption |

## Shared assumptions
- A-001: QUALIFY — in scope (issue supersedes the old invariant); edit must replace the invariant, not delete it; name the supersession in the PR body.
- A-002: QUALIFY — fixes land at implement time as recorded deviations in progress.md, not silent plan edits.
- A-003: QUALIFY — comment strip and continuation join are cheap pre-passes; full heredoc-aware tokenizing in jq is costlier and untimed; do not silently upgrade C-003/C-006 to full shell parsing without a timing proof.
