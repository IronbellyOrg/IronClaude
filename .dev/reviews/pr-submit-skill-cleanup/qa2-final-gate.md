# QA Report — Final Gate (Round 2): pr-submit-skill-cleanup

**Date:** 2026-10-24
**Phase:** fix-cycle / final gate (report-only, fix_authorization = false)
**Base:** HEAD 070399eb + uncommitted working tree

---

## Verdict: FAIL

One IMPORTANT finding (F1). In all four helper scripts, the origin-first line aborts the script under `set -euo pipefail` when origin has no URL, so the `gh repo view` fallback and the "could not resolve target repo" message cannot run. All 11 round-1 findings are fixed. Every other spec item is present and accurate. pytest, ruff and `git diff --check` are clean.

## Checks

| # | Check | Status | Evidence |
|---|---|---|---|
| 1 | Spec items A1-A11 present | FAIL (A5, see F1) | A1 `SKILL.md:189`: origin first, using the same sed program as the scripts (compared byte-for-byte); `gh repo view` only "if origin has no URL"; base from `gh repo view "$REPO" --json defaultBranchRef`; checks "BEFORE creating anything"; URL verified after. A2 `SKILL.md:143-146`. A3 `pr-submit.md:28`. A4 `pr-submit.md:51`. A5: the order is swapped in all four scripts and the comments are updated, but the fallback cannot run (F1). A6 `test_static_grep.py:529-548`. A7 `CLAUDE.md:46`. A8 `test_pre_pr_checks.py:6-7`. A9 `fsm.py:479-481`. A10 `augment-poll.md:8-9`, `ci-poll.md:8-10`. A11: every sub-item is present (module docstring `:3-9`, `_REPO_RESOLVE` comment `:32-34`, CORE_PURE comment `:44`, T-105 docstring and assert `:164-176`, T-1101 docstring `:227-228`, D2 header `:475`, docstring `:495`, message `:513`). |
| 2 | B1-B6 present | PASS | B1 `fsm.py:64,97,118-119,132`. A parser probe gave `--pr 42` → 42, default None, `--pr 0`/`-3` → ValueError "--pr must be a positive PR number", `--pr abc` → SystemExit 2. B2 `pr-submit.md:8,26,53,76`. B3 `SKILL.md:136`. B4 `docs/user-guide/commands.md:368`. B5 `test_skill_parse.py:94-99`. B6 `SKILL.md:189` ("With `--pr <N>`, skip `gh pr create` … `gh pr view <N> --repo "$REPO" --json url`"). |
| 3 | C1-C11 present | PASS | C1 `pr-submit.md:16-19` ("two activation paths", items 1-2). C2 `pr-submit.md:89`. C3: the hook sentence is gone from `SKILL.md:189`. C4 `auggie-review.md:17-18` (items 1-2). C5: the example section is removed and the fences around it are intact (`auggie-review.md:108-126`). C6 `sc-auggie-review-protocol/SKILL.md:361`. C7 `install_hooks.py:76-77`. C8: staged `D` in porcelain, no importer. C9: `HOOK` and `_skill_and_hook_files` are gone; `_command_lines`/`_repo_scoped` keep callers (`:185,233,234,325,566,577`). C10 `test_validation_gate.py:45-46`. C11 `auggie-review.md:160`. |
| 4 | D1-D3 present | PASS | D1: `git grep '\.yes\b\|yes=ns'` finds nothing in pr_submit or tests. D2 `state-machine.md:157-158`. D3 `test_skill_parse.py:102-105`; the probe gives `--yes` → SystemExit 2. |
| 5 | E1 / E1' present | PASS (accuracy, see F1) | New subsection `CHANGELOG.md:7-17`. The #285 bullets at `:25` and `:27` are corrected. E1': the base-branch clause is now on the `/sc:pr-submit` sentence (`:11`). The scripts sentence on `:11` is untrue in the fallback case until F1 is fixed. |
| 6 | Nothing else changed (AC1) | PASS | `git diff HEAD --stat`: 21 files. Every hunk maps to an item in A1-E1'. The only untracked files are the spec and `.dev/reviews/`. |
| 7 | Tables and numbering intact | PASS | `pr-submit.md` Required Input and Options rows have 3 cells each, including the new `--pr <N>` row. Both activation lists are numbered 1-2. CHANGELOG heading levels are consistent (`###` then `####`). |
| 8 | Sweep: hook phrases | PASS | `git grep -i 'offer-pr-review\|PR-creation hook\|post-PR-create\|hook-driven\|three activation paths\|post-pr-creation'` (excluding `.dev`/`.claude`) finds only `CHANGELOG.md:16`, the removal record. No `plugins/` mirror of pr-submit or auggie-review exists (`git ls-files plugins`). |
| 9 | Sweep: `--yes` | PASS | In pr-submit scope, only the CHANGELOG removal lines and the D3 test. Every other hit belongs to a different command (`sprint`, `mcp`, `swarm-wizard`). |
| 10 | Sweep: target resolution and base branch | FAIL (F1) | Every `gh repo view` hit is a fallback, uses `"$REPO"`, or is the unchanged CLAUDE.md pre-PR check 1 (spec section 3). `defaultBranchRef`: `pr-submit.md:51` and `SKILL.md:189` both name `"$REPO"`; `fsm.py:527` is prose. The prose is correct; the script behaviour is not (F1). |
| 11 | Sweep: `--pr <N>` attaches | PASS | The `reflect/commands.py:194-200` and `contract_setup/diagnosis.py:380` READY strings `/sc:pr-submit --monitor 3 --pr <N>` now parse (probe). |
| 12 | Accuracy: SKILL.md Wave 0 | PASS | Matches the scripts' sed, the STOP rule (`:143-146`) and the `--pr` attach path. Attach-mode rebase wording noted as an observation. |
| 13 | Accuracy: CLAUDE.md sentence | PASS | "`<repo>` comes from the `origin` remote" matches Wave 0. |
| 14 | Accuracy: CHANGELOG | FAIL (F1) | `:11` "before anything is created" matches Wave 0; the base-branch clause is placed correctly; `:12` matches `reflect/commands.py:194-200`. The scripts' "same order" claim fails in practice because of F1. `:16-17` are accurate. |
| 15 | Accuracy: test docstrings | PASS | `test_pre_pr_checks.py:6-7`, `test_static_grep.py:3-9` (970c1236 does delete `test_t104_every_gh_call_is_repo_scoped`, per `git show`), `:32-34`, `:164-172`, `:225-228`, `:495`, `:529-531` all match the code. |
| 16 | Accuracy: `fsm.py` docstring, no `gh`/`git` tokens | PASS | `fsm.py:479-481` reads "the origin remote URL first, else the host CLI's default repo". `grep -n -w -E 'gh\|git' fsm.py` finds nothing. T-N50 passes in the suite. |
| 17 | `bash -n` on the four scripts | PASS | OK on all four. |
| 18 | `${REPO:-$(...)}` quoting | PASS (quoting) / FAIL (exit status, F1) | The single quotes sit inside `$(...)`, so they get a fresh quoting context; the sed program has no `}`. With REPO empty the line gives `IronbellyOrg/IronClaude`; with REPO=`x/y` it keeps `x/y`. The exit status of the pipeline, however, aborts the script under `set -e` (F1). |
| 19 | pytest | PASS | `1318 passed, 1 xpassed, 5 warnings in 26.94s` |
| 20 | ruff | PASS | `ruff check`: "All checks passed!"; `ruff format --check`: "6 files already formatted" (install_hooks.py, fsm.py, 4 test files). |
| 21 | `git diff HEAD --check` | PASS | rc=0; `git diff --cached --check` rc=0. |
| 22 | AC7 `make verify-sync` | NOT RUN | BLOCKED, as the spec states (`make` is not installed). |

