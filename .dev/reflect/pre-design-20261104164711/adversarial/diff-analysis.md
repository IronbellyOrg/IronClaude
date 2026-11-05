# Diff Analysis: sc:reflect Tier-2 Reviewer Card Comparison

## Metadata
- Generated: 2026-11-04T17:51:51Z
- Mode: A (compare existing files); focus: correctness, coverage, deviation-classification
- Variants compared: 3
  - Variant A: `variant-1-original.md` (reviewer 1, analyzer, sonnet; findings A-1..A-11)
  - Variant B: `variant-2-original.md` (reviewer 2, qa, glm-5.3 via haiku alias; findings Q-1..Q-8)
  - Variant C: `variant-3-original.md` (reviewer 3, refactorer, opus; findings F-1..F-11)
- Side input: `../artifacts/calibration-t2.yaml` (blind calibrations)
- Reviewed plan and spec: `.dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md` (cited as P) and `source.md` (cited as S)
- Unit of comparison: each FINDING is a topic. Card IDs (A-n, Q-n, F-n) are the reviewers' own; diff IDs (S-, C-, X-, U-, A-NNN with three digits) are this analysis's. The two "A-" schemes are distinct: `A-5` is a reviewer-1 finding, `A-005` is a shared assumption.
- Total differences found: 41
- Categories: structural (6), content (13), contradictions (5), unique (14), shared assumptions (6 enumerated; 3 promoted)

## Finding equivalence map

Canonical findings (CF) after splitting bundled findings (A-6, A-8, A-10, Q-5, Q-6, F-1, F-5 each carry more than one defect).

| CF | Canonical finding | Variant A | Variant B | Variant C | Cards |
|---|---|---|---|---|---|
| CF-01 | Task 13 has no Depends-on although it appends to `test_conflict_scripts.py` created by Task 10 (A, C add: Tasks 11/12/13 append the same file as siblings) | A-1 (M, drift) | Q-2 (M, drift) | F-4 (M, drift) | 3 |
| CF-02 | Task 15 AC calls `parse_resolution_record` / `resolution_record_ok` (Task 4) but depends only on Task 12 | A-2 (M, drift) | Q-3 (M, drift) | F-5a (M, drift) | 3 |
| CF-03 | Task 16 documents `poll-ci-checks.sh --evidence-sha` (Task 13) but depends only on Task 2 | A-3 (L, drift) | Q-4 (M, drift) | F-3 (M, drift; adds Task 6) | 3 |
| CF-04 | Task 20 closure (via 18, 19) never reaches Task 6 or Task 9; spec step 14 depends on all | A-4 (L, drift) | Q-8 (L, drift) | F-5b (M, drift) | 3 |
| CF-05 | Task 4 builds resume-test `state` dicts by hand ahead of the run-log fold (Task 7); spec puts resume rows in step 7 | A-5 (L, drift) | - | F-1b (M, drift) | 2 |
| CF-06 | Task 4 is too large for one QA verdict | A-10a (L, drift) | - | F-1a (M, drift) | 2 |
| CF-07 | Tasks 8, 17, 18 are too large for one QA verdict | A-10b (L, drift) | - | - | 1 |
| CF-08 | Task 20 omits spec step 14's staging instruction | A-6b (M, drift) | Q-7 (L, drift) | - | 2 |
| CF-09 | Task 10 AC "`git ls-files -s` shows mode 100755" is unobservable for a new file no task stages | A-6a (M, drift) | - | - | 1 |
| CF-10 | Pinned-phrase / order-pin / prohibition ACs of Tasks 10, 11, 14, 15 have no failing command until Task 18 | A-7 (L, drift) | - | - | 1 |
| CF-11 | Task 19 lacks the real-git capability skip (S:1316) | A-8a (L, drift) | Q-5b (M, drift) | - | 2 |
| CF-12 | Constraint P:29 drops the fixed author and committer (S:1316); `git commit` fails under `GIT_CONFIG_GLOBAL=/dev/null` | A-8b (L, drift) | Q-5a (M, drift) | - | 2 |
| CF-13 | Task 2 drops the S 6.5 docstring clause | A-8c (L, drift) | Q-6a (L, drift) | - | 2 |
| CF-14 | Task 2 cites `loop-guard.md:86-99`; the list ends at `:103` | A-8d (L, drift) | Q-6b (L, drift) | - | 2 |
| CF-15 | `make test` drop is an authorized override (P:28) with a residual | A-9 (L, authorized) | Q-1 (M, authorized) | F-6 (M, authorized) | 3 |
| CF-16 | No invented functional requirement; additions are verification-only | A-11 (L, authorized) | - | F-11 (L, authorized) | 2 |
| CF-17 | Task 19 misses edges to Task 13 (and Task 6, Task 14); X1 replays ref steps 3-12 | - | - | F-2 (M, drift) | 1 |
| CF-18 | Tasks 11 and 12 do not run the force-push scan that spec step 9's done-when requires | - | - | F-7 (L, drift) | 1 |
| CF-19 | C4's exit 2 could pass for the wrong reason (`poll-ci-checks.sh:30` exits 2 without `--pr`) | - | - | F-8 (L, drift) | 1 |
| CF-20 | E5 / E12 split between Task 1 and Task 17 with no placement anchor in Task 17 | - | - | F-9 (L, necessary) | 1 |
| CF-21 | Some plan edges are stricter than spec section 13 | - | - | F-10 (L, necessary) | 1 |
| CF-22 | Task 11 (F10 `merge_parent_ok`, F12 `merge_preflight_ok`) and Task 18 (`test_push_parent_ok_still_rejects_a_valid_merge_commit`) use Task 4 functions without a path to Task 4 | - | - | - | 0 (calibrators only) |

