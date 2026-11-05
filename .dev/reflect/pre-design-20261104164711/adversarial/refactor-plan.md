# Refactoring Plan: Merge into Base (Variant C)

## Overview
- Base: Variant C (`variant-3-original.md`, reviewer 3, refactorer, opus)
- Incorporating strengths from: Variant A (analyzer, sonnet), Variant B (qa, glm-5.3), and positions no card held: the calibrator finding CF-22, the invariant probe and R-INV
- Planned changes: 11
- Risk level: Medium overall. Change 2 is High because it restructures Task 4 and moves a heading.
- Goal: the merged card carries the consensus CF table below as its findings, with verdict `ready-with-fixes` and no regression claimed (all three cards and all advocates agree).
- Debate result feeding this plan: convergence 0.852 (23 / 27), status CONVERGED, invariant gate cleared by R-INV. Under the reflect routing (0.75 or higher PASS), this is PASS.
- Citation key: P = `.dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md`; S = `source.md` in the same folder; IMPL = `~/.claude/skills/sc-implement-protocol/SKILL.md`. Every P line number below was re-read for this plan.

## Target Content: Consensus CF Table

`*` marks the INV-006 qualifier. The rating is Low only while `/sc:implement` runs sequentially in document order with no parallel-marked set. Under a graph-order or parallel executor the row reverts to Medium (B, round-inv E5: "a future graph-order executor re-opens the cards"). Basis: IMPL:79 ("Ignore MDTM fields (`depends-on`, ...) except `independent`"), IMPL:97 ("Default sequential in source order"), and a grep of P for `independent|parallel` that returns no match.

