# QA Report - Research Gate, gap-fill FINAL re-check round 2 (third review; lens: evidence-quality)

**Topic:** GitHub issue watcher MDTM task build
**Date:** 2026-11-08 (session env date 2026-11-07 per agent context; no effect on findings)
**Phase:** research-gate (fix-cycle re-check, report only, fix_authorization: false)
**Fix cycle:** 2 (third and last review)
**Scope:** research/06-gap-fill-decisions.md (DF-41 to DF-59, Tables 1.3, 1.4, 1.6, phase plan, lookup table), research-notes.md line 26
**Previous reports:** qa/qa-research-evidence-report.md (round 0), qa/qa-research-evidence-report-r2.md (E1 IMPORTANT open; E2-E6 MINOR)

## Progress log

- Header written. Read file 06 in full (314 lines), r2 report, research-notes.md lines 15-54, task dir listing. Spot-checks next.
- Two batched read-only Bash runs plus about 20 Read/Grep calls done (design, spec, repo, task-builder SKILL.md, template, pre-commit, CI, gh help, uv/ruff/pytest probes). Findings below.

---

## Section A. Previous blocking item E1 (DF-07 authorization): resolution check

| Check | Result | Evidence |
|---|---|---|
| Source cited as the coordinator brief | RESOLVED | 06 line 12 defines `[SOURCE: coordinator brief]` (Orca task `task_0b795fb7069a`, dispatch `ctx_58a8c8b54cbd`) as a brief, not a repo text, and not UNVERIFIED. DF-07 (line 30) cites it for steps 6 and 7 (run with `/task`, open PR with `/sc:pr-submit`). I could not read the brief itself (not in the repo): UNVERIFIABLE by me, accepted as the cited source per the review brief |
| Stop rule | RESOLVED | DF-07 item (4): HALT on any commit or hook failure, write the error to the Task Log, stop, no fix-and-retry, never `--no-verify`/`--no-gpg-sign`/`git add -A`, no push, no PR. Scope is one local commit |
| `research-notes.md` no longer contradicts | RESOLVED | `research-notes.md:26` now reads "exactly one local checkpoint commit item before the POST reflect gate (research/06 DF-07)". Grep for `commit\|authoriz\|DF-07` over the file returns only line 26 |
| Preconditions DF-07 states | HOLD | `git rev-parse HEAD` = `e8db2fe660d9104cbe8cdbcdc6f2c967f4994f4b`; `git rev-parse --verify origin/master` = `0b8a5801d75f159bcbca7087b99507c2a50d8dba`; `git merge-base HEAD origin/master` = `e8db2fe6...` (equals HEAD); staged files 83, all under `.dev/tasks/`, none outside; hooks dir holds only `*.sample` files, so no local hook runs |
| Residuals | notes only | Commit authority is inferred ("therefore") from steps 6 and 7, not quoted as an explicit commit instruction. The DEVIATION cell cites "BUILD_REQUEST 'no commit step'", but no BUILD_REQUEST exists in this task dir (`research/04:208` says the same). `research/04` lines 106 and 174 still say "no commit/PR"; 06 line 1 states it supersedes 01-05. See M5 |

## Section B. Spot-check ledger (about 56 distinct cites re-read)

