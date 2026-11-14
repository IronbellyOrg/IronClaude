# Reviewer 3 brief (model opus, persona refactorer)

Work unit (paths below relative to it): /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/
Audit scope only: research/, synthesis/, qa/, gaps-and-questions.md, RESEARCH-REPORT-orchestrator-mode.md, baseline-git-status.txt; tasklist+log = TASK-RESEARCH-orchestrator-supervision-20261107-073942.md. Owner-approved exceptions (NB-4 research-gate exception; Phase 6 anti-omission passed with exceptions, GQ-101/102/103 to /sc:design; the 4 ### Deviations entries) are Authorized/Necessary, not Drift.

## T1 card excerpt

#### (t1-card section) Structural / tech-debt

- **Citation hygiene:** Every `gaps-and-questions.md:NNN` citation in `REPORT` was checked. Row citations at or below line 123 still resolve, because the new rows went in after GQ-100: `:20` severity rule, `:22-70` GQ-01 to GQ-47, `:27` GQ-04, `:82` GQ-59, `:84` GQ-61, `:107` GQ-84, `:119` GQ-96. Only the `:125` count citation went stale (D-1). Pinning a moving summary line by number is fragile. A label citation ("the **Row count:** line") would survive later row additions.
- **Stale history notes, kept on purpose:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:580` ("row-count summary at `gaps-and-questions.md:125` (75 open, 25 resolved)") and `qa/qa-nb4-fix-log.md:39` are timestamped records and correct for their time. `RESEARCH-REPORT-orchestrator-mode.md:1758` ("43 files in `qa/`" as of assembly, against 88 now) says it is a snapshot, so it is acceptable, but a reader may take it as current.
- **Count drift:** "GQ-01 to GQ-100" stays at `REPORT:684`, `:1496` and `synthesis/synth-06-questions-evidence.md:6`, `:228` (D-3, D-4). The report header date is still 2026-11-07 (`REPORT:3`), though `:15` and `:1754` were edited on 2026-11-08 [INFERRED: no "updated" field exists].
- **Placeholders:** `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:466-488`: the Phase 1-6 Findings sections still read "(none yet)". The HALTs are logged in Phase Gate Findings instead, which item (e) at `:504` accepts.
- **Maintainability of the report:** At 1762 lines, the report repeats the gap-count statement in 7 places (`:229`, `:597`, `:1127`, `:1474`, `:1496`, `:1754`, plus `:684` coverage). That repetition is why one owner-approved edit left five stale copies. One authoritative count line, with the other places pointing to it, would stop a repeat of D-1.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-08T00:46:34Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode

### RESEARCH-REPORT-orchestrator-mode.md:1-9

```markdown
# Technical Research Report: Orchestrator mode Phase 1 (read-only /sc:sweep and WC-14), issue #339

**Date:** 2026-11-07
**Depth:** Deep
**Research files:** 8 codebase + 2 web research
**Scope:** `src/superclaude/core/`, `src/superclaude/skills/sc-crash-recovery/`, `src/superclaude/skills/ccsession-tag/`, `src/superclaude/cli/`, `src/superclaude/commands/`, `tests/`, `.dev/orca-command-refactor/inventory/`, the #409 package at `495eb96d` (`.dev/design/orca-observer-20261106/` on the unmerged branch `docs/409-orca-dashboard-designs`)
**Task folder:** `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/` (all `research/`, `synthesis/`, `qa/` and `gaps-and-questions.md` paths below are relative to it)

**Research question:** Orchestrator mode Phase 1 for issue #339: a read-only, coordinator-only `/sc:sweep` that classifies sessions (waiting on a person, working, stalled (proved), could not determine, finished, idle: the research question's six; Section C of `research/research-notes.md` adds fenced as a seventh class, `research/research-notes.md:188`, and six versus seven is an open question, Section 9; safe-to-close is a separate dimension) over a default 6 h window that bounds activity only, writes a dated static report on the #409 layout, and adds a WC-14 coordinator-loop rule to `src/superclaude/core/WORKER-CONTRACT.md`. `/sc:close`, resume, the trust layer, an orchestrator of orchestrators and the management-server relay are later phases, recorded only. Option A4 (extend sc-crash-recovery) is [CODE-CONTRADICTED] and appears only as a rejected option with its reason. (`synthesis/synth-01-problem-current-state.md:5`)
```

### RESEARCH-REPORT-orchestrator-mode.md:597-597

```markdown
| GQ-03 (NB-4): allowlist omitted read verbs | Fixed: `scope-03:99` now allows `task-list`, `run-list`, `run-current` and `gate-list`, and `inbox` stays forbidden | Pinned by SC-2 | Important (resolved) | `qa/qa-nb4-fix-log.md` edits 1-3. The summary line `gaps-and-questions.md:125` now reads Open 75 / Resolved 25. |
```

### RESEARCH-REPORT-orchestrator-mode.md:1127-1127

```markdown
| X-6 | Resolved, not a live conflict: `gaps-and-questions.md:125` reads "Open: 75. Resolved: 25" with GQ-03 counted as resolved | `gaps-and-questions.md:125` | None on the option choice |
```

### RESEARCH-REPORT-orchestrator-mode.md:1474-1474

```markdown
| X-6 | Resolved, not a live contradiction: the gap count at `gaps-and-questions.md:125` reads "Open: 75. Resolved: 25" with GQ-03 resolved | `gaps-and-questions.md:125`; synth-02 4.5 GQ-03 row | None needed; counts agree with synth-02 Section 4 |
```

### RESEARCH-REPORT-orchestrator-mode.md:1754-1758

```markdown
- `gaps-and-questions.md`: GQ-01 to GQ-103; 78 open, 25 resolved (`:125`). GQ-03 (NB-4) was resolved by the NB-4 fix pass and is re-checked at the Phase 5 synthesis gate. GQ-101 (NB-2) and GQ-102 (NB-4c) are the two open blocking findings of the Phase 6 anti-omission gate, carried by owner decision (2026-11-08) to /sc:design; GQ-103 carries the 3 blocking /ponytail-review findings.

### QA reports

Count as of report assembly (end of the Phase 5 synthesis gate): 43 files in `qa/`, listed in the three bullets below (24 + 18 + `qa-nb4-fix-log.md`). The Phase 6 report-lens files (`qa-lens-*`, `qa-consolidated-findings-phase6.md`, `qa-fix-log.md`) were written after assembly and are not counted.
```

### synthesis/synth-06-questions-evidence.md:6-13

```markdown
- `gaps-and-questions.md` (GQ-01 to GQ-100, sections (b) K1-K4, (c) AMBIGUITIES, (d) C1-C15, (e) per-file UNVERIFIED / CODE-CONTRADICTED claims, (f) stale docs S-01 to S-14)
- `research/research-notes.md`, `research/scope-01-contract.md`, `research/scope-02-orca-recovery.md`, `research/scope-03-cli-patterns.md`, `research/scope-04-409-layout.md`, `research/05-orca-row-schema.md`, `research/06-orca-open-questions.md`, `research/07-gate-gap-fill.md`
- `research/web-01-agent-supervisor-session-health.md`, `research/web-02-static-status-report-conventions.md` (external)
- `qa/qa-nb4-fix-log.md`

**NB-4 fix in effect:** GQ-03 (NB-4, the default argv allowlist) is resolved by the fix pass in `qa/qa-nb4-fix-log.md` (2026-11-07). It was a coordinator-approved exception at the Phase 3 research gate. The `scope-03:99` allowlist now includes `orchestration task-list` (`--ready`, `--run <id>`), `run-list`, `run-current` and `gate-list`; `inbox` stays forbidden.

**Gaps-file counts:** 75 open rows, 25 resolved (`gaps-and-questions.md:125`).
```

### synthesis/synth-01-problem-current-state.md:201-201

```markdown
GQ-03 (NB-4) is resolved. The summary counts at `gaps-and-questions.md:125` read "Open: 75. Resolved: 25" after the NB-4 fix, and state "Open blocking QA finding: none". scope-03 still writes `worker-list`, `worker-show` and `worker-read` without the `orchestration` prefix that C13 requires. Callers must spell the full `orca-ide orchestration <verb>` (`qa/qa-nb4-fix-log.md:41`).
```

### TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:466-470

```markdown
### Phase 1 Findings

(none yet)

### Phase 2 Findings
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| Obj 5: six synthesis files + synthesis gate (TASK:64) | C-05 | covered, gate PASS cycle 2 (TASK:527-528) | synthesis/synth-01..06, qa/qa-synthesis-*, qa/analyst-synthesis-* |
| Obj 6: assembled report, 10 sections; lens, fidelity, anti-omission gates (TASK:65) | C-06 | covered; lens PASS, fidelity PASS, anti-omission passed with exceptions (TASK:556) | RESEARCH-REPORT-orchestrator-mode.md:36,44,345,532,690,923,1096,1189,1531,1715; qa/qa-lens-*, qa/qa-fidelity-*, qa/qa-anti-omission-* |
| Obj 7: close-out, presentation, I17 validation, task summary (TASK:66, TASK:348-354) | C-07 | covered (7.1-7.4); 7.5-7.6 pending by design | synthesis/phase7-summary.md, TASK:366-376 |
| Report cross-file line citations to gaps log stay correct after GQ-101..103 were added | C-10 | partial (candidate drift) | RESEARCH-REPORT-orchestrator-mode.md:229 and :1754 cite `gaps-and-questions.md:125` for the row-count summary; that summary is now at gaps-and-questions.md:128 and :125 is the GQ-102 row; :229 also quotes "Open: 75" while :128 says "Open: 78" |