Card-level attributes: verdict ready-with-fixes in all three (agreement); no regression claimed in all three (agreement); self-reported confidence 0.80 / 0.87 / 0.82 (see C-012).

Spot-check of CF-22 (the finding all three cards missed): P:196 Task 11 "Depends on: Task 10"; P:184 Task 10 "Depends on: Task 3"; P:86 Task 3 "Depends on: Task 2". S:1388 (F10) asserts `merge_parent_ok(...)`; S:1390 (F12) asserts `merge_preflight_ok` false; S:1345 defines the Task 18 test with `merge_parent_ok([SHA, OTHER_SHA], SHA, OTHER_SHA)`. Task 18's closure (17 -> 1, 14, 15, 16 -> 11, 12, 13 -> 10 -> 3 -> 2) has no Task 4. Confirmed.

## Structural Differences

| # | Area | Variant A | Variant B | Variant C | Severity |
|---|---|---|---|---|---|
| S-001 | Finding count and bundling granularity | 11 findings; bundles 4 defects in A-8, 2 in A-6, 2 in A-10 | 8 findings; bundles 2 in Q-5, 2 in Q-6 | 11 findings; bundles 2 in F-1, 2 in F-5 | Low |
| S-002 | Severity distribution (no card uses High) | 3 medium, 8 low | 5 medium, 3 low | 6 medium, 5 low | Medium |
| S-003 | Deviation-class vocabulary used | drift 9, authorized 2 | drift 7, authorized 1 | drift 7, authorized 2, necessary 2 (only card using `necessary`) | Low |
| S-004 | Finding order | dependency graph (A-1..A-5), then ACs, then authorized, then sizing | authorized override first (Q-1), then edges, then dropped text | Task 4 split first (F-1), then edges, then authorized, then smaller ACs | Low |
| S-005 | Evidence paths and recommendation shape | package-relative paths plus trailing path footnote; "Verify" clause only in A-1 | package-relative plus footnote; "verify" in Q-2, Q-4 | repo-relative full paths; explicit "Verify:" clause on every recommendation | Low |
| S-006 | Provenance header | recommendations "lightly condensed" | notes haiku alias resolves to glm-5.3; recommendations condensed | "verbatim content" | Low |

## Content Differences

Shared findings with identical presence, severity, class and fix (CF-02; verdict; no-regression claim) are agreements and are not listed; they feed the Shared Assumptions engine.

