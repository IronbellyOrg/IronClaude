Task P2: write the Phase 2 spec (install codegraph by default) and the Coder handoff.

First read /home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init/.dev/codegraph-migration/orchestration/README.md (shared rules; binding). Then read `.dev/codegraph-migration/research/codegraph-evaluation.md`, `.dev/codegraph-migration/research/install-update-flow.md`, `.dev/codegraph-migration/inventory/codebase-memory.md`, `.dev/codegraph-migration/inventory/serena.md` and `.dev/codegraph-migration/inventory/org-repos.md`. Verify facts against source before relying on them.

Target: Phase 2 of issue #323.

Change: write three files.

A. `.dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md` containing:
1. Preflight: every IronClaude file that must change to install codegraph by default (installer modules, `main.py` install/update/doctor/--list wiring, `install_mcp.py` registry, `update.sh` if needed, docs, tests, core CLAUDE.md MCP table), with the change per file.
2. Installer design: pinned version, verified acquisition (checksum), platforms, user-scope registration (exact `claude mcp add` argv from the evaluation), reuse when already present (e.g. baked by Coder), required versus optional phase, `--list`/doctor reporting, idempotency, failure behaviour and exit codes, removal path. Reuse the seams identified in install-update-flow.md; prefer the smallest correct code. If there are multiple viable designs, run `/sc:adversarial` (complex) per README rules; `/sc:design` is optional and only if it adds clarity to the interface.
3. Project indexing and sync: how this worktree and any project get indexed (init on first use, git hooks, watcher, per-worktree), and what IronClaude installs to keep indexes fresh. Mid-level choices go to `/sc:adversarial --depth quick`.
4. Validation plan: an automated test layer (unit tests with mocked subprocess, following tests/cli conventions) plus an integration check that installs codegraph in an isolated HOME sandbox and runs a real index + query in this worktree or an isolated project copy (reuse W4's sandbox recipe). Include exact commands.
5. Task breakdown in execution order, each with files, change, exact acceptance command, and a commit point (conventional commit). Tests after every task group and a final full `uv run pytest`, `make lint`, `make verify-sync`.
6. Progress reporting on issue #323 at each task-group commit (`gh issue comment 323 --repo IronbellyOrg/IronClaude --body ...`).
7. Autonomy rules for the executor (simple self / mid `/sc:adversarial --compare ... --depth quick` / complex `/sc:adversarial --compare ...`), decision logging, minimal human intervention list.
8. Release/ordering: how this lands relative to Phase 1 and the Coder pin bump (from install-update-flow.md section 5).
9. `## Decisions`.

B. `.dev/codegraph-migration/handoff/coder-handoff-prompt.md`: a self-contained prompt for an agent working in the IronbellyOrg/Coder repo. It must: state the goal (existing workspaces, on update, have codebase-memory and Serena removed and codegraph installed and synced; new workspaces get codegraph baked or installed); list the Coder touchpoints found in install-update-flow.md as starting points (not as a finished plan); tell the agent to verify each against current Coder main; tell it to research and decide what other configuration keeps new worktrees and projects indexed/synced on clone or creation (git hooks templates, Orca worktree creation hooks, workspace startup scripts, `core.hooksPath`, post-checkout, code-server tasks, etc.); require it to coordinate with the IronClaude pin (`ARG IRONCLAUDE_GIT_SHA`) and the ordering constraints; require tests, regular commits, a PR on IronbellyOrg/Coder only (never upstream), and progress comments on IronClaude issue #323; and include the same autonomy/decision rules. Keep it under about 150 lines.

C. `.dev/codegraph-migration/handoff/coder-handoff-context.md`: the supporting facts the prompt references (codegraph install facts, IronClaude's new installer contract: what IronClaude will install/remove and what it expects the image to provide, version pin, MCP registration shape, removal list of codebase-memory/Serena artifacts on a workspace).

Constraints: spec and handoff only; no source edits; no Coder writes. Phase 1 owns removal inside IronClaude; reference it, don't duplicate it. Name every file shared with Phase 1 or Phase 3 in a "Shared files" section.

Ownership: write only the three files above and `.dev/codegraph-migration/decisions/P2-*`.

Observable acceptance: three files exist; spec tasks each have an exact acceptance command and commit point; the handoff prompt is self-contained (a reader with no other context can act on it) and contains the research instruction about new worktrees/projects.
