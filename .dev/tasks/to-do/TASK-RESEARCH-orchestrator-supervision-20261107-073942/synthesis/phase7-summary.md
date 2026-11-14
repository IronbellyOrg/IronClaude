# Phase 7 Summary: Orchestrator mode Phase 1 research report (issue #339)

This file copies from the research report only. It adds no new claims. "Report line N" is the line in the report where the copied text sits.

## 1. Report location

`/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/RESEARCH-REPORT-orchestrator-mode.md` (1762 lines; dated 2026-11-07, depth Deep, report lines 3-4).

## 2. Key findings

- The worker contract has no rule that the coordinator keeps polling (G1), none to re-arm the wait after it expires (G2) and no periodic sweep (G3). "A grep for poll, re-arm, cron, sweep and expire matches only :45." Rules WC-2 to WC-13 exist and WC-1 is unused, so WC-14 is the next free ID. Evidence: `src/superclaude/core/WORKER-CONTRACT.md:45`; `research/scope-01-contract.md` G1-G7. (Report lines 48, 70.)
- WC-10: "a missing heartbeat is absence"; a sweep must "Act only on Orca's stall proofs; a late heartbeat never means stalled". Evidence: `src/superclaude/core/WORKER-CONTRACT.md:45`. (Report line 58.)
- The populated `worker-list` row schema has never been captured: "Until it is captured, plan for ceil(N/100) list calls plus N worker-show calls". Section 9 rates GQ-01 "Critical. The classifier cannot rely on list fields it has never seen." Evidence: `05-orca-row-schema.md:186`. (Report lines 1164, 1541.)
- Option A4 (extend sc-crash-recovery) is rejected as [CODE-CONTRADICTED]: crash-recovery says "pure read-only" (`SKILL.md:13,:155`), but `Bash(git stash *)` is allowed (`:4`); it also has scanner bugs at `bootstrap_scan.sh:31`, `:73`, `:136`. (Report lines 325, 1122.)
- The default argv allowlist at `scope-03:99` (NB-4 fix) "now includes `orchestration task-list` (`--ready`, `--run <id>`), `run-list`, `run-current` and `gate-list`; `inbox` stays forbidden." Evidence: `qa/qa-nb4-fix-log.md`. (Report line 13.)
- #409 offers "20 alternative designs, no direction chosen (`PKG/PLAN.md:62`); this research selected header, Attention Ledger and Shift Brief (#409's own picks differ, `PKG/concepts.md:45-49`)", and the #409 package is unmerged at `495eb96d`. (Report line 328.)
- External context: "'Unknown' is a first-class state, separate from unhealthy", applied as "'could not determine' stays its own class". Evidence: https://kubernetes.io/docs/reference/node/node-status/ ; https://github.com/grpc/grpc-proto/blob/master/grpc/health/v1/health.proto ; https://nagios-plugins.org/doc/guidelines.html (Report line 1148.)

## 3. Recommended option (Section 7)

Option A1. Quoted from report line 1098: "**Recommended option: A1.** It is a Python CLI `superclaude sweep` with a pure classifier and one probe module, called by a thin `/sc:sweep` command and the `sc-sweep-protocol` skill."

One-line rationale. Section 7 gives its rationale as a table (report lines 1100-1108), not as one sentence. The one-line statement of it is in the Section 6 effort note, report line 1092: "The recommendation does not rest on effort: A1 is chosen on K-4, K-5 and reuse (Section 7), and it accepts the highest effort as a trade-off." (K-4 is "mock-testable (hard requirement)" and K-5 is "argv allowlist (read-only safety)", report lines 1104-1105.)

## 4. Research file counts

- Codebase research files: 8. `research-notes.md`, `scope-01-contract.md`, `scope-02-orca-recovery.md`, `scope-03-cli-patterns.md`, `scope-04-409-layout.md`, `05-orca-row-schema.md`, `06-orca-open-questions.md`, `07-gate-gap-fill.md`.
- Web research files: 2. `web-01-agent-supervisor-session-health.md`, `web-02-static-status-report-conventions.md`.

