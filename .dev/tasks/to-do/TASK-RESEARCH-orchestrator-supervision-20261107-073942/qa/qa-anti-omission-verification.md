# QA Report — Anti-omission gate, fix-cycle verification

**Topic:** Orchestrator mode Phase 1 (issue #339), research report anti-omission recoveries
**Date:** 2026-11-07
**Phase:** fix-cycle
**Fix cycle:** 1 (review after fix pass 1; cycle 0 had |F_0| = 18)
**Fix authorization:** false (report not edited)
**Inputs:** `qa/qa-anti-omission-consolidated-findings.md`, `qa/qa-anti-omission-fix-log.md`, `RESEARCH-REPORT-orchestrator-mode.md`, cited sources in `research/`, `synthesis/`, `gaps-and-questions.md`

---

## Per-omission verification (AO-01 to AO-18)

Each row was checked by meaning against the cited source and the report text (3.1, 3.2, Section 8 Phase 1, rollback table, 9.4), not by ID and not by the fix log's term list. Report line numbers re-confirmed by grep this pass.

| ID | Status | Report location (verified) | Source checked | Evidence and judgement |
|---|---|---|---|---|
| AO-01 | RECOVERED | 3.1 "Worktree removable", sub-bullet "One package in two worktrees" (`:421`); step 1.3 rule (i); steps 1.8/1.9 | `scope-01:64` (rule 9, `WORKER-CONTRACT.md:108`) | Carries "It never runs one managed package in two worktrees at once."; same package id under two roots prints removable: no and goes to Retained problems (labelled plan decision, new design). Matches source meaning. |
| AO-02 | RECOVERED | 3.1 "Fan-in groups" (`:455`); 3.1 WC-14 G5; step 1.5; step 1.17 G5 (line 1274) | `scope-01:68` (rule 13, `:156`) | Max 10 inputs, merge only with at least 2 admitted, settled/admitted counts against N, `partial` = "usable not yet judged". Step 1.17 restates the bounds. Matches. |
| AO-03 | RECOVERED | 3.1 "Worktree removed mid-sweep" (`:469`); step 1.4 rule (a); steps 1.8/1.10 | `research-notes.md:178`; `seed-brief.md:45` | Vanished root prints could not determine with `unscanned: worktree removed during sweep`; run continues, report written, exit 0. Marker text labelled new design. Matches "reported, not crash the run". |
| AO-04 | RECOVERED | 3.1 skeleton line (`:434`) and rule (`:451`); step 1.5 (2 hits "set union"); step 1.12 | `research-notes.md:143`; `scope-04:194`, `:217`, `:283` | Set-union rule and the fixed line are in the skeleton, the renderer step and the tests. Matches. |
| AO-05 | RECOVERED | 3.1 WC-14 G1 (`:457`); step 1.17 candidate clause (line 1274) | `scope-02:94` (`orca-capabilities.md:113`, UNVERIFIED) | Recorded as an [UNVERIFIED] candidate, added to G1 only after `worker-list --help` shows `--terminal-state` and the guard is confirmed, else Open Questions. The source is itself UNVERIFIED guide text, so a gated candidate is the faithful form, not a weakening. |
| AO-06 | RECOVERED | 3.1 "Context-only Dispatches" (`:411`); step 1.3 rule (ii); steps 1.8/1.9 | `scope-02:95` (`worker-list --help` line 20, CODE-VERIFIED) | Help lines quoted; never working/stalled from liveness; could not determine with a named note unless rule 1/6 matches on a contract; `retained` never terminal releasable. The classification rule the finding asked for is stated. |
| AO-07 | RECOVERED | 3.1 "Package states the ledger reader must recognise" (`:412`); step 1.3 rule (iii); step 1.4 `.archiving` stat | `scope-02:192`; `research-notes.md:177` | archive-blocked is neither unfinished nor finished; `.archiving` goes to Retained problems, is never cleared, worktree removable: no. Matches. |
| AO-08 | RECOVERED (source claim recorded, marked [CODE-CONTRADICTED as a requirement]) | Step 1.22 (line 1284); rollback "Four registries" row (line 1312) | `scope-01:117`; `tests/core/test_how_we_work_routing_table.py:54-55`, `:200-204` re-read this pass | The test comment reads "A row may be added; none of these may be renamed or removed." and `test_ids_unique_kebab_and_stable` asserts `_EXPECTED_IDS <= set(ids)`, a subset. The source's "needs adding there" is therefore not a test requirement. The report records `_EXPECTED_IDS`, the source claim, the contradiction, that step 1.21 adds no routing-table row, and that the rollback needs no revert. The deviation rests on code I read, not on the fix log. |
| AO-09 | RECOVERED | 3.1 "Imported evidence is inert" (`:452`); step 1.5 (`sanitize`); step 1.12 injection case | `scope-04:219` (`PKG/PLAN.md:38`, `canvas.py:10-17`) | ESC/CSI/OSC, C0/C1, CR and bidi sanitising before render, with a test. Matches. |
| AO-10 | RECOVERED | Step 1.5 (line 1246) | `scope-04:334-351` (B-14 table) | Step 1.5 names every column (Owner, Worktree, Lifecycle, Phase, Health, Approval, Freshness, Result, Admission, Evidence, Policy, Tests/review) with "not observed" (7 hits in the line) and "null (unavailable)" for Tests/review. The bare citation is replaced. Matches. |
| AO-11 | RECOVERED | 3.1 "Explicit-questions table (a)" (`:449`) and skeleton (a) heading; step 1.5 | `scope-04:278`, `:311`, `:322-330` | Columns ID / Age / Question / Requested by / Decision owner / Affected / Evidence and the B-12 per-source cell fallbacks. Matches. |
| AO-12 | RECOVERED | 3.1 "Empty lists are not an all-clear" (`:450`) and skeleton; step 1.5 fixed strings; step 1.12 (line 1258) | `scope-04:225` (`PKG/render.py:116`), `:276` | "No matching records. This is not an all-clear." and the (a) heading line ending "This is not an all-clear.", both tested. Matches. |
| AO-13 | RECOVERED | 3.1 "Source loss changes nothing" (`:453`); 3.2 SC-7 (`:481`); step 1.12 | `scope-04:101`, `:221` (`integration-gaps.md:24`) | Rule quoted; "source read, item absent" separated from "source lost" (could not determine with `unscanned:`; nothing resolved, failed, unfrozen or retried). Matches. |
| AO-14 | RECOVERED | 3.1 "Co-location is not ownership" (`:367`); step 1.3 rule (iv) | `scope-04:222` (`integration-gaps.md:12`) | Quoted; path mapping feeds only the Worktree column. Matches. |
| AO-15 | RECOVERED | 3.1 "Peer attribution" (`:368`); step 1.3 rule (iv) | `06:99` (`[CLI]:161`), `:110` | Peer Owner prints "unknown" unless `linked: true`; never attributed by workspace membership. Matches. |
| AO-16 | RECOVERED | 3.1 "`worktree ps` coverage" (`:369`); step 1.4 rules (b)-(c); step 1.10 | `06:97` (`[H:worktree-ps]:3`, `:16-17`), `:109` | `not covered` host prints could not determine, never "no sessions"; `--limit` paging prints "at least <N>" (3 hits in the report; cut-page detection labelled new design). Matches. |
| AO-17 | RECOVERED | 3.1 "Recommendations only" (`:467`); step 1.15 (line 1266); step 1.17 closing sentence (line 1274); 9.4 row 98b (line 1666) | `06:138` (`[G]:156-161`) | The source position is quoted verbatim in all four places and set against steps 1.15/1.17 and #409 rule 5 as one owner decision, with the exact alternate WC-14 closing sentence if the owner adopts it. The finding asked for the conflict to be recorded, not for the steps to be removed. Done. |
| AO-18 | RECOVERED | 3.1 skeleton Scope line (`:429`) and "Counts name their scope and denominator" (`:454`); step 1.5; step 1.12 | `scope-04:67` (`integration-gaps.md:24`) | Scope line names any `--run`/window filter and its denominator; rule quoted; example wording labelled new design. Matches. |

Cycle-0 set: 18 RECOVERED, 0 JUSTIFIED, 0 OPEN.

## Adversarial search for new omissions

Stance: assume at least 5 more omissions exist. Sources scanned for operational rules the report might have dropped: `scope-01-contract.md:50-152`, `scope-02-orca-recovery.md:50-242` (rule table `:82-95`, failure modes `:111-124`, crash-recovery pieces `:126-139`), `scope-04-409-layout.md:55-353`, `06-orca-open-questions.md:60-174`, `research-notes.md:138-227`, and the `gaps-and-questions.md` GQ list (100 IDs; 19 not cited by ID in the report, each read by meaning). Every candidate was grepped in the report and, where hit, read in context.

| # | Candidate (source) | Report coverage found | Grade |
|---|---|---|---|
| N-1 | Print `scope.source` in the header (`scope-02:119`) | `:95` explains `scope.source`; step 1.6 (line 1247) always passes `--run` (default `run-current` binding, else every Run from `run-list`), so `scope.source` is always `flag` and the Scope line names the filter (AO-18) | MINOR: the meaning (scope stated) is kept by another route |
| N-2 | `worker-show` verdict outranks the list row for `missing_status` / `host_unavailable` / `capability_unsupported` (`scope-02:84`, UNVERIFIED) | `:111` and `:101`: the sweep reads liveness only from `worker-show`, one call per row, never from the list row; `:741` no PTY signal counts as proof | MINOR: moot under the chosen read path |
| N-3 | Never release on timeout, TUI idle, heartbeat, status, question, escalation or stale completion (`scope-02:93`, UNVERIFIED) | SC-5 (`:479`) "Absence never reads as death"; `:759` "Absence never authorizes stop, abandon, retry, or release"; safe-to-close is REVIEW only and needs the result read; the sweep never releases | MINOR: covered in meaning |
| N-4 | Report the row total against `page.total` (`scope-02:120`) | Paging on `page.nextCursor` stated at `:94`, `:544`, step 1.4 (line 1245); 100-row truncation rule (8 hits "truncated at 100"); no `page.total` comparison | MINOR: a cross-check, not a missing behaviour |
| N-5 | Executable failure: copy the error verbatim (`scope-02:124`) | 9.2 rows 13 (`:1551`) and 69 (`:1619`): "Copy the error verbatim" | Covered (Open Questions with resolution) |
| N-6 | Running-pipeline guard; Conflicts section that does not pick a side (`scope-02:137-139`) | `:258` (running-pipeline guard, A1 Reuse); `:147` (Conflicts section, "does not pick one"); `:993` | Covered |
| N-7 | `none` `nextAction`: read `liveness.reason` and keep waiting (`scope-02:87`) | `liveness.reason` 5 hits; terminal releasable needs `nextAction` `release`; sweep acts on nothing | Covered |
| N-8 | Placement map as the join of Tasks to worktrees (`scope-01:70`, `WORKER-CONTRACT.md:105`) | Named only in 2.x (`:63`); the design joins through Orca `terminal.worktreePath` (B-14 Worktree column, CODE-VERIFIED field) and Run id for Owner | MINOR: an alternative source in run notes and `worker-start --comment`; its absence leaves no class or column without a source. Worth one sentence in step 1.4 if the implementer wants a sole-writer cross-check |
| N-9 | The sweep must not stage `.dev/tasks` itself (`scope-01:59`) | The sweep runs no `git add` (read allowlist, step 1.4; SC-2); report written under `.dev/sweeps/`, not `.dev/tasks/`; `.dev/tasks/` never disposable (`:420`, `:505`) | Covered |
| N-10 | Routing row may name `/sc:sweep` only after `sweep.md` exists (`scope-01:115`) | Step 1.14 creates `sweep.md` before step 1.21 adds the row; step 1.21 adds only an "Other commands" row, ASCII only | Covered by step order |
| N-11 | Report stays local, never an issue comment (`scope-01:69`, rule 14) | WC-14 G7 "it is never posted" (line 1274), pinned in step 1.19 | Covered |
| N-12 | A worker blocked in `ask` sends no heartbeat (`research-notes.md:144`, `:57`) | "no heartbeat" 6 hits, `:57` cited 6 times | Covered |
| N-13 | `ccsession --list` excluded because it can write (`research-notes.md:179`) | 10 hits | Covered |
| N-14 | GQ-69 to GQ-82, GQ-87, GQ-88, GQ-90 to GQ-93 not cited by ID | Read each in `gaps-and-questions.md:92-116`. GQ-69 to GQ-82 are resolved gate fixes whose content is in the report (C13 verb form; Section C rules 2, 4; B-12/B-14 columns; read-only test SC-2; check modes excluded; lint gates step 1.26). GQ-87, 88, 90 to 93 are Minor wording or tag residuals in source files; GQ-90 (`filterLegacyPeekResult` on every peek) is moot because `check` is off the allowlist (`:476`) | Covered in meaning / MINOR |
| N-15 | Footer "source coverage is not fleet-wide assurance" and historical sessions section (`scope-04:74`, `:272`, `:302`) | 0 hits each | Already MINOR in cycle 0 (report 2 rows 15, 16); not rechecked as blocking |

New blocking omissions: none. The adversarial target of 5 was not met: the five strongest candidates (N-1, N-2, N-3, N-4, N-8) were each traced and the report keeps their meaning by another route or the rule is moot under the chosen design. None changes a class, a column source, a safety rule or a deliverable.

## MINOR notes (not blocking, not rechecked in later rounds)

- N-1 `scope.source` not printed; N-2 show-outranks-row rule not restated; N-3 weak-signal release list not restated as one list; N-4 no `page.total` cross-check; N-8 placement map not used as a join or sole-writer cross-check.
- The 30 cycle-0 MINOR rows stay as recorded in `qa-anti-omission-consolidated-findings.md`; not rechecked.

## Regression and monotonicity

- Regression check (run first): cycle-0 items outside F_0 still hold. `grep -c CONTRADICTION` = 6 and `grep -c NB-4` = 23, equal to the fix log baselines; report length 1760 lines as the fix log states. Steps 1.15 and 1.17 are present (AO-17 did not remove them). No item that passed at cycle 0 fails now. No regression.
- |F_0| = 18, |F_1| = 0. 0 < 18, so the monotonicity guard does not fire. Hard cap: this is fix cycle 1 of 2.

## Items that PASS

AO-01, AO-02, AO-03, AO-04, AO-05, AO-06, AO-07, AO-08, AO-09, AO-10, AO-11, AO-12, AO-13, AO-14, AO-15, AO-16, AO-17, AO-18 (all 18), plus the adversarial new-omission search (0 blocking found) and the regression check.

## Summary

- Checks: 20 (18 omissions, 1 adversarial search, 1 regression check). Passed 20, failed 0.
- Blocking open: |F_1| = 0. Critical 0, Important 0. MINOR notes: 5 new (above).
- Issues fixed in place: 0 (fix authorization false; the report was not edited).

**Confidence:** Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 8 | Grep: 2 | Glob: 1 | Bash: 16 (exact counts after this session's context compaction; before it, about 8 further Reads and 2 Grep/Bash batches of the findings, fix log, report 3.1-3.3 and steps 1.0a-1.12, `scope-01` and `scope-02`, exact count not retained). Read + Grep + Glob after compaction is 11, below the 20 checklist items; with the earlier calls it is about 21. Most per-item checks ran as grep batches inside Bash, which this count does not include. No web research.

## Verdict: PASS



