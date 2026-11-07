# Round 2 rebuttal: advocate for Variant 3 (opus, refactorer)

Paths are relative to the P2 worktree root. "plan" is `.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md`; "spec" is `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Every new citation below was read in this round.

## 1. Response to the criticisms of Variant 3

Steelman of the critics first. Both rebuttals chose V3 as the merge base. They attack it on three grounds: it states some harms more strongly than the evidence supports; its `verified_ok` section reads like a full certificate when it is not one; and it has one counterexample that falls outside the plan's own check. All three grounds are fair, and most of the points below are concessions.

| Criticism | Source | Response | Evidence |
|---|---|---|---|
| R3-F1 overstates the harm ("commit/push") | R1 V1; R2 V1 | **Concede push. Counter in part on the commit.** In Round 1 I dropped commit and push completely. New evidence brings part of the commit back. The `sc:task` protocol's TFEP section says "This report is committed to git alongside other diagnostic artifacts". D-P2-12 turns that off only under `--unattended`, and Stage 9 of tasklist does not pass the flag. So a TFEP inside a nested `sc:task` keeps the committed-report default. That breaks WC-9 ("never commits") in a worker. The harm depends on a TFEP trigger. Push stays dropped: in this protocol "push" is only a task type (EXEMPT list), and the Stage 9 input is a checklist, not a push request. | `sk/sc-task-protocol/SKILL.md:61,266`; plan:57; `sk/sc-tasklist-protocol/SKILL.md:1539-1542`; spec:77 |
| `verified_ok` says "dependency chains correct", but R3-F1 asks for a missing edge | R2 V2 | **Concede the wording. Counter in part.** Each edge the section lists (12->11, 13->5, 16->15, 17->15, 18->4) is correct. "Correct" overstated it, because the card's own fix asks for an edge the section did not check. Keep each check as a bounded claim ("listed edges exist"), never as "all required edges are present". | `D/variant-3-original.md:25-27,184` |
| The R3-F13 dirty-folder example | R2 V2 | **Concede and drop it.** The equality check queries only `src tests plugins`, so `.dev/reflect` cannot fail it. | plan:372 |
| R3-F6 wrongly covers the task handoff | R2 V2 | **Concede.** The brainstorm task handoff calls `task-builder`, not the converted `/sc:task`. R3-F6 now applies only to the tasklist handoff. | `sk/sc-brainstorm-protocol/SKILL.md:349-352` |
| R3-F3 says the test pins the path | R1 | **Concede** (already conceded in Round 1). Lines 837-844 pin tokens, not the path. The real C-002 problem is the first-line reader (section 2). | `tests/skills/test_worker_contract.py:770-775` |
| R3-F2 (FR-G5, `--no-pty`) | R1 | **Concede.** plan:248 settles both. | plan:248 |
| R3-F7 and the second half of R3-F12 are too broad | R1 | **Concede the narrowing.** R3-F7 now covers only the Safety Threshold clause. The second half of R3-F12 is already in D-P2-1. | plan:46 |
| V3 rated X-001 P2 | R1 V2 | **Concede.** P1 (see section 2). | spec:164; plan:248 |
| V3 tags every finding as drift | R1 | **Concede.** Use the four classes per finding (C-008). | -- |
| V3 missed U-004 and C-004 | R1 | **Concede.** Both go into the merge. | -- |

## 2. Updated assessment of V1 and V2

**V1.** Steelman: V1 found the conditional task-builder gate (U-004), the socratic decision and the return-contract.md coherence point. In Round 2 it conceded honestly and chose V3 as the base. I still have two disagreements with it:
- V1 says `--fix --promote` is an *outward* action. That goes too far. The spec lists outward actions as push, merge into a shared branch, PR, GitHub post, a shared install, a VM or a paid run. Local edits and a local folder move are not on that list. The spec does refuse the `git add -A` half of task-builder:2237, which keeps U-004 alive. I side with V2: the `--fix`/`--promote` half is a conditional integration question that the plan's `--no-promote` brief row partly covers, not a WC-9 breach. (spec:77; plan:276)
- On X-001, V1 says `run` "launches with no safety inputs". That is too strong. The brief may pass the safety flags (plan:330, "the run flags"). The actual gap is that nothing blocks when they are missing: spec:164 says "requires `--suite` and the safety flags in the brief, else blocked", but plan:248 blocks only on a missing `--suite`. P1 still holds, for the right reason.

V1's "new evidence" about the Task 12 dependency and the Task 20 literal was already in V3's suggested fix. V2 says the same.

**V2.** Steelman: V2 has the fewest false claims and the best evidence form. It made the correct P1 call on cli-eval, and its relationship-level negative tests are the right fix for C-004. Its Round 2 adds two real findings: `_artifacts_clause` reads only the first line that matches `artifacts` (test:770-775), and `_check_unattended_section` checks for presence only (test:509-512). Both hold. Its gap is coverage: five findings, with no nested-call sweep. Section 3 shows that sweep still finds defects.

## 3. New evidence

1. **The plan misses a second nested call in troubleshoot.** `--diagnosability-handoff` calls `Skill sc:workflow-protocol` (`sk/sc-troubleshoot-protocol/refs/diagnosability-audit.md:245,250`; `SKILL.md:645`; the flag is parsed at `cmd/troubleshoot.md:148`). `/sc:workflow` accepts `--unattended` from P1, so spec:62 requires the flag plus `nested/workflow-<n>/`. Task 11 nests only `adversarial` (plan:220), and "diagnosability" appears 0 times in the plan. If unflagged, the nested workflow follows its own rule, "`.dev/tasks/` is always staged (`git add .dev/tasks`)" (`sk/sc-workflow-protocol/SKILL.md:28`). That is a worker `git add`, which WC-9 forbids (spec:77). Class: drift, P1 (the same type as R3-F1). Fix: Task 11 adds `workflow` to its nested list and to `EXPECTED_NESTING`, or the section refuses `--diagnosability-handoff` under `--unattended`.
2. **R3-F1 has a second harm besides the commit: the impact path.** At STRICT compliance, the unflagged `sc:task` runs its `sc:impact-protocol` call (`sk/sc-task-protocol/SKILL.md:94`). That call writes to `.dev/impact/task-<slug>`, the path D-P2-12 replaces only under the flag (plan:233). So the output is outside the report directory and missing from `artifacts`, which breaks WC-4 and WC-11 (spec:72,79).
3. **The R3-F1 fix must change two test literals, not one.** `test_nested_lists_match_the_p2_nesting` compares the `nested` lists with `EXPECTED_NESTING` for equality (plan:79). The section check requires `nested/<name>-` for each listed name (test:513-517, mirrored at :944-949). So Task 16 must change its `UNATTENDED_EXPECT` entry to nested `reflect` and `task`, and also `"tasklist": ["reflect"]` (plan:290). Changing only one of the two fails the suite.
4. **V2's first-line reader decides how C-002 can be fixed.** The stale `artifacts` sentence is at workflow.md:72. Task 17 replaces only line 75 (plan:303), and the ADDITIVE check allows one deleted line (plan:41). An *added* correcting line placed after line 72 is invisible to `_artifacts_clause`, which reads the first matching line (test:770-775). So either the exemption grows to two lines, or the clause check gets scoped to the right line. An extra sentence alone is not a fix.

## 4. Final per-point positions

| ID | Winner | Position |
|---|---|---|
| S-001 | merge | V3's sections, with `verified_ok` as bounded per-check claims |
| S-002 | merge | V3's finding spine, with V1/V2 unique findings added and the conceded items dropped |
| S-003 | V2 | Repo-relative file:line evidence |
| C-001 | merge | V2's missing-block finding, P1. The fix names the safety flags from `sk/sc-cli-eval-protocol/SKILL.md:128-153` and blocks when they are absent |
| C-002 | merge | V1 and V3, plus new evidence item 4. The fix must reach the line `_artifacts_clause` reads |
| C-003 | merge | V2's complete F1 coverage. Only plan:97 and plan:110 pin "left out (WC-4)" |
| C-004 | merge | V2's relationship-level negatives plus V1's per-gate phrases |
| C-005 | V2 | P3. Compare the full commit manifest including the package. The V3 dirty-folder example is dropped |
| C-006 | merge (V3 lead) | Research arms of D-P2-1 |
| C-007 | merge | Instruction/check collisions (Task 12 "add new lines" vs ADDITIVE and WRITEVERB; Task 17 vs the one-line budget) |
| C-008 | merge | The four classes, assigned per finding |
| X-001 | V2 | **P1** (blocks only when `--suite` is missing; safety flags are not enforced) |
| X-002 | V3 | **Drift**. The plan sets its own one-line cap and leaves a known stale clause; that is not forced by the spec |
| A-001 | qualify | The flags are nameable from the cited cli-eval lines; the plan says only "the run flags" |
| A-002 | qualify | The cap is the plan's own choice (plan:41), not the spec's; the fix may widen it or add a scoped check |
| A-003 | accept | STATED: spec:60 (nested calls never guard-checked) and spec:62 (the propagation rule) |

## 5. Unique contributions

| U | Item | Decision |
|---|---|---|
| U-001 | R3-F1 tasklist Stage 9 `sc:task` | **Correct, keep P1**: push dropped; conditional committed TFEP report (sc-task:266) plus the impact path (sc-task:94); the fix changes both test literals |
| U-002 | R3-F4 | Keep |
| U-003 | R3-F5 | Keep |
| U-004 | R1-F3 task-builder gate | **Correct**: the `git add -A` half is refused by spec:77; the `--fix --promote` half is conditional, not outward |
| U-005 | R1-F4 spec-panel socratic | Keep |
| U-006 | R1-F6 | Correct (narrowed as agreed in Round 1) |
| U-007 | R1-F7 | Keep, bounded |
| U-008 | R1-F9 | Drop |
| U-009 | R2-F5 | Correct, as a matrix note |
| U-010 | R3-F6 | Correct: tasklist handoff only |
| U-011 | R3-F7 | Correct: Safety Threshold clause only |
| U-012 | R3-F9 | Keep as an observation |
| U-013 | R3-F10 | Keep |
| U-014 | R3-F14 | Keep |
| U-015 | verified_ok | Correct: bounded checks, not a certificate |
| new | troubleshoot `--diagnosability-handoff` -> `sc:workflow-protocol` | Add, P1 drift (section 3 item 1) |

## 6. Recommended base

**Use V3 as the base**, which both other advocates also chose. It has the widest coverage and the only nested-call sweep, and that sweep keeps finding real defects (R3-F1, plus section 3 item 1 in this round). Its structure already holds the dependency, nesting and mirror checks that the merge needs. On top of it, add V2's evidence form, the cli-eval P1, the relationship-level negatives, the F1 coverage and the P3 manifest point, and V1's U-004 (corrected), socratic decision and per-gate phrase lists. Drop or narrow the V3 items conceded in section 1.
