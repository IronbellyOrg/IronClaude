# Q33 validation (Stage 1 and Stage 2), 2026-11-14

Base: branch `ironbelly/sweep-git-fix` at `47e1e6962` (PR #539 head), tree clean at start. git 2.47.3.
Experiments: `/tmp/ironclaude-q33/repro.sh`, `repro2.sh`, `repro3.sh`, `repro4.sh`, `measure.py` (throwaway repos deleted after each run; a marker file proves a command ran).

## Stage 1: T2 root cause, per route (sweep's exact call: `git --no-optional-locks -C <wt> status --porcelain=v1 -z --branch --untracked-files=all`, `GIT_OPTIONAL_LOCKS=0`)

| # | Route | Plain call | With `-c core.fsmonitor=false` | Verdict |
|---|---|---|---|---|
| 1 | `core.fsmonitor` in shared `.git/config` | ran | stopped | CONFIRMED |
| 2 | `filter.<d>.clean` + `.gitattributes` | ran | ran | CONFIRMED |
| 3 | `filter.<d>.process` | ran | ran | CONFIRMED |
| 4 | `include.path` to a file setting `core.fsmonitor` | ran | stopped | CONFIRMED |
| 5 | per-worktree config (`extensions.worktreeConfig`) | ran | stopped | CONFIRMED |
| 6 | `GIT_CONFIG_COUNT/KEY_n/VALUE_n` env | ran | stopped (command-line `-c` wins over env) | CONFIRMED |
| 6b | `GIT_CONFIG_PARAMETERS` env | ran | stopped | CONFIRMED (extra) |
| 7a | clone carries no config | status in clone ran nothing | n/a | CONFIRMED |
| 7b | `.gitattributes` alone | nothing runs | n/a | CONFIRMED |
| 7c | other-user repository | `status` exits 128 "dubious ownership" (tested with `GIT_TEST_ASSUME_DIFFERENT_OWNER=1`); `git config --list` exits 0 and silently leaves out the repo config | n/a | CONFIRMED; note the config reader does not fail there |
| 8 (new) | submodule's own config: `core.fsmonitor` in a submodule | ran (outer status starts a child status in the submodule) | stopped (the `-c` is passed down) | NEW ROUTE, confirmed |
| 9 (new) | submodule-local `filter.<d>.clean` | ran | ran | NEW ROUTE, confirmed; invisible to the outer worktree's `git config --list` (count 0) |

Host facts re-verified: `/etc/gitconfig` sets `filter.lfs.clean/smudge/process/required`; all 31 listed worktrees therefore define a filter driver, none selects it. Host environment carries `GIT_CONFIG_COUNT=2` with keys `credential.interactive` and `credential.guiPrompt` (values not read).

Readers that decide without running code (core.fsmonitor set in the shared config):
- `git config --show-origin --list [-z]`, `rev-parse`, `worktree list`: nothing ran.
- `git ls-files` and `git check-attr`: RAN the fsmonitor command. With `-c core.fsmonitor=false` both are quiet. Neither starts a filter (`ls-files`, `ls-files --eol`, `check-attr filter` all quiet with a clean filter set).
- So "could actually run" is decidable for routes 1 to 6b without running repository code, but only if every decision call carries `-c core.fsmonitor=false`.

Code facts (file:line, read on this head):
- `_git` seam: `probes.py:301-326` (argv `git --no-optional-locks -C <cwd> *args`, env copy plus `GIT_OPTIONAL_LOCKS=0`, `check_git_args` first at :307).
- `ALLOWED_GIT`: `probes.py:65-67`, one template (the status call). `check_git_args`: `probes.py:227-229` (exact match).
- Only caller: `_read_worktree` `probes.py:938`. It already turns a failed worktree into `SourceCoverage(name, "unscanned", None, reason)` via `_failed_worktree` (`probes.py:954-958`). That row mechanism exists; a new reason string needs no new JSON key.
- `paths` list: built by `_worktree_paths` (`probes.py:1203-1214`, root plus every `worktree ps` path), used at `:1257` (git status), `:1262` (contract allow-list), `:1263` (transcript scan). Git-only refusal must be inside `_read_worktree`, not by filtering `paths`.
- Pinned tests: `tests/sweep/test_probes_allowlist.py:364` (`ALLOWED_GIT == (GIT_STATUS,)`), `:503` (exact argv), `:594` (argv prefix per path); `tests/sweep/conftest.py:71` (fake records argv); `tests/sweep/test_readonly.py:85` (`argv[1]`), `:156`, `:453` (`argv[:3] == [git, --no-optional-locks, -C]`), `:514` (builds its own argv from `ALLOWED_GIT[0]`). Reason text pinned: `test_probes_allowlist.py:1499`, `test_classify.py:1655` ("worktree not readable").
- NFR-014 in `docs/designs/orchestrator-mode.md:143` and rows 66/816/838: about the ORCA allow-list (ten templates, `--include-remote`). The git list is a separate one-entry tuple; the doc names no git "owner-signed" text beyond the `ALLOWED_GIT` comment.

## Stage 1: T1 (Augment, probes.py:1052)

Code (probes.py:1050-1056): `workers` is the list after dropping non-object entries; `more = page.hasMore is True`; `truncated` is set when `len(workers) >= 100 or more`.
Reproduction (temporary test, removed): 99 objects plus one non-object string, `page: {limit: 100, hasMore: False}` -> `inp.truncated` is False. Expected True: the module's own rule is "a full page sets truncated" (test at `test_probes_allowlist.py:1206`).
Verdict: REAL but narrow. Real Orca replies carry `hasMore` (captured fixture line 393; golden says it is true in the live reply), so truncation is normally caught by `more`. The gap is a full 100-row page with a malformed entry and `hasMore` false or absent. Fix is one expression: count `len(raw)` when `raw` is a list, not `len(workers)`. The dropped malformed entry is also silent today (no row says so); that is a separate wording matter, not touched.

## Stage 2: design validation

(a) Decidable without running repository code? Routes 1 to 6b yes (`git config --show-origin --list -z` run with the sweep's own environment, plus `-c core.fsmonitor=false` on `ls-files` and `check-attr --stdin -z filter`). Filter selection needs `ls-files` piped into `check-attr`, so the seam needs stdin support. Routes 8 and 9 (submodules): NO, the outer config does not show them. Dubious ownership: the reader exits 0 with partial config, but status refuses by itself, so nothing runs.
(b) Without a new JSON key? YES: the `unscanned` source row exists (`probes.py:954-958`); only a reason string is new.
(c) Measured on this host (`orca-ide worktree ps --json`, 31 listed, 31 distinct paths, truncated false): refused by the proposed rule 0 of 31. Live `core.fsmonitor`: 0. Filter selected by a tracked path: 0 (the system-wide `lfs` driver is defined in all 31, selected in none). Worktrees with submodules: 21 of 31 (route 8/9 exposure). Unreadable or missing: 0.
(d) Tests that must change: `test_probes_allowlist.py:364` and `:503` and `:594`, `conftest.py:71`, `test_readonly.py:85/:156/:453` if `-c core.fsmonitor=false` goes before `-C`; if it goes after `-C <path>`, `:85/:156/:453` still pass and only `:364`, `:503`, `:594`, `conftest.py` change. New reason string needs one new test, no golden change.
(e) Cost of a refusal: the worktree loses its git facts (changed paths, branch, dirty) and shows as `unscanned`; its package folders are still read from disk.
(f) Holes found: (1) routes 8 and 9 (submodule-local config) are not seen by the proposed config read; (2) `-c diff.ignoreSubmodules=all` does NOT close route 9 (repo `submodule.<name>.ignore=none` overrides it, repro4 H1); only the flag `--ignore-submodules=all` does (H2), and that is a change to the status argv template; (3) `core.fsmonitor=true` (built-in daemon) is a spawn too: refuse or neutralise it, the "is a program named" test alone would miss it (daemon start was not observed in this temp repo, UNVERIFIED).

Alternative (neutralise): `-c core.fsmonitor=false` cleanly stops routes 1, 4, 5, 6, 6b and the fsmonitor part of 8, with no loss of facts (fsmonitor is only a speed cache). Blanking filters (`-c filter.<d>.clean=`) stops routes 2 and 3 only for names read from the config, and CORRUPTS facts: with a real transforming filter, blanking makes status report a false ` M a.up` (repro3 S2). Unknown submodule filter names cannot be listed from outside. So pure neutralise is refuted for filters; neutralise is right for fsmonitor only.

## Verdict: VALIDATED WITH AMENDMENTS, but gate STOP (owner choice needed)

Amendments:
1. Neutralise fsmonitor (add `-c core.fsmonitor=false`) instead of refusing on it; refuse only when a filter driver with a non-empty `clean` or `process` is selected by a tracked path (`ls-files` + `check-attr`), or the config cannot be read, or the filter check is unclear.
2. The two decision calls (`config --show-origin --list -z`, `ls-files -z`, `check-attr --stdin -z filter`) are new allow-list entries, all read-only, all with `-c core.fsmonitor=false`.
3. Route 9 (submodule-local filter) needs a choice: see the owner question.
4. Close T1 with `len(raw)`.

Owner choice that blocks implementation (two genuinely different designs for submodules):
- A: add `--ignore-submodules=all` to the status template. Closes 8 and 9 completely and with no recursion. Cost: a submodule's own dirt is no longer reported (the sweep only uses changed paths for package activity under `.dev/tasks/`, so the practical loss looks small; 21 of 31 worktrees have submodules). Changes the pinned status argv (`test_probes_allowlist.py:364`, `:503`, `test_readonly.py:30`).
- B: leave submodule routes open and document them as a residual hole.
- C: also read each submodule's config and refuse on its filters (more code, more allow-list entries).
