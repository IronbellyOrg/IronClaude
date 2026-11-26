# Analyze report: src/superclaude/cli/issue_pipeline (architecture, quick)

Run: 2026-11-24, master HEAD f2894fc44, worktree Realign. Command: `/sc:analyze src/superclaude/cli/issue_pipeline --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/7/analyze`
Codegraph: index_state=fresh, checked_at=2026-11-24T22:19:04Z; degraded: none (codegraph used only for status; findings below were confirmed by Grep and Read)

## Layout
Nine modules, 2122 lines in total under `src/superclaude/cli/issue_pipeline/`: `cli.py` (489, verb group `superclaude issue-pipeline`), `approval_record.py` (416), `complete.py` (431), `stage_predicates.py` (301), `reads.py` (182), `plan_hash.py` (90), `brief.py` (80), `release.py` (66), `approval_line.py` (62). This is the only coordinator-side code on master. No `superclaude coordinator` or `superclaude orchestrator` verb group exists.

## Findings
| # | Severity | Finding | Evidence |
|---|---|---|---|
| 1 | Medium | No text-hygiene layer: nothing in the package scans written text for dashes or secrets. The only dash/name refusal is shell, in `/sc:closeout` (`src/superclaude/skills/sc-closeout-protocol/scripts/settle.sh:161-188`, refuses the whole text, does not mask). Bears on #802. | Grep, Read |
| 2 | Medium | A secret detector with a `[REDACTED]` marker exists elsewhere (`src/superclaude/cli/audit/credential_scanner.py:18`, `:64`, `redact_output` `:157`) but keeps `match_text` in memory (`:74`). Reuse must not log it. Bears on #802. | Read |
| 3 | Low | No tier setting anywhere in the package (grep `tier` in `issue_pipeline/*.py` finds nothing). The per-repo watcher config rejects unknown keys (`src/superclaude/cli/issue_watch/cycle.py:59-72`, `:223-226`). Bears on #803. | Grep, Read |
| 4 | Low | Verb-group spelling is split: `settle.sh:1037` calls `superclaude orchestrator report-entry`; the plan says `superclaude coordinator` (SPEC.md:228). Neither exists. Bears on #802. | Read |
| 5 | Info | No coordinator spec home on master (no `SPEC-AGENT-WORK-COORDINATOR`). The coordinator rules live in `~/.claude/WORKER-CONTRACT.md` (installed from the repo core folder). Bears on #805. | Grep |

## Recommendations
Reuse the settle.sh dash rule and the credential_scanner marker when the writer verbs are built; do not add a tier key until the owner decision on R38 is clarified; name the spec home in chat first.
