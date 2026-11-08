# QA Report - Research Gate, gap-fill re-check round 1 (lens: evidence-quality)

**Topic:** GitHub issue watcher MDTM task build
**Date:** 2026-11-07
**Phase:** research-gate (fix-cycle re-check of the gap-fill file)
**Fix cycle:** 1 (report only, fix_authorization: false)
**Scope:** research/06-gap-fill-decisions.md (DF-01 to DF-40, Tables 1.2 to 1.6, Sections 2 and 3)
**Previous report:** qa/qa-research-evidence-report.md (2 IMPORTANT: B.1 orca-ide stub, B.2 ORCA_AGENT instruction)

## Progress log

- Header written. Read file 06 (218 lines) and the previous report in full. Spot-checks next.
- Five batched read-only spot-check runs done (git, uvx ruff, sed/grep of repo, design, spec, SKILL.md, template). Findings below.

---

## Section A. Previous blocking items: resolution check

| Previous item | Status | Evidence |
|---|---|---|
| B.1 IMPORTANT: no `orca-ide` stub; PATH of `/usr/bin:/bin` exposes real binaries | RESOLVED | DF-10 and Table 1.4 (06 lines 31, 66-77): stubs `gh`, `orca`, `orca-ide`, `git`; PATH is `<tmp>/stubbin:<tmp>/linkbin` only; `shutil.which(name, path=PATH)` guard per stub. Host facts re-checked: `which -a` lists `/usr/bin/orca-ide` (symlink to `/opt/Orca/resources/bin/orca-ide`), `/usr/bin/gh`, `/usr/bin/git`; `_ORCA_CLIS = ("orca-ide", "orca")` at `install_user_setup.py:35`, loop `:204-205`; `/usr/bin/env` is a regular executable (56144 bytes), so the `env` symlink and `#!/usr/bin/env python3` work. |
| B.2 IMPORTANT: contradictory `ORCA_AGENT` instruction, unsourced "no model name" rule | RESOLVED, with a MINOR residual (E2) | DF-11 (06 line 32) gives one instruction: literal `"claude"`, stated in the task file, pinned in `test_launch.py`. Value confirmed: `seed-brief.md:64` reads `orca agent launch --agent claude ...`. Rule scope confirmed by me: `spec-refactor-log.md:47` says "no model name may appear in the spec" and `:81` "the rule wins; the value is defined by reference", so the ban is spec-only and DF-11 is consistent with it. 06's line 1 states it supersedes 01-05, so 05 T-F no longer conflicts. `orca agent launch --help` confirms `--agent <id>`. |

## Section B. Spot-check ledger (about 55 distinct cites re-read; every one listed holds unless marked)