| # | Topic | Variant A Approach | Variant B Approach | Variant C Approach | Severity |
|---|---|---|---|---|---|
| C-001 | CF-01 Task 13 edge: scope and fix | A-1: also flags concurrent edits by 11/12/13; fix "Depends on: Task 10", optionally chain 11 -> 12 -> 13 | Q-2: Task 13 only; fix "Depends on: Task 10" | F-4: flags sibling appends as a conflict; fix chain 12 on 11, 13 on 12 (minimum Task 10) | Medium |
| C-002 | CF-03 Task 16 edge: severity and dependency set | A-3: low; add Task 13 | Q-4: medium; add Task 13 plus a grep that the fenced usage line matches the script header | F-3: medium; add Task 6 and Task 13 (ci-poll.md item 4 also documents `ci.expect_checks_after_push`, S:1070) | Medium |
| C-003 | CF-04 Task 20 closure: severity and fix | A-4: low; add Tasks 6, 9, 18, 19 | Q-8: low; add Tasks 6, 9, 18, 19 | F-5b: medium (bundled with CF-02); add Tasks 9, 18, 19 only, which suffices because Task 9 depends on Task 6 (P:171) | Low |
| C-004 | CF-05 resume tests ahead of the fold: severity and fix | A-5: low; move the resume cases to Task 8, or add Task 7 to Task 4's deps and build state from `RunLog.rebuild_state()` | not raised | F-1b: medium; split Task 4 and place 4b (resume planners + tests, deps 4a and Task 7) between Task 7 and Task 8 | Medium |
| C-005 | CF-06 Task 4 size: where to split | A-10a: low; split router vs gates/records/messages (resume handled per A-5) | not raised | F-1a: medium; split non-resume functions (4a) vs resume planners (4b) | Medium |
| C-006 | CF-08 staging omission: severity and fix | A-6b: medium; add `git add -- src tests CHANGELOG.md` and `git add .dev/tasks` to Task 20 with an AC on `git diff --cached --name-only` | Q-7: low; stage src/, tests/, CHANGELOG.md, .dev/tasks/ only; notes the `.claude/` check is vacuous | not raised | Medium |
| C-007 | CF-11 + CF-12 capability skip and fixed identity: severity | A-8a/b: low, bundled with two cosmetic defects | Q-5: medium; names concrete breakage of F9, F10, X1, X3 (S:1316 confirms both requirements) | not raised | Medium |
| C-008 | CF-13 + CF-14 docstring clause and line range | A-8c/d: low; same fix as B | Q-6: low; quote the clause, use `:86-103` | not raised (coverage gap only) | Low |
| C-009 | CF-15 `make test` override residual: severity and fix | A-9: low; reword P:19 "source wins, except the make test override", record "VG-2 not run" in Task 20 log | Q-1: medium; add `tests/cli/reflect/test_contract_status_cli.py` to Task 20 plus the Task 9 import smoke | F-6: medium (calibrator: overstated); add the same reflect test to Task 9 and Task 20 | Medium |
| C-010 | CF-16 authorized verification additions | A-11: no change | not raised | F-11: no change; optionally tighten Task 17 to "net +15" (S:1426) | Low |
| C-011 | Citation grounding (calibrated) | 0.92; no citation defect flagged | 0.85; Q-1 cites S:1392 for the make-test step, actual S:1408 | 0.90; no citation defect flagged | Low |
| C-012 | Confidence: self-reported vs calibrated | 0.80 vs 0.82 | 0.87 vs 0.78 (overconfident by 0.09) | 0.82 vs 0.82 | Low |
| C-013 | Summary framing and coverage caveats | "coverage faithful", no invented requirement | 21 unmapped-union INF rows could not be resolved to spec sections | "order matches spec section 13" | Low |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Variant C Position | Impact |
|---|---|---|---|---|---|
| X-001 | Deviation class of moving resume tests into Task 4 (CF-05) | A-5: "drift" | silent | F-1: "drift" | Medium |
|  | Evidence: P:93 states the move ("resume tests build `state` dicts directly; the run-log integration is Task 8"); calibration-t2 rules A-5 "plan states the deviation; Refinement not Drift". P:19 says the source wins on disagreement, so a stated deviation is still a deviation. Debate must settle drift vs documented refinement. | | | | |
| X-002 | Size of the `make test` residual risk (CF-15) | A-9: "the tests/cli/reflect blast radius is smaller than claimed because every tests/pr_submit test already imports the package" | Q-1: the reflect test is "the only test outside tests/pr_submit that exercises superclaude.pr_submit", left outside every run | F-6: the reduced set leaves out `commands.py:99`, which runs the `__init__` Task 9 rewrites | Medium |
|  | Spot-check: `tests/cli/reflect/test_contract_status_cli.py:33` imports `superclaude.cli.reflect.commands`; its docstring (:47) says `contract-status` imports only from `superclaude.pr_submit.contract_setup`. Any `__init__` import failure also breaks every `tests/pr_submit` test, so A is right on import breakage; B and C are right that the CLI behaviour itself is unexercised. | | | | |
| X-003 | Deviation class of the E5 / E12 split (CF-20) | silent | silent | F-9: "necessary" | Low |
|  | calibration-t2: "drift, not necessary". Spot-check: the spec itself splits E5 (step 1 "rebase sentence only, not the operation check yet", S:1416; step 11 "E5 operation check", S:1426) and E12 (first two rows / last three rows). The split is spec-conformant; the real defect is the missing placement anchor in Task 17. Neither label fits cleanly. | | | | |
| X-004 | F-10 claim that Task 5 on Task 4 and Task 8 on Task 4 are "stricter than spec section 13" | silent | silent | F-10: stricter edges, "necessary" | Low |
|  | Spot-check: spec step 3 is all of `conflicts.py` (S:1418), implemented by plan Tasks 3 + 4; spec steps 4 and 7 depend on 3 (S:1419, S:1422). Those two edges are spec-required, not stricter. Only Task 9 on Task 6 is stricter (spec step 8 depends on 3, 4; S:1423). F-10's claim is partly false. | | | | |
| X-005 | Severity scale for a missing upstream edge (intra-variant) | A rates CF-01 and CF-02 medium but the same defect type at Task 16 (A-3) and Task 20 (A-4) low | rates Task 13, 15, 16 edges medium, Task 20 low | rates all five edge findings medium | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | C | F-2: Task 19 has no path to Task 13 (or Task 6, Task 14). X1 replays ref steps 3-12; step 11 calls `expect_checks_after_push` with `poll-ci-checks.sh --evidence-sha` input (S:303). Task 19's closure (5, 4, 3, 2, 8, 7, 11, 10, 12) excludes 13 and 6. Spec step 13 depends on all of step 9 (S:1428). | High |
| U-002 | A | A-6a: Task 10's "`git ls-files -s` shows mode 100755" cannot pass for an unstaged new file; use `test -x` or stage first. | Medium |
| U-003 | C | F-7: spec step 9 done-when requires `test_skill_forbids_force_push` green over the new files (S:1424); Tasks 11 and 12 run only `test_conflict_scripts.py` (P:203, P:213). | Medium |
| U-004 | C | F-9: Task 17 names no insertion point for the E5 operation-check sentence and E12 rows 3-5 after Task 1 removes the old substring; proposes exact anchors and a final-substring AC. | Medium |
| U-005 | C | F-8: `poll-ci-checks.sh:30` exits 2 when `--pr` is missing (confirmed), so C4's expected exit 2 could pass for the wrong reason; AC should run C1-C4 without `--pr` and check stderr names the SHA. | Medium |
| U-006 | A | A-7: pinned-phrase, order-pin and prohibition ACs of Tasks 10, 11, 14, 15 have no failing command until Task 18; add literal grep checks saved to `./artifacts/`. | Low |
| U-007 | A | A-10b: Tasks 8, 17, 18 are oversized; require per-family log sections. | Low |
| U-008 | A | A-9 residual: P:19 "source wins" does not state the `make test` exception; Task 20 log should record that VG-2 was not run. | Low |
| U-009 | C | F-3 extra: Task 16 also needs Task 6, because ci-poll.md item 4 documents `ci.expect_checks_after_push` (S:1070). | Low |
| U-010 | B | Q-4 extra: assert the fenced usage line in ci-poll.md matches the script header. | Low |
| U-011 | B | Q-1 extra: add the Task 9 import smoke to Task 20's run. | Low |
| U-012 | C | F-10 extra: optionally drop Task 9's edge on Task 6 (the only edge genuinely stricter than spec). | Low |
| U-013 | C | F-11 extra: tighten Task 17's "at most 15 lines" to the spec's "net +15" (S:1426). | Low |
| U-014 | B | Q-7 extra: without a staging step, Task 20's "no staged `.claude/` path" check (P:307) is vacuously true. | Low |

