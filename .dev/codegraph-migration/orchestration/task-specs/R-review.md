Task R: adversarial review of the three phase specs and the Coder handoff.

First read /home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init/.dev/codegraph-migration/orchestration/README.md (shared rules; binding).

Target: `.dev/codegraph-migration/specs/phase-1-removal-spec.md`, `.dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md`, `.dev/codegraph-migration/specs/phase-3-codegraph-adoption-spec.md`, `.dev/codegraph-migration/handoff/coder-handoff-prompt.md`, `.dev/codegraph-migration/handoff/coder-handoff-context.md`. Evidence: the inventories and research under `.dev/codegraph-migration/` and the real source tree.

Change: write `.dev/codegraph-migration/review/review.md`. Start from the assumption that the specs contain mistakes. Challenge and report findings on:
1. Task boundaries: tasks too big, overlapping, or split across phases wrongly.
2. Dependencies and ordering: within each phase and across phases (Phase 1 removal versus Phase 2 install versus Phase 3 adoption; IronClaude release versus Coder pin bump). Can the test suite stay green at each commit?
3. Shared-file conflicts: the same file edited by more than one phase or task (install_mcp.py, main.py, docs/user-guide/mcp-installation.md, core/CLAUDE.md, HOW-WE-WORK.md copies, plugins mirror, tests). Say which phase owns which hunk.
4. Missing work: re-run the inventories' rg commands yourself (codebase-memory and Serena terms, outside `.dev/`); any file not covered by a spec task is a finding. Also: user-environment cleanup on existing workspaces, settings.json permissions, `.claude/settings.json`, CI workflows, CHANGELOG, plugin mirror, `make verify-sync`, installed-path rule, Serena memory replacement, codex/opencode companion files.
5. Acceptance checks: every task must have an exact, runnable, falsifiable check; flag vague ones ("verify it works").
6. Feasibility: claims about codegraph tool names, install commands and behaviour must match `.dev/codegraph-migration/research/codegraph-evaluation.md` evidence; flag unverified claims driving tasks.
7. Handoff quality: is the Coder prompt self-contained, does it include the research instruction about new worktrees/projects, ordering with the pin, PR target IronbellyOrg/Coder, progress comments on #323?
8. Autonomy: are human-intervention points minimal and justified; are decision rules and issue-#323 progress comments present in every phase?

Each finding: id, severity (CRITICAL / IMPORTANT / MINOR), file and section, problem, concrete fix. End with a binary verdict per spec (PASS / FAIL; any finding is FAIL) and, if zero findings for a spec, a Self-Audit naming what you checked.

Skill use: none required. You may spawn one /sc:adversarial run only if two specs contradict each other and the evidence cannot settle it.

Constraints: review only; do not edit the specs.

Ownership: write only `.dev/codegraph-migration/review/review.md`.

Observable acceptance: file exists; includes the rg commands you re-ran with hit counts; findings have ids and concrete fixes; verdict per spec.
