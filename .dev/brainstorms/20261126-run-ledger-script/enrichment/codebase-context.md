# Codebase context (Wave 2A, tier: primary, via augment_code_search + direct reads)

- Sweep CLI: `src/superclaude/cli/sweep/commands.py`. `superclaude sweep run` takes repeatable `--run`, validates each with `probes.RUN_ID_RE`, and exits 2 with "no Run bound: pass --run <id>" when none is given and no Run is bound to the terminal. Flags: `--run`, `--window`, `--root`, `--output`.
- Sweep Orca allowlist: `src/superclaude/cli/sweep/probes.py` `ALLOWED_ORCA` pins 10 call templates (run-current, worker-list --run X --json, worker-show, task-list [--ready] --run X --json, worktree ps/list/current --json). `run-list` is NOT allowed there, so the ledger builder is a separate tool, not part of sweep. Test pinning the allowlist: `tests/sweep/test_probes_allowlist.py` (names `run-list` as a rejected shape).
- Sweep skill allowed tools: `Bash(superclaude sweep run:*)` only (`~/.claude/skills/sc-sweep-protocol/SKILL.md`). So the ledger must reach sweep through a `superclaude sweep run` flag or through the `--run` args the coordinator passes.
- Hook pattern: `~/.claude/hooks/require-orca-worktree-agent.sh` (PreToolUse, jq + awk tokenizer, fail open, exit 2 to block). A PostToolUse hook for run-create can be far simpler because it blocks nothing.
- Orca CLI shapes (verified by `--help` on this host): `run-create --objective <text> [--json]`; `task-list [--status] [--ready] [--run] [--json]`; `worker-list [--run] [--terminal-state] [--cursor] [--limit 1-100] [--json]`; `worktree list --json` returns `worktrees[]` with `id` of the form `<repoId>::<absolute path>`, `path`, `repoId`, `projectId`.
- `run-list --json` returns `result.runs[]` with `id, objective, coordinator_handle, legacy, created_at, updated_at` and no status field.
- Install surface: the CLI is registered in `src/superclaude/cli/main.py`; hooks install via `src/superclaude/cli/install_hooks.py`.
- Not verified yet: what a PostToolUse hook receives from `run-create` (needs a throwaway Run or Claude Code docs).
