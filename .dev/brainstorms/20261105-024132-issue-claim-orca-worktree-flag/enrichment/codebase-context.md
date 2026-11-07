---
source: codebase
quality_tier: primary
method: augment_code_search (1 query) + Grep + Read + Bash (orca --help, git check-ignore)
collected: 2026-11-05T02:45:00+00:00
---

# Codebase context: `/sc:issue --claim` plus an Orca worktree flag

## 1. Where the claim stops today (read from disk)

- `src/superclaude/skills/sc-issue-protocol/refs/claim.md:90`: Wave 6 step 4, "Print the `next-steps.md` path and STOP. Do not stage or commit `.dev/issues/`".
- `src/superclaude/skills/sc-issue-protocol/SKILL.md:88` (claim step 7) and `:150` (Will Not: "Run any next-step command, brainstorm, design, plan or implementation").
- `src/superclaude/commands/issue.md` Will Not: "Run any next-step command (brainstorm, design, workflow, implement, troubleshoot)"; line 71 tells the user to run `next-steps.md` in their own session.
- `docs/designs/sc-issue-command.md:27` defines B2: "`--claim` stops after writing the next-step prompt to `.dev/issues/<number>/next-steps.md` and links it in the issue comment." B2 is a ruled design decision, so a flag that launches an agent running the chain is a deliberate exception to B2; a flag that only creates a worktree is not a "next-step command".
- Flag-scope precedent: `E-CREATE-ONLY-FLAG` (`commands/issue.md:48`, `SKILL.md:123`).
- Return contract (`SKILL.md:103-117`) has no field for a worktree; a new optional field would be needed.

## 2. What pins this code today

- Tests that name `/sc:issue`: `tests/commands/test_issue_command.py`, `tests/skills/test_issue_protocol.py`, `tests/skills/test_issue_worker_agents.py`, `tests/skills/test_issue_repo_resolution.py`, `tests/skills/test_clickup_claim.py`, `tests/cli/test_issue_body_templates.py`, plus `tests/core/test_how_we_work_routing_table.py` and `tests/recommend/test_routing_refresh.py`.
- A search of the first three of those for `orca|worktree|B2|next-step command|Will Not` found nothing: no existing test pins the absence of Orca.
- Docs and mirrors that mention it: `docs/user-guide/commands.md`, `docs/designs/sc-issue-command.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (byte-for-byte mirror of `src/superclaude/core/HOW-WE-WORK.md`).

## 3. Orca CLI facts (live `--help` run today, 2026-11-05)

- `orca worktree create --name <name>` options include `--repo`, `--base-branch`, `--branch`, `--parent-worktree`, `--no-parent`, `--setup run|skip|inherit`, `--agent`, `--prompt`, `--model`, `--effort`, `--surface chat|terminal`, `--comment`, `--activate`, `--json`, `--retry-launch <operationId>`, and the link flags `--issue`, `--pr`, `--reference`, `--linear-issue`, `--gitlab-*`.
- Default: "creates the worktree and its first terminal without switching the active Orca view"; no agent starts unless `--agent` is passed. `--prompt` goes to that agent. A taken `--branch` name gets a numeric suffix. If `--repo` is omitted Orca infers it from the current Orca-managed worktree. Parent lineage is inferred from the caller unless `--no-parent`.
- `orca worktree list [--repo] [--limit] [--json]` can be used for duplicate detection; `orca worktree rm --worktree <selector>` removes one.
- `orca worktree current --json` from this checkout returned the main worktree (`branch refs/heads/master`, `isMainWorktree: true`).
- Project rule (CLAUDE.md): never pass `--issue`, `--pr` or other Orca link flags for this repo; `--reference <github issue url>` is a link flag in all but name, so treat it as forbidden too (this reading of `--reference` is my inference, not a stated rule).
- Default worktree location observed 2026-11-02: `/home/coder/workspaces/worktrees/<repo>/<name>` (memory `orca-default-worktree-paths`, 3 days old, not re-verified today).

## 4. Existing precedent in the repo (from grep hits; the full files were not read)

- `.dev/orca-command-refactor/decisions/D3/RECOMMENDATION.md` and its debate: a per-PR child worktree is created with `orca worktree create --name <name> --parent-worktree <feature worktree> --base-branch <feature branch> --setup run --json` and **without `--agent`**.
- Same program, `.dev/orca-command-refactor/decisions/D1/debate/adversarial/merged-output.md:188`: whether Orca's `--setup run` performs `make sync-dev` in the new worktree is UNVERIFIED (`CR01:42`). If not, the new worktree's project `.claude/` copy (gitignored) would be missing or stale, so `/sc:` commands from this repo could be absent in it.
- `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:27`: `orca worktree create --agent claude` started Claude in the new worktree (PASS). A prompt that starts with `/` and the chat surface are UNVERIFIED (D3 debate transcript line 510).
- `D3/RECOMMENDATION.md:110` open item 7: whether an agent started by `orca agent launch` carries an Orca worker preamble that could refuse some commands in a launched tab.
- `~/.claude/WORKER-CONTRACT.md` exists (36 KB) and has a never-as-worker list; whether `/sc:issue` is on it was not checked (UNVERIFIED).
- `src/superclaude/cli/reflect/config.py:202` uses raw `git worktree add --detach`; that is one of the five CLAUDE.md "internal temporary checkout" exceptions, not a precedent for this feature.

## 5. Git facts that shape the design

- `git check-ignore .dev/issues/...` printed nothing, so `.dev/issues/` is not ignored. Some files under `.dev/issues/433/` are tracked; the claim output of a new issue is untracked.
- A worktree created from `origin/<default branch>` therefore has no `.dev/issues/<N>/next-steps.md` or `issue-summary.md`. `next-steps.md` refers to `@.dev/issues/<N>/issue-summary.md` (relative), so the flag must copy the directory into the worktree (leaving untracked files there) or rewrite paths to absolute ones.

## 6. Gaps this research did not close

- Real default worktree path today and exact `--json` result shape of `worktree create` (only `--help` was read; no worktree was created).
- Whether `--setup run` runs `make sync-dev`; whether `--agent claude --prompt "/sc:..."` delivers a slash command.
- Whether `/sc:issue` is allowed to run inside an Orca-launched tab (worker contract).