## Round-1 Finding Re-check

| Report | Finding | Status | Evidence |
|---|---|---|---|
| qa-spec-conformance | F1 `auggie-review.md:160` hook-driven | FIXED | `:160` now reads "explicit `/sc:auggie-review` invocation or a programmatic call from another `/sc:*` command only". Spec C11 was added and AC2 now includes `hook-driven`. |
| qa-spec-conformance | F2 stale T-104 text in `test_static_grep.py` | FIXED | `:3-9` names T-105/T-1101/D2/D3 and notes T-104 was retired in 970c1236 (verified by `git show 970c1236`). The old `:167` and `:231` claims are gone (`:166-172`, `:227-228`). Spec A11 records "T-105, not T-104". |
| qa-spec-conformance | F3 D2 "fallback" wording | FIXED | `:475`, `:495` and `:513` all say "origin-URL resolution" or "origin-URL `sed` program". |
| qa-spec-conformance | F4 unspecified `--pr` parenthetical in Wave 0 | FIXED | Spec B6 added; `SKILL.md:189` defines the attach URL check through `gh pr view <N> --repo "$REPO" --json url`. |
| qa-spec-conformance | F5 base-branch clause on the scripts sentence | FIXED | `CHANGELOG.md:11`: the clause is now on the `/sc:pr-submit` sentence. |
| qa-orphan-sweep | F1 `auggie-review.md:160` | FIXED | Same as conformance F1. |
| qa-orphan-sweep | F2 `fsm.py` `pr_target_ok` docstring | FIXED | `:479-481` gives the new order with no `gh`/`git` tokens. |
| qa-orphan-sweep | F3 `augment-poll.md:8` nameWithOwner | FIXED | `:8-9` reads "origin's `owner/repo`, parsed from `git remote get-url origin`"; the T-104 claim is gone. |
| qa-orphan-sweep | F4 `ci-poll.md:8-9` | FIXED | `:8-10`, same wording. |
| qa-orphan-sweep | F5 `_REPO_RESOLVE` comment | FIXED | `test_static_grep.py:32-34` calls it "the fallback when the origin remote has no URL". |
| qa-orphan-sweep | F6 T-105 assertion | FIXED | `:173-176` asserts `"git remote get-url origin" in script_text`, with a matching message. |

