# Cross-Validation Report: sweep architecture

- **Date:** 2026-11-23
- **Claims verified:** 5
- **Command:** /sc:analyze src/superclaude/cli/sweep --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g1/339/analyze
- **Template:** installed analyst-cross-validation_report_template.md, extended with analysis sections required by the command.
- **Codegraph:** index_state=fresh, checked_at=2026-11-23T23:02:12Z; degraded: graph:truncated

## Scope and metrics
Quick static pass on the six Python files in `src/superclaude/cli/sweep/`, with coordinator-contract and closeout-command boundary checks. This is the narrow implemented package covering the session-state collection and reporting part of issue 339; the wider orchestrator has no single implementation package.

Separation: CLI validation/publication (`commands.py`), models (`models.py`), bounded input reads (`probes.py`), classification and joins (`classify.py`), presentation (`report.py`) and package export (`__init__.py`). The entry point at `commands.py:269-277` runs collect, classify, render and publish in order. Codegraph found the production CLI caller plus test callers; the caller response showed 10 of 17, so it is not exhaustive. Checkout: a7ae3dd30fcf88aaab655c37e94e58e121c2d863.

## Validation Results
| # | Claim | Source | Code Path Checked | Verdict | Notes |
|---|-------|--------|-------------------|---------|-------|
| 1 | The six-hour sweep exists, but only reads and reports. | Issue 339; PR 539 | `commands.py:27,214-288`; `probes.py:49-80` | VERIFIED | The sole CLI subcommand is run; it collects, classifies and publishes, with no resume/remove dispatch in this flow. |
| 2 | Safe-to-close means removal is authorized. | Original issue's requested action phase | `classify.py:455-504` | CONTRADICTED | The checks refuse unsafe conditions, otherwise return could-not-determine, never yes. Open PRs and report admission are not observable here. |
| 3 | The working class is still inert. | Older issue comments and user-guide limit | `classify.py:251-269` | CONTRADICTED | Live + in-progress + observed null agentWait now yields working; PR 579 is merged. A non-null wait still lacks a captured example. |
| 4 | Large/restarted Runs are fully described. | Goal of supervising all sessions | `probes.py:89,124-167`; `classify.py:272-291` | CONTRADICTED | 50 detailed reads per pass, 100-row page bound, and finished normally requires a parsed contract. Issues 534 and 590 track the gaps. |
| 5 | Closeout replaces safe worktree removal. | Possible confusion with current closeout command | `src/superclaude/commands/closeout.md:14-19,68-77` | CONTRADICTED | Closeout settles issue/report/task state after merge, explicitly not branches, worktrees or terminals. |

## Severity-rated findings
- **Medium, coverage limitation (existing):** the fixed detailed-read budget and one worker-list page do not cover all historical workers. This affects the issue's scale target and restart summaries; 534 and 590 already own this work. Not a newly discovered defect.
- **Medium, feature gap (intentional):** safe removal, automatic recovery, signed delegated grants and management-server relay are not implemented by this package. Do not attach these actions to observational rows without a separate authorization design.
- **Note, stale documentation:** the user guide says working is never produced (`docs/user-guide/orchestrator-mode.md:69`), but `classify.py:251-269` now implements it. The guide must not be used as proof that the code is still inert.
- No new high-severity defect established by this quick static pass; this is not a security or performance certification.

## Recommendations
Preserve the read-only collector/classifier/presenter split. Complete the existing 590 coverage follow-up first, then define safe close/recovery separately, using the coordinator's existing admission and user-authorization boundaries instead of treating a class label as permission. Correct the stale guide sentence with the next documentation change; no source edit is part of this task.

## Limits
No dynamic sweep, benchmarks or tests run: the selected command is a quick static architecture review and forbids dynamic analysis. PR test totals are historical author reports, not fresh results. Graph source was confirmed by direct Read; its capped caller response is retained as graph:truncated, not a complete inventory. No source, git index, remote, issue or PR changed. Scope does not establish the absence of a trust/relay subsystem elsewhere; the final issue report records broader searches separately.
