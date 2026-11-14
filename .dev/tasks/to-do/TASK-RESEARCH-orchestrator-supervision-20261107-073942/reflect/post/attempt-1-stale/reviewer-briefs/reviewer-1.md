# Reviewer 1 brief (model sonnet, persona analyzer)

Work unit (paths below relative to it): /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/
Audit scope only: research/, synthesis/, qa/, gaps-and-questions.md, RESEARCH-REPORT-orchestrator-mode.md, baseline-git-status.txt; tasklist+log = TASK-RESEARCH-orchestrator-supervision-20261107-073942.md. Owner-approved exceptions (NB-4 research-gate exception; Phase 6 anti-omission passed with exceptions, GQ-101/102/103 to /sc:design; the 4 ### Deviations entries) are Authorized/Necessary, not Drift.

## T1 card excerpt

#### (t1-card section) Root-cause / deviations

### D-1: Gap-count citation `GAPS:125` and the "Open: 75" quote went stale after GQ-101 to GQ-103 were added

- **Location:** `RESEARCH-REPORT-orchestrator-mode.md:229`, `:597`, `:1127` (2 times), `:1474` (2 times), `:1496`, `:1754`
- **Mapped tasklist item:** Objective 6 (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:65`), and the owner decision that added GQ-101 to GQ-103 (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:556`)
- **Evidence:** `RESEARCH-REPORT-orchestrator-mode.md:229`: "The summary counts at `gaps-and-questions.md:125` read "Open: 75. Resolved: 25"". The actual text is now at `gaps-and-questions.md:128`: "**Row count:** 103 rows. Open: 78. Resolved: 25". `gaps-and-questions.md:125` is now the GQ-102 row.
- **Classification:** Drift
- **Rationale:** The owner-approved edit added three rows above the summary line and fixed only `REPORT:1754`'s numbers (78/25), not its line citation. Five other report sites still quote 75 open and cite `:125`. Undocumented and inaccurate. Nothing that passed before now fails, so it is not a Regression.
- **Severity:** important (6 sites in the report contradict the gaps log and `REPORT:1754`)
- **Default remediation:** In `REPORT`, change every `gaps-and-questions.md:125` / `` `:125` `` count citation to `:128`. Change "Open: 75" / "Open 75" to 78 at `:229`, `:597`, `:1127`, `:1474` and `:1496`, or mark each as the Phase 5 snapshot ("75 open before GQ-101 to GQ-103").

### D-2: Section 2 still says "Open blocking QA finding: none", which the gates left open

- **Location:** `RESEARCH-REPORT-orchestrator-mode.md:229`
- **Mapped tasklist item:** Check (7), report states nothing the gates left open as settled. Owner decision at `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:556`.
- **Evidence:** `RESEARCH-REPORT-orchestrator-mode.md:229`: "and state "Open blocking QA finding: none"". `gaps-and-questions.md:128`: "Open blocking QA finding: none at the research and synthesis gates; ... GQ-101 (NB-2) and GQ-102 (NB-4c) are open blocking findings".
- **Classification:** Drift
- **Rationale:** The quote drops the qualifier "at the research and synthesis gates". That makes the report say there are no open blocking findings. That contradicts `REPORT:15` and the anti-omission HALT (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:550-556`). The same unqualified wording comes from `synthesis/synth-01-problem-current-state.md:201` and `synthesis/synth-02-target-gaps.md:7`.
- **Severity:** important
- **Default remediation:** Rewrite the `REPORT:229` sentence to quote `GAPS:128` in full, or add "(research and synthesis gates; Phase 6 left GQ-101 and GQ-102 open, see :15)".

### D-3: Section 9 says it cites every open gap row, but GQ-101 to GQ-103 are missing; coverage tables stop at GQ-100

- **Location:** `RESEARCH-REPORT-orchestrator-mode.md:1537`, `:684`, `:1496`
- **Mapped tasklist item:** Objective 6 (10-section report, `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:65`); owner decision `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:556`
- **Evidence:** `RESEARCH-REPORT-orchestrator-mode.md:1537`: "Every open GQ row is cited." A grep for `GQ-10[123]` in `REPORT` hits only `:15` and `:1754`. `REPORT:684`: "Every row GQ-01 to GQ-100".
- **Classification:** Drift
- **Rationale:** The owner decision named only `:15` and `:1754` as the places to record the exception. It did not change Section 9's claim that it covers every open row. GQ-101 to GQ-103 are open Important plan blockers (`gaps-and-questions.md:124-126`), and the 117-row Section 9 has no row for them. /sc:design reads Section 9 as its open-questions input [INFERRED], so it would miss them there.
- **Severity:** important
- **Default remediation:** Add three 9.1 rows (GQ-101, GQ-102, GQ-103) pointing to `GAPS:124-126` and `REPORT:15`, and widen `:684` and `:1496` to "GQ-01 to GQ-103". If rows are added, update the Task Summary count of 117 (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:374`) and `synthesis/phase7-summary.md:34`.

### D-4: Synthesis files carry the same stale `:125` / "Open 75" statements

- **Location:** `synthesis/synth-01-problem-current-state.md:201`, `synthesis/synth-02-target-gaps.md:7`, `:230`, `synthesis/synth-04-options-recommendation.md:220`, `synthesis/synth-05-implementation-plan.md:261`, `:283`, `synthesis/synth-06-questions-evidence.md:6`, `:13`, `:228`
- **Mapped tasklist item:** Objective 5 (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:64`)
- **Evidence:** `synthesis/synth-02-target-gaps.md:7`: "its summary line `:125` reads Open 75 / Resolved 25 with no open blocking QA finding."
- **Classification:** Drift
- **Rationale:** These statements were correct when the synthesis gate passed them (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:527`). They are now wrong about the live gaps file, with no history note. Lower impact than D-1 because the report replaces the synthesis files as the deliverable.
- **Severity:** minor
- **Default remediation:** Add a one-line "snapshot as of the Phase 5 gate; see `GAPS:128`" note at the top of each synthesis file, or leave them as is and fix only `REPORT` (D-1).

### D-5: "Is re-checked at the Phase 5 synthesis gate" is still written as future, though the re-check already passed

- **Location:** `RESEARCH-REPORT-orchestrator-mode.md:1754`, `gaps-and-questions.md:128`
- **Mapped tasklist item:** Research-gate exception follow-through (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:521`, `:524`)
- **Evidence:** `RESEARCH-REPORT-orchestrator-mode.md:1754`: "GQ-03 (NB-4) was resolved by the NB-4 fix pass and is re-checked at the Phase 5 synthesis gate." `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:524`: "NB-4 re-check PASS 10 of 10."
- **Classification:** Drift
- **Rationale:** The wording is left over from before the gate ran. It does not change any outcome.
- **Severity:** minor
- **Default remediation:** Change it to "was re-checked at the Phase 5 synthesis gate (PASS, 10 of 10)".

### D-6: Counter labels in the fidelity cycle-2 verification are off by one from the task log

- **Location:** `qa/qa-fidelity-verification-cycle1.md:77`, `:79`
- **Mapped tasklist item:** Fidelity gate cycle control (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:540-542`)
- **Evidence:** `qa/qa-fidelity-verification-cycle1.md:77`: "Previously open blocking: |F_0| = 4 (C1-01 to C1-04)"; `:79`: "**|F_1| = 0**". The task log says `|F_1| = 4` and `|F_2| = 0` (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:540`, `:542`).
- **Classification:** Drift
- **Rationale:** The numbers agree (4 then 0) but the index labels do not. Every other gate's cycle-1 verifier uses the task log's indexing (for example `qa/qa-synthesis-verification-cycle1.md:68`). Cosmetic, with no effect on the verdict.
- **Severity:** minor
- **Default remediation:** None needed for the outcome. Optionally relabel to `|F_1| = 4`, `|F_2| = 0`.

### D-7: Research-gate pass-by-exception for NB-4

- **Location:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:519-521`, `:578`; `qa/qa-nb4-fix-log.md`; `RESEARCH-REPORT-orchestrator-mode.md:13`; `gaps-and-questions.md:7`
- **Mapped tasklist item:** Objective 3 (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:62`); item 182 precondition
- **Evidence:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:521`: "Research gate closed as PASS-BY-EXCEPTION at cycle 2 with 1 open blocking finding (NB-4); the exception is recorded in the final report."
- **Classification:** Authorized expansion
- **Rationale:** The coordinator approved it (msg_c2aed3001b18). `REPORT:13` states it accurately. The `|F|` sequence 28 -> 3 -> 1 matches `qa/qa-consolidated-findings-phase3.md:116`, `qa/qa-consolidated-findings-phase3-cycle1.md:15` and `qa/qa-research-verification-qualitative-cycle1.md:82`.
- **Severity:** minor
- **Default remediation:** None.

### D-8: Anti-omission gate passed with exceptions (NB-2, NB-4c as GQ-101 and GQ-102; ponytail-review findings as GQ-103)

- **Location:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:549-556`; `gaps-and-questions.md:124-126`; `RESEARCH-REPORT-orchestrator-mode.md:15`, `:1754`; `qa/ponytail-review-phase1-plan.md`
- **Mapped tasklist item:** Objective 6 anti-omission gate (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:65`)
- **Evidence:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:556`: "The anti-omission gate is passed with exceptions, not clean: it halted on the 2-cycle limit with 2 open blocking findings."
- **Classification:** Authorized expansion
- **Rationale:** The owner decided it (msg_5970c0dfc669). `REPORT:15` matches the log: "18 -> 1 -> 2", `[HALT-MONOTONICITY] |F|=2`, 2026-11-08, carried to /sc:design. The /ponytail-review file is an owner-requested addition outside the checklist. The related stale citations are D-1 to D-3.
- **Severity:** minor
- **Default remediation:** None beyond D-1 to D-3.

### D-9: Pointer prompts instead of retyped prompts for subagents

- **Location:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:577`
- **Mapped tasklist item:** Every agent-spawn item
- **Evidence:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:577`: "each subagent is given a pointer prompt ... instead of a retyped copy".
- **Classification:** Necessary deviation
- **Rationale:** Forced by the coordinator's context limits after the autocompact thrash, and documented. The agent reads the same instruction bytes from disk.
- **Severity:** minor
- **Default remediation:** None.

### D-10: WebSearch/WebFetch fallback for Tavily, and the rf-analyst re-run in Phase 4

- **Location:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:579`; `research/web-01-agent-supervisor-session-health.md`; `research/web-02-static-status-report-conventions.md`; `RESEARCH-REPORT-orchestrator-mode.md:1734`, `:1739`
- **Mapped tasklist item:** Objective 4 (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:63`)
- **Evidence:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:579`: "Tavily MCP tools are not available in this session, so both Phase 4 web items use the WebSearch/WebFetch fallback".
- **Classification:** Necessary deviation
- **Rationale:** An environment limit, documented in the log, in both output files and in report Section 10.
- **Severity:** minor
- **Default remediation:** None.

### D-11: NB-4 fix ran as its own pass between Phase 4 and Phase 5

- **Location:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:580`; `qa/qa-nb4-fix-log.md`
- **Mapped tasklist item:** Coordinator decision at `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:521`
- **Evidence:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:580`: "Phase 4 here is external research and synthesis is Phase 5. So the fix ran as one serialized rf-qa fix pass after Phase 4 and before Phase 5".
- **Classification:** Necessary deviation
- **Rationale:** It resolves a contradiction between the coordinator's wording and the phase numbering, and it is documented. The synthesis gate re-checked NB-4 and passed it 10 of 10 (`TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:524`).
- **Severity:** minor
- **Default remediation:** None.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-08T00:46:34Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode

### TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:509-521

```markdown
### Phase Gate Findings

Record here, per gate, the cycle number, `|F_n|`, the verdict, and any byte-exact halt message (`Regression detected on Item X.Y, previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` or `[HALT-MONOTONICITY] |F|=<n>`). Each gate (research gate, synthesis gate, lens QA, fidelity, anti-omission) keeps its own counter.

Research gate (own counter):
- Cycle 0 review (10 gate reports): |F_0| = 28, verdict FAIL.
- Fix pass 1 (qa/qa-research-fix-log.md) then verification: |F_1| = 3 (structural PASS 0; qualitative FAIL 3: NB-1/B-05, NB-2/B-13, NB-3 new), verdict FAIL.
- Cycle control after |F_1|: no regression (B-05 and B-13 also failed at cycle 0); monotonicity 3 < 28 OK; 1 of 2 fix cycles used. Starting repeat cycle 1 (second and last fix pass) from qa/qa-consolidated-findings-phase3-cycle1.md.

- Fix pass 2 (qa/qa-research-fix-log-cycle1.md) then verification: |F_2| = 1 (structural PASS 0; qualitative FAIL 1: NB-4 new, scope-03:99 allowlist omits orchestration task-list/run-list/run-current/gate-list used by research-notes.md:172,:197, 05:175, scope-04:330,:339,:345, 07:41-47), verdict FAIL.
- Cycle control after |F_2|: no regression (qualitative report: no previously PASS item fails); monotonicity 1 < 3 OK; hard cap reached (2 fix cycles, 3 reviews). HALT. Open blocking finding escalated: NB-4 (full text and required fix at qa/qa-research-verification-qualitative-cycle1.md:42). MINOR notes stay as notes. Phase 4 not started.

- Coordinator decision 2026-11-07T20:05Z (reply to escalation msg_c2aed3001b18): proceed. NB-4 is carried into gaps-and-questions.md as an open Important gap; its spelled-out fix (add orchestration task-list, run-list, run-current, gate-list to the scope-03:99 default allowlist; keep inbox forbidden) is applied during Phase 4 synthesis and re-checked by the Phase 5 synthesis gate. Research gate closed as PASS-BY-EXCEPTION at cycle 2 with 1 open blocking finding (NB-4); the exception is recorded in the final report.
```

### TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:549-556

```markdown
- Cycle 2 (`qa/qa-anti-omission-verification-cycle1.md` PASS, `qa/qa-anti-omission-verification-qualitative-cycle1.md` FAIL): |F_2| = 2, verdict FAIL. Regression check: no item that passed at cycle 1 now fails (AO-01 to AO-18 and NB-1 stay RECOVERED; the two findings below are new). Monotonicity check:
- [HALT-MONOTONICITY] |F|=2
- Fix-cycle cap also reached (2 fix cycles, 3 reviews). Open blocking findings:
  - NB-2 (IMPORTANT): the fix-pass-2 pre-pass `mark_shared_packages` flags a package as "one package in two worktrees" when its folder is found under `.dev/tasks/{to-do,done}/*/` in two worktrees. Those folders are committed, so every worktree branched from master holds the same ones (master today: 44 folders in `to-do/`, 26 in `done/`); a live sweep would mark nearly every worktree "removable: no". The source rule (`WORKER-CONTRACT.md:108`) is about running a package in two worktrees, not its folder being present. The step 1.8 fixture uses two synthetic records, so the tests would pass while live output is wrong. Required fix: count only packages being run in a worktree (for example a package whose ledger or folder differs from the base branch), ignore unchanged committed packages, and let the Retained problems line name more than two worktrees; add a fixture of two worktrees that share unchanged committed packages and assert no flag.
  - NB-4c (IMPORTANT): a package present in both `to-do/` and `done/` is a conflict to report (`sc-crash-recovery/refs/pipelines.md:198`; stop code `E-MANAGED-CONFLICT`, `sc-implement-protocol/SKILL.md:39`). Neither the research files nor the report name it; the plan would produce two rows and the `done/` copy could read as finished, hiding the conflict. Required fix: add "conflict" as a fourth package state that blocks removal, with a step 1.8 fixture and a step 1.9 test.
- MINOR notes carried to the plan stage: structural cycle-2 N-1 to N-5; qualitative cycle-2 NB-3 (rule (ii) context-only Dispatch never fires on live rows until the marking field is captured; no Open Questions row for capturing it) and "JSON output carries no package states"; earlier M-1 to M-6 and the 5 structural cycle-1 notes.
- anti-omission gate HALTED at cycle 2; escalated to the coordinator (run:run_93bfa00cae2b). Item 340 stays unchecked until the coordinator answers.
- Owner decision (coordinator msg_5970c0dfc669, 2026-11-08T00:38Z): carry NB-2 and NB-4c as open Important gaps (gaps-and-questions.md GQ-101, GQ-102) to be fixed at the /sc:design step; no further fix pass and no fourth review. The anti-omission gate is passed with exceptions, not clean: it halted on the 2-cycle limit with 2 open blocking findings. Recorded in the report (exception paragraph after the NB-4 note near :15, Gaps Log bullet near :1754). The 3 blocking /ponytail-review findings (qa/ponytail-review-phase1-plan.md) are carried the same way as GQ-103.
```

### TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:575-580

```markdown
### Deviations

- 2026-11-07T18:58Z, executor (all agent-spawn items): to stay inside the coordinator's context rules after the 18:11 autocompact thrash, each subagent is given a pointer prompt ("your instructions are the quoted prompt in item N.M at line L of this task file; follow it exactly") instead of a retyped copy, and asked to reply with only its output path and verdict. The agent reads the same bytes from disk, so the instructions it follows are unchanged.
- 2026-11-07T20:10Z, executor (items 180-182, Phase 4-5): the research gate hit the 2-fix-cycle cap with 1 open blocking finding (NB-4, qa/qa-research-verification-qualitative-cycle1.md:42). Coordinator authorized proceeding (reply to msg_c2aed3001b18): NB-4 carried as an open Important gap in gaps-and-questions.md, its fix applied in Phase 4 synthesis, re-checked by the Phase 5 synthesis gate, and the exception stated in the final report. Item 182's 'after the gate is PASS' precondition is satisfied by this exception. Cycle-file naming: the repeat cycle after the Step 3.2 fix pass used suffix -cycle1 (|F_1|=3), and its verification files -cycle1, matching item 180's 'cycle N (1 or 2)' wording.
- 2026-11-07T20:19Z, Phase 4: Tavily MCP tools are not available in this session, so both Phase 4 web items use the WebSearch/WebFetch fallback, which each output file records. The `deep-research` agent type has no Write tool: item 192's first run wrote nothing and was re-run as `rf-analyst`; item 196's agent returned the full file in its reply, and the executor saved it unchanged to `research/web-02-static-status-report-conventions.md` (the file carries a provenance note).
- 2026-11-07T20:24Z, NB-4 fix: the coordinator said to apply NB-4's fix "during Phase 4 synthesis", but Phase 4 here is external research and synthesis is Phase 5. So the fix ran as one serialized rf-qa fix pass after Phase 4 and before Phase 5 (log `qa/qa-nb4-fix-log.md`, 3 edits). The `inbox` reason was copied from `07:92` and `06:161` because scope-03 gave none. The executor corrected the row-count summary at `gaps-and-questions.md:125` (75 open, 25 resolved). The Phase 5 synthesis gate must re-check NB-4.
```

### RESEARCH-REPORT-orchestrator-mode.md:13-15

```markdown
**NB-4 fix in effect:** GQ-03 (NB-4, the default argv allowlist) is resolved by the fix pass in `qa/qa-nb4-fix-log.md` (2026-11-07). It was a coordinator-approved exception at the Phase 3 research gate. The `scope-03:99` allowlist now includes `orchestration task-list` (`--ready`, `--run <id>`), `run-list`, `run-current` and `gate-list`; `inbox` stays forbidden. (`synthesis/synth-06-questions-evidence.md:11`)

**Phase 6 anti-omission gate passed with exceptions, not clean:** the gate halted on its 2-fix-cycle limit (blocking findings 18 -> 1 -> 2, `[HALT-MONOTONICITY] |F|=2`) with two open blocking findings, and the owner chose (2026-11-08) to carry them as open Important gaps to be fixed at the /sc:design step, with no further fix pass. GQ-101 (NB-2): the step 1.3 one-package-in-two-worktrees pre-pass must count only packages actually running in a worktree, not committed folders every worktree shares (`src/superclaude/core/WORKER-CONTRACT.md:108`). GQ-102 (NB-4c): a package in both `to-do/` and `done/` is a fourth package state, conflict, that blocks removal (`~/.claude/skills/sc-crash-recovery/refs/pipelines.md:198`; `~/.claude/skills/sc-implement-protocol/SKILL.md:39`). Section 8 Phase 1 steps 1.2, 1.3, 1.8 and 1.9 are not yet corrected for either. A later /ponytail-review of the plan added three more blocking plan fixes, carried the same way as GQ-103 (`qa/ponytail-review-phase1-plan.md`). (`gaps-and-questions.md` GQ-101 to GQ-103)
```

### RESEARCH-REPORT-orchestrator-mode.md:229-229

```markdown
GQ-03 (NB-4) is resolved. The summary counts at `gaps-and-questions.md:125` read "Open: 75. Resolved: 25" after the NB-4 fix, and state "Open blocking QA finding: none". scope-03 still writes `worker-list`, `worker-show` and `worker-read` without the `orchestration` prefix that C13 requires. Callers must spell the full `orca-ide orchestration <verb>` (`qa/qa-nb4-fix-log.md:41`).
```

### RESEARCH-REPORT-orchestrator-mode.md:1537-1537

```markdown
Every open GQ row is cited. Rows that share one resolution are grouped.
```

### RESEARCH-REPORT-orchestrator-mode.md:1754-1754

```markdown
- `gaps-and-questions.md`: GQ-01 to GQ-103; 78 open, 25 resolved (`:125`). GQ-03 (NB-4) was resolved by the NB-4 fix pass and is re-checked at the Phase 5 synthesis gate. GQ-101 (NB-2) and GQ-102 (NB-4c) are the two open blocking findings of the Phase 6 anti-omission gate, carried by owner decision (2026-11-08) to /sc:design; GQ-103 carries the 3 blocking /ponytail-review findings.
```

### gaps-and-questions.md:124-128

```markdown
| GQ-101 | NB-2 (Phase 6 anti-omission gate): the report's one-package-in-two-worktrees pre-pass (step 1.3 rule (i), `mark_shared_packages`) counts committed `.dev/tasks/{to-do,done}/*/` folders, which every worktree shares (master has 44 to-do and 26 done folders), so nearly every worktree would be flagged not removable. The source rule is about a package being run in two worktrees. | Important | `src/superclaude/core/WORKER-CONTRACT.md:108`; `qa/qa-anti-omission-verification-qualitative-cycle1.md` NB-2 | open (plan, fix at /sc:design) | Owner decision 2026-11-08: carried as an open gap, no further fix pass. Fix at /sc:design: count only packages actually running in a worktree (a ledger or folder that differs from the base branch), ignore unchanged committed packages, let the line name 3 or more worktrees, and add a shared-folders fixture asserting no flag. |
| GQ-102 | NB-4c (Phase 6 anti-omission gate): a package folder present in both `to-do/` and `done/` is a conflict state; the report's package states (step 1.2 `archive_states`, step 1.3 rule (iii)) lack it | Important | `~/.claude/skills/sc-crash-recovery/refs/pipelines.md:198`; `~/.claude/skills/sc-implement-protocol/SKILL.md:39` (`E-MANAGED-CONFLICT`); `qa/qa-anti-omission-verification-qualitative-cycle1.md` NB-4c | open (plan, fix at /sc:design) | Owner decision 2026-11-08: carried as an open gap, no further fix pass. Fix at /sc:design: add "conflict" as a fourth package state that blocks worktree removal, plus a fixture and a test. |
| GQ-103 | /ponytail-review of the Phase 1 plan (owner request, 2026-11-08), 3 blocking: (1) plain `git status` can take a worker's `index.lock`, and WC-9 tells a worker that finds it to report `blocked`; (2) `classify` is not given the `--window` value; (3) the step 1.2 types lack fields the rule-1 and GQ-84 tests read (brief blocked-gate policy, `worker_done`, transcript readable, contract `report_path` / `artifacts`) | Important | `qa/ponytail-review-phase1-plan.md` findings 1-3; `src/superclaude/core/WORKER-CONTRACT.md:44` (WC-9 `index.lock`) | open (plan, fix at /sc:design) | Fix at /sc:design: run every `_git` call with `--no-optional-locks`; pass the window into `classify`; add the missing fields. The review's 7 minor findings (4-10) stay in the review file as plan notes. |

**Row count:** 103 rows. Open: 78. Resolved: 25 (GQ-03, 07, 13, 18, 20, 42, 45, 55, 68-83, 96). GQ-40 is counted as open although its sweep-side rule is settled. Open Critical: GQ-01, GQ-02, GQ-04, GQ-06. Open blocking QA finding: none at the research and synthesis gates; GQ-03 (NB-4) was fixed by the NB-4 fix pass (`qa/qa-nb4-fix-log.md`) and is re-checked at the Phase 5 synthesis gate. Phase 6 anti-omission gate: GQ-101 (NB-2) and GQ-102 (NB-4c) are open blocking findings carried by owner decision to /sc:design; GQ-103 adds the 3 blocking /ponytail-review findings.
```

### synthesis/synth-02-target-gaps.md:7-7

```markdown
**State of the inputs at synthesis:** NB-4 is fixed. The `scope-03:99` default Orca read allowlist now includes `orchestration task-list`, `run-list`, `run-current` and `gate-list`, and `inbox` stays forbidden (`qa/qa-nb4-fix-log.md` edits 1-2). `gaps-and-questions.md:26` marks GQ-03 resolved, and its summary line `:125` reads Open 75 / Resolved 25 with no open blocking QA finding.
```

### qa/qa-fidelity-verification-cycle1.md:75-80

```markdown
## Gate arithmetic

- Previously open blocking: |F_0| = 4 (C1-01 to C1-04)
- Resolved: 4. Still open: 0. New blocking: 0.
- **|F_1| = 0**
- Regression check (step 1): no item that passed earlier now fails. Monotonicity (step 2): 0 < 4, no halt. Hard cap (step 3): this is the third and last review; nothing is left to escalate.
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| Obj 3: research gate, 2 fix cycles, gaps file (TASK:62) | C-03 | covered by exception (NB-4, TASK:521, TASK:578) | qa/qa-research-*, qa/qa-consolidated-findings-phase3*.md, qa/qa-nb4-fix-log.md, gaps-and-questions.md |
| Obj 6: assembled report, 10 sections; lens, fidelity, anti-omission gates (TASK:65) | C-06 | covered; lens PASS, fidelity PASS, anti-omission passed with exceptions (TASK:556) | RESEARCH-REPORT-orchestrator-mode.md:36,44,345,532,690,923,1096,1189,1531,1715; qa/qa-lens-*, qa/qa-fidelity-*, qa/qa-anti-omission-* |
| Read-only constraint: no file outside task folder changed (TASK:56, TASK:352(f)) | C-08 | covered | baseline-git-status.txt:1-3 equals `git status --porcelain` at 2026-11-08T00:47Z (3 identical untracked entries) |
| Owner exceptions GQ-101/102/103 recorded in report and gaps log (TASK:556) | C-09 | covered | RESEARCH-REPORT-orchestrator-mode.md:15, :1754; gaps-and-questions.md:124-128 |
| Report cross-file line citations to gaps log stay correct after GQ-101..103 were added | C-10 | partial (candidate drift) | RESEARCH-REPORT-orchestrator-mode.md:229 and :1754 cite `gaps-and-questions.md:125` for the row-count summary; that summary is now at gaps-and-questions.md:128 and :125 is the GQ-102 row; :229 also quotes "Open: 75" while :128 says "Open: 78" |