## Shared Assumptions

Enumeration (all agreement-derived preconditions):

| # | Agreement Source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | All three audit spec "depends on step 3" edges against plan Task 3 (CF-02 is the only Task 4 consumer any card finds) | Plan Task 3 alone stands for spec step 3 when checking edges | UNSTATED | Yes |
| A-002 | All three find missing edges by matching functions named in a task's body or AC text | An edge audit by named-artifact matching is complete | UNSTATED | Yes |
| A-003 | All three rate missing-edge findings medium or low, never as harmless | The executor runs tasks in Depends-on order (possibly parallel), not document order | STATED (F-4: "graph-ordered or parallel execution") | No |
| A-004 | All three classify the `make test` drop as authorized | The orchestrator brief cited at P:28 can override spec section 12.5 | STATED (P:28) | No |
| A-005 | All three return ready-with-fixes with no regression | The unresolved coverage-matrix rows hide no gap | STATED (Q summary: 21 unmapped-union INF rows unresolved) | No |
| A-006 | All three use spec section 13's "Depends on" column as the authority for edges | Spec section 13's dependency column is itself complete | UNSTATED | Yes |

Classification note: A-001 and A-002 are classified UNSTATED because no card states them; calibration evidence also refutes them (CF-22), so they are promoted and flagged for debate attention rather than left unpromoted as CONTRADICTED.

