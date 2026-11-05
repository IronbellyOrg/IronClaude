# Merge Execution Log

## Metadata
- Base: Variant A (sonnet:analyzer), `variant-1-original.md` (reviewer 1 card)
- Non-base: Variant B (`variant-2-original.md`, reviewer 2 card)
- Plan: `refactor-plan.md` (19 changes, auto-approved)
- Context: `debate-transcript.md`, `invariant-probe.md`
- Output: `.dev/reflect/pre-phase2CodegraphI-20261029192356/adversarial/merged-reviewer-findings.md`
- Executor: merge-executor agent
- Changes applied: 19 of 19 planned
- Status: success
- Timestamp: 2026-10-29T20:21:08Z
- Method: the merged file was written as a header stub first, then one Edit per entry (M-01 to M-19), then the closing note. Nothing in the source, tests, docs, plan or spec was changed. No git commands were run.
- Observation: the plan's approval timestamp (2026-10-29T20:40:00Z) is later than this merge's clock time. It has no effect on the merge and is recorded only.

## Changes Applied

### Change 1: M-01 plan:48 `.claude/` guard
- **Status**: Applied
- **Source**: Base R1-01; Variant B P2R2-7 (Task 1 part); debate X-001, A-001; INV-019
- **Target**: Merged finding M-01 (restructure)
- **Before**: R1-01 drift / important. plan_ref plan:48; spec_ref source.md:440-442, 445. Fix: `test -z "$(… || true …)"`. P2R2-7 called the guard benign with fix "None".
- **After**: authorized / plan / important. plan_ref adds plan:21; spec_ref adds source.md:436 and 755. The claim states the inverted exit status and the vacuous `test -z` repair. The fix is the two-line file-first block with the `if … ; then exit 1; fi` negative.
- **Provenance tag**: `<!-- Source: Base R1-01 (original, modified) + Variant B P2R2-7 (Task 1 part); debate X-001, A-001; INV-019 — merged per Change #1 -->`
- **Validation**: Structural integrity PASS | References PASS (plan:21, 23, 48; source.md:436, 445, 755 checked. source.md:440-442: see Citation check D-1) | Contradictions PASS

### Change 2: M-02 Task 16 scope checks abort the exit-0 block
- **Status**: Applied
- **Source**: R1-02; P2R2-1; advocate A Round 1 concession 10 and Round 2 New evidence 2; advocate B Round 2 item 7; INV-001 to INV-005
- **Target**: M-02 (restructure)
- **Before**: R1-02 drift / important, plan:277-278 vs plan:286. Fix: move the local-scope jq out with `|| echo LOCAL_SCOPE_HIT`.
- **After**: necessary / inherited-from-spec / important. Fix (a) to (d): each scope check's rc is recorded in a `/tmp` file and gated with `test "$rc" -le 1`; read-only jq prints the user-scope and local-scope remove commands; the user-scope gate is deferred to the end of the block (INV-001 correction); a seventh, non-blocking human item is added.
- **Provenance tag**: `<!-- Source: Base R1-02 (original, modified) + Variant B P2R2-1; advocate A Round 1 concession 10 and Round 2 New evidence 2; advocate B Round 2 item 7; INV-001 to INV-005 — merged per Change #2 -->`
- **Validation**: Structural integrity PASS | References PASS (plan:27, 275-286, 277, 278, 279-284, 286; source.md:197, 209-211, 210, 211, 705, 709-716 checked. source.md:757-765: see D-2) | Contradictions PASS

### Change 3: M-03 `$E` undefined in Task 5
- **Status**: Applied
- **Source**: R1-03; P2R2-2; X-002; INV-023
- **Target**: M-03 (modify; class necessary → drift)
- **Before**: R1-03 necessary / minor. Fix: "say E is built as in source.md T2 step 1".
- **After**: drift / plan / minor. The fix is one fenced block: MT with `test -n`, then E exactly as source.md:534, then the `jq -e --argjson` check.
- **Provenance tag**: `<!-- Source: Base R1-03 (original, modified: class necessary → drift) + Variant B P2R2-2; debate X-002; INV-023 — merged per Change #3 -->`
- **Validation**: Structural integrity PASS | References PASS (plan:107; source.md:533-534, 534, 540) | Contradictions PASS

