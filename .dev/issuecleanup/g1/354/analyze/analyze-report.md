# Cross-Validation Report: issue 354 architecture analysis

- **Date:** 2026-11-23
- **Claims verified:** 4
- **Template:** /home/coder/.claude/templates/modularization-template-review/analyst-cross-validation_report_template.md, extended for architecture findings.
- **Command:** /sc:analyze src/superclaude --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g1/354/analyze
- **Scope:** src/superclaude is the narrowest common source ancestor for this issue: its release-wide runbook spans cli installers/pipelines, hooks, commands, skills and output styles. A quick issue-focused scan, not a whole-package defect audit. The two assignment guides under docs/testing/v5.0.0/impact-validation are supporting evidence, not the source target.

Codegraph: index_state=fresh, checked_at=2026-11-23T23:04:48Z; degraded: graph:truncated

## Validation Results
| # | Claim | Source | Code Path Checked | Verdict | Notes |
|---|-------|--------|-------------------|---------|-------|
| 1 | Installation validates live codegraph operation | Issue #354 release validation scope | src/superclaude/cli/install_mcp.py:949-965 | CONTRADICTED | Installation acquires the binary and verifies registration, explicitly not indexing or a live handshake. Runtime measurements remain separate evidence. |
| 2 | Fresh-worktree index builds are globally serialized or memory-budgeted | Issue #648 concurrency question | src/superclaude/hooks/scripts/codegraph-session-start.sh:11-31 | CONTRADICTED | Per-checkout database existence is the only build-presence guard; detached launch has no workspace-wide lock, queue or available-memory check. |
| 3 | Current commands still provide every 5.0.0 pipeline | Historical guides | src/superclaude/cli/main.py:557-596; absent cli/{sprint,roadmap,tasklist,cli_portify} directories | CONTRADICTED | PR #632 removed roadmap/tasklist/sprint and #629 removed cli-portify. Historical guides must remain version-scoped. |
| 4 | Generated release guides certify all measured impacts | Issue #354 done-when list | src/superclaude/skills/sc-post-release-protocol/SKILL.md:41-61; refs/golden-rule-evidence.md:13-17 | CONTRADICTED | The protocol documents and tests external surfaces and explicitly permits reported gaps. It is not a replacement for completed dated measurements. |

## Prioritized architecture findings
- **High operational concern, already tracked by #648:** new worktrees can launch independent background indexes without a shared memory budget. The source supports the concurrent-build scenario; #648 supplies measured scale. Do not infer machine failure from the peak sum: the reported 38 builds completed.
- **Medium evidence mismatch:** the issue body and 5.0.0 guide checklist predate later owner scope changes and current command removals. Treat latest dated owner rulings and recorded dispositions as the completion boundary; do not rerun removed pipelines on current master and call it release verification.
- **Medium completion distinction:** install success and generated hand-test guides do not certify release impact. Separate registration checks, actual runtime observations, missing historical evidence and policy acceptance.
- No new product defect or source modification is proposed by this quick scan. Four architecture claims checked; no security vulnerability or execution-performance claim independently established. No runtime metrics collected.

## Recommendations and verification limits
Finish only the remaining December 16 measurement/reporting obligation unless the owner explicitly retires it, then obtain the required closing summary. Handle concurrency policy through #648; the token overage is already accepted. Keep parked and removed command families out of new implementation work.

The codegraph check was fresh with MCP access; file discovery and caller lookups returned capped lists, recorded as graph:truncated below. Read/Grep/Glob confirmed the cited source details; graph rows were leads only. Augment's first request defaulted to nonexistent main and failed BRANCH_NOT_FOUND; retrying master succeeded. A guessed hook location outside scripts did not exist; Glob resolved the actual script. No index mutation, install, product test, headless run, paid model test, or GitHub write occurred. This review does not certify historical raw captures or all current features. A missing private GitHub event timeline is reported in the main findings, not silently treated as an empty timeline.
