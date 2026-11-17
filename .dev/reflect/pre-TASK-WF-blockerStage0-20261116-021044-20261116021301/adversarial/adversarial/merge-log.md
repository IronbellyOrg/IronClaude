# Merge Log

## Metadata

- Base variant: `adversarial/adversarial/variant-1-original.md` (reviewer-1, analyzer persona, haiku class)
- Non-base sources: `variant-2-original.md` (reviewer-2, qa persona, opus class), `invariant-probe.md`
- Refactoring plan: `adversarial/adversarial/refactor-plan.md` (11 planned changes, risk Low)
- Merged output: `adversarial/merged-review-card.md`
- Merge date: 2026-11-16
- PLAN = `.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md` (defined once in the card's header comment; citations use `PLAN:<line>`). PF = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115`, written out in full in every citation.
- No plan file was edited. Every quote in the card was read from the live file during this merge.

## Changes Applied

| # | Finding | Status | Source | Provenance tag |
|---|---|---|---|---|
| 1 | F1 (MAJOR, blocking true, data-loss): Task 3 rerun overwrites `results.md` | Applied. Base F1 rewritten with the plan's claim text, the Round 2 fix and the blob id; 7 citations | Base V1 F1; Round 2; probe INV-001, INV-002, INV-003 | `<!-- Source: Variant 1 F1 (base), ... -->` |
| 2 | F2 (MAJOR, blocking true, other): SubagentStart hook injects the old rule into the "new text" arm | Applied. New finding, 5 citations | Probe INV-006 | `<!-- Source: invariant probe INV-006 ... -->` |
| 3 | F3 (MINOR, blocking false, missing-requirement): Task 9 sweep misses spec lines 1011 and 1108 | Applied; 4 citations | Probe INV-005 | `<!-- Source: invariant probe INV-005 -->` |
| 4 | F4 (MINOR, blocking false, other): Task 5 cluster rule leaves repeats unpaired | Applied; 3 citations | Probe INV-007 | `<!-- Source: invariant probe INV-007 -->` |
| 5 | F5 (MINOR, blocking false, missing-requirement): Task 10 acceptance lines omit OD list, five findings and ledger decision | Applied; 5 citations | Both calibrators, Round 2, probe INV-012 | `<!-- Source: both calibrators, Round 2 ... -->` |
| 6 | F6 (MINOR, blocking false, other): Task 2 frame left to the executor | Applied; 3 citations | Variant 2 F2, debate C-003 | `<!-- Source: Variant 2 F2 ... -->` |
| 7 | F7 (MINOR, blocking false, other): Tasks 5 and 6 both include the Task 2 sample | Applied; 3 citations | Variant 2 F3(b), debate C-005, probe INV-011 | `<!-- Source: Variant 2 F3(b) ... -->` |
| 8 | F8 (MINOR, blocking false, other): Task 7 sizing will fall back to advisory | Applied; 2 citations | Variant 2 F3(a), debate C-004 | `<!-- Source: Variant 2 F3(a) ... -->` |
| 9 | F9 (MINOR, blocking false, missing-requirement): always-staged constraint missing | Applied; 2 citations | Variant 2 F1, debate C-002, T1 calibrator | `<!-- Source: Variant 2 F1 ... -->` |
| 10 | F10 (MINOR, blocking false, unpassable-check): Task 6 disjointness check cannot fail | Applied; 3 citations | Probe INV-009 | `<!-- Source: invariant probe INV-009 -->` |
| 11 | F11 (MINOR, blocking false, other): `@E2` Evidence paths readable only through git | Applied; 2 citations | Probe INV-010 | `<!-- Source: invariant probe INV-010 -->` |
| 12 | Verdict: NEEDS-REVISION with blocking count (2) and main cause | Applied | Plan overview; X-001 (V2's PASS-with-notes dropped) | none (section header) |
| 13 | Checked: merged both variants' bullets (duplicate Task 9 anchor bullet dropped) and added the probe's count checks | Applied; 10 bullets | V1, V2, probe INV-003, INV-004, INV-008 | `<!-- Source: Checked bullets ... -->` |
| 14 | Self-report: confidence 0.85, merged self-report string; header `merged_from` line and header comments | Applied | Instruction from orchestrator | header comments |

Changes NOT made, as the plan states: V2's PASS-with-notes verdict; V1's "Task 9's evidence pointer" wording (the card says the cited content, not the path, is lost); V2's "a short spec cannot hold that many defects" (softened to "almost certainly use the advisory fallback"); INV-003, INV-004, INV-008 and INV-013 as findings (used only as Checked bullets).

## Post-Merge Validation

- Findings present: 11 (F1 to F11), in the plan's order.
- Blocking: F1 true, F2 true. F3 to F11: false (9 findings).
- Every finding has at least one citation (counts above: 7, 5, 4, 3, 5, 3, 3, 2, 2, 3, 2).
- Required sections present once each, in order: Verdict, Findings, Checked, Self-report. Heading levels consistent (all `##`).
- No cited line number was changed from the plan. PLAN paths shortened to `PLAN:<line>` per instruction; `PF/` expanded to the full repo-relative path.
- Count checks done live: 318 `F-B` rows in `master-table.md` and in each of the three blind tables; 15 `@E2` rows in the master table; git blob id of `results.md` is `d9616dd28fbb08daa565b11c69ef75cb7819f274` (matches F1); 10 `## Task` and 4 `## Phase` headings in the plan; 139 files in the run-2 `qa/` folder; PF `git diff` is empty.
- Citation support from the live files:
  - Quotes were taken verbatim from the live file wherever the plan gave none.
  - Citation not supported by its line: `TASK-RESEARCH-review-panel-run2-20261114-075454/qa/gate5-cycle-control.md:1` (F6). Line 1 is only the file title, so it shows the file exists; the claim itself rests on the plan lines (PLAN:42, PLAN:45-48) and on the folder holding 139 files, which I counted. The quote given is that title.
  - Citation that shows an absence: `PLAN:17-26` (F9) cannot quote a missing sentence; the quote is the `## Constraints` heading. A grep of the whole plan for "always staged" returns nothing, which supports the claim.
  - Citation that is a pointer to a range: `PLAN:139-142` (F5) is quoted from line 139 only; lines 140 to 142 also contain no OD list or five-findings requirement.
  - `PLAN:69` (F2) supports the "movement counts" half of the claim only; the hook half rests on `hooks.json:173` and `pragmatic.md:225`. I confirmed that this session's own subagent context carries the old-rule sentence, which matches the claim.
- Severity wording: the plan's overview calls F3 to F7 "Medium" (the debate's grade) while its change headings say MINOR. The card uses the headings (MINOR), as the card scale has only CRITICAL, MAJOR and MINOR.
- Side observation, not part of the card: `git status` shows `PF/stage-requests/` as untracked, which conflicts with the rule that `.dev/tasks/` is always staged. Not touched here.

## Summary

All 11 planned findings were written. 2 blocking, 9 non-blocking. Nothing was skipped or improvised; the one item the live files could not support (the F6 line-1 citation) is recorded above.
