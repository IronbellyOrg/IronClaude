# QA Report — Spec Conformance + Factual Accuracy (pr-submit-skill-cleanup)

**Spec:** `.dev/specs/pr-submit-skill-cleanup.md`
**Base:** HEAD 070399eb (uncommitted working tree under review)
**Date:** 2026-10-24
**Fix authorization:** false (report-only)

## Verdict: FAIL

Five findings: 1 IMPORTANT (F1) and 4 MINOR (F2-F5). The code is correct: the scripts, the parser, the new tests and every gate pass. The failures are text that no longer matches the code: one hook reference that survived the cleanup, and stale or inaccurate wording in test docstrings and the CHANGELOG.

## Per-item table

| ID | Status | Evidence |
|---|---|---|
| A1 | PASS (see F4) | `SKILL.md:189` Wave 0: `REPO` from `git remote get-url origin \| sed -E '<same program as the scripts>'`. `gh repo view --json nameWithOwner` is used only "if origin has no URL". Base from `gh repo view "$REPO" --json defaultBranchRef`, with the `--base` override. "BEFORE creating anything: confirm ... rebase", then `gh pr create --repo "$REPO"`, then the URL is verified. The extra text "(or attach to `--pr <N>`)" is not in the spec -> F4. |
| A2 | PASS | `SKILL.md:143-145` reads "(origin's `owner/repo`, parsed from `git remote get-url origin`)". Parentheses balance. |
| A3 | PASS | `commands/pr-submit.md:28` uses the same wording as A2. |
| A4 | PASS | `commands/pr-submit.md:51` reads `gh repo view "$REPO" --json defaultBranchRef`. |
| A5 | PASS | In all four scripts, the first line is `REPO="${REPO:-$(git remote get-url origin ... \| sed -E '<unchanged>')}"` and the second is `[ -n "$REPO" ] \|\| REPO="$(gh repo view ... \|\| true)"`. The sed program is byte-identical to HEAD (diff). The comments at `reply-resolve-thread.sh:53` and `retrigger-review.sh:45` read "(the origin remote, then gh repo view)". `bash -n` is OK on all four. Runtime check: with `REPO=''` the expansion gives `IronbellyOrg/IronClaude`; with `REPO='x/y'` it keeps `x/y`. |
| A6 | PASS | `test_static_grep.py:532` `test_repo_resolution_prefers_origin_over_gh_default`. I ran its exact predicate (read-only) on `git show HEAD:<script>`. All four HEAD scripts have origin_at > gh_at, so the test fails on the old order (poll-augment 19/18, poll-ci 34/33, retrigger 47/46, reply-resolve 55/54). All four pass on the worktree. The `--repo)` argument lines and `REPO=""` are excluded by the startswith/substring filter. |
| A7 | PASS | `CLAUDE.md:46` reads "where `<repo>` comes from the `origin` remote". Pre-PR check 1 (`CLAUDE.md:60`) is unchanged. The claim is true per SKILL.md Wave 0. |
| A8 | PASS (see F2, F3) | `test_pre_pr_checks.py:6-7` now gives origin first, `gh repo view` as the fallback. `test_static_grep.py:3-8` drops "+ the hook" and gives the new order. The spec says "T-104 docstring", but no T-104 test exists; the edit was made to the T-105 docstring (`:173`). Stale text remains elsewhere -> F2, F3. |
| B1 | PASS | `fsm.py:64` `pr: int \| None = None`; `:97` `add_argument("--pr", type=int, default=None)`; `:118-119` raises ValueError "--pr must be a positive PR number"; `:132` `pr=ns.pr`. Probe: `--pr 42` gives 42, the default is None, `--pr 0` and `--pr -3` raise ValueError, `--yes` raises SystemExit(2). The dataclass, the parser and the return agree (12 fields each). |
| B2 | PASS | `pr-submit.md:8`: argument-hint has `[--pr <N>]`. `:26`: Required Input reads "... (`--pr <N>`)". `:53`: Options row "Attach to an existing PR instead of opening one." `:76`: the activation context names `--pr <N>`. Table column counts are intact. |
| B3 | PASS | `SKILL.md:136` Required Input row. |
| B4 | PASS | `docs/user-guide/commands.md:368`: the syntax line has `[--pr <N>]`, in the same order as the argument-hint. |
| B5 | PASS | `test_skill_parse.py:94-99` covers 42, None, and the `--pr 0` ValueError. |
| C1 | PASS | `pr-submit.md:16-19` says "two activation paths". The hook item is removed and Programmatic is now item 2. |
| C2 | PASS | `pr-submit.md:89` reads "the sibling PR-review command." |
| C3 | PASS | The hook sentence is gone from `SKILL.md:189`. |
| C4 | PASS | `auggie-review.md:17-18` has two items, renumbered. |
| C5 | PASS | The hook example section is removed. The fences and headings around it are intact (`auggie-review.md:112-124`). |
| C6 | PASS (see F1) | `sc-auggie-review-protocol/SKILL.md:361` matches the command's Triggers (`auggie-review.md:17-18`). It does not match the command's own stale line `:160`. |
| C7 | PASS | `install_hooks.py:76-77`. |
| C8 | PASS | Staged deletion (`D ` in porcelain). `git grep 'test_hook_update\|_run_hook'` finds no importer. The `_run_hook` hits are separate local helpers in `tests/hooks/*`. |
| C9 | PASS | The `HOOK` constant and `_skill_and_hook_files` are removed. No reference remains in `test_static_grep.py`. |
| C10 | PASS | `test_validation_gate.py:45-46` uses `reject-workspace-writes.sh` and still asserts `is True`. |
| D1 | PASS | The `yes` field, the `--yes` argument and `yes=ns.yes` are removed. A repo-wide search for `.yes` and `yes=` finds only `cli/main.py:339`, the click `mcp` command's own `yes` parameter, which is unrelated. `SkillArgs` has no consumers outside `fsm.py`. |
| D2 | PASS | `state-machine.md:157` reads "(Wave 6 has no confirm step)". The rewrap leaves one 132-character line; MD013 is disabled in `.markdownlint.json`, so this is cosmetic only. |
| D3 | PASS | `test_skill_parse.py:102-105`. |
| E1 | PASS (see F1, F5) | New subsection at `CHANGELOG.md:7-19`. The #285 bullets at `:27` and `:30` are corrected as specified. Accuracy notes -> F1, F5. |
| AC2 | PASS (literal) | `git grep` finds only `CHANGELOG.md:16`. The pattern misses "hook-driven" at `auggie-review.md:160` -> F1. |
| AC3 | PASS | Only `test_skill_parse.py:103,105`. |
| AC4 | PASS | Every `gh repo view` that reads the base branch names `"$REPO"` (`pr-submit.md:51`, `SKILL.md:189`). The scripts do not read the base branch. |
| AC5 | PASS | `1318 passed, 1 xpassed, 5 warnings in 32.89s`. |
| AC6 | PASS | `ruff check`: "All checks passed!". `ruff format --check`: "6 files already formatted". `git diff HEAD --check` rc=0 and `git diff --cached --check` rc=0. `bash -n` OK on all four scripts. |
| AC7 | NOT RUN | BLOCKED, as the spec says (`make` is not installed). |
| AC8 | FAIL | F1, F2, F3, F5. |

