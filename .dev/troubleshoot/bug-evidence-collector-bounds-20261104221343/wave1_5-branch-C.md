# Wave 1.5 Branch C (semantic restrictions), persisted on receipt; degraded: true (auggie not in the analyst roster; Grep/Read fallback)

| source_file:line | quoted_text (abridged) | applies_to |
|---|---|---|
| tests/pr_submit/test_conflict_scripts.py:1410-1411 | shebang `#!/usr/bin/env bash`; `set -u -o pipefail` | A2 |
| tests/pr_submit/test_conflict_scripts.py:1413-1424 | whole-file bans incl. comments: `\bpush\b`, `stash`, `force`, `git config`, `--no-verify`, `--amend`, `src/superclaude`, `git (checkout|switch|reset|commit|add|rm|worktree|rebase|merge)`, `\bgh\b` ("force-kill" would fail) | A2 |
| tests/pr_submit/test_conflict_scripts.py:1185-1187 | no `.git/sc-pr-submit-tmp` left; exactly one stdout line (a background child must be dead and silent on stdout) | A2 |
| tests/pr_submit/test_conflict_scripts.py:1180 | the collector must not change status, HEAD or the index | A2 |
| tests/pr_submit/test_conflict_scripts.py:1386-1405 | timeout test stubs exit 124 and asserts `60-second budget` in stderr; skipped when `timeout` is absent, so the fallback has no test | A2 |
| tests/pr_submit/test_conflict_scripts.py:1193 | `res.stdout == f"EVIDENCE_FAIL {reason}\n"` | A2 |
| scripts/collect-conflict-evidence.sh:12-14, 18, 25-27 | writes only into --out and a temp dir removed on exit; exactly one stdout line; whole run bounded to 60 s; no stdin, no prompt | both |
| tests/pr_submit/test_conflict_scripts.py:1209 | `out = tmp_path / "evidence" / "sync" / "sync-1" / "1"` (the script enforces no layout) | C1 |
| tests/pr_submit/test_conflict_scripts.py:1294-1312 | E4: non-empty --out fails out_not_empty and writes nothing | C1 |
| tests/pr_submit/test_conflict_e2e.py:288, 290, 610, 845, 847, 888, 997, 1020 | `sync_dir = run_log.output_dir / "sync" / cycle_id`; `out = sync_dir / str(n)`; message.txt, manifest.txt, resolution.md directly under sync_dir | C1 |
| tests/pr_submit/test_conflict_sync_protocol.py:357-370 | only conflict-intent.md may name collect-conflict-evidence.sh | C1 |
| tests/pr_submit/test_conflict_sync_protocol.py:419-435, 482-494 | PROHIBITED_OPERATIONS scan over the new refs and scripts; only ("conflict-mechanical.md", "git checkout") allowed | both |
| tests/pr_submit/test_conflict_sync_protocol.py:40, 514-538 | ALLOWED_PROGRAMS {git, gh, uv, make, jq}; first word of every fenced command line in the refs must be one of these or scripts/ | C1 |
| src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:4 | allowed-tools: Read, Grep, Glob, Write, Edit, Bash(gh/git/uv/make/jq *), Task, Skill | C1 |

- C1 ref text to update (no test pins it by substring): conflict-intent.md:19, :71, :99; conflict-mechanical.md:97, :103. test_conflict_e2e.py hard-codes the sync layout and must follow the change.
- A2: `kill`, `kill -0` and `sleep` are allowed by the static rules; the words "force" and "push" are not, even in comments.