| CF | Severity | Class | Fix (plan location) | Verify | Provenance |
|---|---|---|---|---|---|
| CF-01 | Low* | drift | P:207 Task 12 becomes "Depends on: Task 11"; insert "Depends on: Task 12" under the Task 13 heading (P:215). This gives the chain 10 → 11 → 12 → 13. | Every task that edits `tests/pr_submit/test_conflict_scripts.py` has a path to every earlier editor. | Base F-4; A-1, Q-2; C-001 |
| CF-02 | Low* | drift | P:239 Task 15 becomes "Depends on: Task 4a, Task 12". P:241 "from Task 4" becomes "from Task 4a". | Task 15's closure contains 4a. | Base F-5 (part a); A-2, Q-3 |
| CF-03 | Medium (header check); the edge part is Low* | drift | P:250 Task 16 becomes "Depends on: Task 2, Task 6, Task 13". Add a Task 16 AC: grep that the fenced `scripts/poll-ci-checks.sh --evidence-sha <sha> --repo <owner/repo>` line in `ci-poll.md` matches the script header, with output saved under `./artifacts/`. | No ref task runs before the script or function its text names. The grep output exists. | Base F-3; B Q-4 (grep); A-3; C-002; round-inv A and C: "only the edge part is lowered" |
| CF-04 | Low* | drift | P:300 Task 20 becomes "Depends on: Task 6, Task 9, Task 18, Task 19". | Task 20's closure covers 1, 2, 3, 4a, 4b and 5-19. | A-4, Q-8; base F-5 (part b), whose "9 suffices" C conceded in R2 |
| CF-05 | Low | drift | The R-INV resolution: see Change 2 for the exact edits. | See Change 2. | Base F-1b, amended by A (4b on 5), B (8 → 4b) and C's fallback (5 → 4a, 9 → 4b) |
| CF-06 | Low | drift | Split Task 4 into 4a and 4b along the resume boundary (Change 2). | See Change 2. | Base F-1a; C-005 |
| CF-07 | Low | advisory (not a deviation) | Optional per-family log sections for Tasks 8, 17 and 18. No plan change is required. | n/a | A-10b (A withdrew it as drift, R1); B and C agree it is advisory (R2) |
| CF-08 | Medium | drift | Add a staging step to Task 20 after the `make sync-dev` instruction (P:302): `git add -- src tests CHANGELOG.md` and `git add .dev/tasks`, and no commit. Add an AC that `git diff --cached --name-only` lists only those paths, which makes P:307's "no staged `.claude/` path" check non-vacuous. | The `git diff --cached --name-only` output is saved to `./artifacts/t20-checks.log`. | A-6b; B Q-7 / U-014 (vacuity); C-006 |
| CF-09 | Medium | drift | P:191 Task 10 AC: replace "`git ls-files -s` shows mode 100755" with `test -x <path>`. Apply the same check to the scripts of Tasks 11 and 12. Use a `git ls-files -s` mode check only after the CF-08 staging. | `test -x` exits 0 for each new script. | A-6a (U-002) |
| CF-10 | Low | drift | Tasks 10, 11, 14, 15: one literal `grep -cF` per pinned phrase, ascending line numbers for order pins, and forbidden-regex greps with no hits, saved under `./artifacts/`. | The grep files exist and have the expected counts. | A-7 (U-006) |
| CF-11 | Medium | drift | P:291 Task 19: add Task 10's module-level capability skip (skip unless `git merge-tree --write-tree HEAD HEAD` works in a scratch repository) alongside the `uv`-absent skip. | X1-X3 skip, rather than error, where merge-tree is unsupported. | B Q-5b (the named breakage framing); A-8a; S:1316 |
| CF-12 | Medium | drift | P:29: add a fixed `GIT_AUTHOR_NAME`, `GIT_AUTHOR_EMAIL`, `GIT_COMMITTER_NAME` and `GIT_COMMITTER_EMAIL` to the real-git test constraint. | F9, F10, X1 and X3 commit under `GIT_CONFIG_GLOBAL=/dev/null`. | B Q-5a; A-8b; S:1316 |
| CF-13 | Low | drift | P:51 Task 2: quote the S:728 clause "plus the two conflict-cycle events `sync_started` and `sync_concluded`" for both docstrings. | A grep of the `models.py` docstrings finds the clause. | A-8c, Q-6a |
| CF-14 | Low | spec defect | P:53: cite `loop-guard.md:86-103`. The plan copies S:731's `:86-99`; the list ends at `:103`. | n/a | A-8d, Q-6b; class from A (R1), conceded by B and C (R2) |
| CF-15 | Low | authorized | P:306: add `tests/cli/reflect/test_contract_status_cli.py` to Task 20's pytest run. The first line of `./artifacts/t20-checks.log` reads "make test (VG-2) not run per orchestrator brief". | `t20-checks.log` shows the reflect test passing. | Base F-6 (lowered from Medium; Task 9 dropped); A-9; Q-1 (cite corrected to S:1408) |
| CF-16 | Low | authorized | None. | n/a | Base F-11; A-11 |
| CF-17 | Low* | drift | P:289 Task 19 becomes "Depends on: Task 5, Task 8, Task 11, Task 12, Task 13". The Task 6 and Task 14 edges are optional. | Task 19's closure includes Tasks 10-13. | Base F-2, reduced (C, R1: S:1400 omits `expect_checks_after_push`) |
| CF-18 | Low | drift | P:203 and P:213: add `tests/pr_submit/test_static_grep.py` to the pytest commands of Task 11 and Task 12. | The logs include `test_skill_forbids_force_push`. | Base F-7 |
| CF-19 | Low | drift | Task 13 AC (P:220): C1-C4 invoke the script with `--evidence-sha` and `--repo` only (no `--pr`); C4 asserts that stderr names the invalid SHA. | The C-case argument lists contain no `--pr`. | Base F-8 (`poll-ci-checks.sh:30` exits 2 without `--pr`) |
| CF-20 | Low | drift | Task 17 (P:267): the E5 operation-check sentence goes right after Task 1's text ending "so report how many commits it is behind instead)."; E12 rows 3-5 go after the "Behind base branch (create path at L1+, or `--pr`)" row. AC: the final Wave 0 substring equals the full E5 replacement in source section 8.1. | The substring check is recorded in the Task 17 evidence. | Base F-9, relabelled from `necessary` (X-003) |
| CF-21 | Low | necessary | Keep Task 9 → Task 6 (P:171), because Task 9's AC collects `test_ci_classify.py` (P:178). No change. | n/a | Base F-10, claim corrected (X-004) |
| CF-22 | Low* | drift | P:184 Task 10 becomes "Depends on: Task 3, Task 4a". | Task 11 (F10 `merge_parent_ok`, F12 `merge_preflight_ok`; S:1388, S:1390), Task 15 and Task 18 (S:1345) all reach 4a. | Calibrators (`calibration-t2.yaml` missed lists); A-001 |
| INV-007 | Low | not assigned in debate (the spec carries the same gap, S:1416, S:1418) | P:66 Task 3 becomes "Depends on: Task 1, Task 2". | Task 1 and Task 3 (both edit `test_static_grep.py`, P:40, P:75) are ordered. | Invariant probe INV-007; R-INV E4, accepted by A, B and C |

