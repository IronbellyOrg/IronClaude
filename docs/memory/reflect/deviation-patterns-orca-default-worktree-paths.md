# Reflect deviation patterns — orca-default-worktree-paths

## pre-refactorIronClau-20261102175540 (UC-1, Orca default worktree-path refactor plan, 2026-11-02)
- Recurring pattern: a spec that defines scope by a `git grep` of shell text misses subprocess calls written as argument lists (`["git", "worktree", "add", ...]`, `_git(cwd, "worktree", "add", ...)`). A plan that copies the spec's grep faithfully inherits the gap; one reviewer (refactorer lens) found it, two accepted the hit count as proof of scope. Lesson: "the counts match the grep" proves the grep output, not the spec's "every tracked file".
- Recurring pattern: tightening an absolute rule in CLAUDE.md without naming the lines in the same section that now contradict it (pre-PR checks that query or close an upstream PR). Generic "edit only where they contradict" instructions leave the executor to find them; acceptance criteria then pass with the contradiction in place.
- Recurring pattern: "keeps working" requirements proved only by "file unchanged"; the obvious fix (run the tests) can pass vacuously when modules skip on shallow CI clones (actions/checkout@v4 without fetch-depth) or as root. Require `-rs` and zero skips or a recorded reason.
- Repo fact found: this repository has only an `origin` remote; CLAUDE.md's "upstream remote" wording does not match the clone.

## pre-revisedPlanRefac-20261102214256 (UC-1, revised plan, 2026-11-02)
- Recurring pattern (confirmed again): "edit only where they contradict the rules above" without naming the lines. The revision named checks 1 and 3 but left CLAUDE.md:50 (`gh pr create --repo <repo>`) and :70 unnamed, and :50 fails the plan's own gh-line check.
- New pattern: a regression test that loads a script with `importlib.util.spec_from_file_location` + `exec_module` crashes when the script uses `@dataclass` under `from __future__ import annotations`, unless the module is first put in `sys.modules`. Probe the cited loader against the target file before trusting "the pattern at X".
- New pattern: module-level paths computed from `REPO_ROOT` at import (`RESULTS_DIR` in scripts/eval_runner.py) do not move when a test patches `REPO_ROOT`; tests of `main()` write into the real checkout unless every derived path is patched too.
- New pattern: replacing a persistent checkout with a create-and-remove temporary one deletes whatever subprocesses wrote inside it (E2E `eval-results/` relative to cwd). Check every cwd-relative write before adding `git worktree remove --force`.
- New pattern: an absolute "never interact with upstream" rule collides with a tool whose project id names the upstream repo (Orca `github:superclaude-org/superclaude_framework`); scope such bans to link flags and network calls.
- Repo fact found: the two `.dev/worktrees/` checkouts recorded in the plans were gone by 22:40Z on 2026-11-02; plans that name live checkouts by path go stale within hours.
- Process note: none of the three reviewers found the four most consequential Task 2 risks; the Round 2.5 invariant probe did. Keep the probe at standard depth.
