# Orca command-refactor spec run

Shared context for every worker in this run. Read this file first.

## Goal
Write a reviewed spec for refactoring IronClaude commands so Orca orchestration coordinates them as workers (Orca on top; commands stay the units of work), instead of rewriting commands to call Orca internally. Planning only: nothing is implemented in this run.

Worktree (repo root for every path below): /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs
Branch: ironbelly/OrcaCLICommandRefactor-Specs. Output folder: .dev/orca-command-refactor/

## Evidence to read (do not assume)
- `.dev/codegraph-migration/orchestration/README.md`: an earlier run where Orca workers invoked SC commands (for example `/sc:adversarial`); that work landed as PR #329.
- `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`: a supervised Claude worker that waits on a question fails Orca's 60-second readiness limit.
- `~/.claude/commands/sc/pr-submit.md` and `~/.claude/skills/sc-pr-submit-protocol/SKILL.md`: a command that must run as a top-level session, not inside an Agent-tool subagent.
- `.dev/research/recovered-command-evaluation-20261027/`: historical command evaluation. It explicitly excludes Orca. Historical research, not current policy.
- `src/superclaude/core/HOW-WE-WORK.md`: current routing policy.
- Orca's version-matched guides: `orca-ide skills get orchestration` and `orca-ide skills get orca-cli` (use `orca-ide`, never bare `orca`, outside an Orca terminal).

## Output files
| Task | Output |
|---|---|
| 1. Inventory A | `inventory/commands-a.md` |
| 2. Inventory B | `inventory/commands-b.md` |
| 3. Orca facts | `inventory/orca-capabilities.md` |
| 4. Spec | `specs/orca-worker-contract-spec.md` |
| 5. Review | `review/spec-panel.md` |
| 6. Revise | `specs/orca-worker-contract-spec.md` (edit) and `review/disposition.md` |

## Rules for every worker
- Planning only. Do not edit `src/`, `tests/`, `docs/`, `.claude/`, `~/.claude` or Orca settings. Write only your assigned files under `.dev/orca-command-refactor/`.
- No git commits, pushes, PRs or GitHub comments.
- Cite `path:line` (or a URL) you actually read for every claim. Mark anything unverified UNVERIFIED.
- Create each output as a header stub first, then fill it section by section.
- Use `uv run` for Python.
- If blocked on a question, ask the coordinator through the `ask` command in your Orca preamble. Never open a local question prompt.
- Decide simple choices yourself and record each in a `## Decisions` section (decision, options, rationale).
- After any command, `git status --short` must show no modified tracked file caused by you.
- Finish with `worker_done` per your Orca preamble, with `--report-path` set to your output file.
