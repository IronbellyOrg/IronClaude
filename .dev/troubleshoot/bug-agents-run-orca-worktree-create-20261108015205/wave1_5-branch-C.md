# Wave 1.5 Branch C (semantic restrictions), returned by troubleshoot-analyst, persisted by parent on receipt 2026-11-08T01:56Z. Degraded (Grep + Read).

```json
[
 {"source_file":"CLAUDE.md","file_line":41,"quoted_text":"no tool call (gh, git or Orca) and no gh or Orca link flag that resolves to it.","applies_to":"Orca link flags / upstream ban"},
 {"source_file":"CLAUDE.md","file_line":54,"quoted_text":"Until `orca worktree current --json` shows the fork's project id, `--issue`, `--pr` and other Orca link flags are never passed for this repo.","applies_to":"Orca link flags"},
 {"source_file":"CLAUDE.md","file_line":307,"quoted_text":"**ABSOLUTE RULE — every project worktree is created through Orca and lives at Orca's default worktree location.**","applies_to":"worktree creation"},
 {"source_file":"CLAUDE.md","file_line":312,"quoted_text":"Never create a project worktree with raw `git worktree add`, under the retired `.dev/worktrees/` location, or under `.claude/worktrees/`.","applies_to":"worktree creation"},
 {"source_file":"CLAUDE.md","file_line":313,"quoted_text":"Do **not** use the `EnterWorktree` tool: it hardcodes `.claude/worktrees/`, which is gitignored sync-dev territory.","applies_to":"worktree creation"},
 {"source_file":"CLAUDE.md","file_line":314,"quoted_text":"Never pass Orca link flags (`--issue`, `--pr`) for this repo; the fork rule above (`## ABSOLUTE RULE: PR Target = Fork`) governs them.","applies_to":"Orca link flags"},
 {"source_file":"CLAUDE.md","file_line":315,"quoted_text":"a CLI, script or test that creates and removes its own checkout keeps using `git worktree add` directly and must work without Orca.","applies_to":"worktree creation exception"},
 {"source_file":"CLAUDE.md","file_line":347,"quoted_text":"After editing, copy it byte-for-byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` and re-run the level-table copy into `src/superclaude/core/CLAUDE.md` (tests check both). Never add it as an `@` import.","applies_to":"fix constraint: copy rule (HOW-WE-WORK only)"},
 {"source_file":"src/superclaude/core/CLAUDE.md","file_line":47,"quoted_text":"For a new ccsession-backed Claude session, choose **Claude (CLI)**, never **New Terminal**.","applies_to":"Claude session launch"},
 {"source_file":"src/superclaude/core/CLAUDE.md","file_line":49,"quoted_text":"in an existing worktree or `worktree create --agent` for a new checkout; request","applies_to":"Claude session launch"},
 {"source_file":"src/superclaude/core/CLAUDE.md","file_line":50,"quoted_text":"`--surface terminal` when a CLI session is required. `terminal create` is for shells,","applies_to":"terminal creation"},
 {"source_file":"src/superclaude/core/CLAUDE.md","file_line":52,"quoted_text":"For supervised workers, keep `worker-start` and the dispatch preamble authoritative;","applies_to":"Claude session launch (supervised)"},
 {"source_file":"src/superclaude/skills/ccsession-tag/README.md","file_line":230,"quoted_text":"For a new ccsession-backed Claude session, choose **Claude (CLI)**, never **New Terminal**.","applies_to":"Claude session launch (duplicate section)"},
 {"source_file":"src/superclaude/skills/ccsession-tag/README.md","file_line":234,"quoted_text":"not agent sessions. This requires the `ccsession-orca` Claude command configuration above;","applies_to":"Claude session launch"},
 {"source_file":"src/superclaude/core/WORKER-CONTRACT.md","file_line":62,"quoted_text":"The worker's top-level session never calls `worker-start`, `dispatch` or `task-create`, Orca's low-level dispatch, or `orca-cli` `worktree create --agent` or `agent launch`, at any depth setting.","applies_to":"workers"},
 {"source_file":"src/superclaude/skills/sc-issue-protocol/SKILL.md","file_line":176,"quoted_text":"- Pass an Orca link flag, or call `orca` anywhere but `scripts/orca_worktree.py`.","applies_to":"Orca call site"},
 {"source_file":"src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py","file_line":951,"quoted_text":"argv = [\"orca\", \"agent\", \"launch\", \"--agent\", \"claude\", \"--worktree\"]","applies_to":"two-step launch"}
]
```

pinned_by_tests (worker):
- tests/core/test_orca_session_launch_guidance.py:10-31 pins 12 phrases of `### Orca session launches` in core/CLAUDE.md and ccsession-tag/README.md (additions allowed; phrases must stay in both).
- tests/skills/test_issue_protocol.py:339-368 forbids many flags in orca_worktree.py; `--agent/--prompt/--surface` only inside cmd_launch.
- tests/skills/test_issue_orca_worktree.py:264-279 FORBIDDEN_FLAGS includes `--agent` for the worktree step; 1046-1069 pin the exact launch argv.
- tests/skills/test_worker_contract.py:1032 uses "Then run orca worktree create." as a deliberate defect in the unattended section check.
- No test pins root CLAUDE.md lines 303-325.

Worker impact notes: fix (b) `--agent claude` matches core/CLAUDE.md:49 but must not reach /sc:issue's create step (tests forbid) nor supervised workers (WC-13). Fix (a) closing the seeded terminal: no rule limits `orca terminal close`. Edits to the launch section must change both core/CLAUDE.md and ccsession-tag/README.md.
