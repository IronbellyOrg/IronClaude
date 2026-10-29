Task P1: write the Phase 1 spec (complete removal of codebase-memory-mcp and Serena).

First read /home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init/.dev/codegraph-migration/orchestration/README.md (shared rules; binding). Then read the wave-1 outputs: `.dev/codegraph-migration/inventory/{codebase-memory.md,serena.md,org-repos.md,primitive-usage.md}` and `.dev/codegraph-migration/research/install-update-flow.md`. Verify any fact you rely on against the source file before writing it into the spec.

Target: Phase 1 of issue #323.

Change: write `.dev/codegraph-migration/specs/phase-1-removal-spec.md`. It must contain:
1. Preflight section: the two comprehensive file lists required by the user (every file outside `.dev/` associated with codebase-memory; every file outside `.dev/` associated with Serena), each row with path and removal action. Take them from the inventories and re-run the inventories' rg commands to confirm nothing is missing; note any delta.
2. Goal and the definition of done: after the change, `./update.sh` on an existing workspace and `superclaude install` on a fresh one leave no codebase-memory or Serena binary registration, MCP entry, permission, companion skill/agent/hook, CLAUDE.md mention or docs reference that IronClaude owns; historical `.dev/` stays. State which leftovers are owned by the Coder image instead (handed to Phase 2's Coder handoff) and which by the upstream binary's own uninstaller.
3. Existing-workspace cleanup design: how `superclaude install`/`./update.sh` actively removes previously installed codebase-memory and Serena registrations and companion files on existing workspaces, safely (exact user scope, never touch unrelated or same-named project entries, keep indexes or delete them: decide per README rules). This is a real design decision; use `/sc:adversarial` (complex) if there is more than one viable approach.
4. Primitive gap policy: Serena/codebase-memory references in skills/commands/agents that are load-bearing (see primitive-usage.md) must not be left dangling between Phase 1 and Phase 3. Decide, per README rules, whether Phase 1 rewrites them to a neutral fallback (rg/Read/auggie) or Phase 1 only removes decorative mentions and defers load-bearing ones to Phase 3. Record the decision.
5. Serena memory replacement (from serena.md) decision applied.
6. Other-org-repo removal: a section listing the repos and files from org-repos.md and a ready-to-use handoff note per repo (the Coder repo's part is merged into Phase 2's Coder handoff; list it here as a cross-reference).
7. Task breakdown in execution order. Each task: files touched, the change, acceptance check (exact command, e.g. `uv run pytest tests/cli -q`, `make verify-sync`, `make lint`, an rg command that must return zero hits outside `.dev/`), and a commit point (conventional commit message). Tests and a commit at least after every task group; final full `uv run pytest` and `make verify-sync`. Include the `src/superclaude/core/HOW-WE-WORK.md` / `plugins/superclaude` mirror and `src/superclaude/core/CLAUDE.md` copy rules from the repo CLAUDE.md if those files change.
8. Progress reporting: the executor posts a brief comment on issue #323 (`gh issue comment 323 --repo IronbellyOrg/IronClaude --body ...`) at each task-group commit.
9. Autonomy rules for the executor: simple decisions self, mid-level `/sc:adversarial --compare ... --depth quick`, complex `/sc:adversarial --compare ...`; log decisions in the task package; never gate on the user. Human intervention points: list only the unavoidable ones (if any).
10. `## Decisions` section for decisions you made while writing the spec.

Skill use: no /sc:workflow here (a later task runs it on this spec). /sc:design is not needed. Use /sc:adversarial only per README decision rules.

Constraints: spec only; no source edits. Phase 2 owns installing codegraph; Phase 3 owns codegraph adoption in primitives. Name every file shared with Phase 2 (e.g. install_mcp.py, main.py, docs/user-guide/mcp-installation.md, core/CLAUDE.md) in a "Shared files" section with what Phase 1 leaves behind for Phase 2.

Ownership: write only `.dev/codegraph-migration/specs/phase-1-removal-spec.md` and `.dev/codegraph-migration/decisions/P1-*`.

Observable acceptance: spec exists with all ten sections; every task has an exact acceptance command and a commit point; both preflight lists present.