Severity count: 5 Medium (CF-03 for the header check, CF-08, CF-09, CF-11, CF-12). Everything else is Low, and 6 of the Low rows carry the `*` qualifier. No row is High.

## Planned Changes

### Change 1: Re-key the findings to CF rows, one defect per row (from the debate consensus)
- **Source**: `diff-analysis.md` finding equivalence map; S-001 consensus
- **Target**: Base `findings` list (restructure)
- **Rationale**: S-001, agreed at 80%. Every R2 table splits the bundled findings A-8, A-6, A-10, Q-5, Q-6, F-1 and F-5. All three cards failed rubric Structure-3 (separation of concerns) for bundling.
- **Integration point**: Replace the ids F-1..F-11 with CF-01..CF-22 plus INV-007, in the table order above. Keep the base's per-finding fields (`severity`, `deviation_class`, `claim`, `evidence`, `recommendation`) and add a `Verify:` sentence to every recommendation (the base's convention, S-005 kept). Convert evidence paths imported from A and B to repo-relative form, as in the base.
- **Risk**: Medium. It touches every finding. A dropped row loses a consensus fix.

### Change 2: Apply the R-INV resolution for CF-05 and CF-06 (from Variant C's F-1, amended by A, B and R-INV)
- **Source**: Base F-1; A R2 (4b on Task 5); B R2 (Task 8 → 4b); C R2 fallback (5 → 4a, 9 → 4b); `invariant-probe.md` CF-05 verdict; `round-inv-advocate-{A,B,C}.md` qualifiers
- **Target**: Base F-1 recommendation (replace)
- **Rationale**: C-004 and C-005, unanimous after R-INV (90% and 95%). The probe blocked convergence on INV-001, INV-002 and INV-005. All three round-inv files state that R-INV, with these qualifiers, fully addresses all three.
- **Integration point**: The CF-05 / CF-06 recommendation lists these plan edits:
  1. **Heading 4a.** P:84 becomes ``## Task 4a: Add routing, gates, records and messages to `conflicts.py` ``. P:86 stays "Depends on: Task 3". P:88's lead sentence says "the remaining non-resume functions of source section 5.3". P:90 and P:91 stay in 4a.
  2. **Heading 4b.** Insert ``## Task 4b: Add the resume planners to `conflicts.py` (after the run-log fold)`` after Task 7's last line (P:151) and before `## Task 8` (P:153). It has the line "Depends on: Task 4a, Task 5, Task 7". Add a body sentence saying that 4b extends `conflicts.py` and sits after Task 7 because its Resume tests build `state` with `RunLog.rebuild_state()` (A and C qualifiers; IMPL:71 normalizes the heading to `T4b`, and IMPL:75 requires body text). The heading sits under "Phase 3: Changes to the existing core modules" (P:102), and its text names `conflicts.py` (C, cosmetic).
  3. **Split P:92.** The `crash_resume_plan` / `conflict_resume_plan` bullet moves to 4b.
  4. **Split P:93.** The Router, Gates, Cycle ids, and Record and message cases, plus every listed property (monotonicity, `c_initial` default row, the Wave 8a Tier 1 column, the `merge_parent_ok` matrix and disjointness, the `evaluate_sync_decision` truth tables, branch-literal equality, `REPORT_REASONS & HALT_REASONS`), stay in 4a. The Resume cases move to 4b. Delete the parenthesis "(resume tests build `state` dicts directly; the run-log integration is Task 8)". 4b builds `state` from `RunLog.rebuild_state()` (base F-1).
  5. **Split P:99.** The clause `prior_conflict_cycles(["sync-1"], "sync-1") == 0` (a 4a function, P:91) becomes a 4a AC. The `conflict_resume_plan` directive clause becomes a 4b AC. Add a 4b AC for `crash_resume_plan` against source section 4.8's second table, because it has no AC today (A qualifier). P:96, P:97 and P:98 stay in 4a.
  6. **Split P:100.** 4a: `uv run pytest tests/pr_submit/test_conflicts_core.py -q`, log `./artifacts/t4a-tests.log`. 4b: the same command, log `./artifacts/t4b-tests.log`.
  7. **Re-point edges.** P:106 Task 5 "Depends on: Task 4" becomes "Depends on: Task 4a". P:155 Task 8 "Depends on: Task 4, Task 7" becomes "Depends on: Task 4b, Task 7" (B's re-point, kept). P:171 Task 9 "Depends on: Task 5, Task 6" becomes "Depends on: Task 4b, Task 5, Task 6".
  8. **Stale reference.** P:241 "from Task 4" becomes "from Task 4a" (A and C; R-INV omitted it). The CF-02 and CF-22 edges also name 4a.
  9. **Task 3 on Task 1 (INV-007).** P:66 becomes "Depends on: Task 1, Task 2" (see Change 3).
  - Resulting document order: 1, 2, 3, 4a, 5, 6, 7, 4b, 8, 9, 10-20. Every edge points to an earlier task, so the graph has no cycle (INV-001). Task 9's closure is {1, 2, 3, 4a, 4b, 5, 6, 7}, which covers the S:744 exports (INV-002). Under `/sc:implement` the document position is what orders execution (INV-005).
  - Verify: `grep -n '^## Task' P` shows `## Task 4b` between `## Task 7` and `## Task 8`; `grep -n 'Task 4\b' P` returns no bare "Task 4"; no Resume test uses a dict literal in place of `rebuild_state()` output; and each Depends-on target sits above its dependent.
- **Risk**: High. If the heading is not moved, INV-005 reopens. If P:106 or P:171 is missed, INV-001 or INV-002 reopens.

### Change 3: Add the INV-007 row (from the invariant probe)
- **Source**: `invariant-probe.md` INV-007; R-INV E4 (A, B and C ACCEPT)
- **Target**: Base, new finding after CF-22 (append)
- **Rationale**: Tasks 1 and 3 both edit `tests/pr_submit/test_static_grep.py` (P:40, P:75) with no ordering edge. The problem is latent under document order (C: Low).
- **Integration point**: Insert the INV-007 row as written in the table. The class is left unassigned because the debate never assigned one.
- **Risk**: Low. Additive, and the new edge points backward.

### Change 4: Add CF-22 and the A-002 method note (from the calibrators and the consensus)
- **Source**: `calibration-t2.yaml` missed lists; A-001 and A-002 (ACCEPT by all three, R1 and R2)
- **Target**: Base, new finding CF-22 plus one sentence in `summary` (append)
- **Rationale**: Every card missed CF-22. One edge (Task 10 on 4a) gives Task 11, Task 15 and Task 18 a path to 4a.
- **Integration point**: Insert the CF-22 row. Add a method sentence to `summary`: "Edge audit expands spec test-case IDs and export lists (S:741-749) into the functions they use, and computes closures from the plan graph, not by name matching."
- **Risk**: Low. Additive.

### Change 5: Rewrite the edge findings CF-01, CF-02, CF-03, CF-04 and CF-17 (from base F-2..F-5, with A and B additions)
- **Source**: Base F-2, F-3, F-4, F-5; B Q-4 (grep); A-4 / Q-8 (Task 6 named explicitly)
- **Target**: Base F-2..F-5 (replace)
- **Rationale**: C-001 (95%), C-002 (90%), C-003 (95%), U-001, and A-006 QUALIFY (the step 10 column needs Task 6; the step 13 column is adequate).
- **Integration point**: Split F-5 into CF-02 and CF-04. Add Task 6 to CF-04. Add B's header-match grep to CF-03. Cut F-2 down to the required Task 13 edge, with Tasks 6 and 14 optional. Keep F-4's chain.
- **Risk**: Medium. It modifies existing base recommendations.

### Change 6: Apply the INV-006 regrade with its qualifier (from the invariant probe and round-inv E5)
- **Source**: `invariant-probe.md` INV-006; round-inv E5 (A, B and C QUALIFY)
- **Target**: Severity fields of CF-01, CF-02, CF-03 (edge part only), CF-04, CF-17 and CF-22, plus one sentence in `summary`
- **Rationale**: Each of these edges is already satisfied by document order, which is the only order `/sc:implement` uses (IMPL:79, IMPL:97). That refutes the premise behind the Medium ratings (A-003).
- **Integration point**: Set these rows to Low and add the sentence: "Low only while /sc:implement runs sequentially in document order with no parallel-marked set; a graph-order or parallel executor restores Medium." CF-03's header-match check stays Medium and stays in the fix (A and C).
- **Risk**: Medium. If the qualifier is dropped, the regrade becomes unconditional, which no advocate accepted.

### Change 7: Add the acceptance-criteria findings CF-07, CF-08, CF-09, CF-10, CF-13 and CF-14 (from Variant A)
- **Source**: Variant A: A-10b, A-6b, A-6a, A-7, A-8c, A-8d; B Q-6 and Q-7 for CF-08, CF-13 and CF-14
- **Target**: Base, new findings (append)
- **Rationale**: C-006 (A, 95%), C-008 (A, 90%), U-002, U-006 and U-007. The base has none of these (RC 13 / 22).
- **Integration point**: Insert the rows as written in the table, with CF-14's class as `spec defect` and CF-07 as `advisory`.
- **Risk**: Low. Additive.

### Change 8: Add CF-11 and CF-12 as two findings (from Variant B)
- **Source**: Variant B Q-5; A-8a and A-8b
- **Target**: Base, new findings (append)
- **Rationale**: C-007 (B, 95%). B named the breakage of F9, F10, X1 and X3, and A conceded Medium in R2.
- **Integration point**: Insert both rows, each at Medium and citing S:1316.
- **Risk**: Low. Additive.

### Change 9: Lower CF-15 (from base F-6, with A's severity and log line)
- **Source**: Base F-6; A-9; X-002 / C-009 (A, 85-90%)
- **Target**: Base F-6 (replace)
- **Rationale**: An `__init__` import failure already breaks every `tests/pr_submit` test, so only the CLI path is unexercised. C conceded Low and Task 20 only (R1), and B conceded (R2).
- **Integration point**: Severity Medium becomes Low. Remove Task 9 from the recommendation. Add the "make test (VG-2) not run per orchestrator brief" first line. The evidence cites S:1408.
- **Risk**: Low.

### Change 10: Correct labels and claims in CF-16, CF-20 and CF-21 (from the debate)
- **Source**: Base F-9, F-10, F-11; X-003, X-004, C-010
- **Target**: Base F-9, F-10, F-11 (replace)
- **Rationale**: C conceded that F-9 is drift and that F-10's claim is wrong for Task 5 and Task 8. All R2 tables carry CF-16 as "None".
- **Integration point**: F-9 becomes CF-20, with class `necessary` changed to `drift` and the anchors kept. F-10 becomes CF-21: rewrite the claim to "Only Task 9 → Task 6 is stricter than spec section 13 (step 8 depends on 3, 4; S:1423); Task 5 and Task 8 on Task 4 are spec-required (step 3 = Tasks 3 + 4)". Its recommendation becomes "Keep the edge"; delete "optionally drop". F-11 becomes CF-16 with "No change"; delete "optionally tighten Task 17 to 'net +15'".
- **Risk**: Low.

### Change 11: Update the card header, summary and verdict (from all three cards)
- **Source**: All three cards; `calibration-t2.yaml`
- **Target**: Base header comment, `verdict`, `self_reported_confidence`, `summary`
- **Rationale**: The verdict (`ready-with-fixes`) and the no-regression claim are identical across the cards (diff-analysis similarity check).
- **Integration point**:
  - Header: "Merged by sc:adversarial Mode A from reviewers 1-3; base reviewer 3."
  - `verdict`: `ready-with-fixes`.
  - `self_reported_confidence`: keep the base's 0.82, which equals its calibrated value. The calibrations are A 0.82, B 0.78 and C 0.82.
  - `summary`: 22 CF rows plus INV-007. Five are Medium (CF-03 header check, CF-08, CF-09, CF-11, CF-12), and the rest are Low. Six Low rows carry the document-order qualifier. Task 4 is split into 4a/4b, with 4b placed between Task 7 and Task 8. No regression. Add the method sentence from Change 4 and the qualifier sentence from Change 6.
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale |
|------------|-------------------|---------------------------|
| C-004 | A-5: move the resume tests to Task 8, no new task | A adopted C's 4a/4b split in R2, because moving the tests leaves resume code untested in Task 4. |
| C-005 | A-10a: split Task 4 into router vs gates/records/messages | C-005 (95%): the split goes along the resume boundary, which is where the Task 7 dependency falls. |
| C-004 | C's own R2 edge set (Task 5 on 4b; 4b on 4a, 7) | This is a base-adjacent position being dropped. Under IMPL:97 it holds only if Task 7 moves above Task 5 (INV-005), and it is stricter than spec step 4 (INV-014). C conceded in round-inv. |
| C-004 | B R1: CF-05/06 as "necessary deviation, Medium" | X-001: B conceded drift and Low in R2, because S:1422 gives a spec-compliant placement. |
| U-001 | Base F-2: Task 6 and Task 14 as required Task 19 edges | X1's command list (S:1400) omits `expect_checks_after_push`. Only Task 13 is required (C conceded in R1). |
| C-003 | Base F-5b: "Task 9 suffices" for Task 20 | C conceded in R2. Listing Task 6 costs nothing and survives later edge edits. |
| C-009 / U-011 | Base F-6 and Q-1: the reflect test and an import smoke in Task 9 | Redundant: every `tests/pr_submit` test already imports the package `__init__` (C conceded in R1, B in R2). |
| U-008 (part) | A-9: reword P:19 ("source wins, except the make test override") | No R2 table carries it, including A's own. Only the "VG-2 not run" log line is kept. |
| X-003 | Base F-9: class `necessary` | The spec itself splits E5 and E12 (S:1416, S:1426). C conceded. |
| X-004 / U-012 | Base F-10: "Task 5 and Task 8 on Task 4 are stricter"; "optionally drop Task 9 → 6" | Both edges are spec-required (spec step 3 = Tasks 3 + 4). Keep 9 → 6 as necessary (CF-21). |
| U-013 | Base F-11: tighten Task 17 to "net +15" | No R2 table carries it. All three say "None". |
| CF-07 | A-10b: required per-family log sections | Withdrawn as a deviation. Tasks 8, 17 and 18 mirror spec steps 7, 11 and 12. The row stays as advisory only. |
| C-002 | A R1: CF-03 at Low | A conceded in R2. The header-match grep makes Task 16's AC read Task 13's script. |
| INV-006 | Unconditional Medium (or unconditional Low) for CF-01, 02, 04, 17, 22 | Both forms are rejected. The rating is Low under the stated executor, with the qualifier recorded (A, B and C, round-inv E5). |
| C-011 | Q-1's citation S:1392 | Corrected to S:1408 (B conceded). |
| S-004, S-005, S-006 | Card order, path style and header of A or B | Unresolved and not debated. Keep the base format (C's order, repo-relative paths, Verify clauses). No debate evidence favours a change. |
| C-013 | B's caveat: "21 unmapped-union INF rows could not be resolved" | Unresolved. Only C's advocate supported it, and no majority formed. It is not imported as consensus; it is reported as an unresolved point to the sc:reflect orchestrator. |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Medium | A dropped or merged row loses a consensus fix | Rebuild the rows from the consensus table above |
| 2 | High | A missed P:106 or P:171 edit reopens INV-001 or INV-002; an unmoved heading reopens INV-005 | Revert to base F-1 and re-run the invariant probe |
| 3 | Low | Additive; Tasks 1 and 3 stay unordered (latent) | Remove the row |
| 4 | Low | Additive | Remove CF-22 and the method sentence |
| 5 | Medium | Wrong edge lists in the four edge rows | Revert to base F-2..F-5 text |
| 6 | Medium | Missing qualifier makes the regrade unconditional | Restore Medium on the six rows |
| 7 | Low | Additive | Remove the inserted rows |
| 8 | Low | Additive | Remove the inserted rows |
| 9 | Low | Severity text only | Revert to base F-6 |
| 10 | Low | Label and claim text only | Revert to base F-9..F-11 |
| 11 | Low | Header and summary text only | Revert to the base header and summary |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-04T18:48:52Z
