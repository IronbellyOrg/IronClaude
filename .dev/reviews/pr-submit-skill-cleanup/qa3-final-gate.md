# QA Report — Final Gate 3 (pr-submit-skill-cleanup)

**Topic:** pr-submit skill cleanup (spec `.dev/specs/pr-submit-skill-cleanup.md`, Revision 2 > Revision 1 > section 2)
**Date:** 2026-10-24
**Phase:** final gate (spec conformance, behaviour, accuracy, orphan sweep)
**Fix cycle:** N/A (report-only, fix_authorization = false)

---

## Verdict: PASS

All four scripts now reach the `gh repo view` fallback, or the "could not resolve" message, when `git remote get-url origin` fails, and the origin path still wins when it works. This was shown by running the real scripts. A13 fails on the pre-A12 copy. Every spec item is present, the sweep found no remaining contradiction, and all gates are clean.

## Checks

| # | Check | Status | Evidence |
|---|-------|--------|----------|
| 1 | A12 by execution: real scripts, stub `git`/`gh` first on PATH | PASS | Driver `scratch/a12-driver.sh` runs the real `poll-augment-review.sh`, `poll-ci-checks.sh`, `reply-resolve-thread.sh` (`--pr 7 --comment-id 11 --body-file`), `retrigger-review.sh` (`--pr 7`) with no `--repo`. (a) git returns `https://github.com/acme/widgets.git`: all four call gh with `--repo acme/widgets` / `repos/acme/widgets` / `owner=acme repo=widgets`; no `gh repo view` call. (b) git exits 2: all four call `gh repo view --json nameWithOwner -q .nameWithOwner`, then use `upstream/parent` in the next gh call. (c) git and `gh repo view` both fail: all four exit 2 with `<script>: could not resolve target repo (pass --repo <owner/repo>)`. No silent exit in any of the 12 runs. |
| 2 | Mutation control for A12 | PASS | `mutation/poll-ci-checks.sh` differs from the real script only at line 34 (no `\|\| true`). Same driver: with git failing it exits rc=2 with empty stderr and never calls `gh` — the qa2 defect reproduces, so check 1 is a real discriminator. |
| 3 | A13 exercises the real lines and fails without A12 | PASS | `_run_resolution` (test_static_grep.py) reads each script's own `REPO=` / `[ -n` lines containing `git remote get-url origin` or `gh repo view` and runs them under `set -euo pipefail` with stub git/gh. `scratch/a13_mutation_check.py` calls that helper: real script gives `acme/widgets` and `upstream/parent`; the mutation copy raises `AssertionError: poll-ci-checks.sh: resolution aborted`. A missing origin or gh line would also fail (wrong or empty result), so the extraction cannot pass vacuously. |
| 4 | Scope: nothing else changed (AC1) | PASS | `git status --porcelain`: 20 modified + 1 staged deletion, all mapped to spec IDs (CHANGELOG E1/E1'; CLAUDE.md A7; commands.md B4; install_hooks.py C7; auggie-review.md C4/C5/C11; pr-submit.md A3/A4/B2/C1/C2; fsm.py B1/D1/A9; auggie SKILL C6; pr SKILL A1/A2/B3/B6/C3; augment-poll/ci-poll A10; state-machine D2; 4 scripts A5/A12; test_hook_update C8; test_pre_pr_checks A8; test_skill_parse B5/D3; test_static_grep A6/A8/A11/C9/A13; test_validation_gate C10). Every hunk of `git diff HEAD` read and mapped; no unmapped hunk. Untracked: only the spec and `.dev/reviews/pr-submit-skill-cleanup/` (this gate adds `scratch/` there). |
| 5 | P1 items A1-A13 | PASS | A1/B6: SKILL.md:189 origin first with the scripts' exact sed program, `gh repo view` only when origin has no URL, base from `gh repo view "$REPO" --json defaultBranchRef`, confirm + rebase BEFORE `gh pr create --repo "$REPO"`, URL verified after; `--pr <N>` skips create and checks `gh pr view <N> --repo "$REPO" --json url`. A2 SKILL.md:143-146, A3 pr-submit.md:28, A4 pr-submit.md:51. A5: all four scripts origin line then `gh repo view`; comments updated in reply-resolve-thread.sh:53 and retrigger-review.sh:45. A6 `test_repo_resolution_prefers_origin_over_gh_default`. A7 CLAUDE.md:46; pre-PR check 1 at CLAUDE.md:60 unchanged (spec §3). A8 test_pre_pr_checks.py:6-7. A9 fsm.py pr_target_ok docstring. A10 augment-poll.md:8-9, ci-poll.md:8-10, "(T-104 greps for it)" gone. A11: module docstring names T-105/T-1101/D2/D3 and the 970c1236 retirement (confirmed: `git show 970c1236` deletes `test_t104_every_gh_call_is_repo_scoped` and the hook tests); `_REPO_RESOLVE` comment, T-105 docstring and assertion (`git remote get-url origin`), T-1101 docstring, CORE_PURE comment, D2 header/docstring/message all as specified. A12/A13: checks 1-3. |
| 6 | P2 items B1-B6 | PASS | fsm.py: `pr: int \| None = None`, `--pr type=int`, `ValueError("--pr must be a positive PR number")`, `pr=ns.pr`. pr-submit.md argument-hint, Required Input row, Options row, Activation bullet; SKILL.md:136; commands.md:368. Tests `test_pr_attaches_to_existing_pr` pass. The form printed by `reflect contract-status` (`--monitor 3 --pr 42`, tests/pr_submit/test_detection_contract.py:98) now parses. |
| 7 | P3 items C1-C11 | PASS | pr-submit.md:16-19 "two activation paths", items 1-2; Related Commands line trimmed; SKILL.md Wave 0 hook sentence gone; auggie-review.md:17-18 items 1-2, hook example section removed (fences balanced), Will Not line = C11 text; auggie SKILL.md:361 = C6 text; install_hooks.py:76-77; test_hook_update.py staged `D`; `HOOK` and `_skill_and_hook_files` removed; test_validation_gate.py uses `reject-workspace-writes.sh`, which exists in `src/superclaude/hooks/scripts/`. |
| 8 | P4 items D1-D3 | PASS | `grep -nE '\bgh\b\|\bgit\b\|\byes\b' fsm.py` → no output; state-machine.md:157 "(Wave 6 has no confirm step)"; `test_yes_flag_removed` asserts `SystemExit`. |
| 9 | E1 / E1' CHANGELOG | PASS | New subsection CHANGELOG.md:7-17 covers P1-P4; base-branch clause is in the `/sc:pr-submit` sentence, the scripts sentence only claims resolution order (true: scripts never read the base). Old bullets at :25 and :27 no longer claim the gh-repo-view target or the accepted `--yes`. |
| 10 | Orphan sweep (excl. `.dev/`, `.claude/` dev copies, spec §3) | PASS | `git grep -i -E 'offer-pr-review\|PR-creation hook\|post-PR-create\|hook-driven\|three activation paths'` → only CHANGELOG.md:16 (the removal bullet). Tracked `.claude/settings.json` has no hook registration. `git grep -E -- '--yes\b'` near pr-submit → only CHANGELOG and the D3 test. `gh repo view` / `nameWithOwner` / `defaultBranchRef` hits: all origin-first or `"$REPO"`-scoped, plus CLAUDE.md:60 (kept by spec §3) and pre-existing stubs in tests that pass `--repo`. Wording sweep (`then the origin`, `origin's nameWithOwner`, gh-then-origin) → no hits. `T-104` → only refs/review-retrigger.md:8,11,29 (spec §3) and the retirement note. No `plugins/` mirror of pr-submit or auggie-review exists (`git ls-files plugins` grep empty). |
| 11 | Accuracy: SKILL Wave 0, CLAUDE.md, CHANGELOG, test docstrings, fsm.py docstring | PASS | Each changed sentence compared with the code after the change: SKILL Wave 0 matches script order and sed; CLAUDE.md "comes from the `origin` remote" matches; CHANGELOG claims match fsm.py and scripts (pre-change parser used `parser.parse_args`, so `--pr` was rejected — HEAD fsm.py:109); test docstrings describe origin-first; fsm.py docstring has no `gh`/`git` token (T-N50 passes). |
| 12 | Markdown tables and numbering | PASS | `scratch/md_tables.py` over the 10 changed .md files: every table has a consistent cell count, every file has balanced code fences. Numbered lists in pr-submit.md and auggie-review.md read 1, 2. |
| 13 | `bash -n` on the four scripts | PASS | `bash -n OK` for poll-augment-review.sh, poll-ci-checks.sh, reply-resolve-thread.sh, retrigger-review.sh. |
| 14 | pytest | PASS | `uv run pytest tests/pr_submit tests/core tests/cli/reflect tests/skills -q -p no:cacheprovider` → `1319 passed, 1 xpassed, 5 warnings in 25.02s` (warnings are pre-existing Click `isolated_filesystem` deprecations). |
| 15 | ruff | PASS | `uvx ruff check --no-cache` on the 6 changed .py files → `All checks passed!`; `uvx ruff format --check --no-cache` → `6 files already formatted`. |
| 16 | `git diff HEAD --check` | PASS | No output, rc=0. |
| 17 | AC7 `make verify-sync` | N/A | Recorded BLOCKED by the spec (no `make`); not part of this gate's run list. |

## Findings

None. No defect of any severity was found.

Observations considered and not counted as defects (recorded so the next reviewer does not re-derive them):

| Location | Observation | Why it is not a defect |
|---|---|---|
| tests/pr_submit/test_static_grep.py:167 | The rewrapped T-105 docstring line is 109 characters. | `pyproject.toml:186` ignores E501; ruff check and format both pass; the file already has pre-existing lines of 93-101 characters (:180, :197). |
| refs/state-machine.md:158 | The reflowed blockquote line is longer than its neighbours. | Renders identically in Markdown; no table or list structure involved. |
| CHANGELOG.md:16 | The removal bullet lists the main removed hook references, not every one (the SKILL Wave 0 sentence, the pr-submit Related Commands note, and the two Will Not lines are not named). | The bullet's claims are all true; a changelog summary is not required to list every line. |
| CHANGELOG.md:12 | Quotes the printed command as `--pr <N>`; the code prints `--pr 42` or `--pr <number>`. | `<N>` is a placeholder for the number, used the same way in the spec and the command file. |
| `.dev/reviews/pr-submit-skill-cleanup/scratch/` | Added by this gate (driver, stubs, logs, helper scripts). | QA scratch inside the allowed review folder; not part of the change. Remove before committing if it should not ship. |

## Self-Audit

Zero findings, so this is what was actively checked and why no defect remains:

- **A12 behaviour** was proven by running the four real scripts (not extracted lines) under three stub scenarios each (12 runs), reading the stub call logs to see which repo every later `gh` call used, plus a mutation control that reproduces the qa2 silent abort. The fix is the `|| true` inside the command substitution; with it, a failing `git` gives an empty `REPO`, the `gh repo view` line runs, and the final guard prints "could not resolve" when both fail.
- **A13** was checked by feeding its own helper the pre-A12 copy: it raises, so the test discriminates. The helper extracts lines by content, so a missing origin line or gh line gives a wrong or empty result and fails the test.
- **Spec conformance** was checked hunk by hunk against every row of §2, Revision 1 and Revision 2, with exact wording compared for C6, C11, A9, B1 and D2, and each cited line number re-checked with grep.
- **Orphan sweep** used `git grep` across the whole tracked tree (including the tracked `.claude/settings.json` and `plugins/`) for the hook names and phrases, `--yes`, `--pr`, `gh repo view` / `nameWithOwner` / `defaultBranchRef`, gh-then-origin wording, and `T-104`. Every remaining hit is the intended new text, the CHANGELOG record, or an item in spec §3.
- **Accuracy**: the commit cited as retiring T-104 (`970c1236`) was opened and does delete `test_t104_*` and the hook tests; `reject-workspace-writes.sh` exists; the HEAD parser used `parser.parse_args`, so the CHANGELOG claim that `--pr` used to be rejected is true; fsm.py has zero `gh`/`git`/`yes` tokens.
- **Gates**: `bash -n`, pytest (1319 passed, 1 xpassed), ruff check, ruff format, and `git diff HEAD --check` were all run in this session; result lines are in the Checks table.

**Confidence:** Verified: 16/17 | Unverifiable: 1 (AC7 `make verify-sync`: `make` not installed, spec marks it BLOCKED, CI is the gate) | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 5 | Grep: 0 (searches run as `git grep`/`grep` inside Bash) | Glob: 0 | Bash: 14 | Write: 4 (report stub + 3 scratch helpers) | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0 (no external lookup needed)