### Change 4: M-04 `./artifacts/` paths resolve to the never-staged project root
- **Status**: Applied
- **Source**: R1-04 (path part); P2R2-4; C-004; X-003; INV-008; INV-009
- **Target**: M-04 (new entry, split out of R1-04)
- **Before**: R1-04 bundled three defects (paths, Task 14 copies, Task 3 hash). Fix: a Constraints `$ART`.
- **After**: drift / plan / "important (minor for the prose-only refs at plan:79 and plan:237)". The fix uses the literal package path in each block, `mkdir -p` in Tasks 3 and 14, and an absolute worktree root for Task 3 before `rm -rf "$W"`.
- **Provenance tag**: `<!-- Source: Base R1-04 (path part, split) + Variant B P2R2-4; debate C-004, X-003; INV-008, INV-009 — merged per Change #4 -->`
- **Validation**: Structural integrity PASS | References PASS (plan:24, 79, 85, 237, 253, 272, 287; source.md:527) | Contradictions PASS (overlap with M-07 on plan:272/287 noted under Contradiction Re-Scan)

### Change 5: M-05 Task 14 never writes its required evidence files
- **Status**: Applied
- **Source**: R1-04 (Task 14 part); X-004; INV-007; INV-010
- **Target**: M-05 (new entry, split out of R1-04)
- **Before**: part of R1-04: "add explicit cp lines to Task 14".
- **After**: drift / plan / important. The copies sit right after plan:243 and plan:246, the perf.json restore moves ahead of `test ! -s`, and the Task 14 evidence is always committed.
- **Provenance tag**: `<!-- Source: Base R1-04 (Task 14 part, split); debate X-004; INV-007, INV-010 — merged per Change #5 -->`
- **Validation**: Structural integrity PASS | References PASS (plan:237, 242-253, 243, 246, 247, 248, 253, 259; source.md:669-684) | Contradictions PASS

### Change 6: M-06 Task 3 real-hash criterion has no before-hash
- **Status**: Applied
- **Source**: R1-04 (hash part); P2R2-3; C-002; INV-012; INV-013
- **Target**: M-06 (new entry, split out of R1-04; relabelled authorized per INV-013)
- **Before**: part of R1-04: "give Task 3 an explicit H0 before and a final equality test". P2R2-3: drift / minor with a shell-variable H0.
- **After**: authorized / plan / minor. H0 is stored in `/tmp/p2-t3-h0.txt` and compared at the end.
- **Provenance tag**: `<!-- Source: Base R1-04 (hash part, split) + Variant B P2R2-3; debate C-002; INV-012, INV-013 (relabelled authorized) — merged per Change #6 -->`
- **Validation**: Structural integrity PASS | References PASS (plan:23, 73-77, 86; source.md:522, 525, 755) | Contradictions PASS (label consistent with M-01 under the classification rule)

### Change 7: M-07 Task 16 writes an in-repository artifact the spec forbids
- **Status**: Applied
- **Source**: P2R2-7 calibrator note; A-003 (CONTRADICTED); both advocates' A-003 comments; INV-022
- **Target**: M-07 (insert)
- **Before**: Did not exist in the base. Only reviewer 2's calibrator noted the source.md:706 conflict.
- **After**: drift / plan / minor. Output goes to `/tmp/p2-t16-live-verify.txt` and into the G6 comment with the M-02 markers. The file clause is dropped from plan:272 and plan:287.
- **Provenance tag**: `<!-- Source: Variant B P2R2-7 calibrator note; shared assumption A-003 (CONTRADICTED) and both advocates' A-003 comments; INV-022 — merged per Change #7 -->`
- **Validation**: Structural integrity PASS | References PASS (plan:24, 272, 287; source.md:706, 719) | Contradictions PASS

