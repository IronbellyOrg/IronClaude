# /sc:analyze report: issue 774 area (architecture, quick)

Targets: docs/designs/issue-watcher.md, src/superclaude/core/WORKER-CONTRACT.md, src/superclaude/skills/sc-issue-protocol
Codegraph: index_state=fresh, checked_at=2026-11-24T20:45:30Z; degraded: graph:unused-for-docs (targets are mostly Markdown; the one code symbol checked, the loader, was read directly)

## Findings (severity-rated)

1. MEDIUM, contract contradiction. src/superclaude/core/WORKER-CONTRACT.md:155 and :158 allow a coordinator restart (L4) on Orca's positive stall proof (budget 1 per 60 min, 2 per lineage). Line 303 ("Never: ... relaunch a dead worker by itself (WC-6 and the person decide)") forbids it for issue-pipeline workers. Line 79 also lets the coordinator settle a crashed attempt itself. No sentence says which governs a watcher-claimed worker. Needs an owner ruling.
2. LOW, stale status text. docs/designs/issue-watcher.md:3 says "never run live; enabled ships as false; no schedule is installed". This host's crontab holds an `* * * * *` issue-watch entry (read-only `crontab -l`).
3. LOW, stale cadence. docs/designs/issue-watcher.md:15 ("Every 5 minutes") and docs/designs/issue-watcher-zero-setup-coder-handoff.md:23 (`*/5 * * * *`) disagree with the installed `* * * * *`.
4. LOW, stale role wording. docs/designs/issue-watcher.md:43 "person-opened coordinator"; docs/user-guide/orchestrator-mode.md:11 and :19. HOW-WE-WORK.md:356 already says "whether a person opened it or a script started it".
5. LOW, approval wording. The loader (src/superclaude/cli/issue_watch/cycle.py:247-254) rejects a `labels.approval` value other than the default pseudo label, with a message that approval is the Approved issue field; it does not reject every use of the key. Docs and docstrings (cli.py:267, stage_predicates.py:1, :24) still say "approval label".
6. LOW, Full wording. src/superclaude/commands/issue.md:16 and the skill/design copies say `full` "also implements"; tests/skills/test_issue_protocol.py:878-880 pins that sentence.
7. LOW, commit wording. docs/designs/issue-watcher-status-pipelines.md:19 (Research row, Full column) says one local commit; templates/launch-prompt.md:28 says make no commit.

## Architecture note
All findings are text drift between design docs, the contract and the code; no code path disagrees with the merged design (R38). The ship gate is closed (src/superclaude/cli/issue_watch/launch.py:48 GOVERNED_LEVELS_ALLOWED = False), so only Pipeline None launches.

## Not verified
Whether the Approved field is a Project field or an organization issue field (the issue says the code calls it an organization issue field); not checked in code.