How this was decided: a Glob of `research/*.md` in the task folder returned 10 files. Two names start with `web-`, and Section 5's "Inputs" line (report line 694) lists exactly those two as its web research. The other 8 are the files Section 10 lists under "Codebase Research" (report lines 1719-1730). The report header gives the same split, "8 codebase + 2 web research" (report line 5).

## 5. Open questions (Section 9)

How Section 9 counts: it does not print a total. It numbers its rows 1 to 109 across 9.1 to 9.5, plus 8 lettered sub-rows (33a, 81a, 81b, 81c, 81d, 98a, 98b, 98c), so 117 rows in all (report lines 1539-1685). Subsection 9.1 (rows 1-64 plus 33a) says "Every open GQ row is cited. Rows that share one resolution are grouped." (report line 1537). Some rows are marked settled rather than open: rows 7, 57, 106 and 109. Subsection 9.6 lists resolved rows separately (report lines 1687-1694). The gaps-log count that Section 10 copies is "GQ-01 to GQ-103; 78 open, 25 resolved (`:125`)" (report line 1754).

Highest impact: Section 9 marks four rows "Critical" (rows 1, 2, 3 and 5). Row 5 is the sweep feature itself (resolution: "Build `/sc:sweep` in Phase 1 as scoped."), so the three open questions quoted are rows 1, 2 and 3:

- Row 1 (report line 1541): "GQ-01 (G-A, C10): what is the full `worker-list --run <id> --json` row schema?" Impact: Critical. The classifier cannot rely on list fields it has never seen.
- Row 2 (report line 1542): "GQ-02 (G-B, C11): there is no non-consuming read of pending questions." Impact: Critical. "Waiting on a person" may be missed.
- Row 3 (report line 1543): GQ-04 (G1): how does WC-14 state "keep polling"? Impact: Critical. This is the coordinator duty the rule must carry.

## 6. Follow-up phases recorded but not designed

All five are listed together as "Out of scope for Phase 1 and recorded only" at report line 40 (and in the research question, report line 9). Each has its own row under "Later phases (recorded only, not designed)" (report line 1322). The phase numbers are "this report's, not a source's" (report line 1324).

- `/sc:close`: Phase 2, report line 1328.
- Resume: Phase 3, report line 1329.
- Trust layer: Phase 4, report line 1330.
- Orchestrator of orchestrators: Phase 5, report line 1331.
- Management-server relay: Phase 6, report line 1332.

## 7. Gate exceptions (report lines 13-15)

- Report line 13: "**NB-4 fix in effect:** GQ-03 (NB-4, the default argv allowlist) is resolved by the fix pass in `qa/qa-nb4-fix-log.md` (2026-11-07). It was a coordinator-approved exception at the Phase 3 research gate. The `scope-03:99` allowlist now includes `orchestration task-list` (`--ready`, `--run <id>`), `run-list`, `run-current` and `gate-list`; `inbox` stays forbidden. (`synthesis/synth-06-questions-evidence.md:11`)"
- Report line 15: "**Phase 6 anti-omission gate passed with exceptions, not clean:** the gate halted on its 2-fix-cycle limit (blocking findings 18 -> 1 -> 2, `[HALT-MONOTONICITY] |F|=2`) with two open blocking findings, and the owner chose (2026-11-08) to carry them as open Important gaps to be fixed at the /sc:design step, with no further fix pass. GQ-101 (NB-2): the step 1.3 one-package-in-two-worktrees pre-pass must count only packages actually running in a worktree, not committed folders every worktree shares (`src/superclaude/core/WORKER-CONTRACT.md:108`). GQ-102 (NB-4c): a package in both `to-do/` and `done/` is a fourth package state, conflict, that blocks removal (`~/.claude/skills/sc-crash-recovery/refs/pipelines.md:198`; `~/.claude/skills/sc-implement-protocol/SKILL.md:39`). Section 8 Phase 1 steps 1.2, 1.3, 1.8 and 1.9 are not yet corrected for either. A later /ponytail-review of the plan added three more blocking plan fixes, carried the same way as GQ-103 (`qa/ponytail-review-phase1-plan.md`). (`gaps-and-questions.md` GQ-101 to GQ-103)"