Promoted [SHARED-ASSUMPTION] diff points:

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | [SHARED-ASSUMPTION] Plan Task 3 alone satisfies a spec "depends on step 3" edge. The plan split spec step 3 (all of `conflicts.py`, S:1418) into Tasks 3 and 4, but Task 10 depends on Task 3 only (P:184), so every task reached only through Task 10 (Task 11: F10 `merge_parent_ok`, F12 `merge_preflight_ok`, S:1388, S:1390; Task 15; Task 18: S:1345) lacks Task 4. One root-cause fix, Task 10 "Depends on: Task 4" (spec-faithful: step 9 depends on 3, S:1424), closes CF-22 and covers CF-02. | Edge audits in A-2, Q-3, F-5 | High | UNSTATED; refuted by calibration-t2 and spot-check; needs debate |
| A-002 | [SHARED-ASSUMPTION] Matching named functions in task text finds every missing edge. Task 11 and Task 18 consume Task 4 functions only through spec test cases they cite by ID (F10, F12, a test name), so the name-match audits of all three cards missed them. | Method shared by all edge findings | Medium | UNSTATED; refuted by calibration-t2 missed lists |
| A-006 | [SHARED-ASSUMPTION] Spec section 13's "Depends on" column is complete. Step 13 (X1-X3) depends on 4, 6, 9 but X1 replays ref step 11, which calls `expect_checks_after_push` from `ci.py` (spec step 5; S:303, S:1428); step 10 (refs) depends on 9 only, yet ci-poll.md item 4 documents the same function (S:1070). F-2 and F-3 add Task 6 from content, but no card says the spec column itself is incomplete. | CF-03, CF-04, CF-17 edge recommendations | Medium | UNSTATED |

## Similarity Check

- Comparable items: 22 canonical findings plus 3 card-level attributes (verdict, no-regression claim, confidence) = 25.
- Items identical across all three cards (same presence, severity, class and fix): CF-02, verdict, no-regression claim = 3.
- Items that differ: 22 of 25 (88%). Seventeen of the 22 canonical findings are missing from at least one card; of the five present in all three, four (CF-01, CF-03, CF-04, CF-15) differ in severity, scope or fix.
- Result: differences are far above the 10% threshold. The variants are NOT substantially identical; the debate (Steps 2-3) proceeds.

## Summary
- Total structural differences: 6
- Total content differences: 13
- Total contradictions: 5
- Total unique contributions: 14
- Total shared assumptions surfaced: 6 (UNSTATED: 3, STATED: 3, CONTRADICTED: 0); promoted: 3
- Total differences found: 41 (6 + 13 + 5 + 14 + 3 promoted)
- Highest-severity items: U-001, A-001
