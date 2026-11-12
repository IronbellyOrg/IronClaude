# Anchor inventory at start base 5dc29d23 (item 1.4)

Each row was read from the file on disk (10-line window around the cited line) on 2026-11-08. Status values: CONFIRMED, MOVED to line N, CHANGED.

| # | File | Cited line | Quoted text found | Status |
|---|------|-----------|-------------------|--------|
| 1 | `src/superclaude/cli/main.py` | 565 | `main.add_command(issue_watch_group, name="issue-watch")` | CONFIRMED |
| 2 | `src/superclaude/core/WORKER-CONTRACT.md` | 23 | `- **Never-as-worker list**: \`/sc:agent\`, \`/sc:git\`, \`/sc:help\`, \`/sc:issue\`, \`/sc:pm\`, \`/sc:spawn\` and \`/sc:swarm-wizard\`, plus \`/sc:pr-submit\` while the answer to decision D3 keeps it off workers.` | CONFIRMED |
| 3 | `src/superclaude/core/WORKER-CONTRACT.md` | 110 | `**The sweep.** After every wake or timeout, at most once every 5 minutes, the coordinator runs one sweep: one \`worker-list\`, one prompt-wait listing (\`worktree ps --agent-wait\`) and one \`stat\` per wor...` | CONFIRMED |
| 4 | `src/superclaude/core/WORKER-CONTRACT.md` | 273 | `For N input Tasks feeding one merge Task (for example N \`/sc:troubleshoot\` workers, then \`/sc:adversarial --compare\`): wait until all N have settled.` (fan-in paragraph) | CONFIRMED |
| 5 | `src/superclaude/core/WORKER-CONTRACT.md` | 275 | `### Worked example: gate hit, answer, new Task` | CONFIRMED |
| 6 | `tests/skills/test_worker_contract.py` | 25 | `RULE_PHRASES = {` | CONFIRMED |
| 7 | `tests/skills/test_worker_contract.py` | 89 | `` "`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, " `` (never-as-worker phrase) | CONFIRMED |
| 8 | `tests/skills/test_worker_contract.py` | 165-172 | `"WC-15": (` ... `"Context-safe reading and handoff files"` ... closing `),` at 172 (WC-15 entry) | CONFIRMED |
| 9 | `tests/skills/test_worker_contract.py` | 173 | `"heartbeats": (` | CONFIRMED |
| 10 | `tests/skills/test_worker_contract.py` | 382-391 | `NEVER_AS_WORKER = (` at 382 ... `"/sc:pr-submit",` at 390, `)` at 391 | CONFIRMED |
| 11 | `tests/skills/test_worker_contract.py` | 912 | `def test_never_as_worker_list_names_all_seven_commands():` | CONFIRMED |
| 12 | `tests/skills/test_worker_contract.py` | 1322 | `assert "load" not in UNATTENDED_COMMANDS` (the load assertion) | CONFIRMED |
| 13 | `src/superclaude/core/HOW-WE-WORK.md` | 333 | `` | `/sc:spawn` | Requested decomposition with sequential/parallel/adaptive strategy and normal/deep depth. ... `` (`/sc:spawn` row) | CONFIRMED |
| 14 | `src/superclaude/core/HOW-WE-WORK.md` | 403 | `- **Some commands are never workers.** \`/sc:pr-submit\` and the other commands on the never-as-worker list in \`~/.claude/WORKER-CONTRACT.md\` stay with the coordinator or t...` | CONFIRMED |
| 15 | `src/superclaude/core/HOW-WE-WORK.md` | 404 | `- **Orca creates the worktrees.** Feature and child worktrees are created by Orca at its default paths, ...` | CONFIRMED |
| 16 | `docs/user-guide/commands.md` | 115 | `` | [`/sc:issue`](#scissue---github-issue-claim-and-create) | Claim a GitHub issue (assign, accuracy check, summary, next-step prompt, ... `` (`/sc:issue` row) | CONFIRMED |
| 17 | `CHANGELOG.md` | 5 | `## [Unreleased]` | CONFIRMED |
| 18 | `.gitignore` | 254 | `.dev/sprint-state/` | CONFIRMED |

## Line counts (`wc -l`)

| File | Now | Build time |
|------|-----|-----------|
| `docs/designs/orchestrator-mode.md` | 1013 | 1013 |
| `src/superclaude/core/WORKER-CONTRACT.md` | 327 | 327 |
| `tests/skills/test_worker_contract.py` | 3195 | 3195 |
| `src/superclaude/cli/main.py` | 569 | 569 |

## HOW-WE-WORK mirror

`cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` exit code: 0 (identical, as expected).

## Result

18 of 18 anchors CONFIRMED at the cited lines; no row is MOVED or CHANGED. No later item needs to read a moved line from this file.
