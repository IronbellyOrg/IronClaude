---
title: "sc:pr-submit cleanup: origin-first target, --pr flag, drop dead hook refs and --yes"
version: "1.0.0"
status: draft
feature_id: PR-SUBMIT-SKILL-CLEANUP
spec_type: component
complexity_class: SMALL
created: 2026-10-23
branch: fix/pr-submit-skill-cleanup
base: origin/feature/pr-submit-default-monitor-3 @ 070399eb (stacked on PR #285)
---

# sc:pr-submit cleanup

## 1. Goal

Fix the four pre-existing `/sc:pr-submit` problems logged in `.dev/specs/pr-submit-default-monitor-3.md` §4 (user-approved 2026-10-23: "fix them"):

| # | Problem | Fix |
|---|---|---|
| P1 | The target repo is resolved with `gh repo view` first. gh prefers an `upstream` remote over `origin`, so a PR could be opened on the public parent before the post-create URL check catches it. | Resolve from the `origin` remote first (`gh repo view` only as a fallback when origin has no URL), in the skill's Wave 0 AND in the four scripts' `--repo` fallback. Read the base branch from `gh repo view "$REPO"` (explicit repo), not the CLI default. |
| P2 | `superclaude reflect contract-status` recommends `/sc:pr-submit --monitor 3 --pr <N>`, but the parser has no `--pr`. | Add `--pr <N>` (positive int, attach to an existing PR) to the parser, the command's `argument-hint` and Options, the skill's Required Input, and the user guide syntax line. |
| P3 | `offer-pr-review.sh` is referenced as an activation path but does not exist. | Remove every reference (user: "we do not really need this hook"). |
| P4 | `--yes` is parsed but nothing reads it. | Remove it (user: "we should remove this"). |

## 2. Changes (exhaustive)

### P1 — origin-first target

| ID | File | Change |
|---|---|---|
| A1 | `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` Wave 0 bullet | Resolve `REPO` from `git remote get-url origin` (same sed as the scripts), falling back to `gh repo view --json nameWithOwner` only when origin has no URL; base branch from `gh repo view "$REPO" --json defaultBranchRef` (overridable via `--base`); confirm `$REPO` and rebase if behind `origin/<base>` BEFORE `gh pr create --repo "$REPO" ...`; still verify the returned URL afterwards. |
| A2 | `SKILL.md` STOP rule (lines 143-146) | Target described as origin's `owner/repo` parsed from `git remote get-url origin`, not "via `gh repo view`". |
| A3 | `src/superclaude/commands/pr-submit.md:29` | Same as A2. |
| A4 | `src/superclaude/commands/pr-submit.md:52` (`--base` row) | `gh repo view "$REPO" --json defaultBranchRef` (explicit repo). |
| A5 | `scripts/poll-augment-review.sh`, `poll-ci-checks.sh`, `reply-resolve-thread.sh`, `retrigger-review.sh` (`--repo` fallback block) | Order swapped: origin remote (existing sed program unchanged) first, then `gh repo view`. Comments in `reply-resolve-thread.sh` and `retrigger-review.sh` updated to "(the origin remote, then gh repo view)". |
| A6 | `tests/pr_submit/test_static_grep.py` | New test: in each of the four scripts the `git remote get-url origin` resolution line comes before the `gh repo view` fallback line. |
| A8 | `tests/pr_submit/test_pre_pr_checks.py` module docstring; `tests/pr_submit/test_static_grep.py` module docstring and T-104 docstring | Describe the resolution order as origin remote first, `gh repo view` fallback; the T-104 module docstring no longer says "+ the hook". |
| A7 | `CLAUDE.md` mandatory-PR paragraph | "`<repo>` is what `gh repo view` reports (pre-PR check 1 makes sure that is the fork)" becomes "`<repo>` comes from the `origin` remote". Pre-PR check 1 itself stays (it still protects any bare `gh` use). |

### P2 — `--pr`

| ID | File | Change |
|---|---|---|
| B1 | `src/superclaude/pr_submit/fsm.py` | `SkillArgs.pr: int | None = None`; `parser.add_argument("--pr", type=int, default=None)`; `parse_args` rejects `--pr < 1` with `ValueError("--pr must be a positive PR number")`; passes `pr=ns.pr`. |
| B2 | `src/superclaude/commands/pr-submit.md` | `argument-hint` gains `[--pr <N>]`; Required Input row reads "... OR an existing PR number (`--pr <N>`)"; Options table gains a `--pr <N>` row ("Attach to an existing PR instead of opening one"); Activation "Pass the following context" names `--pr <N>`. |
| B3 | `SKILL.md` Required Input row | "... OR an existing PR number (`--pr <N>`)". |
| B4 | `docs/user-guide/commands.md` `/sc:pr-submit` syntax line | Gains `[--pr <N>]`. |
| B5 | `tests/pr_submit/test_skill_parse.py` | New test: `--pr 42` parses to 42; default is `None`; `--pr 0` raises `ValueError`. |

### P3 — dead hook references

| ID | File | Change |
|---|---|---|
| C1 | `src/superclaude/commands/pr-submit.md:16-20` | "three activation paths" becomes "two"; the PR-creation-hook item is removed; the Programmatic item becomes 2. |
| C2 | `src/superclaude/commands/pr-submit.md:89` | Drop "(offered together by the post-PR-create hook)". |
| C3 | `SKILL.md` Wave 0 bullet | Drop "The `offer-pr-review.sh` hook may then mention `sc:pr-submit --monitor`." |
| C4 | `src/superclaude/commands/auggie-review.md:16-20` | PR-creation-hook activation item removed; items renumbered. |
| C5 | `src/superclaude/commands/auggie-review.md:123-130` | The "Hook-driven post-PR-creation review" example section is removed. |
| C6 | `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:361` | "explicit `/sc:auggie-review` invocation or PR-creation hook only" becomes "explicit `/sc:auggie-review` invocation or a programmatic call from another `/sc:*` command only" (matching the command's remaining activation paths). |
| C7 | `src/superclaude/cli/install_hooks.py:77` comment | "same pattern as `reject-workspace-writes.sh` and `offer-pr-review.sh`" becomes "same pattern as `reject-workspace-writes.sh`". |
| C8 | `tests/pr_submit/test_hook_update.py` | Deleted: it holds only a helper that runs the missing hook; its tests were already retired in `970c1236`. Nothing imports it. |
| C9 | `tests/pr_submit/test_static_grep.py` | Remove the `HOOK` constant and the unused `_skill_and_hook_files()` helper (no callers). |
| C10 | `tests/pr_submit/test_validation_gate.py:45` | Example path becomes an existing hook script, `src/superclaude/hooks/scripts/reject-workspace-writes.sh` (the assertion still exercises "shared infra (hooks) escalates"). |

### P4 — `--yes`

| ID | File | Change |
|---|---|---|
| D1 | `src/superclaude/pr_submit/fsm.py` | Remove `SkillArgs.yes`, `parser.add_argument("--yes", ...)`, and `yes=ns.yes`. |
| D2 | `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md` §5.3 | "(Wave 6 has no confirm step, and the `--yes` flag the parser accepts has no effect)" becomes "(Wave 6 has no confirm step)". |
| D3 | `tests/pr_submit/test_skill_parse.py` | New test: `--yes` is rejected by the parser (`SystemExit`). |

### Record

| ID | File | Change |
|---|---|---|
| E1 | `CHANGELOG.md` `[Unreleased]` | New subsection for P1-P4. In the existing pr-submit subsection (from PR #285): the pre-PR-check bullet no longer claims `/sc:pr-submit` takes its target from `gh repo view`; the §5.3 bullet no longer says the `--yes` flag is still accepted. |

### Revision 1 (after QA round 1: `qa-spec-conformance.md`, `qa-orphan-sweep.md`)

| ID | File | Change |
|---|---|---|
| C11 | `src/superclaude/commands/auggie-review.md:160` (Will Not) | "explicit invocation or hook-driven only" becomes "explicit `/sc:auggie-review` invocation or a programmatic call from another `/sc:*` command only" (same as C6). |
| A9 | `src/superclaude/pr_submit/fsm.py` `pr_target_ok` docstring | Resolution order "the origin remote URL first, else the host CLI's default repo" (no `gh`/`git` tokens: the file is in the T-N50 zero-token set). |
| A10 | `refs/augment-poll.md:8-9`, `refs/ci-poll.md:8-10` | Pin described as origin's `owner/repo` parsed from `git remote get-url origin`; the false "(T-104 greps for it)" is dropped (T-104 was retired in `970c1236`). |
| A11 | `tests/pr_submit/test_static_grep.py` | Module docstring: the repo-pin paragraph names the live tests (T-105, T-1101, D2, D3) and notes T-104 was retired in `970c1236`; `_REPO_RESOLVE` comment calls `gh repo view` the fallback; T-105 docstring drops the T-104 comparison and its assertion now requires `git remote get-url origin`; the T-1101 docstring drops the claim that `test_t104` scans the files; the CORE_PURE comment points at T-1101 only; the D2 header, docstring and assertion message say "origin-URL resolution", not "fallback". (Supersedes the A8 wording for this file: A8 named a "T-104 docstring"; the edited docstring is T-105's.) |
| B6 | `SKILL.md` Wave 0 | With `--pr <N>`, skip `gh pr create`, attach to that PR, and check the URL from `gh pr view <N> --repo "$REPO" --json url`. |
| E1' | `CHANGELOG.md` | The base-branch clause belongs to the `/sc:pr-submit` sentence, not to the helper-scripts sentence (the scripts never read the base branch). |

### Revision 2 (after QA round 2: `qa2-final-gate.md`)

The reordered origin-first line aborted every script under `set -euo pipefail` when `git remote get-url origin` failed, so the `gh repo view` fallback and the "could not resolve" message never ran.

| ID | File | Change |
|---|---|---|
| A12 | The four scripts' origin line | `... | sed -E '<unchanged>' || true)}"`: the substitution can no longer abort the script; an empty result falls through to the `gh repo view` line. |
| A13 | `tests/pr_submit/test_static_grep.py` | New `test_repo_resolution_runs_origin_first_then_falls_back`: runs each script's two resolution lines under `set -euo pipefail` with stub `git`/`gh` and asserts (a) origin wins over gh's default repo, (b) a failing `git` falls back to `gh repo view` instead of aborting. Verified to fail on a copy of the script without A12 (mutation artifact: `.dev/reviews/pr-submit-skill-cleanup/mutation/poll-ci-checks.sh`, not committed). |

## 3. Deliberately unchanged

| What | Why |
|---|---|
| `CLAUDE.md` pre-PR check 1 (`gh repo view` must print the fork) | Still useful for any bare `gh` use; only the sentence claiming the skill depends on it changes (A7). |
| The sed program in the four scripts | Tested by `test_repo_resolution_sed_handles_all_url_forms`; only the order of the two resolution lines changes. |
| `.dev/` history, including `.dev/specs/pr-submit-default-monitor-3.md` | Records, not instructions. |
| `refs/review-retrigger.md:8-11` and `:29` mention the retired T-104 test | Pre-existing stale test IDs on lines this change does not touch; they do not describe target resolution, the hook, `--pr` or `--yes`. Follow-up, not in scope. |
| `.claude/` dev copies | Gitignored; `make sync-dev` refreshes them; never staged. |

## 4. Acceptance criteria

| ID | Check | Pass when |
|---|---|---|
| AC1 | Every change in §2 | Present as specified; nothing else changed except this spec and QA reports under `.dev/reviews/pr-submit-skill-cleanup/`. |
| AC2 | `git grep -n -i 'offer-pr-review\|PR-creation hook\|post-PR-create\|hook-driven' -- ':!.dev'` | Only the E1 `CHANGELOG.md` bullet that records the removal. |
| AC3 | `git grep -n -E -- '--yes\b' -- src/superclaude/pr_submit src/superclaude/skills/sc-pr-submit-protocol src/superclaude/commands/pr-submit.md tests/pr_submit` | Only the D3 test that asserts rejection. |
| AC4 | In each of the four scripts and in SKILL.md Wave 0 | `git remote get-url origin` is used before `gh repo view` for the target; every `gh repo view` for the base branch names `"$REPO"`. |
| AC5 | `uv run pytest tests/pr_submit tests/core tests/cli/reflect tests/skills -q` | Passes. |
| AC6 | `uvx ruff check` and `uvx ruff format --check` on changed `.py` files; `bash -n` on the four scripts; `git diff --check` | Clean. |
| AC7 | `make verify-sync` | BLOCKED locally (`make` not installed); CI is the gate. |
| AC8 | Accuracy | Every changed sentence matches the code after the change. |