## Findings

| # | Severity | Location | What is wrong | What it should be |
|---|---|---|---|---|
| F1 | IMPORTANT | `src/superclaude/commands/auggie-review.md:160` | A dead hook reference survives. The "Will Not" line still says "explicit invocation or hook-driven only". C4/C5 removed the hook path, so this contradicts the same file's Triggers (`:17-18`, direct + programmatic) and the updated skill wording at `sc-auggie-review-protocol/SKILL.md:361`. P3 says "Remove every reference", and the CHANGELOG `:16` bullet says the activation paths in `/sc:auggie-review` were removed. The spec's C-list and the AC2 grep pattern (`offer-pr-review\|PR-creation hook\|post-PR-create`) both miss "hook-driven". | Replace it with "explicit `/sc:auggie-review` invocation or a programmatic call from another `/sc:*` command only" (the C6 wording). Add the item to the spec (C11) and widen the AC2 pattern with `hook-driven`. |
| F2 | MINOR | `tests/pr_submit/test_static_grep.py:3-8` (edited by A8); also `:167` and `:231` | The edited module docstring still describes "T-104" as a live test ("T-104: every `gh` command in the skill sources is REPO-scoped ..."). `test_t104_every_gh_call_is_repo_scoped` was deleted in `970c1236`, and its only helper, `_skill_and_hook_files`, is removed here because nothing calls it. `:167` ("T-104 proves no UNSCOPED gh command exists") and `:231` ("The broad test_t104 already scans them via SKILL_DIR.rglob") are false for the same reason. The spec's A8 also names a "T-104 docstring" that does not exist; the implementer correctly edited T-105 (`:173`). | Say that T-104 was retired in `970c1236` (or drop the T-104 paragraph), and correct `:167` and `:231`. Change the spec's A8 from "T-104 docstring" to "T-105 docstring". (Pre-existing staleness, but the A8 edit touched the sentence, so AC8 applies.) |
| F3 | MINOR | `tests/pr_submit/test_static_grep.py:478`, `:498`, `:516` | The D2 section header, the test docstring and the assertion message still call the origin-URL `sed` the "fallback" ("$REPO origin-URL resolution fallback (sed)", "the $REPO origin-URL fallback `sed` program", "no `sed -E '…'` origin-URL fallback found"). After A5 it is the primary resolution and `gh repo view` is the fallback. This contradicts A8's intent and the new test at `:532-534`. | Use "origin-URL resolution (sed)" / "the $REPO origin-URL `sed` program" / "no `sed -E '…'` origin-URL resolution found". |
| F4 | MINOR | `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:189` | The Wave 0 bullet adds "(or attach to `--pr <N>`)". Neither A1 nor B3 specifies it, and AC1 says nothing else changed. It also leaves "verify the returned URL's `owner/repo`" undefined for the attach case, where `gh pr create` returns no URL. The addition is reasonable, but it is outside the spec. | Record it in the spec as part of B3/A1. In the attach case, say the check runs on `gh pr view <N> --repo "$REPO" --json url`. Alternatively, remove the parenthetical. |
| F5 | MINOR | `CHANGELOG.md:13` | The base-branch clause is attached to the helper-scripts sentence: "The four helper scripts (...) resolve in the same order when called without `--repo`, and the base branch is read with `gh repo view "$REPO"`." The scripts never read the base branch (it appears only in `SKILL.md:189` and `pr-submit.md:51`), so the sentence implies a script behaviour that does not exist. | Move the clause to the `/sc:pr-submit` sentence, e.g. "... uses `gh repo view` only when origin has no URL, and reads the base branch with `gh repo view "$REPO"`." |

