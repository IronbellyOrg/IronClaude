# QA Report — Anti-omission verification, cycle 2 review (after fix pass 2)

**Topic:** Orchestrator mode Phase 1 (issue #339)
**Date:** 2026-11-08
**Phase:** fix-cycle
**Fix cycle:** 2 (last review allowed; a FAIL here HALTs and escalates)
**Fix authorization:** false (report only; the report was not edited)
**Inputs:** `qa/qa-anti-omission-consolidated-findings-cycle1.md` (|F_1| = 1: NB-1), `qa/qa-anti-omission-fix-log-cycle1.md`, `RESEARCH-REPORT-orchestrator-mode.md`, cited sources under `research/`, `synthesis/`, `gaps-and-questions.md`

---

## 1. Baseline and constraint checks

| Check | Result | Evidence |
|---|---|---|
| Report unchanged in size, markers kept | PASS | `wc -l` = 1760; `grep -c CONTRADICTION` = 6; `grep -c NB-4` = 23 (all equal to the fix-log baseline). Report mtime 00:07:09, after the consolidated findings (00:04:52) and before the fix log (00:07:30), so the text read here is the fix-pass-2 text. |
| Edits contained to the spots the fix log names | PASS | `grep -n` for `archive-blocked`, `interrupted archive`, `two worktrees`, `unsupervised`, `archive_state`, `package_ids`, `terminal_state`, `next_action`: every hit is on lines 411, 412, 421, 1243, 1244, 1246, 1254 or 1255; none elsewhere, so no older paragraph still describes the pre-fix model. |
| No regression of AO-01 to AO-18 | PASS | Anchor strings for all 18 recoveries still present (`grep -c -F`): "one managed package in two worktrees" 2, "at most 10 inputs" 3, "worktree removed during sweep" 3, "set union, not a sum" 3, "terminal-state reclaimable --json" 2, "context-only Dispatch" 5, "interrupted archive" 5, `_EXPECTED_IDS` 2, `sanitize()` 2, "Freshness (`:23`)" 1, the (a) table header 3, "No matching records. This is not an all-clear." 3, `integration-gaps.md:24` 5, "Workspace co-location alone is not ownership." 2, `linked: true` 2, never "no sessions" 1, "must not propose stop/abandon/retry/release" 4, "denominator" 4. |

## 2. Blocking omission from the previous cycle

| ID | Status | Where verified (report line) | Verification |
|---|---|---|---|
| NB-1 | RECOVERED | 1243 (step 1.2), 1244 (step 1.3), 1246 (step 1.5), 1254 (step 1.8), 1255 (step 1.9); 411, 412, 421 (3.1) | Each of the three breaks the qualitative verifier named is closed. (1) Rule (i): `WorktreeState.package_ids` and `shared_package_ids` are defined in step 1.2; step 1.3 adds the pure pre-pass `mark_shared_packages(worktrees: list[WorktreeState]) -> list[WorktreeState]`, called once by `commands.py` after the probes and before any `safe_to_close`, so the one-worktree signature can now compute the rule; step 1.8 builds the two-root fixture through that pre-pass and step 1.9 tests both the shared and the non-shared case. One choice (pre-pass, signature unchanged) is used in 1.3, 1.8, 1.9 and 3.1 line 421, as the consolidated finding required. (2) Rule (iii): `WorktreeState.archive_states: tuple[tuple[str, str], ...]` is defined in step 1.2 (the deviation from the suggested `str \| None` is stated and reasoned: one worktree can hold several packages); step 1.5 names the print locations: a Worktrees "Package state" column for both states and a Retained problems line for "interrupted archive"; step 1.9 asserts exactly those locations. (3) Rule (ii): `OrcaObservation.unsupervised`, `terminal_state` and `next_action` are defined in step 1.2; step 1.3 rule (ii) names which function reads which field. The two-worktree pair also has a Retained problems line in step 1.5. Every new field and location carries "plan decision, new design". |

### Source fidelity of the recovered rules (re-read, not taken from the fix log)

| Rule | Report wording | Source re-read | Match |
|---|---|---|---|
| (i) | "It never runs one managed package in two worktrees at once." (421, 1244) | `research/scope-01-contract.md:64`; `src/superclaude/core/WORKER-CONTRACT.md:108` (read directly) | Exact |
| (ii) | `worker-list --help` line 20 and `worker-show --help` line 15 quotes (411) | `research/scope-02-orca-recovery.md:95`; `research/05-orca-row-schema.md:20`, `:28` | Exact; "JSON field not captured" matches 05, which records help text only |
| (iii) | archive-blocked and `.archiving` rules (412, 1244) | `research/scope-02-orca-recovery.md:192`; `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:190`, `:199` (read directly) | Exact, including "never infer the owner is dead from `FINAL:`/`ARCHIVE:` lines" |

## 3. Adversarial search for further omissions

Stance: assume at least 5 omissions remain. Probes run against the sources and the report:

| # | Probe | Result |
|---|---|---|
| P-1 | Every `GQ-` id in `gaps-and-questions.md` (100 ids) against the report | 19 ids not named singly (GQ-69 to GQ-75, GQ-77 to GQ-82, GQ-87, GQ-88, GQ-90 to GQ-93). All are covered by meaning through ranges: "GQ-68 to GQ-83" (report 598, 1377, 1691; gaps rows 92-105 are all `resolved` research-gate items) and "GQ-86 to GQ-95" (587, 1599). No omission. |
| P-2 | Source rules near the recovered ones: WC-3 no heartbeat while blocked in `ask`; terminal state separate from Task status; WC-6 retry as a new Task; weak-signal release list | Present (report 57, 501, 726; "new Task" 10 hits). The weak-signal list is the structural verifier's existing MINOR note; not rechecked. |
| P-3 | `pipelines.md:177-201`, the full range scope-02 `:192` cites, line by line | One state not in the report: `:198` "Present in both `to-do/` and `done/` → conflict. Report it; do not merge, move or delete either copy." Graded MINOR, note N-1. |
| P-4 | The new fields and functions against every step that consumes them (1.2 -> 1.3 -> 1.5 -> 1.6 -> 1.8 -> 1.9) | Four wording or detail gaps, all MINOR: notes N-2 to N-5. |

### New findings (all MINOR; notes only, no fix pass)

| ID | Severity | Location | Finding | Why MINOR, not blocking |
|---|---|---|---|---|
| N-1 | MINOR | 3.1 "Package states" (412); step 1.3 rule (iii) | `pipelines.md:198` defines a third package state, a package present in both `to-do/` and `done/` = conflict, "Report it; do not merge, move or delete either copy". The report recognises archive-blocked and interrupted archive only. | The state is absent from every research, synthesis and gaps file (scope-02 `:192` summarises the range without it), so it is not an omission of research content; the fidelity gate already graded the same source gap MINOR (`qa/qa-source-fidelity-report-2.md:18`, F2). The sweep is read-only, so it cannot act on the conflict wrongly. Plan stage: add "conflict" to `archive_states`. |
| N-2 | MINOR | Step 1.2 (1243) | The clause "read by step 1.3 rule (ii) and the terminal-releasable half of safe-to-close only, never to set the class" is attached to all three new `OrcaObservation` fields, but step 1.3 rule (ii) (1244) and 3.1 (411) have `classify` read `unsupervised` to route the row to could not determine, which does set the class. | Wording scope only: step 1.3 states "`classify` reads `row.orca.unsupervised`" and step 1.9 pins the behaviour, so an implementer cannot build the wrong thing without a failing test. Fix wording: "never to set the class" applies to `terminal_state` and `next_action`. |
| N-3 | MINOR | Step 1.5 (1246) | "One line per package id in `shared_package_ids`" is per worktree record, and the pre-pass sets the id on both records, so the pair line would print twice unless deduplicated; three or more roots do not fit "<path 1> and <path 2>". | Rendering detail; the step 1.9 assertion "the pair prints under Retained problems" holds either way. Plan stage: one line per shared id, listing every root. |
| N-4 | MINOR | Step 1.2 `archive_states` (1243); step 1.4 | "Every task complete" (archive-blocked) needs the plan's full task set; `progress.md` has per-task `start`/`complete` lines and a `PLAN:` hash line but no task count (checked on `.dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325/progress.md`). The report names no rule (for example a `FINAL: pass` line with no `ARCHIVE:` completion). The ledger grammar is documented in-repo at `sc-implement-protocol/refs/ledger.md:121`, `:231`, which no research file read; the report says the ledger record format is "not known" (1244, 1633). | Not in any research file, so outside this gate's source set; the same open point already applies to the pre-existing refusal condition 4 (unfinished ledger), which earlier gates accepted. Record for the plan stage. |
| N-5 | MINOR | Step 1.6 (1247) | The JSON schema has no worktree-level key, so package states and the two-worktree pair appear only in the Markdown report, not in the stdout JSON. | The skill reads the report file (step 1.15), not the JSON, for its output, so nothing is lost to the user. Pre-existing schema scope, not introduced by the fix. |

**Result of the adversarial search:** no new blocking omission. Five findings, all MINOR (N-1 to N-5), which meets the "at least 5" expectation without any of them being a wrongly graded blocking omission. Earlier MINOR notes (5 structural, M-1 to M-6) were not rechecked, per the fix-cycle rule.

## 4. Cycle control

| Guard | Result |
|---|---|
| Regression (runs first) | None. Every item that passed at the previous review (AO-01 to AO-18, structural checks) still passes (Section 1). |
| Monotonicity | Open blocking count went from 1 (NB-1) to 0: strictly smaller, no halt. |
| Hard cap | This is the third and last review of the anti-omission gate; with 0 open blocking findings no escalation is needed. |

## 5. Items that PASS

- **Blocking omissions:** NB-1 RECOVERED. None JUSTIFIED, none OPEN.
- **Earlier recoveries (no regression):** AO-01 to AO-18, all still RECOVERED and in place.
- **Checks:** baseline and marker counts; edit containment; source fidelity of rules (i), (ii), (iii); single pre-pass design used in steps 1.3, 1.8, 1.9 and 3.1; print locations in step 1.5 match the step 1.9 assertions; "plan decision, new design" labels on every new field, function and print location; GQ coverage (P-1); neighbouring source rules (P-2).
- **Not in the PASS set (notes, not blocking):** N-1 to N-5.

## 6. Open blocking count

**|F_1| = 0** (open blocking findings after fix pass 2; the consolidated findings file's previous count was 1, NB-1).

## 7. Confidence and tool engagement

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
  (1 step 1.2 fields; 2 pre-pass used consistently in 1.3/1.8/1.9; 3 step 1.5 print locations; 4 Section 3.1 consistency; 5 source fidelity of the three rules; 6 marker and line counts; 7 AO-01 to AO-18 regression anchors; 8 edit containment; 9 adversarial omission search P-1 to P-4; 10 regression and monotonicity guards.)
- **Tool engagement:** Read: 10 | Grep: 4 | Glob: 1 | Bash: 10. No web research.
- UNCHECKED items: none. UNVERIFIABLE items: none.
- Not checked: earlier MINOR notes (5 structural, M-1 to M-6), by the fix-cycle rule; report lines outside the fix pass 2 edit lines were checked only through the regression anchors and the probes above.

## Verdict: PASS