## Findings

| # | Severity | Location | What is wrong | What it should be |
|---|---|---|---|---|
| F1 | IMPORTANT | `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh:19`, `poll-ci-checks.sh:34`, `reply-resolve-thread.sh:55`, `retrigger-review.sh:47` | The `gh repo view` fallback cannot run. All four scripts use `set -euo pipefail` (`:4`, `:16`, `:19`, `:19`). The new first line puts the `git remote get-url origin \| sed -E '…'` pipeline inside a plain assignment, with no `\|\| true`. When origin has no URL (the exact case the fallback exists for), `git` exits 2. Under `pipefail` the pipeline returns 2, the assignment returns 2, and `set -e` kills the script. The next line, `[ -n "$REPO" ] \|\| REPO="$(gh repo view …)"`, and the `die "could not resolve target repo (pass --repo <owner/repo>)"` message after it never run. The script exits with code 2 and prints nothing. At HEAD the first line was `$(gh repo view … \|\| true)`, which could not fail, so this regression comes from the reorder. Evidence: I ran the real scripts with an exported `git` function that fails (`return 2`) and a stub `gh` that prints `fallback/repo`. All four exited with `rc=2` and empty output. A control run with a working `git` stub resolved `acme/widgets` and reached the `gh api … repos/acme/widgets/issues/1/comments` call. The same two lines in the HEAD order reached `REPO=fallback/repo`, rc 0. This breaks spec P1/A5 ("`gh repo view` only as a fallback when origin has no URL"). It also makes the CHANGELOG `:11` sentence ("The four helper scripts … resolve the repo in the same order when called without `--repo`") untrue for the fallback case. No test catches it: `test_repo_resolution_prefers_origin_over_gh_default` (`test_static_grep.py:529`) only compares line numbers, and every subprocess test passes `--repo`. | Make the origin pipeline unable to fail inside the substitution, mirroring the old first line: `REPO="${REPO:-$(git remote get-url origin 2>/dev/null \| sed -E '<unchanged program>' \|\| true)}"` in all four scripts. The D2 sed-extraction regex and the ordering test still match that form. Also add a test that runs one script with a failing `git` stub first on `PATH` and asserts it reaches the `gh repo view` fallback, or the `could not resolve target repo` message when `gh` also returns nothing. |

### Observations (not counted as defects)

- `SKILL.md:189`: with `--pr <N>`, the sentence "BEFORE creating anything: confirm … and rebase if behind `origin/<base>`" still applies to an already-pushed PR head. The text does not say whether an attach-mode rebase is skipped or followed by a push. B6 specifies only "skip `gh pr create` … check the URL", so this does not go beyond the spec. It is a possible follow-up clarification.
- `SKILL.md:189`: "byte-for-byte identical to today (AC-1)" and "Explicit 0 = open PR only (byte-identical to today)" are claims from the original monitor spec, carried over unchanged. They compare L0 with the no-monitor behaviour, not with the target-resolution order, and spec section 3 leaves the surrounding text alone.
- `refs/state-machine.md:158` is one line of about 132 characters. MD013 is disabled; round 1 already accepted it.
- `refs/review-retrigger.md:8,11,29` still name T-104. Spec section 3 keeps this on purpose.

## Self-Audit

There is one finding (F1), so the zero-finding justification does not apply. All 11 round-1 findings are fixed. F1 is new. Neither round-1 report caught it because both ran the `${REPO:-…}` line only with a working origin remote.

What I checked, with tools:

- I read the full spec, including Revision 1, and both round-1 reports. I read the full `git diff HEAD` (21 files) and `git status --porcelain`, and mapped every hunk to an item.
- Scripts: `bash -n` on all four. I listed every `REPO=` line and every `set` line. Then I reproduced F1 three ways:
  - the isolated lines, in the new and the HEAD order;
  - the real scripts with failing `git` and stub `gh`/`jq` shell functions, which gave `rc=2` with empty output for all four;
  - a control run with a working `git` stub, which reached `gh api`.
  Nothing outside the worktree was touched. The stubs were in-process shell functions, so no files were written.
- Parser: probed `--pr 42`, the default, `0`, `-3`, `abc` and `--yes`.
- Sweeps: `git grep` (excluding `.dev`/`.claude`) for the hook phrases, `--yes`, `gh repo view`, `defaultBranchRef`, `nameWithOwner` and `T-104`. Also `git ls-files plugins` for mirrors, and `.yes`/`yes=ns` readers.
- History: `git show 970c1236` confirms `test_t104_every_gh_call_is_repo_scoped` was deleted there. `git log` confirms the hook script existed before.
- Gates: pytest, ruff check, ruff format --check, and `git diff HEAD --check` / `--cached --check`, with the results recorded above.

**Confidence:** Verified: 21/22 | Unverifiable: 1 (AC7, no `make`) | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 7 | Grep: 0 (searched with git grep/grep via Bash) | Glob: 0 | Bash: 10 | tavily/web: 0 (no external lookup needed)