## Self-Audit

What I checked, with tools:

- I read the full diff (`git diff HEAD`, 19 files) and the porcelain status. Every hunk maps to an item in A1-E1. There are no extra hunks outside the spec's files. The only extra content is inside a specified hunk (F4).
- Scripts: `bash -n` on all four. I listed every `REPO` line in each script and in `git show HEAD:` for each script. I ran the new `${REPO:-$(...)}` expansion with REPO empty and REPO preset; quoting and braces are correct and there is no `}` inside the sed program.
- New ordering test: I replayed its predicate on the HEAD and worktree copies of each script. It fails on all four HEAD copies and passes on all four worktree copies. Nothing was mutated.
- Parser: I probed `--pr 42`, the default, `--pr 0`, `--pr -3` and `--yes`. I read `fsm.py:50-133` for agreement between the dataclass, the parser and the return. I searched the repo for `.yes`/`yes=` readers and `SkillArgs` consumers.
- Wave 0 consistency: origin first; the `gh repo view` fallback only when there is no origin URL; base via `"$REPO"`; checks before `gh pr create`; URL verified after. All hold. Observation (not a defect; the spec requires both): if origin has no URL and the fallback runs, the next step ("confirm origin = `$REPO`") cannot pass, so in Wave 0 the fallback always ends in HALT. That outcome is safe.
- Accuracy: CLAUDE.md A7 is true. The `reflect contract-status` claim is true (`cli/reflect/commands.py:195` prints ` --pr {diagnosis.pr_number}`), and the old parser rejected `--pr` (argparse `parse_args`, not `parse_known_args`). The command and skill activation paths agree. SKILL.md:361 agrees with auggie-review.md:17-18, but not with :160 (F1).
- Greps: AC2 and AC3 as written. I also grepped for `hook-driven` (which found F1), `gh repo view`, `defaultBranchRef` and `T-104`.
- Gates: pytest `1318 passed, 1 xpassed`. ruff check and ruff format are clean on the 6 changed .py files. `git diff HEAD --check` and `--cached --check` are clean.

Not counted as defects:
- The 132-character line at `state-machine.md:158` (MD013 is disabled).
- The CHANGELOG `:16` Removed list does not mention the SKILL.md Wave 0 sentence, the `pr-submit.md` Related Commands parenthetical, or the test constants. It is a summary, not a false statement.
- AC7 is blocked (no `make`).

Pre-existing and out of scope: `refs/augment-poll.md:9` and `refs/ci-poll.md:10` say "T-104 greps for it", but that test was retired in `970c1236`.

**Confidence:** Verified: 31/32 | Unverifiable: 1 (AC7, no `make`) | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 6 | Grep: 0 (searches done through git grep in Bash) | Glob: 0 | Bash: 16 | tavily/web: 0