| # | Claim in 06 | Check | Result |
|---|---|---|---|
| 1 | HEAD, origin/master, merge-base SHAs (DF-07) | `git rev-parse` x3 | HOLDS |
| 2 | 83 staged `.dev/tasks` files, none elsewhere | `git diff --cached --name-only` | HOLDS |
| 3 | design and spec are untracked; D 935 lines, S 515 lines | `git status`, `wc -l` | HOLDS |
| 4 | D 807-827 is the Defaults table (timeouts, caps, state dir) | Read | HOLDS |
| 5 | D 892 AC-19 text; D 896 AC-23 | Read | HOLDS |
| 6 | D 399 `audit.jsonl` "every exit of `once` and `reset`" | Read | HOLDS |
| 7 | D 545-549 (G3 to G7) | Read and grep: G3 `EVENTS_JQ` is line 545, G4 `MARKER_JQ` is line 546, G5 547, G6 548, G7 549 | DF-14 (547-548), DF-20 (G2 at 544), DF-28 (554) hold; DF-18 and DF-21 transposed 545/546 (M1) |
| 8 | D 244 ends "`cli.py` imports the package lazily from `main.py`" | Read | HOLDS (DF-29) |
| 9 | D 102 (C21) "mandatory on every G2 to G7 argv" | Read | HOLDS (DF-28) |
| 10 | D 265 `run(self, argv, timeout)`; D 625 `cwd=worktree`; D 222 `check_origin(runner, worktree, timeout)`; D 843 `git -C` argv; D 317, 329 | Read | HOLDS (DF-01) |
| 11 | D 777 `FakeClock(now, mono)`, D 778 `FakeLauncher`, D 779 `CrashingStore(real, crash_at=...)`; D 297, 298, 295, 776 | Read | HOLDS (DF-24, DF-48) |
| 12 | D 745 `slo_numbers(lines, doc, now)` vs D 224 `(lines, store, now)` | Read | HOLDS (DF-25) |
| 13 | D 711 `issue` optional on warning lines; D 701-716 key table; D 718 `ValueError`; D 722 `stderr_fallback(reason, exit)`; D 720 exit-75 appends without rotation | Read | HOLDS (DF-03, DF-57) |
| 14 | D 441 migrated store saved; D 449 unparseable `dry-run.json`; D 503 skew; D 351 warning at >= 80; D 714-715 keys | Read | HOLDS (DF-17, DF-22) |
| 15 | D 476-490 T-1..T-13; "any other pair raises" at D 492 | Read | HOLDS: T-1 is from `(none)` only, T-3 sits inside `record.fail`, so DF-43 is a real gap |
| 16 | D 525-531 C1 to C5 | Read | HOLDS: Table 1.3 triggers match each row |
| 17 | D 571, 572, 575 paging and incomplete rules | Read | HOLDS (DF-02) |
| 18 | D 693 "seeded `random.Random(331)` loop of 2,000 draws" and `property_based` tag | Read | HOLDS; but DF-12 tags seed and draws as [PROPOSAL] (M3) |
| 19 | D 768 "Not changed" list; D 95 (C14); D 93 (C12) | Read | HOLDS |
| 20 | D 238-239 import rules (`github` may import `predicates`; `record` may not import `audit`) | Read | HOLDS (DF-21, DF-42) |
| 21 | S reason table S 332-358 holds 52 names | Counted row by row: 6,1,5,5,2,2,1,3,3,2,1,2,2,2,1,1,1,2,1,1,1,2,2,1,2 | HOLDS; 52 + five proposals (`marker_unreadable`, `edits_unreadable`, `operator_reset`, `dry_run_shadow_reset`, `reset_refused`) = 57 |
| 22 | S 336 (exit-6 reasons are kind cycle), S 343, S 358 | Read | HOLDS |
| 23 | S 136, 161, 163-164, 181, 190-191, 196, 213 (5 reruns), 267, 297, 309, 366, 379, 384-395 | Read | HOLDS |
| 24 | `test.yml:12, 22, 29, 44-47, 106, 123, 131, 135, 137` | `sed -n` | HOLDS |
| 25 | `Makefile:13-15, 48-50, 109, 166, 356-358` | `sed -n` | HOLDS |
| 26 | `.pre-commit-config.yaml` lines 9, 11, 15, 17, 19, 21, 26-41, 47, 54-63, 74, 88, 98-103 | Read lines 1-66, `sed -n` | HOLDS (DF-32, DF-58) |
| 27 | `pyproject.toml:16, 50-54, 71, 114, 135` | `sed -n` | HOLDS |
| 28 | `main.py:547`, `559-561`, `564-565`, 565 lines; no `subprocess` or `which(` in `main.py` | `sed -n`, `wc -l`, grep | HOLDS (DF-29, DF-34) |
| 29 | `install_user_setup.py:35` `_ORCA_CLIS`; `:216` inside `try`; `:219` outside it | `sed -n 198,221p` | HOLDS (DF-36) |
| 30 | `FULL_ID` at `test_model_alias_policy.py:50`; test at `:137` | `sed -n` | HOLDS (DF-11; r2 E2 fixed) |
| 31 | `swarm/atomic.py:14` signature, `:33` `except Exception`, `os.replace`, `mkstemp` tmp name | Read | HOLDS: the one-shot `os.replace` patch in Table 1.3 C2 works and `SystemExit` leaves an orphan tmp file |
| 32 | `reflect/commands.py:222`, docstring 4-5; `cli/__init__.py:13`; `plugins/superclaude/` contents | `sed -n`, `ls` | HOLDS (DF-26) |
| 33 | `poll-augment-review.sh:57` `length <= 100` | file is `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh` | HOLDS (DF-19; 06 gives the bare name only) |
| 34 | `refs/claim.md:88` edits the earlier claim comment; both claim files exist | `sed -n`, `ls` | HOLDS (DF-16, DF-46) |
| 35 | `seed-brief.md:64` `--agent claude`; `spec-refactor-log.md:47, 81` | `sed -n` | HOLDS (DF-11) |
| 36 | `uvx --offline ruff@0.15.20 --version` | ran | `ruff 0.15.20`. HOLDS |
| 37 | bare `uv run ruff` is 0.17.3; `.venv/bin/ruff` absent; local Python 3.11.15 | ran `uv run --offline --no-sync ruff --version`, `ls`, `python --version` | HOLDS (r2's inference is now executed) |
| 38 | xdist resolves offline for G-3 | `uv run --offline --with "pytest-xdist>=3.5,<4"` | 3.8.0. HOLDS |
| 39 | G-1 exits 5 at P1 with a package and no tests (DF-56) | ran pytest on a temp package with an `__init__.py` and no tests, outside the repo | `no tests ran`, exit 5. HOLDS |
| 40 | Every G-2 file exists; `tests/pr_submit/__init__.py`, `tests/cli_portify/__init__.py`, `tests/cli_portify/test_cli.py` exist (DF-27) | `ls` | HOLDS |
| 41 | `tests/conftest.py` lines 14, 28, 82 (DF-39) | `sed -n` | HOLDS |
| 42 | `test_conflict_scripts.py:1555-1571` stub dir on PATH | `sed -n` | HOLDS |
| 43 | task-builder SKILL.md 1149-1152 (M4 minimum 2), 1164-1167, 1186-1187, 2140, 2223 | Read, `sed -n` | HOLDS |
| 44 | template I22 (797; standard row 807: intermediate 3, final 7, M4 2), I15 (635-636), F2 (422, item 428), M2 (1051, row 1056), 1100, I19 table 713-715 (8 and 10) | Read, grep | HOLDS; line 1110 is not what DF-08 says it is (M2) |
| 45 | `gh issue list --label strings`; `gh api` default method becomes POST with parameters | `gh ... --help` | HOLDS (DF-20 correctly tagged UNVERIFIED for comma splitting; DF-28) |
| 46 | `/usr/bin/env` exists; DF-23 mountinfo field layout | `ls -l`; kernel format (field 5 mount point, type after ` - `, octal escapes) | HOLDS |
| 47 | Table 1.6 arithmetic 4 x 6 + 7 + 2 = 33; DF-40 lists 24 yes rows | computed; compared with every DEVIATION cell | HOLDS (24 = DF-01..07, 09, 10, 12, 13, 17, 18, 20, 22, 24, 25, 27-29, 43, 50, 55, 57) |
| 48 | GraphQL drafts against the public schema | by knowledge only; no live call | consistent; stays [PROPOSAL, UNVERIFIED] as labelled |

## Section C. [PROPOSAL] and [UNVERIFIED] labelling (lens focus 3)

- `marker_unreadable`, `edits_unreadable` (DF-02, "Add two [PROPOSAL] reasons"), `operator_reset` (DF-03), `dry_run_shadow_reset` (DF-22), `reset_refused` (DF-57 "[PROPOSAL]"; DF-04 says its reason "is a [PROPOSAL] outside S 330-358"; DF-41 lists "the five proposals"): all labelled. The 52-to-57 count is consistent across DF-02, DF-22, DF-31, DF-41, P2.
- GraphQL drafts: Table 1.5 heading and DF-14 carry [PROPOSAL, UNVERIFIED]; the tests assert only `mutation` absence, the literal repository and a nullable `$after`.
- Also correctly tagged: DF-16, DF-18, DF-19, DF-20 ([UNVERIFIED] plus [PROPOSAL]), DF-23, DF-33, DF-35, DF-37 ([UNVERIFIED]), Table 1.4 State snapshot [PROPOSAL].
- Over-tagged: DF-12 calls seed 331 and 2,000 draws a [PROPOSAL]; D 693 fixes both (M3).
- Not carried: G5 required-field list. DF-18 defines required fields for G3 and G4 only, while DF-02 sends "a required field null" on G5 to `edits_unreadable`. A GraphQL comment by a deleted user has `author: null`, so a reader could make one such comment skip the issue for good (fail closed, safe, but unspecified) (M6).

## Items Reviewed (research-gate checklist, evidence-quality lens, applied to file 06)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | File inventory | PASS | `Status: Complete` at line 312 |
| 2 | Evidence density | PASS (Dense) | Every DF row carries source ids and D/S lines; 56 cite groups re-read, 53 hold exactly, 3 imprecise (M1, M2, M3) |
| 3 | Scope coverage | PASS | Section 3 lookup rows map every target file to D, S, repo anchors and DF rows; D 807-827 present on `github.py`, `launch.py`, `cycle.py` |
| 4 | Doc cross-validation tags | PASS | UNVERIFIED items tagged (Section C) |
| 5 | Contradiction resolution | PASS with notes | E1 contradiction removed; stale lines in research 04 and research-notes are superseded by 06 line 1 (M5) |
| 6 | Gap severity | PASS | No CRITICAL or IMPORTANT gap found; M1 to M7 are notes |
| 7 | Depth appropriateness | PASS | Tables 1.2 to 1.5 give runnable commands and recipes |
| 8 | Integration point coverage | PASS | DF-01, 29, 30, 36 verified against code |
| 9 | Pattern documentation | PASS | DF-29, 34, 35 |
| 10 | Incremental writing | UNVERIFIABLE | no write history |

## Summary

- Checks passed: 9 / 10. Failed: 0. Unverifiable: 1.
- Critical: 0. Important: 0. Minor: 7 (M1 to M7).
- Fixes applied: 0 (report only).

**Confidence:** Verified: 9/10 | Unverifiable: 1 | Unchecked: 0 | Confidence: 100.0% of checkable items (9/9).

**Tool engagement:** Read: 14 | Grep: 8 | Glob: 2 | Bash: 5 (two batched read-only scripts under a private `/tmp` directory with cleanup trap, plus three single read-only commands: gh help and atomic.py, ruff and python versions, pytest empty-package probe). No Tavily or web tools used; no external-web claim needed checking.

**UNCHECKED:** none. **UNVERIFIABLE:** item 10 (no per-write history); the coordinator brief text behind DF-07 (not in the repo); the GraphQL field names (no live `gh api graphql` call made).

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| M1 | MINOR | 06 DF-18 (line 145), DF-21 (line 148) | The two design line numbers are swapped. DF-18 cites "G3 (projection D 546)"; the G3 projection (`EVENTS_JQ`) is D 545. DF-21 cites `MARKER_JQ` at "D 545"; it is D 546 (G4). The claims are true, the locators are off by one. | Swap the numbers. Not rechecked later |
| M2 | MINOR | 06 DF-08 (line 31), Table 1.6 M4 row | DF-08 says M4 is split by document "because together they exceed the 1,000-line partition threshold (template line 1110)". Template line 1110 says "minimum 2, partitioned to 3-4 if source docs exceed 1000 lines total" (D 935 + S 515 = 1,450), and line 1106 says standard intensity is 2. 06 picks 2 and cites the rule that points to 3-4, and does not list this in the Open Questions (DF-40 lists only 2140 vs I19). Each of the two agents stays under 1,000 source lines, so the choice is defensible. | Reword to "template 1106 gives 2 at standard; 1110 would give 3-4 above 1,000 source lines; 2 per-document agents chosen" and add it to the Open Questions beside the 2140 tension |
| M3 | MINOR | 06 DF-12 (line 35) | "[PROPOSAL: seed 331 and 2,000 draws]": D 693 states both values. | Drop the tag; keep the marker deviation only |
| M4 | MINOR | 06 DF-57 (line 191), DF-03/DF-41 | The DEVIATION cell names the exit-6 reasons written on `warning` lines but not `lock_held` (spec kind cycle, S 340, exit 75), which DF-57 also writes on a warning line. `REASON_TABLE` is typed `(kind, exit)`, and the kind literal for the dual-use `operator_reset` ("skip/warning") is not given. DF-57 also gives no failure action for a failed P10 allowlist check (only commit and hook failures HALT). | Add `lock_held` to the DF-57 cell; state the `operator_reset` kind string; state HALT for an allowlist violation |
| M5 | MINOR | `research/04` lines 106 and 174; `research-notes.md` lines 19-20, 24; DF-07 DEVIATION cell | Stale statements remain: "no commit/PR", `stubs/gh` and `stubs/orca`, and the C14 collision rationale. They are overridden by 06 line 1 and DF-10, DF-27. The DF-07 cell cites a "BUILD_REQUEST" that is not in the task dir. | Optional: reword the cell to "coordinator brief"; the builder is told to follow 06 |
| M6 | MINOR | 06 DF-18 | No required-field list for G5 (see Section C); a deleted-user comment (`author: null`) would give `edits_unreadable` for that issue. | State that `author` may be null and means "not own login" |
| M7 | MINOR | 06 DF-19 line 146 and Table 1.2 | `poll-augment-review.sh:57` is cited without its path (`src/superclaude/skills/sc-pr-submit-protocol/scripts/`); P8 runs G-1, G-3, G-8 only, so P8 test files are first linted at P9 (G-5 full tree). | Add the path; optional G-5 at P8 |

## Recommendations

- Blocking items from r2: E1 resolved. No new CRITICAL or IMPORTANT issue. The M items are notes under the review severity rule; they need no re-review.
- The register is strongly evidenced: about 56 cites re-read against the real repo, design, spec, SKILL.md, template and host tools, and every blocking-relevant claim holds.

VERDICT: PASS

## QA Complete