| # | Claim in 06 | Check | Result |
|---|---|---|---|
| 1 | Reason table S 334-358 holds 52 names; 56 after DF-02 (+2), DF-03 (+1), DF-22 (+1) | Printed S 330-360, counted names row by row (6,1,5,5,2,2,1,3,3,2,1,2,2,2,1,1,1,2,1,1,1,2,2,1,2 = 52) | HOLDS; the table is exactly lines 334-358; 52+4=56 |
| 2 | ruff pin 0.15.20; `uvx --offline ruff@0.15.20 --version` prints it | Ran it: `ruff 0.15.20`; `pyproject.toml:50-54` comment plus `"ruff==0.15.20"` | HOLDS |
| 3 | `.venv/bin/ruff` absent; bare `uv run ruff` is 0.17.3 | `ls` fails; `which -a ruff` gives `/usr/local/bin/ruff`, `--version` gives 0.17.3 | HOLDS (that `uv run ruff` picks `/usr/local/bin/ruff` is an inference, not executed) |
| 4 | xdist pin `test.yml:29`, `-n auto` at `:47`, `python-version: "3.10"` at `:22`, job name `:12` | `sed -n` | HOLDS |
| 5 | Makefile 13-15 (test), 48-50 (lint), 109 (sync-dev), 166 (verify-sync), 356-358 (verify-deps) | `sed -n` | HOLDS |
| 6 | pre-commit: check-json line 15, detect-secrets 26-41, markdownlint 74-88, shellcheck 98-103; none installed locally | `sed -n`; `which pre-commit shellcheck markdownlint detect-secrets` prints nothing | HOLDS |
| 7 | origin/master `0b8a5801...`, merge-base = HEAD = `e8db2fe6...` | `git rev-parse --verify origin/master`, `git merge-base HEAD origin/master`, `git rev-parse HEAD` | HOLDS (exact SHAs) |
| 8 | `find_orca` order, `:35`, `:198-221`, `:216-219`; DF-36 error shapes | Read lines 198-221: `.get("topics", [])` inside `try`, `any(t.get(...) for t in topics)` at 219 outside it. `None` and int raise `TypeError`; str, non-empty dict, non-dict element raise `AttributeError`; all uncaught | HOLDS |
| 9 | `main.py:547` swarm import, `:559-561` reflect import and `add_command`, `:564-565` guard, 565 lines | `sed -n`, `wc -l` | HOLDS (DF-29, DF-34) |
| 10 | `tests/conftest.py:14` collect-ignores `sprint/test_property_based.py`; `pyproject.toml:135` marker text; "only user is collect-ignored" | `sed -n`; `grep -rln property_based tests src`: only `tests/sprint/test_property_based.py` applies the marker (the roadmap file mentions it in a docstring only) | HOLDS (DF-12) |
| 11 | `swarm/atomic.py:14` signature, `:33` `except Exception`, `os.replace`, orphan name `dispatch.json.*.tmp` | Read: file is `src/superclaude/cli/swarm/atomic.py`; `mkstemp(prefix=path.name + ".", suffix=".tmp")`; `os.replace(tmp_name, str(path))` via `import os`, so the Table 1.3 C2 patch of `os.replace` works; `SystemExit` skips `except Exception` | HOLDS (DF-15, DF-30) |
| 12 | Design lines D 69, 93, 100, 102, 110, 118-119, 121, 137, 177, 218, 220, 224, 237, 244, 265, 296-298, 344, 347, 351, 354, 399, 441, 449, 502, 503, 509, 525-531, 547-548, 554, 560, 570, 572, 625, 693, 704-715, 718, 720, 722, 745, 751-761, 765, 777-780, 784, 788, 790, 791, 798, 805, 896 | Printed each; text matches the DF row that cites it (D 265 signature, D 625 `cwd=worktree`, D 745 `doc: StoreDoc`, D 779 `crash_at`, D 441 "migrated store is saved under the lock", D 711 warning column `optional`) | HOLDS; D is 935 lines, S is 515 lines, both untracked (`git status` `??`) |
| 13 | Spec lines S 136, 181, 190-191, 213 (5 reruns), 297, 309, 366, 379 | Printed each | HOLDS |
| 14 | `reflect/commands.py:222`, `cli/__init__.py:13` (DF-26) | `sed -n` | HOLDS |
| 15 | `refs/claim.md:88` re-claims by editing the earlier comment (DF-16) | Line 88 says "Edit the earlier claim comment with `gh api -X PATCH ...`" | HOLDS |
| 16 | `poll-augment-review.sh:57` page bound 100 (DF-19) | Line 57 has `length <= 100` | HOLDS |
| 17 | `tests/cli/test_verify_sync_hooks.py` rewrites real files under `src/superclaude/hooks/` (DF-05) | Docstring lines 5-16 | HOLDS |
| 18 | `tests/conftest.py` autouse `_pollution_snapshot` (28) and `_redirect_reflexion_writes` (82) (DF-39) | `sed -n` | HOLDS |
| 19 | DF-27: `tests/cli_portify/test_cli.py` exists and its dir is a package; `tests/pr_submit/__init__.py` exists | `find tests -name test_cli.py`: one hit, in a package | HOLDS: the C14 premise is false |
| 20 | G-2 files all exist; `tests/pr_submit/test_conflict_e2e.py` exists | `ls` | HOLDS |
| 21 | `test_conflict_scripts.py:1555-1571` stub dir on PATH precedent | Read: symlinked `bin_dir`, `git` wrapper, `env = dict(repos.env, PATH=str(bin_dir))` | HOLDS |
| 22 | task-builder SKILL.md 1186-1187 (intermediate gate under 5 rejected), 2140 (any gate under 6 CRITICAL), 2223 (reflect `--diff {BASE}..HEAD`), M4 minimum 2 at 1149-1152 | `sed -n` | HOLDS; see E5 |
| 23 | Table 1.6 arithmetic 4 x 6 + 2 + 7 = 33 | computed | HOLDS |
| 24 | DF-40 DEVIATION=yes list (01, 02, 03, 04, 05, 07, 10, 12, 17, 20, 22) equals the table's yes rows | compared | HOLDS (11 rows) |
| 25 | `orca agent launch --agent <id>` flag surface | `orca agent launch --help` | HOLDS |
| 26 | `tests/docs/test_retired_docs_absent.py` behaviour | Read: fails only on retired file paths and markdown links to them, scanning `README.md`, `src/superclaude`, `plugins/superclaude`, `docs` | HOLDS (consistent with the P9 runbook rule) |
| 27 | `test_model_alias_policy.py:140` holds the `^claude-(opus\|sonnet\|haiku\|fable)-\d` regex | Line 140 is `for path in sorted(SRC.rglob("*.py")):`; the regex is `FULL_ID` at line 50 | WRONG LOCATOR (E2); the behaviour claim (bare `claude` does not match) is correct |
| 28 | G-5 note: explicit file list "avoids the 12 pre-existing Markdown hits" | Research 03:151 attributes the 12 to ruff 0.17.3 `format --check`; pinned `uvx --offline ruff@0.15.20 format --check src/ tests/` gives "1204 files already formatted"; `ruff@0.15.20 check .` prints no findings | MISATTRIBUTED (E4); no effect on the command |
| 29 | Python 3.10 not installed locally; local is 3.11.15 | `uv python list --only-installed --offline`: 3.13.5 and 3.11.15 only | HOLDS |
| 30 | D 756 names `ORCA_AGENT` | `sed -n 756p` | HOLDS |
| 31 | DF-07 "owner-authorized for this task only" | `grep -rn authoriz` over the task dir: no source. `research-notes.md:26` says "no commit or PR step inside the task file". No BUILD_REQUEST exists in the task dir (only `qa/`, `research/`, `research-notes.md`) | UNSUPPORTED (E1) |

