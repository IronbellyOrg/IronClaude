# Invariant Probe Results

## Round 2.5: Fault-Finder Analysis

Run by an independent general-purpose agent (sonnet class) that took no side in the debate. Checked against the repository; where it ran read-only probes the output is quoted.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | count_divergence | "Check the exit status first; non-zero means could not run" is safe for a paginated read | UNADDRESSED | MEDIUM | Probe with `gh api --paginate` and a `--jq` filter that fails on page 2: gh 2.103.0 printed `#849 https://x`, then `error: boom`, exit 1. A later-page failure leaves lines from earlier pages plus a non-zero exit, so the consensus rule would drop a proven blocker. Needs more than 30 blockers (default per_page 30). Refined rule: any line matching `^#[0-9]+ https://` stops the claim whatever the exit status |
| INV-002 | guard_conditions | "On exit 0 count only matching lines; anything else is could not run" covers every exit-0 output | UNADDRESSED | LOW | Mixed output on exit 0 is undefined by the rule; an object body exits 1 through the filter; multi-digit numbers are covered; origin_repo.py:18-21 accepts only github.com origins. Fix: any matching line wins (see INV-001) |
| INV-003 | state_variables | The held "could not run" line reaches the user even when a later STOP ends the claim | UNADDRESSED | MEDIUM | claim.md:138-150 (Final output is the only place); later STOPs at claim.md:55, 63, 93 and SKILL.md:150 do not route through it; Task 6 helper checks only that Final output has the line. Fix: a later STOP prints the held line before the STOP message, plus one Task 6 assertion |
| INV-004 | interaction_effects | The classification entry can be written in the same edit or after the final wording and will pass | UNADDRESSED | MEDIUM | Key is (path, verb, whole stripped line) incl. the "5. " prefix (test_worker_contract.py:1938-1958); a stale entry fails 3171-3176; the jq text `\(` must be `\\(` in a Python literal (ruff W605 selected at pyproject.toml:185; existing entry at test_worker_contract.py:2047 uses `\\(`); Task 6's lint criterion (plan line 92) names only test_issue_protocol.py while `make lint` is repo-wide (Makefile:48-50) |
| INV-005 | interaction_effects | The `## Final output` and Wave 2 wording traps are harmless Notes | UNADDRESSED | LOW | test_issue_orca_worktree.py:1788-1790 strict two-way split on "## Final output"; plan Task 1 text uses that notation; today the count is 1; test_issue_protocol.py:625 forbids the capitalised phrase |
| INV-006 | interaction_effects | Extending Final output item 4 and renumbering Wave 2 breaks no existing test | ADDRESSED | LOW | test_issue_protocol.py:612-618 (line containing "Every warning"), 639, 641; no test cites Wave 2 item numbers; `_wave` regex at 237-241 |
| INV-007 | interaction_effects | Keeping `gh api` out of SKILL.md, the command file and the guide is enough, and the plan states it | ADDRESSED | LOW | AUDIT_ROOTS covers skills, commands, agents (test_worker_contract.py:1886-1890); the guide is not scanned; gh_lines_missing_repo matches only `gh issue|pr|label` (test_issue_worker_agents.py:28, 45-62). The plan's Constraints do not state the rule yet (carry it into the plan) |
| INV-008 | interaction_effects | Task 4's guide-row wording is safe to copy from the issue text | UNADDRESSED | LOW | issue-summary.md:11 uses curly quotes; test_how_we_work_routing_table.py:329-334 requires ASCII; a `|` would break the table; no unknown `/sc:` token allowed (282-298) |
| INV-009 | collection_boundaries | Empty, single, many, closed and pull-request blockers are handled by the filter | ADDRESSED | LOW | Probes: issue 590 exit 0 empty; issue 612 one line; closed dropped by `select(.state == "open")`; cross-repo blockers the token cannot see are a residual gap outside the protocol |
| INV-010 | interaction_effects | A new E-BLOCKED STOP is safe for the issue watcher (out of scope in the plan) | UNADDRESSED | LOW | cli/issue_watch/launch.py:1-5, 112-131, 324; predicates.py:171-178, 327-341: an E-BLOCKED STOP leaves no assignee and no marker, like closed-issue STOPs; inference only: a blocked issue may be re-launched on each sweep. Out of scope by the issue's own text |
| INV-011 | guard_conditions | Orchestrator-run `gh api` in Wave 2 fits the lookup rule | ADDRESSED | LOW | claim.md:25 (worker first), claim.md:16-18 (orchestrator reads in Wave 0), claim.md:9 allows `repos/<R>/` paths; no test bans orchestrator reads in Wave 2 |
| INV-012 | sufficiency_challenge | The consensus fix set alone makes Task 6's acceptance criteria pass | ADDRESSED | LOW | Gates traced: test_worker_contract.py:1951-1958, 3167, 3171-3176, 3179-3185, 3188-3194; test_issue_protocol.py:936-938, 953-958, 664-698, 612-618; test_issue_orca_worktree.py:1788-1793; SKILL.md 197 lines; test_routing_plugin_parity.py:24-36. Sufficient for the acceptance criteria, not for correctness (INV-001, INV-003) |
| INV-013 | sufficiency_challenge | "Shows no new failure compared with the same run before Task 1" (plan line 91) can be evaluated | UNADDRESSED | LOW | No step captures the baseline run; plan line 37's grep criterion read literally can never pass because claim.md:9 names `gh api` without a path; should say "no new non-path `gh api` line" |

## Summary

- **Total findings**: 13
- **ADDRESSED**: 5 (INV-006, 007, 009, 011, 012)
- **UNADDRESSED**: 8
  - HIGH: 0
  - MEDIUM: 3 (INV-001, INV-003, INV-004)
  - LOW: 5 (INV-002, 005, 008, 010, 013)

No HIGH-severity UNADDRESSED item, so the invariant gate does not block convergence. The three MEDIUM items are logged as warnings and folded into the merged card.