### Change 8: M-08 U11 assigned to the wrong task
- **Status**: Applied
- **Source**: R1-05; INV-016
- **Target**: M-08 (modify; origin inherited)
- **Before**: R1-05 necessary / important. plan_ref plan:92, 96 vs 104-110; spec_ref source.md:296, 101, 33.
- **After**: necessary / inherited-from-spec / important. plan_ref plan:92; 96; 104. spec_ref source.md:101; 296; 466; 486. The fix names all three plan lines and flags U22 (source.md:307) as UNVERIFIED.
- **Provenance tag**: `<!-- Source: Base R1-05 (original, modified: origin inherited); INV-016 — merged per Change #8 -->`
- **Validation**: Structural integrity PASS | References PASS (plan:92, 96, 104; source.md:101, 296, 307, 466, 486. The fix's "plan:104 ("U11-U19, U23, U25")" is the target wording; plan:104 currently reads U12-U19, as the finding says) | Contradictions PASS

### Change 9: M-09 `&&` / `!` lines do not gate inside blocks
- **Status**: Applied
- **Source**: R1-07; INV-015; INV-020; orchestrator run
- **Target**: M-09 (modify; class drift → necessary; plan:84 dropped; plan:163 and source.md:602, 637 added)
- **Before**: R1-07 drift / important. plan_ref plan:84, 162, 165, 202-203, 244; spec_ref source.md:445; 625; 325.
- **After**: necessary / inherited-from-spec / important. plan_ref plan:162, 163, 165, 202, 203, 244. spec_ref source.md:601, 602, 604, 636, 637, 675; 625. The fix keeps each positive grep before its negative.
- **Provenance tag**: `<!-- Source: Base R1-07 (original, modified: class drift → necessary; plan:84 citation dropped; plan:163 and source.md:602, 637 added); INV-015, INV-020; orchestrator run — merged per Change #9 -->`
- **Validation**: Structural integrity PASS | References PASS (each plan line re-read: 162 `sh -n && cmp`, 163 `make sync-dev && make verify-sync`, 165 and 244 `grep && ! grep`, 202 and 203 `rg -q && rg -q`. plan:84 confirmed standalone. Spec lines map one-to-one, and source.md:625 holds the if-form note) | Contradictions PASS

### Change 10: M-10 `uv run --no-project` yaml import
- **Status**: Applied
- **Source**: R1-08; INV-014
- **Target**: M-10 (modify; origin inherited; claim narrowed)
- **Before**: R1-08 necessary / minor, "likely fails" (pyproject.toml:38).
- **After**: necessary / inherited-from-spec / minor. The claim is narrowed: the command works here because uv finds `.venv`. The fix is optional.
- **Provenance tag**: `<!-- Source: Base R1-08 (original, modified: origin inherited; claim narrowed); INV-014 — merged per Change #10 -->`
- **Validation**: Structural integrity PASS | References PASS (plan:216; source.md:649-651; pyproject.toml:38 `"pyyaml>=6.0"` confirmed) | Contradictions PASS

### Change 11: M-11 `grep -i connected` matches "Disconnected"
- **Status**: Applied
- **Source**: R1-09; INV-024
- **Target**: M-11 (keep)
- **Before**: R1-09 necessary / minor. Its fix also said "copy the get output into the t16 artifact".
- **After**: necessary / inherited-from-spec / minor. The claim is R1-09's, verbatim, because the plan's Change 11 gives no Claim and its Target is "keep". The fix is the plan's: the negative grep only. The t16-artifact clause is not carried over, which matches the plan text and M-07.
- **Provenance tag**: `<!-- Source: Base R1-09 (original; claim kept verbatim, fix per plan); INV-024 — merged per Change #11 -->`
- **Validation**: Structural integrity PASS | References PASS (plan:282; source.md:374-375, 714) | Contradictions PASS

### Change 12: M-12 Task 2 drops the T0b coordinator report
- **Status**: Applied
- **Source**: R1-10
- **Target**: M-12 (keep)
- **Before**: R1-10 drift / minor.
- **After**: drift / plan / minor. The claim is R1-10's, verbatim (the plan gives no Claim; Target is "keep"). The fix is the plan's.
- **Provenance tag**: `<!-- Source: Base R1-10 (original; claim kept verbatim, fix per plan) — merged per Change #12 -->`
- **Validation**: Structural integrity PASS | References PASS (plan:54; source.md:448) | Contradictions PASS

### Change 13: M-13 Task 6 `--list` Ready line depends on Task 7
- **Status**: Applied
- **Source**: R1-06 (calibrator: overstated)
- **Target**: M-13 (keep at minor; class necessary, origin inherited)
- **Before**: R1-06 necessary / important. The fix offered two options, including "move codegraph_ready() into Task 5".
- **After**: necessary / inherited-from-spec / minor. The claim frames it as an ordering ambiguity only. The fix has one option: the Ready line lands in Task 7.
- **Provenance tag**: `<!-- Source: Base R1-06 (original, modified: kept at minor as overstated; class necessary, origin inherited) — merged per Change #13 -->`
- **Validation**: Structural integrity PASS | References PASS (plan:120, 125, 131; source.md:142, 561-563, 573) | Contradictions PASS

### Change 14: M-14 Task 13 sandbox fallback only by reference
- **Status**: Applied
- **Source**: R1-11 (calibrator: overstated)
- **Target**: M-14 (keep at minor)
- **Before**: R1-11 necessary / minor, plan_ref plan:227, "Task 13 omits the fallback".
- **After**: drift / plan / minor, plan_ref plan:223-227. The claim is that the fallback is included only by reference (plan:19, plan:223). The class follows the plan's Content line.
- **Provenance tag**: `<!-- Source: Base R1-11 (original, modified: kept at minor as overstated; class necessary → drift) — merged per Change #14 -->`
- **Validation**: Structural integrity PASS | References PASS (plan:19, 223, 223-227; source.md:416) | Contradictions PASS

### Change 15: M-15 T1 coverage-matrix false attributions
- **Status**: Applied
- **Source**: P2R2-5 with the calibrator's U23 correction; C-003
- **Target**: M-15 (insert)
- **Before**: Not in the base. P2R2-5 mislabelled INF-056 as U25.
- **After**: drift / reflect-artifact / minor. INF-056 is U23 (source.md:308). The carriers are Task 4 and Task 5.
- **Provenance tag**: `<!-- Source: Variant B P2R2-5 (with the calibrator's U23 correction); debate C-003 — merged per Change #15 -->`
- **Validation**: Structural integrity PASS | References PASS (source.md:289, 308; coverage-matrix.yaml:319-325 shows INF-037 → Task 7, and :454-461 shows INF-056 → Task 3, citation source.md:308) | Contradictions PASS

### Change 16: M-16 T1 coverage-matrix under-sampling
- **Status**: Applied
- **Source**: P2R2-6 (calibrator: overstated)
- **Target**: M-16 (insert at minor)
- **Before**: Not in the base. P2R2-6 listed spans including §8 (767-785) as rowless.
- **After**: drift / reflect-artifact / minor. The spec_ref is the plan's span list without §8. The plan gives no separate Claim for Change 16, so the claim restates the plan's own fix wording ("these spans have no matrix rows … by-reference triage"). No content was added beyond the plan text.
- **Provenance tag**: `<!-- Source: Variant B P2R2-6 (calibrator: overstated; kept at minor) — merged per Change #16 -->`
- **Validation**: Structural integrity PASS | References PASS with note D-3 (INF-093 at coverage-matrix.yaml:746 cites source.md:725, outside 727-741, so keeping the 727-741 span is consistent. INF-104 cites source.md:780, inside §8) | Contradictions PASS

### Change 17: M-17 Task 2 "commit only if a file changed"
- **Status**: Applied
- **Source**: P2R2-7; INV-018
- **Target**: M-17 (insert)
- **Before**: Not in the base. P2R2-7 called it benign, fix "None".
- **After**: authorized / plan / minor. The condition names `phase-1-removal-spec.md` or the facts file.
- **Provenance tag**: `<!-- Source: Variant B P2R2-7 (Task 2 part); INV-018 — merged per Change #17 -->`
- **Validation**: Structural integrity PASS | References PASS (plan:24, 54; source.md:459 has an unconditional commit line, so the condition is a plan addition) | Contradictions PASS

### Change 18: M-18 Task 7 retire-test selector can be empty
- **Status**: Applied
- **Source**: reviewer 1 calibrator `extra_risk`; INV-006; orchestrator check
- **Target**: M-18 (insert)
- **Before**: Only reviewer 1's calibrator `extra_risk` line, not a finding.
- **After**: necessary / inherited-from-spec / important. The fix is `F=$(rg -l -g '*.py' …)`, then `test -n "$F"`, then pytest. This applies the HIGH invariant INV-006.
- **Provenance tag**: `<!-- Source: reviewer 1 calibrator extra_risk (Variant A); INV-006 (HIGH); orchestrator check — merged per Change #18 -->`
- **Validation**: Structural integrity PASS | References PASS (plan:131, 134-135; source.md:572, 576-577; pyproject.toml:108 `testpaths = ["tests"]` confirmed) | Contradictions PASS

### Change 19: M-19 Acceptance checks that pass vacuously
- **Status**: Applied
- **Source**: INV-011; INV-017
- **Target**: M-19 (insert)
- **Before**: Did not exist.
- **After**: necessary / inherited-from-spec / minor. plan:21 becomes "if and only if". plan:167 becomes file-first then `test ! -s`. plan:228 becomes a `test … = LAYER2_OK`.
- **Provenance tag**: `<!-- Source: invariant probe INV-011, INV-017 — merged per Change #19 -->`
- **Validation**: Structural integrity PASS | References PASS (plan:21, 167, 217, 228; source.md:606, 661. plan:217 has no counterpart in source.md T8, so "plan-added" holds) | Contradictions PASS

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: PASS. One H1 ("Merged Reviewer Findings: Phase 2 plan (issue #323)"). Three H2: "Classification rule", "Findings", "Unaddressed invariants". Nineteen H3 entries M-01 to M-19, all under "Findings", none skipping a level.
- Section ordering: PASS. The provenance header comes first, then the H1, the classification rule, the findings in plan order M-01 to M-19 (each provenance tag names Change #1 to #19 in sequence), and the closing note.
- Document flow: PASS. No leftover merge anchor.
- Entry schema (checked mechanically with `yaml.safe_load` on each fenced block):
  - 19 of 19 blocks parse.
  - Each has exactly the 9 keys in order: id, sources, class, origin, severity, plan_ref, spec_ref, claim, fix.
  - `sources` is a YAML list in every entry.
  - Every `id` matches its heading.
  - Each M-NN appears exactly once.
- Class values, all in {authorized, necessary, drift, regression}:
  - authorized 3: M-01, M-06, M-17
  - necessary 8: M-02, M-08, M-09, M-10, M-11, M-13, M-18, M-19
  - drift 8: M-03, M-04, M-05, M-07, M-12, M-14, M-15, M-16
  - regression 0
- Origin values, all in {plan, inherited-from-spec, reflect-artifact}:
  - plan 9
  - inherited-from-spec 8
  - reflect-artifact 2 (M-15, M-16)
- Plan fidelity: for all 19 entries, class, origin, severity, plan_ref and spec_ref equal the refactor-plan.md Content values exactly (mechanical string compare, 0 mismatches). Claims and fixes are the plan's text. The exceptions are M-11 and M-12, whose claims are base text kept verbatim per "keep", and M-16, whose claim restates the plan's fix wording. The plan gives no Claim for those three changes. Nothing was added, dropped or softened.

### Internal References (citation check)
Every plan:N and source.md:N citation in the merged file was re-read against `.dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/TASK-WF-phase2CodegraphI-20261029-192001.md` (287 lines) and `source.md` in that folder (863 lines).
- Total unique references: 101 (49 plan:N, 52 source.md:N)
- Resolved: 101. The highest plan line cited is 287, which is the last plan line. The highest spec line cited is 765.
- Broken (wrong line or wrong content): 0
- Imprecise ranges (the plan's value was kept, recorded only):
  - **D-1**: M-01 spec_ref `source.md:440-442`. The T0 acceptance commands are lines 440-441. Line 442 is the closing code fence. Harmless.
  - **D-2**: M-02 spec_ref and claim `source.md:757-765`. The six-item human list is lines 757-763. Line 764 is blank, and line 765 is the `## 8. Release and ordering` heading. The range runs two lines past the list. (The invariant probe used 758-763.)
  - **D-3**: M-16 spec_ref `source.md:59-193`. §2.1-§2.11 end at line 188. Lines 190-193 are the §2.12 heading and its requirement paragraph. This range is Variant B's original, and the plan kept it.
- Other references verified:
  - pyproject.toml:38 (pyyaml) and :108 (`testpaths = ["tests"]`)
  - coverage-matrix.yaml:319-325 (INF-037) and :454-461 (INF-056)
  - INF-093 at coverage-matrix.yaml:746 (cites source.md:725) and INF-104 at :834 (cites source.md:780)

### Contradiction Re-Scan
- New contradictions introduced: 0
- Details (pairs checked):
  - M-04 vs M-07 (both cite plan:272 and plan:287). This is overlap, not a contradiction. M-04's claim covers the path drift for all six references. Its fix's `mkdir -p` and absolute-root steps name only Tasks 3 and 14. M-07 governs Task 16 by moving its output to `/tmp` and dropping the file clause. This overlap comes from the plan itself (Changes 4 and 7). The merge did not create it.
  - M-11 vs M-07: base R1-09's "copy the get output into the t16 artifact" is not carried over, so M-11 no longer conflicts with M-07.
  - M-02 vs M-07: both send Task 16 output to `/tmp` and the G6 comment. Consistent.
  - M-01 vs M-06 vs M-17: all three plan additions backed by a rule are labelled authorized, which matches the classification rule (INV-013 resolved).
  - M-01 vs M-19: both treat plan:21 as the standard. M-19's "if and only if" wording strengthens it and does not conflict.
  - M-05 vs M-09: M-05 moves the perf.json restore ahead of `test ! -s`. M-09 splits plan:244 while keeping the positive grep first. The two are compatible.
  - M-08 vs M-15: M-08 moves U11 to Task 5. M-15 places U4 in Task 4 and U23 in Task 5. Consistent.

## Summary
- Total changes planned: 19
- Successfully applied: 19
- Failed: 0
- Skipped: 0
- Escalations to orchestrator: none. Every planned change applied as written.
- Unaddressed invariants: INV-001 and INV-006 (HIGH) were not re-debated at depth standard. They are applied as corrections in M-02 and M-18 and stated in the merged file's closing section.
- Post-merge validation: PASS
