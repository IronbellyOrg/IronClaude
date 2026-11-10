### Variant B Advocate (opus:qa), Round 1

## Position summary
Variant B wins on two narrower points. It is the only card that checks coverage line by line, and it finds the missing heartbeat condition (B-F3). Its fix for the copy/no-path conflict also respects the repo's no-`src/superclaude` rule better. Variant A is the stronger card overall: it finds three high-severity defects that B misses entirely (C-004, C-005, C-006), and its deviation classes and confidence are better calibrated. The merge should take A's findings and B's coverage map, heartbeat finding and C-001 fix.

## Steelman of Variant A
A's strongest case: it is the only card that checked the plan against the repo's existing test suite, not just against the spec, and those checks hold up.
- A-F2 holds. `tests/skills/test_review_severity_rule.py:36-56` builds its corpus from `git ls-files` only; the new untracked command, SKILL.md and script are never scanned, so source.md:124 is unenforced unless Task 7 adds its own assertion.
- A-F3 holds. `tests/recommend/test_routing_refresh.py:647-648` globs `src/superclaude/commands/*.md` and subtracts `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue"}` (`:33`); a new `spec-panel-ledger.md` breaks that equality, and Task 8's suite list (plan:155) omits this test.
- A-F4 is a real ordering defect: Task 2's AC (plan:68) need a round-3 `begin` and `E-CAP`, which need `verify` and `close` from Task 3.
- A classes deviations more accurately (necessary/drift rather than regression), and its self-confidence (0.80) is close to the calibrated C (0.78).

## Strengths claimed
1. Explicit coverage audit (S-001): B's `lexical_misses_confirmed_covered` maps 36 inferred rows to plan lines (variant-2:9-13); A has no positive coverage evidence.
2. The heartbeat gap is real and only B found it (C-007, B-F3): source.md:144 requires spawn AND keeping the 5-minute heartbeat; the plan conditions the route on spawning alone at plan:125, plan:172 and plan:200. Spawn-succeeds/heartbeat-dies picks the subagent route and the worker is killed mid-sweep; no AC covers it (INF-134).
3. B's fix for C-001 is safer (B-F1): spec-panel.md:220 contains `src/superclaude/examples/release-spec-template.md`; A's first option (scope the pin to the loop section) would let an installed primitive ship a `src/superclaude` path, which the repo CLAUDE.md rule and Constraints (plan:25) forbid. B keeps the whole-file check and pins a narrow, authorized replacement of that one clause.
4. B-F2 finds an inconsistency inside the plan: Task 1 skips the sweep after a review-1 PASS (plan:44) while Task 6 runs the sweep "after a terminal `close`" (plan:125); an executor cannot satisfy both.
5. B's single skip predicate (review 1, loop PASS, live-document hash equals the reviewed snapshot, in Tasks 1, 4, 6, with two tests) is directly checkable.

## Weaknesses identified in Variant A
1. A-F10 is wrong: source.md:159-163 leave duplicates between U3, W, O to a blinded analyst; disjointness is not required; calibrator marked it refuted.
2. A's C-001 option 1 introduces a rule violation (see Strength 3), and A recommends dropping the whole-file greps.
3. A-F8 is unverified and partly overstated: plan:177 already requires "the only difference is the inserted … text".
4. A-F4 overstates "cannot": a test could rebuild state and recompute `body_sha256`; the ordering problem is still real.
5. A misses the heartbeat half of source.md:144 (C-007).

## Concessions
- "regression" is not defensible for B-F1 or B-F2: B-F1 is inherited from a spec-internal contradiction (source.md:83/124 vs :125); B-F2 is a dropped condition, i.e. drift.
- B is overconfident (0.92 vs calibrated 0.72).
- B missed three high-severity defects (C-004, C-005, C-006); C-004 and C-005 are certain from reading deterministic code.
- B's X-001 position is weaker: no AC would catch a `--role` flag or a `subprocess` git call; "covered by reference" is not "covered by a check".
- B-F4 is thin: residual risk at source.md:72/:227, not in the section 5 metrics list (:157).

## Per-point positions
| point | superior | one-line reason |
|---|---|---|
| S-001 | B | line-mapped coverage list makes coverage auditable |
| S-002 | A | 11 findings with 3 unique high-severity ones beat 4 |
| S-003 | equal | same short references in the card copies |
| C-001 | B (fix), A (class) | B keeps the whole-file pin; A's "necessary" class is closer |
| C-002 | equal | B finds Task 1 vs Task 6; A finds the undefined k=1 ESCALATE tail |
| C-003 | A | no AC enforces the absence rules; plan:53 lets subprocess through |
| C-004 | A | `git ls-files` scope (test_review_severity_rule.py:36-56) |
| C-005 | A | test_routing_refresh.py:647-648 with :33 breaks on a new command |
| C-006 | A | Task 2 AC depend on Task 3 |
| C-007 | B | source.md:144 requires spawn and heartbeat |
| C-008 | B (weak) | valid but minor |
| C-009 | A | source.md:60 names the third-fix-cycle refusal |
| C-010 | A (weak) | plausible but unverified |
| C-011 | A | `.dev/brainstorms/346-ledger/` already untracked |
| C-012 | B | A-F10 refuted by source.md:163 |
| C-013 | A | minor but accurate (spec-panel.md:23) |
| C-014 | A | same FAIL; A's confidence is calibrated |
| X-001 | A | covered only if a check would fail on violation |
| X-002 | A | inherited from the spec, not a regression |
| X-003 | A | dropped condition is drift |

## Shared assumptions
- A-001: QUALIFY. The contradiction starts in the spec (source.md:83, :124 vs :125) but still blocks the plan because both AC cannot pass (plan:132 vs :145); the fix needs a recorded owner decision in Constraints, pointing at rewriting line 220 in the variant rather than relaxing the pin.
- A-002: QUALIFY. Static reading suffices for the two deterministic cases (test_review_severity_rule.py:36-56; test_routing_refresh.py:26/33/647-648), not for A-F8 or runtime heartbeat behaviour.
- A-003: ACCEPT. Two AC that cannot both pass fail mechanically under per-task QA; an executor resolving "skip" vs "sweep after every terminal close" alone produces unapproved behaviour.

Verified spec-panel.md:220, test_review_severity_rule.py:36-56, test_routing_refresh.py:26/33/646-648; did not read the S1 briefs; ran no tests.