## Section C. [UNVERIFIED] and [PROPOSAL] labelling

- Properly labelled: DF-02, DF-03, DF-22 (new reason names are [PROPOSAL]); DF-14 and Table 1.5 ([PROPOSAL, UNVERIFIED], tests assert no `mutation`); DF-20 (comma splitting, [UNVERIFIED] plus [PROPOSAL]); DF-23 ([PROPOSAL]); DF-37 ([UNVERIFIED]); G-3 ("UNTESTED here", SKIP allowed). No new reason name is stated as a fact.
- The legend (06 line 12) defines [PROPOSAL] as "a value chosen here that no source fixes". DF-16 (`marker_time = max(created_at, updated_at)`), DF-18 (null-equals-missing rules), DF-19 (over-100 pages unreadable), DF-33 (`AuditLog(state_dir)` signature) and DF-12 (2,000 draws, seed 331) match that definition but carry no tag and sit in DEVIATION = no rows. They are presented as DECISIONS, not as facts about the repo, so this is labelling inconsistency only (E3).
- DF-35 asserts `fromisoformat` rejects a trailing `Z` before 3.11 without a tag. That is documented CPython behaviour and the local interpreter cannot test it; no action.

## Items Reviewed (research-gate checklist, evidence-quality lens, applied to file 06)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | File inventory (Status: Complete, summary) | PASS | `Status: Complete` at line 217; purpose statement at line 1 |
| 2 | Evidence density | PASS (Dense) | Every DF row carries source ids and design or spec line numbers; 31 groups re-read, 28 hold, 3 imprecise/unsupported |
| 3 | Scope coverage | PASS | Section 3 maps every target file to D, S, repo anchors and DF rows |
| 4 | Doc cross-validation tags | PASS | Claims taken from design text are tied to a re-read line; [UNVERIFIED] items tagged (Section C) |
| 5 | Contradiction resolution | PASS with notes | The two prior contradictions are resolved (Section A); E5 is an undisclosed rule tension |
| 6 | Gap severity | FAIL | E1: git-mutation authorization asserted with no source |
| 7 | Depth appropriateness | PASS | Tables 1.2 to 1.5 give runnable commands and recipes |
| 8 | Integration point coverage | PASS | DF-01, 29, 30, 36 cover the reused helpers with line anchors |
| 9 | Pattern documentation | PASS | DF-29, 34, 35 |
| 10 | Incremental writing | UNVERIFIABLE | no write history |

