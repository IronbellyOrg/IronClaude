# Item 5.5 — Markdown gate input manifest

Scope: exact 19 Markdown paths from item 5.1 plus `.pre-commit-config.yaml`. Inventory is built incrementally; no staging, source changes, task edits, or other task items are performed.

## Review inputs

- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` — 653 lines; tracked modified.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md` — 389 lines; tracked modified.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` — 180 lines; tracked modified.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md` — 324 lines; tracked modified.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/triage-checklist.md` — 80 lines; tracked modified.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` — 91 lines; tracked modified.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/hardening-output-contract.md` — 73 lines; tracked modified.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/pipeline-hardening-closure.md` — 63 lines; tracked modified.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/unmask-and-sweep.md` — 52 lines; tracked modified.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/runtime-entrypoint-verification.md` — 47 lines; tracked modified.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/contract-enumeration.md` — 30 lines; tracked modified.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/effective-input-proof.md` — 27 lines; tracked modified.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/primitive-differential.md` — 58 lines; untracked new.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/agent-assertions.md` — 37 lines; untracked new.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/environment-deltas.md` — 16 lines; untracked new.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md` — 10 lines; untracked new.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/agents/confidence-calibrator.md` — 158 lines; tracked modified.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/agents/evidence-validator.md` — 147 lines; tracked modified.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/commands/troubleshoot.md` — 204 lines; tracked modified.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/.pre-commit-config.yaml` — 134 lines; tracked modified.

## Counts and diff scope

Total review inputs: **20 files, 2,773 current-content lines**. Counts measure newline bytes; all inputs have a final newline. Markdown: 2,639 lines; configuration: 134 lines.

| Measurement | Files | Additions | Deletions | Changed lines (sum) |
| --- | ---: | ---: | ---: | ---: |
| Full worktree tracked unstaged diff | 18 | 394 | 205 | 599 |
| Manifest-scoped tracked unstaged diff | 16 | 390 | 201 | 591 |
| Two existing Python test edits outside manifest | 2 | 4 | 4 | 8 |

**Diff output-line count: 1,446** (`git diff | wc -l`). Includes headers, context and metadata; NOT the changed-line total. Actual full tracked changed-line total: **599**; manifest-scoped: **591**.

Untracked files are absent from `git diff`: primitive-differential.md **58**, agent-assertions.md **37**, environment-deltas.md **16**, probe-packs/read-parse.md **10**; **4 files, 121 current-content lines**, separate from Git's diff statistics. Manifest review-change volume including new-file content: **712** (591 + 121); whole-worktree equivalent: **720** (599 + 121). These derived volumes are not raw Git diff totals.

## Captures and verification

Status: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/phase-outputs/test-results/git-status-phase5.txt`.

Diff stat: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/phase-outputs/test-results/git-diff-stat-phase5.txt`. Contains full `git diff --stat` followed by numeric diff output-line count.

Staged-path check: `git diff --cached --name-only -z` returned zero staged paths, hence no staged `.claude/` paths. Status capture contains exactly one literal `CLEAN: no .claude staged` line. Nothing was staged.

Final verification checks exactly 20 bullets, distinct absolute existing paths, each line count, the exact item 5.1 set plus configuration, unchanged captured Git status/diff statistics, and no staged `.claude/` paths. No Phase 6 gate is run; task checkbox remains untouched.
