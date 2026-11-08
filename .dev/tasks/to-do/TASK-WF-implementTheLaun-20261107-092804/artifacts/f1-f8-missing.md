# Panel findings F1 to F8: source file missing (Task 16)

Checked 2026-11-07 in the worktree `issue-394-launch-level-hook`.

- `.dev/brainstorms/20261105-170229-launch-level-hook/spec-panel-20261106/review.md` is absent.
- `ls .dev/brainstorms/20261105-170229-launch-level-hook/spec-panel-20261106` printed:
  `ls: cannot access '.dev/brainstorms/20261105-170229-launch-level-hook/spec-panel-20261106': No such file or directory`
- The parent directory `.dev/brainstorms/20261105-170229-launch-level-hook/` holds only
  `adversarial/`, `enrichment/`, `merged-requirements.md`, `return-contract.yaml` and `seed-brief.md`.
- `find .dev -type d -name "spec-panel*"` finds no spec-panel directory for this hook (only
  `.dev/troubleshoot-meta/20260610T141100Z/spec-panel`, its copy under `.dev/research/...`, and
  `.dev/brainstorms/20260618-per-phase-turn-budget/spec-panel`, all unrelated).
- `grep -rln "spec-panel-20261106" --include=*.md .` (excluding `.claude/`) finds the name only as a
  reference: in `docs/designs/sc-issue-launch-level-hook.md`, the plan file of this package, its
  `artifacts/b-ctx-verdict.md` and T1 retry prompts, `.dev/issues/394/` notes, the
  `TASK-WF-implementDocsDes-20261106-210206` package and `.dev/reflect/pre-implementTheLaun-20261107093251/`.
  None of these is the review itself.

Consequence for Task 16: no F-numbered case was written. The corpus tests cite MR sections 8.3 and
8.4 and design sections 4, 5, 10 and 16 only.
