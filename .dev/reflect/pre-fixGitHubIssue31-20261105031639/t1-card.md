# T1 reflection card (UC-1, orchestrator-authored; hypothesis_source: inline)

- Spec (driving source): .dev/tasks/to-do/TASK-WF-fixGitHubIssue31-20261105-031410/source.md (one line)
- Tasklist: .dev/tasks/to-do/TASK-WF-fixGitHubIssue31-20261105-031410/TASK-WF-fixGitHubIssue31-20261105-031410.md (11 tasks, 5 phases)

## Coverage
- Parsed requirement IDs: 0. Inferred (Pass 2) rows: 17. coverage_pct_union 0.7059 by the deterministic containment rule; 5 rows unmatched by word containment: INF-007, INF-008, INF-014, INF-015, INF-016.
- Manual read of the five misses: INF-007 (safety net) is planned in Task 2 and Task 4 (ratio 0.59, just under the 0.6 threshold); INF-008 (30 s timer then auto-name) is planned in Task 2 and Task 4 (0.57); INF-014 (real pty runs, throwaway HOME) is in Task 7 and the plan Constraints (0.50); INF-015 (build on master, not the clayphi branch) and INF-016 (Coder out of scope) are only in the plan Constraints section, which the matcher does not read. These are matcher limits, not planned gaps. The matrix value is reported as computed.
- coverage_degraded: parsed-sparse (inferred 17 > parsed 0) forbids a Tier-1 stop; S_dev_density 0.2941 > 0.20 also escalates (rule 5).

## Candidate risks seen while reading (unverified; reviewers must confirm or reject)
- R1. Task 2 plans exit status 3 with the pasted text on stdout. ccsession-orca reads it with command substitution, which strips trailing newlines and cannot tell a message from a name by content; the plan keys on the exit status, which looks right, but multi-line text and NUL/escape bytes through `$(...)` and `read -r` need checking.
- R2. Task 2 detects a multi-line paste by "more bytes already waiting after the line", reusing the python `select` probe that needs line mode switched off; the existing probe is run once before the question. A second probe after `read` has a timing race (a paste may not have fully arrived).
- R3. Task 3 and Task 4 auto-name every non-interactive launch that carries a task (prompt-bearing, no terminal). Orchestrators that start many sessions will add many saved names; no cleanup or cap is planned.
- R4. Task 3 classifies `--session-id` as task-carrying and auto-names it. Passing both ccsession `--name` and Claude `--session-id` may conflict with the label/resume logic in ccsession (a saved label resumes by id).
- R5. Task 3 lifts a Claude `--name`/`-n` out of Orca's arguments into ccsession's `--name`; this changes today's behaviour (the value currently reaches Claude as-is and the question is still asked) and is not in the source text. It is listed in Constraints as a plan-author decision.
- R6. Print mode (`-p`/`--print`) and `CCSESSION_AUTOSTART=0` stay untagged by plan-author decision, also not in the source text.
- R7. Task 7 depends only on Task 5 and Task 8 only on Task 5; Task 6 depends on Task 5 while it tests behaviour added in Tasks 1 and 2. Ordering is valid but Task 6 and Task 7 are large single tasks.
- R8. The plan does not name src/superclaude/skills/ccsession-tag/SKILL.md or hooks/session-name.sh; whether an auto-named session is recorded in the saved-session list by the hook is only checked inside Task 7 (listed by `ccsession --here`).

## Calibration inputs
- Citation grounding: plan names real files and line regions taken from .dev/issues/315/analysis/analyze-ccsession-tag.md; none re-verified by the orchestrator beyond reading ccsession-orca and the ask_session_name region.
- Self-confidence (not used in routing; calibrator re-grades): 0.70