## Summary

- Checks passed: 8 / 10 (one with notes). Failed: 1 (item 6). Unverifiable: 1.
- Critical: 0. Important: 1 (E1). Minor: 5 (E2 to E6).
- Fixes applied: 0 (report only).

**Confidence:** Verified: 9/10 | Unverifiable: 1 | Unchecked: 0 | Confidence: 100.0% of checkable items (9/9). Verdict is FAIL because one blocking item is open.

**Tool engagement:** Read: 3 | Grep: 0 (grep run inside batches) | Glob: 0 | Bash: 8 (five batched read-only scripts plus three single reads; the first attempt at a bare-python version probe was blocked by the UV-only hook and replaced with `uv python list`). No Tavily or web tools used; no external-web claim needed checking.

**UNCHECKED:** none. **UNVERIFIABLE:** item 10 (no per-write history); the `uv run ruff` to `/usr/local/bin/ruff` resolution was inferred, not executed.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| E1 | IMPORTANT | 06 DF-07 (line 28), P10 (line 178) | DF-07 says the local commit is "owner-authorized for this task only". Nothing in the task directory records that authorization. `research-notes.md:26` states the opposite constraint ("no commit or PR step inside the task file"), and the global rule is to commit only when asked. The task builder will encode a git mutation (`git add`, `git commit`) on the strength of an unsourced claim, and P10 and the POST reflect depend on it. | Cite the authorization (owner message and date, or the BUILD_REQUEST line), or relabel it [UNVERIFIED: needs owner confirmation] and make the P10 commit item conditional on a confirmation written in the Task Log, with a stated fallback for the POST reflect diff if it is not given. |
| E2 | MINOR | 06 DF-11 (line 32) | `test_model_alias_policy.py:140` is cited for the model-id regex; the regex is `FULL_ID` at line 50. The "no model name" rule behind the old 05 T-F is not cited (`spec-refactor-log.md:47`, `:81`; spec-only scope). | Change `:140` to `:50`; add the PF-034 cite and the words "spec only". |
| E3 | MINOR | 06 DF-03, DF-16, DF-18, DF-19, DF-33; legend line 12 | DF-03 gives `operator_reset` "kind `skip`" yet writes one of its two uses on a `warning` line. Several rows meet the [PROPOSAL] definition without the tag. DF-16 cites "S 3" for spec Section 3; S line 3 is blank. | Tag them; write "spec section 3". |
| E4 | MINOR | 06 Table 1.2 G-5 notes | "12 pre-existing Markdown hits" belong to ruff 0.17.3 format check, not to the pinned 0.15.20 (zero on `src/ tests/`). | Reword to "0.17.3 only". |
| E5 | MINOR | 06 DF-08, Table 1.6 | The register rejects 3-agent gates using SKILL.md 1186-1187 and 2140 but does not note that the same line 2140 ("ANY QA gate under 6 agents is CRITICAL") can flag the 2-agent M4 gate. M4 allows 2 (SKILL.md:1149-1152; template I22 standard, `research-notes.md:49` sets qa_intensity standard). I22 is not cited, and under FULL I19 a final gate for more than 1500 output lines would need 10 or more agents. | Add one sentence citing I22 standard and `research-notes.md:49`, and record the 2140 tension in the Open Questions. |
| E6 | MINOR | 06 Table 1.4 | `linkbin/env` symlink is unnecessary: the shebang names `/usr/bin/env` by absolute path. | Optional: drop it. |

## Recommendations

- Fix E1 only (one sentence plus a conditional in P10). E2 to E6 are notes under the review severity rule and need no re-review.
- The register is otherwise strongly evidenced: about 55 cites re-read, all but the three listed hold, and both prior IMPORTANT items are resolved.

VERDICT: FAIL

## QA Complete
