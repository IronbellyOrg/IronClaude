### Variant A Advocate (opus:analyzer), Round 1

## Position summary
Variant A is the stronger card for correctness and coverage. It finds three blocking defects that B misses, each confirmed in the repo: the severity scan reads tracked files only, the routing-refresh test pins the command set, and Task 2's criteria depend on Task 3. Its classes for C-001 and C-002 follow the taxonomy better than B's "regression". A misses the heartbeat condition (B-F3), A-F10 is wrong, and A-F1's first remedy conflicts with a repo rule.

## Steelman of Variant B
B is the more precise card: all four findings were confirmed (R2-F3 partly), none refuted, and it is the only card that shows its coverage work (`lexical_misses_confirmed_covered`, ~36 rows; all 37 in-scope unmapped rows checked). B-F3 is real: source.md:144 requires spawn AND keeping the 5-minute heartbeat; plan :125 and :172 condition on spawning only. B-F2 finds a cross-task inconsistency A missed: plan :125 runs the sweep after any terminal `close` while plan :44 says a review-1 PASS needs no sweep. B's C-001 fix keeps the no-source-path check and pins a narrow exception, matching the repo CLAUDE.md rule and plan Constraints :25.

## Strengths claimed
1. A-F2 (C-004) confirmed: `_tracked_text()` runs `git ls-files -z -- src plugins ...` (test_review_severity_rule.py:36-44); both scans go through `_files_under` (:174, :323). The plan never commits (Constraints :28), so new files stay unscanned; source.md:124 requires the command test itself to assert both rules; Task 7 (:140-145) has neither.
2. A-F3 (C-005) confirmed: test_routing_refresh.py:647 globs the filesystem; :648 asserts `shipped - _POST_REFRESH_ADDITIONS == active` with :33 = {graph, impact, issue}; adding spec-panel-ledger.md breaks it; Task 8 (:155, :159) omits it; fixing it needs an owner-approved edit of an existing test (Constraints :19, source.md:79), so `necessary` is right.
3. A-F4 (C-006): Task 2 AC (:68) need round-3 `begin` and `E-CAP`; reaching round 3 needs a committed review-2 close; without `verify` (Task 3) `I` fails, the loop ESCALATEs (source.md:51-52) and the next `begin` gets `E-TERMINAL`. Inference: after review 3 (always terminal, :79) a fourth `begin` likely meets `E-TERMINAL` before `E-CAP`; the plan does not order the two checks.
4. A-F5 (C-002) right class: plan :44 drops "with the document unchanged" (source.md:28): an omission, so drift; the hash-tied skip with exit 12 fits the exit codes (:45).
5. A-F1 (C-001) right class: spec-panel.md:220 names `src/superclaude/examples/release-spec-template.md`; the conflict comes from the spec (source.md:83 vs :124); `necessary` fits; precedent for section-scoped pins at test_spec_panel_review_loop.py:157-159.
6. A-F7 (C-003/X-001): absence rules at source.md:17, :60, :120 have no AC; the import check (:53) accepts `subprocess`; Constraints :27 widens the module list without saying so.
7. A-F9 (C-011) confirmed: `.dev/brainstorms/346-ledger/` is already untracked and :207 builds from `git status --porcelain --untracked-files=all`.
8. Calibration: A 0.80 self vs 0.78 calibrated; B 0.92 vs 0.72.

## Weaknesses identified in Variant B
1. Wrong class on B-F1 and B-F2 (inherited conflict and omission are not regressions; B's own calibrator agrees; B classification score 0.55).
2. Misses three high-severity blockers (C-004, C-005, C-006); they are test-mechanics defects, not unmapped rows.
3. X-001 ruling too loose: pointing at a spec section verifies nothing; :53 would accept a `subprocess` git call (source.md:120).
4. B-F4 weak on scope: source.md:72/:227 are cause tables; the section 5 metrics list (:157) names only per-cycle bytes.

## Concessions
- A-F10 is wrong (source.md:163 leaves duplicates to an analyst; plan :93 copies the spec's U3 wording; headline_raw is a union).
- A-F1's first remedy is unsafe (would let an installed primitive reference `src/superclaude/examples/`); only the second remedy, matching B's, is sound.
- A-F4 "cannot" is too strong (a test could rebuild state and recompute `body_sha256`); the defect is ordering.
- A-F5's second half is an edge case (k=1 ESCALATE needs `not I` or `X > 0` with no plan rows).
- A-F8 is low value and unverified (:177 already checks content).
- A-F2 nuance: `git ls-files` also lists staged files; the plan as written never stages src/.
- A missed B-F3 and the Task 6 sweep inconsistency.

## Per-point positions
| Point | Superior | One-line reason |
|---|---|---|
| S-001 | Equal | A's D1-D4 vs B's coverage map; both useful |
| S-002 | A | 11 findings incl. 3 high-severity blockers |
| S-003 | Equal | style only |
| C-001 | Split: A class, B remedy | `necessary`; B's keep-the-pin exception respects CLAUDE.md |
| C-002 | Split: A class, B content | drift; B catches the Task 6 conflict |
| C-003 | A | no AC; :53 allows subprocess |
| C-004 | A | test_review_severity_rule.py:36-44, :174, :323 |
| C-005 | A | test_routing_refresh.py:33, :647-648 |
| C-006 | A | Task 2 needs Task 3 |
| C-007 | B | source.md:144 spawn and heartbeat |
| C-008 | B | real, minor |
| C-009 | A | source.md:60; minor |
| C-010 | A (weak) | unverified |
| C-011 | A | pre-existing untracked files trip :207 |
| C-012 | B (by absence) | A-F10 refuted |
| C-013 | A | spec-literal, worth a note |
| C-014 | A | calibrated confidence |
| X-001 | A | no AC pins the absence rules |
| X-002 | A | `necessary` |
| X-003 | A | `drift` |

## Shared assumptions
- A-001: QUALIFY. Starts in the spec (source.md:83 vs :124) but resolving it is the plan's job (owner-decision Constraints :21-24); blocking is right because :132 and :144-145 cannot both pass; class `necessary` with an owner decision.
- A-002: QUALIFY. Static reading suffices for C-004/C-005 (deterministic paths at :38-39 and :647-648); running would settle them; staged files are also scanned.
- A-003: ACCEPT. The plan tells the executor to report, not fix (:155); an executor settling a contradiction alone would itself be drift.

Read both cards, diff analysis, plan and spec; checked spec-panel.md:220, test_review_severity_rule.py:36-56/:174/:323, test_routing_refresh.py:33/:647-648, test_spec_panel_review_loop.py:157-159. Did not open the S1 briefs or run tests.
