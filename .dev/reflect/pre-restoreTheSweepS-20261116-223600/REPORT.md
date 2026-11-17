```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 1
confidence_calibrated: 0.80   # UNVERIFIED by a blind calibrator agent: none was spawned (see Run limits)
citations_total: 9
citations_revalidated: 9
citations_dropped: 0
citations_inferred: 1
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

# Pre-execution reflection: sweep working-class restore plan

Spec: `.dev/tasks/to-do/TASK-WF-restoreTheSweepS-20261116-223216/source.md`
Tasklist: `.dev/tasks/to-do/TASK-WF-restoreTheSweepS-20261116-223216/TASK-WF-restoreTheSweepS-20261116-223216.md`

## Run limits (read first)

This was a bounded Tier 1 pass by the orchestrating session, not the full protocol. The spec has no labeled requirement IDs, so the parse-density guard (`coverage_degraded: parsed-sparse`) requires Tier 2 (heterogeneous reviewers plus adversarial merge). Tier 2, the blind calibrator and the evidence-validator agent were NOT run, so `status` is `partial` and the confidence figure is the orchestrator's own estimate. This report is advisory and changed nothing in the plan.

## Coverage matrix (Pass 2, inferred requirements; no labeled IDs exist)

| INF id | Requirement (quote, source.md) | Task |
|---|---|---|
| INF-001 | "parse_worker_show must read agentWait presence and value from result.observation.agentWait, falling back to result.terminal.agentWait" | Task 2 |
| INF-002 | "_rule_working (rule 5) must match only when liveness_verdict == live, outcome == in_progress ..., agent_wait_present is True and agent_wait is None" | Task 3 |
| INF-003 | "a non-null agentWait stays rule 4 waiting and never working" | Task 3 (tests) |
| INF-004 | "classify.py:245 orca.status == ready is NOT a mismatch ... so leave it" | Constraints, Task 3 acceptance, Task 5 note |
| INF-005 | "update models.py reserved-field comments, docs/designs/orchestrator-mode.md (...)" | Task 2, Task 5 |
| INF-006 | "mark non-null agentWait meaning UNVERIFIED" | Tasks 2, 3, 5 |
| INF-007 | "update tests pinning the stub (...) and add tests built from a sanitized fixture" | Tasks 1, 2, 3, 4 |
| INF-008 | "sweep stays read-only, no new Orca command in the allow list, no change to INV-008 git protections, edit src/superclaude only, no push or PR" | Constraints, Task 2 and Task 5 acceptance |
| INF-009 | "Verify with uv run pytest tests/sweep -q and uv run ruff check ..." | Task 5 acceptance |

All nine inferred requirements map to at least one task. Coverage over the inferred union: 9 of 9.

## Findings

Grounded (each re-read against the repository on 2026-11-16):

- The plan's field names match the real code: `parse_worker_show` sets `status` from `dispatch.status` and `outcome` from `projection.outcome` (src/superclaude/cli/sweep/probes.py:479-480), `agent_wait`, `agent_wait_present`, `agent_wait_since` exist (src/superclaude/cli/sweep/models.py:98-110), and `_rule_working` is the stub (src/superclaude/cli/sweep/classify.py:251-257).
- The `ready` question is closed correctly: the sweep sets `status="ready"` itself for `task-list --ready` rows (src/superclaude/cli/sweep/probes.py:1244) and tests it at classify.py:245 and report.py:148.
- The existing fixtures `captured-worker-show-1..5.json` carry no `agentWait` key and all show `exited`, so none of them can become `working` after the change.
- No other caller of `parse_worker_show` exists outside `_run_rows` and tests (codegraph, nine callers; def-line rows).

Medium (follow-up candidates, none blocks the plan):

- Task 4 asserts "the recorded argv list contains no template outside ALLOWED_ORCA"; whether the `env` fixture of tests/sweep/test_cli_contract.py records argv was not checked. The executor must read the fixture first; if it records nothing, drop that bullet and rely on tests/sweep/test_probes_allowlist.py.
- Task 3 lists test line numbers (524, 537, 642, 660, 1065) from a pre-change read; they may shift. The task already says to check every live and in_progress case, so no plan change is needed.

[INFERRED] The report footnote constant `SP24` stays correct because stalled and fenced remain unobserved; no test was run to confirm that nothing else in the report text says working is unobserved (a Grep of report.py found no such sentence).

## Owner decisions

None found. The plan treats a non-null `agentWait` as rule 4 (waiting on a person), which is the behavior the code already has; its real shape stays UNVERIFIED.
