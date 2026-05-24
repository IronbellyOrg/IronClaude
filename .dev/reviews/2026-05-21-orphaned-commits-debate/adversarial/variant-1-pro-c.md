# Variant 1 — PRO-Option-C ("Open the PR as stated")

**Position**: Execute Option C as originally proposed — open a follow-up PR
from `fix/prd-build-task-file-glob` containing all three orphaned commits
(`1550ea5f`, `fcd28bfa`, `e1c458bd`) cherry-picked or merged onto current
HEAD.

## Argument

**1. Recovers an active CI regression.** Commit `1550ea5f` fixes a real,
currently-failing test: `tests/cli/eval/test_eval_group.py::test_run_skeleton_emits_deferral_notice_on_stderr`
raises `TypeError: CliRunner.__init__() got an unexpected keyword argument 'mix_stderr'`
because Click 8.3.2 dropped the kwarg. The fix is one line (drop `mix_stderr=False`
at `test_eval_group.py:114`) plus three import deletions (`os`, `secrets`,
`HomeContainmentViolation` at `commands.py:31,34,75`) plus deletion of two
stale T04.09 skeleton tests + their backing constants. This work is already
done and committed; opening a PR is the cheapest path to land it.

**2. Lands defense-in-depth on the freshness hook.** Commit `e1c458bd` adds
two-line stderr messages to `src/superclaude/hooks/scripts/freshness-pre-edit.sh`
explicitly naming `mdformat`/`prettier`/`sed -i`/`script` as avoidance
anti-patterns. Without this hook strengthening, only the B7 memory
(`feedback_no_strategy_pivot_to_avoid_hooks.md`) carries the lesson, and
memory is a reasoning-layer guard that hooks can also enforce mechanically.
Two layers of protection are better than one — the hook strengthening
catches the avoidance pattern even in sessions where the memory doesn't
fire.

**3. Restores `.markdownlint.json` policy.** Commit `fcd28bfa` includes a
9-line `.markdownlint.json` at repo root setting `line_length: 160` and
disabling MD013 for tables / code blocks / headings. Without this config,
the repo inherits markdownlint's default 80-char limit, and every future
skill/command/agent commit with wrapped prose hits the wall (as the
2026-05-21 incident demonstrated). The policy file alone is worth a PR
because it unblocks every future contributor.

**4. Preserves commit-level rationale.** Each of the three commits has a
multi-paragraph commit message documenting the why, the verification, and
the `--no-verify` rationale (where applicable). Re-applying the work as
fresh commits requires re-writing those messages and loses the historical
narrative of how the work was conceived.

## Conceded weaknesses

- `fcd28bfa` touches 10 files; some will conflict with PR #70's parallel
  SoT restoration work. Conflict resolution adds non-trivial overhead.
- Commit messages reference dated context (e.g., "--no-verify per maintainer
  policy" wording) that may confuse future readers.
- The PR description has to explain why 3 disparate commits are bundled.
