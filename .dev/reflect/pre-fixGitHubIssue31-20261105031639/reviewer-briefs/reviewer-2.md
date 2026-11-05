# Reviewer 2 brief (persona: qa; model class: haiku)

You are a read-only Tier-2 reviewer for a UC-1 (pre-execution) reflection. Audit whether the proposed tasklist covers the driving spec. You may Read, Grep and Glob; you may not run commands or edit files. RETURN your card as the final message (YAML, format at the end); do not write files. Tag every claim Grounded (with a `file:line` you actually Read) or `[INFERRED]`. Drop claims you can tag neither way. Start from an adversarial position: assume the plan drops requirements and look for them.

Driving spec: .dev/tasks/to-do/TASK-WF-fixGitHubIssue31-20261105-031410/source.md (one long line)
Tasklist: .dev/tasks/to-do/TASK-WF-fixGitHubIssue31-20261105-031410/TASK-WF-fixGitHubIssue31-20261105-031410.md
Persona lens: coverage and acceptance. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Then check that every task's acceptance criteria are observable and that the tests named would fail if the behaviour broke.

## T1 card excerpt

- Parsed requirement IDs: 0. Inferred (Pass 2) rows: 17. coverage_pct_union 0.7059 by the deterministic containment rule; 5 rows unmatched by word containment: INF-007, INF-008, INF-014, INF-015, INF-016.
- Manual read of the five misses: INF-007 (safety net) is planned in Task 2 and Task 4 (ratio 0.59, just under the 0.6 threshold); INF-008 (30 s timer then auto-name) is planned in Task 2 and Task 4 (0.57); INF-014 (real pty runs, throwaway HOME) is in Task 7 and the plan Constraints (0.50); INF-015 (build on master, not the clayphi branch) and INF-016 (Coder out of scope) are only in the plan Constraints section, which the matcher does not read.
- R3. Task 3 and Task 4 auto-name every non-interactive launch that carries a task (prompt-bearing, no terminal). Orchestrators that start many sessions will add many saved names; no cleanup or cap is planned.
- R7. Task 7 depends only on Task 5 and Task 8 only on Task 5; Task 6 depends on Task 5 while it tests behaviour added in Tasks 1 and 2. Ordering is valid but Task 6 and Task 7 are large single tasks.
- R8. The plan does not name src/superclaude/skills/ccsession-tag/SKILL.md or hooks/session-name.sh; whether an auto-named session is recorded in the saved-session list by the hook is only checked inside Task 7 (listed by `ccsession --here`).

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-05T03:16Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-315-ccsession-name-prompt projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-315-ccsession-name-prompt (the index holds python and yaml only; ccsession and ccsession-orca are bash, so use Read and Grep for them)

### .dev/tasks/to-do/TASK-WF-fixGitHubIssue31-20261105-031410/source.md:1-1
Whole file (it is one line; Read it, it is the spec body). Its requirement-bearing spans, in order: one naming-question rule; unique valid auto-name for every launch without a name (timeout, Enter, keys typed ahead, no terminal, prompt-bearing); a 30-second timer inside ask_session_name for every caller; Ctrl+C exits 130 with no Claude start and ccsession-orca stops trapping INT; keep the PR 355 reopen ahead of the question; decision (a) CCSESSION_NAME and the narrow safety net, 30 s timer with auto-name as last backstop; decision (b) Agent Teams documented exception and follow-up; Enter gets an auto-name; Coder bare claude entry and New Terminal hook out of scope; add --fork-session and --session-id to the launch-carries test or fix README drift; update README.md, CHANGELOG.md Unreleased, D08 guide; update tests in test_ccsession_tag.py and test_ccsession_tiers.py (three named tests); real pty runs of every launch path in a throwaway HOME; build on master, never on the clayphi branch; Coder out of scope.

### .dev/reflect/pre-fixGitHubIssue31-20261105031639/artifacts/coverage-matrix.md:1-30
Read it: the deterministic Pass 2 matrix (17 INF rows, best task and ratio per row).

### Verification surface in the repo
Read tests/unit/test_ccsession_tag.py lines 1305-1480 (helpers `_orca_env`, `_orca_tty`, `_orca_no_tty`, `_spawn_on_pty`, constant `ORCA_QUESTION`) and the Orca tests at 1485-1703 that the plan says must change.

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-001 one question rule | Task 3 | covered | plan Task 3 |
| INF-002 unique valid auto-name | Task 1, Task 4 | covered | plan Tasks 1, 4 |
| INF-005 keep the 355 reopen first | Task 3 | covered | plan Task 3 |
| INF-006 CCSESSION_NAME | Task 3 | covered | plan Task 3 |
| INF-009 Agent Teams exception | Task 9 | covered | plan Task 9 |
| INF-011 --fork-session / --session-id or README drift | Task 3, Task 9 | covered | plan Tasks 3, 9 |
| INF-012 README, CHANGELOG, D08 | Task 9, Task 10 | covered | plan Tasks 9, 10 |
| INF-013 tests in two files | Task 5 to 8 | covered | plan Tasks 5 to 8 |
| INF-014 pty runs per launch path | Task 7 | covered | plan Task 7 |

## Card format to return

```yaml
reviewer: 2
persona: qa
findings:
  - id: F1
    claim: <one sentence>
    tag: grounded | inferred
    evidence: <file:line you Read, or null when inferred>
    severity: blocking | minor      # blocking = a spec requirement has no task, or an acceptance criterion cannot be observed or would pass when the behaviour is broken
    deviation_class: authorized | necessary | drift | regression | none
    recommendation: <file + change + how to verify>
matrix_gaps: [<spec spans absent from the matrix, quoted verbatim, or empty>]
verdict: ready | ready-with-notes | not-ready
self_confidence: <0.0-1.0>
```
