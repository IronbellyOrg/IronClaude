# Merged Tier 2 review card: P0 live plan (UC-1 pre)

- Subject: `.dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/TASK-WF-writeTheP0LivePl-20261103-215902.md`
- Base: reviewer-1 (analyzer, sonnet, calibrated 0.87). Merged from reviewer-2 and reviewer-3 per `refactor-plan.md`.
- Verdict: **FAIL**. 2 blocking, 11 should-fix, 10 minor (23 findings). Full per-finding fields (claim, evidence, fix) are in `merged-verdict.yaml`; this card adds provenance and the cross-cutting rules.

## Cross-cutting rules for whoever revises the plan

1. Apply every fix before `/sc:implement` writes its first `T<id>: start` line. After that line any plan edit stops the run with `E-PLAN-CHANGED` (`~/.claude/skills/sc-implement-protocol/refs/managed-workspace.md:43`). This is why the Orca `--help` check (D-009) runs before the run, not in Task 1.
2. One invariant covers D-004, D-007 and D-008: at most one worktree and one worker per live check, ever. Resume, fix passes, repairs and retry attempts detect earlier progress from Orca state (`worktree list`, `worker-list --run`) and from `./artifacts/`, and only rebuild the record.
3. A worker parked on a human prompt or blocked on a question is not stopped on that signal alone (`.dev/orca-command-refactor/inventory/orca-capabilities.md:114`, `:125`, `:129`). Stop only on Orca's positive stall proof or the person's explicit go-ahead.
4. Fixing the two blocking findings is not enough to reach `archived` on a correct run: apply D-005 and D-006 in the same revision (invariant INV-007).

## Findings with provenance

| ID | Severity | Title | Sources | Base / merged from |
|---|---|---|---|---|
| D-001 | blocking | Post-archive `git add .dev/tasks` stages the superseded package | F-001, R1-01 | base |
| D-002 | blocking | Task 1 AC: "four untracked folders", five exist, no saved status | F-009, R1-10, R2-01, R3-05, F-010 | base + R2, R3 |
| D-003 | should-fix | Step 7 drops `--run` (Drift from spec:293) | F-004, R1-04, R3-04 | base + R3 |
| D-004 | should-fix | No exit for a parked, stalled or failed-to-start worker | F-003, R1-03, R3-08 | base + R3; stop rule rewritten (A-004) |
| D-005 | should-fix | FINAL may read intended failures as `issues` | F-002, R1-02 | base |
| D-006 | should-fix | End-state ACs with no saved evidence | F-010, R2-02, R3-06 | R2, R3 |
| D-007 | should-fix | Retry ladder would re-run a one-shot live check | R1-09, R3-09 | base + R3 |
| D-008 | should-fix | No resume rule | F-008, R1-08 | base |
| D-009 | should-fix | Unverified Orca flags; correction only before the run | F-005, R1-05, R3-03 | base; fix from R3 + X-001 |
| D-010 | should-fix | Branch-remaining name pattern | F-006, R1-06 | base (weak, inferred) |
| D-011 | should-fix | Workflow worker stages `.dev/tasks`; plan:22 overclaims | F-007, R1-07 | base |
| D-012 | should-fix | 240 s wait vs 120 s Bash timeout | F-013, R2-03 | R2 |
| D-013 | should-fix | Task 3 plan-file copy not in the evidence-copy step | R3-07 | R3 |
| D-014 | minor | `--base-branch` vs unpushed commit | R1-11 | base (weak; downgraded) |
| D-015 | minor | Absent `agentWait` passes vacuously | F-011, R2-04 | R2 |
| D-016 | minor | `grep -c` exit 1 on pass | F-012, R2-05, R1-12 | base + R2 |
| D-017 | minor | AC-0.6 transcript read not placed | F-014, R2-06 | R2 |
| D-018 | minor | `Worktree:` free-text slot | F-015, R3-01 | R3 |
| D-019 | minor | Procedure inside Constraints | F-017, R3-03 | R3 |
| D-020 | minor | Heartbeat fallback weakens spec:291 | R2-07 | R2 |
| D-021 | minor | `--report-path` match rule | R2-08 | R2 (weak) |
| D-022 | minor | AC-0.6 excerpt missing from phase report | R2-09 | R2 |
| D-023 | minor | Step-2 message handling; brief quoting | R1-12 | base |

Rejected: F-016 (Task 4 truly depends on Task 2, plan:35; R3-02).
