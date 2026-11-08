# Cross-Validation Report, round 2: gap-fill file 06 against files 01-05, design and spec

**Analysis type:** completeness-verification, lens: cross-validation (gap-fill re-check, round 1)
**Date:** 2026-11-07
**Scope:** `research/06-gap-fill-decisions.md` (218 lines) against `research/01..05`, `docs/designs/issue-watcher.md` (D) and `.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md` (S)
**Prior report:** `qa/analyst-cross-validation-report.md` (X-1 to X-15)
**Status:** Complete. VERDICT: FAIL (0 CRITICAL, 2 IMPORTANT, 11 MINOR)

Method: read file 06 and the prior report in full; read 01-05 through targeted greps and section reads for every contradiction named in the prompt; re-ran read-only checks against the repo. No research file was modified. No web research.

---

## 1. Internal consistency of file 06 (DF against DF)

Result: no hard contradiction between two DF decisions. The soft inconsistencies are listed as R2-M1 to R2-M11 in section 5. Details per check:

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Stub PATH design (DF-10, Table 1.4) against the stub list | CONSISTENT | DF-10 names `gh`, `orca`, `orca-ide`, `git`. Table 1.4 "Stub files" lists the same four, the "Guard" row loops over the same four, PATH = `<tmp>/stubbin:<tmp>/linkbin` with no `/usr/bin` (so the real `/usr/bin/orca-ide`, `/usr/bin/gh` are unreachable). `find_orca` tries `orca-ide` first (`install_user_setup.py:35`, verified) and a stub exists for it. The precedent cited (`test_conflict_scripts.py:1555-1571`) really does build a PATH holding only symlinks plus a wrapper (`PATH=str(bin_dir)`, verified). `linkbin/env` is not needed (the shebang uses the absolute `/usr/bin/env`) but is harmless. |
| 2 | Stub plan against DF-34 (e2e through `sys.executable -m superclaude.cli.main` with `env=`) and DF-01 (cwd) | CONSISTENT | Real process, so PATH stubs apply; stub log header records `os.getcwd()`, which is how DF-01's "launch recorded with cwd = configured worktree" is checked end to end. `main.py:564-565` has the `__main__` guard (verified). |
| 3 | Reason-list size 52 to 56 against tests and the `REASONS` pin | CONSISTENT | Spec table `S 330-358` hand-counted: 52 names (row by row: 6+1+5+5+2+2+1+3+3+2+1+2+2+2+1+1+1+2+1+1+1+2+2+1+2 = 52). DF-02 adds 2 (`marker_unreadable`, `edits_unreadable`), DF-03 adds 1 (`operator_reset`), DF-22 adds 1 (`dry_run_shadow_reset`) = 56. The same "56" appears in DF-02, DF-22 (test_audit), DF-31 (pin embeds 56 literals) and phase P2. No place says 52 or 55. `re-approved` is one of the 52 (kind "decision note"). |
| 4 | DF-40's list of DEVIATION rows against the register | CONSISTENT | Rows marked yes: DF-01, 02, 03, 04, 05, 07, 10, 12, 17, 20, 22. DF-40 lists exactly these eleven. DF-06 and DF-15 are marked no with a reason. |
| 5 | Gate counts against the gate map | CONSISTENT | DF-08 says 4 x 6 + 2 + 7 = 33. Table 1.6 rows: A 6, B 6, C 6, D 6, M4 2, Final 7 = 33. Section 2 "Gate" column: P3 = A, P5 = B, P7 = C, P8 = D, P9 = M4 then Final; P1/P2/P4/P6/P10 none. "Covers" in 1.6 (A: P2-P3, B: P4-P5, C: P6-P7, D: P8) matches the "covered by Gate X" notes in the P2/P4/P6 rows. The 7 for the final gate matches SKILL.md 2363 ("standard: 7"). One tension with SKILL.md 2140: R2-M1. |
| 6 | Commit item (DF-07, P10) against DF constraints on staged paths | CONSISTENT, one gap | DF-07 stages explicit paths plus `.dev/tasks` and forbids `.claude/`, `.dev/issues/`, `.dev/brainstorms/`, `git add -A`, `--no-verify`, push, PR. DF-31 says the design file is never edited and is committed unchanged: it is untracked today (`git status`: `?? docs/designs/issue-watcher.md`, verified), so adding it is correct. Current index: 83 staged paths, all under `.dev/tasks/`; none under the forbidden prefixes (verified). `.dev/issues/331/` and `.dev/brainstorms/...` are untracked and stay out. No pre-commit framework or hook is installed in this checkout (`command -v pre-commit` empty; hooks dir holds only `.sample` files), so DF-32 "pre-commit hooks not run locally" is accurate. The commit carries the required `Co-Authored-By: Claude Code <noreply@anthropic.com>` trailer. Gap: R2-M5. |
| 7 | DF-01 (Runner cwd) against DF-24 (FakeRunner) and D 776 | CONSISTENT | DF-01 fixes `Runner.run(argv, timeout, *, cwd=None)`; `FakeRunner` records `(tuple(argv), cwd)`. DF-24 only renames `FakeLauncher`/`FakeClock`. The `FakeRunner` script value type is still open (05 G-14), see I-1. |
| 8 | DF-02 (`marker_unreadable`) against DF-18, DF-19 | CONSISTENT | DF-02 cites "a required field null (DF-18)" and "page longer than 100 (DF-19)"; DF-18 treats a null `login` as "not own login", not as unreadable; DF-19 maps G4 over-long pages to `marker_unreadable`. Matches D 570 (more than 5 pages) and D 572. Missing sub-cases: R2-M3. |
| 9 | DF-03 (`operator_reset`) against the audit schema | CONSISTENT, one wobble | DF-03's decision-line keys (issue, login null, no `state`, approval fields null, no `note`) match D 711-716. A warning line may omit `issue` (D 711 "optional"). DF-03 calls the reason kind `skip` but also uses it on a `warning` line: R2-M2. |
| 10 | DF-05 (no local full `make test`) against G-2 and the CI facts | CONSISTENT | `test.yml:47` runs `pytest ... -n auto --maxfail=3 --ignore=tests/cli/test_verify_sync_hooks.py`, and its comment (lines 44-45) says the lint job runs that file serially (verified). G-2 does not include `test_verify_sync_hooks.py`. Wording: R2-M6. |
| 11 | DF-29 (eager registration) against D 760, DF-06 and P7 | CONSISTENT | D 760 says "Two lines after line 561"; DF-29 inserts the import line and `add_command` (with a blank line between); P7 says "two lines after 561". |
| 12 | DF-10/DF-31/DF-32 (nothing executable committed) against D 765/780 and the ACs | CONSISTENT | `grep stubs` in D: lines 208, 765, 780, 870 only; AC-20/AC-21 do not name a `stubs/` path. Only D 765 and D 780 need the deviation and DF-10 records both. |

## 2. Earlier contradictions: X-1 to X-15 and the section 4 register of the first report

Legend: RESOLVED = a DF decision fixes it and no 01-05 text contradicts the fix after the 06 header ("supersedes research files 01 to 05 wherever they conflict"). PARTIAL = fixed in part. NOT RESOLVED = no DF row.

### 2.1 The fifteen X items

| X | Topic | Status | DF | Check |
|---|---|---|---|---|
| X-1 | Verb count (five Click commands vs "six verbs") | RESOLVED | DF-06 | Five names, "five commands, six usage forms", `test_cli.py` asserts exactly five, G-9 lists exactly five. 05's four "six verbs" statements and D 177/759 are overridden by the 06 header; DF-06 itself says "wording fix inside the design". |
| X-2 | `ORCA_AGENT` handling | RESOLVED | DF-11, DF-31 | Literal `"claude"` stated (verified at `seed-brief.md:64`: `orca agent launch --agent claude ...`); pinned as a literal in `test_launch.py`, no `.dev/` read. 05's "never print it" rule is overridden (its source was UNVERIFIED in the first report). Citation slip: R2-M7. |
| X-3 | Stubs do not isolate `orca-ide`/`git` | RESOLVED | DF-10, Table 1.4 | Four stubs, PATH holds only stub and link dirs, `shutil.which(name, path=PATH)` guard for each. |
| X-4 | No consolidated register; items in one file only | PARTIAL | DF-01 to DF-40 | See 2.2: the 02 items are all covered except G7/G9; 05 items G-06, G-07, G-09, G-10 (part), G-11, G-12, G-13, G-14, G-15, G-16, G-17, G-18 (part), G-21 have no DF row. Blocking: I-1. |
| X-5 | QA gate size | RESOLVED with a risk | DF-08, Table 1.6 | 6-agent intermediate gates, 7-agent final. The 2-agent M4 gate is allowed by SKILL.md 1151 ("Minimum 2 fidelity agents") but SKILL.md 2140 says "ANY QA gate ... fewer than 6 ... CRITICAL". DF-08 quotes 2140 and does not say how the M4 gate escapes it: R2-M1. |
| X-6 | False premise of design C14 | RESOLVED | DF-27 | Reason is the repo convention. Verified: `tests/cli_portify/__init__.py` and `tests/pr_submit/__init__.py` exist. |
| X-7 | Pinned ruff vs local 0.17.3 | RESOLVED | DF-09, G-4, G-5 | Verified: `uvx --offline ruff@0.15.20 --version` prints `ruff 0.15.20`; `.venv/bin/ruff` absent; `/usr/local/bin/ruff` is 0.17.3. |
| X-8 | `make test` and `-n auto` | RESOLVED | DF-05, G-2, G-3 | Affected subset locally; full suite in CI; xdist form gets `--offline`, marked UNTESTED with SKIP allowed. xdist is absent from `pyproject.toml` (grep empty). |
| X-9 | Stub materialisation; e2e invocation; lock-test mechanism | RESOLVED | DF-10 (a), DF-34 (b, c) | Runtime-written stubs; subprocess for e2e and `CliRunner` for `test_cli.py`; `multiprocessing` for the lock test (D 785). |
| X-10 | `property_based` tag | RESOLVED | DF-12 | No marker. Verified: marker text "Property-based tests using hypothesis (T09.03)" at `pyproject.toml:135`; only user is collect-ignored at `tests/conftest.py:14`. D 96 (C15) already says "seeded `random` strings", so DF-12 agrees with it; only D 93 (C12) is overridden. |
| X-11 | "9 source files" prose | RESOLVED | DF-38 | Eight modules plus `__init__.py`; `main.py` is the tenth changed file. D 751-759 confirms. |
| X-12 | `cwd` not propagated | RESOLVED | DF-01 | Final signature stated once, with the files that use it. See R2-M4 for one open detail (`git -C` vs cwd). |
| X-13 | 3.10 grep lacks `fromisoformat` | RESOLVED | DF-35, G-7 | G-7 includes `fromisoformat`, `ExceptionGroup`, `except*`, `asyncio.timeout`, `typing.Self`. |
| X-14 | `find_orca` parity exclusions too narrow | RESOLVED | DF-36 | Every non-object or non-list-of-dict `topics` shape is "rejects only". Matches `install_user_setup.py:216-219` (line 219 `any(t.get("name") ...)` sits outside the `try`, verified). |
| X-15 | Gap-ID collisions | RESOLVED | 06 header | DF-nn ids only; header bans citing 02 `G1..G15`, 05 `G-01..G-21`, `X1..X15`. Side effect: it makes the un-ported 05 decisions unreachable, see I-1. |

Items named in the task prompt that are not X numbers: "test class names". No contradiction about test class names exists in 01-05 (grep for `class Test` and similar finds none), and the first report does not list one. The only related fact is `python_classes = ["Test*"]` at `pyproject.toml:110` (verified), which 06 neither states nor contradicts; the 06 helpers (`FakeRunner`, `FakeClock`, `FakeLauncher`, `CrashingStore`) do not start with `Test`, so they are not collected. Status: NOT FOUND AS A CONTRADICTION; no action.

### 2.2 The X-4 register, item by item

| Source item | Topic | DF row | Status |
|---|---|---|---|
| 02 G1 / 05 G-01 | Runner cwd | DF-01 | RESOLVED (05 G-01 says `Path`, DF-01 says `str`; DF-01 wins) |
| 02 G2 / 05 G-08 | C21 wording | DF-28 | RESOLVED |
| 02 G3 | Missing reasons | DF-02 | RESOLVED |
| 02 G4 | `marker_time` | DF-16 | RESOLVED |
| 02 G5 / 05 G-03 | Stubs, git | DF-10 | RESOLVED |
| 02 G6 | Crash recipes | DF-15, Table 1.3 | RESOLVED |
| 02 G7 / 05 G-02 | Spec names vs design names | DF-01 (no `run_command`) | PARTIAL: 02's "make `which` a keyword argument with default `shutil.which`" is not carried; D 604 has `find_orca(runner, which)` and D 299 has a `which` seam row, so low impact |
| 02 G8 | Migration save in dry-run | DF-17 | RESOLVED |
| 02 G9 / 05 G-16 | Spec-vs-design deviations (retry argv, S1, 3600 s clamp, `last_completed_cycle_at`, `status` exit 1) | none | NOT RESOLVED. The design already holds owner questions Q1-Q4 (D 866), but DF-40 says the Open Questions list is the DEVIATION=yes rows of 06 only |
| 02 G10 / 05 G-20 | `ORCA_AGENT` | DF-11, DF-31 | RESOLVED |
| 02 G11 / 05 X14 | Eager import | DF-29 | RESOLVED |
| 02 G12 | Null fields | DF-18 | RESOLVED in principle; the event rule is wrong for `renamed`, see I-2 |
| 02 G13 | Page over 100 | DF-19 | RESOLVED |
| 02 G14 | Comma in label | DF-20 | RESOLVED |
| 02 G15 | Marker literal | DF-21 | RESOLVED |
| 05 G-04 | `reset` audit | DF-03, DF-04 | RESOLVED |
| 05 G-05 | `stderr_fallback` signature | DF-33 | RESOLVED |
| 05 G-06 | `REASONS` companion mapping (kind, exit per reason) | none | NOT RESOLVED. `REASONS` is a frozenset (D 718) while D 5.2 wants "kind and exit per reason" |
| 05 G-07 | `last_reason` enum vs `record` cannot import `audit` | none | NOT RESOLVED |
| 05 G-09 | `failed` to `failed` is not a T-row | none | NOT RESOLVED |
| 05 G-10 | `sweep`/`day_cap_count` take store or doc | DF-25 | PARTIAL (only `slo_numbers`) |
| 05 G-11 | Owner module of `Deps`, `CycleResult` | none | NOT RESOLVED (D 302 gives the `Deps` fields only) |
| 05 G-12 | Which path `test_marker_contract` reads | DF-21 says only "via the dual surface (D 791)" | NOT RESOLVED. `.claude/skills` is absent in this worktree and gitignored, `~/.claude` is absent in CI; the always-present path is `src/superclaude/skills/sc-issue-protocol/...` (verified present and tracked) |
| 05 G-13 | Account-rename test (S 213 lists it under NFR-005) | none | NOT RESOLVED; no test item exists in 06 |
| 05 G-14 | `FakeRunner` script value type | none | NOT RESOLVED (D 295 `CommandResult \| Callable`, D 776 `Reply`) |
| 05 G-15 | `_assumed_shape` fixture file names | DF-32 mentions the folder only | NOT RESOLVED (names) |
| 05 G-17 | FR-028 120 s case is reachable only on G1 | none | NOT RESOLVED |
| 05 G-18 | Network-FS check needs an injectable reader | DF-23 gives a pure `fs_type_of` | PARTIAL: tests of `check-config` on a CI tmp dir on 9p/nfs still depend on the real `/proc/self/mountinfo` unless the reader is injectable |
| 05 G-19 | `reset N` with no entry | DF-04 | RESOLVED |
| 05 G-21 | `init-state` network-FS refusal | none | NOT RESOLVED |

05 supplies a default for every NOT RESOLVED row (05 lines 431-451), and none of them conflicts with a DF row. So the content exists, but DF-40 declares 06 "the only decision source" and the header bans citing G-ids, so a builder who follows 06 literally cannot use them. That is I-1.

## 3. Repo spot-checks of facts asserted by file 06 (target at least 10; 32 done)

Tags: VERIFIED = repo matches; CONTRADICTED = repo differs. All checks were read-only (Read, Grep, `sed -n`, `git` plumbing, `uvx --offline ruff --version`).

| # | Claim in 06 | Checked at | Result |
|---|---|---|---|
| 1 | D is 935 lines; S is 515 lines (header) | `wc -l` | VERIFIED (935 and 515). Both untracked (`git status` shows `??` for `docs/designs/issue-watcher.md` and the brainstorm folder). |
| 2 | `origin/master` exists: `0b8a5801d75f159bcbca7087b99507c2a50d8dba`; merge-base = HEAD = `e8db2fe660d9104cbe8cdbcdc6f2c967f4994f4b` (DF-07) | `git rev-parse HEAD`, `git rev-parse --verify origin/master`, `git merge-base HEAD origin/master` | VERIFIED, all three SHAs byte-equal to 06. HEAD is an ancestor of origin/master, so `BASE` = HEAD and the later commit gives a non-empty `BASE..HEAD`. `origin` is the only remote and points at `IronbellyOrg/IronClaude`. |
| 3 | D 265 `Runner.run(argv, timeout)` without cwd; D 625 "called with `cwd=worktree`"; S 309 `run_command(argv: list[str], timeout)` (DF-01) | `sed -n` | VERIFIED (all three lines read verbatim). |
| 4 | D 118-119 `reset` rows, D 121 usage rule, D 177 and D 759 say "6 verbs" (DF-03, DF-06) | `sed -n` | VERIFIED. |
| 5 | `tests/skills/test_model_alias_policy.py` exists; the model-id regex is `^claude-(opus\|sonnet\|haiku\|fable)-\d` at `:140` (DF-11) | `ls`, `grep -n opus`, `sed -n 138,142p` | FILE VERIFIED; LINE CONTRADICTED. The regex is `FULL_ID` at line 50 (`re.compile(r"^claude-(opus\|sonnet\|haiku\|fable)-\d")`) and is applied inside `test_python_selection_constants_are_not_full_model_ids` (def at 137). Line 140 is a `for path in sorted(SRC.rglob("*.py"))` loop. Conclusion holds: `"claude"` alone does not match, and the test scans `src/` only. R2-M7. |
| 6 | `tests/docs/test_retired_docs_absent.py`, `tests/cli/test_cli_registration.py`, `tests/swarm/test_cli_registration.py`, `tests/recommend/test_cli_registration.py` exist (G-2) | `ls -l` | VERIFIED, all four plus the alias-policy test exist. |
| 7 | `pyproject.toml:135` marker text "Property-based tests using hypothesis"; `:139` `thread_safety`; ruff pin comment `:50-53`; `ruff==0.15.20` at `:54`; `python_classes` at `:110` (DF-12, DF-09, DF-26) | `sed -n` | VERIFIED. The pin value itself is on line 54; 06 cites the comment block 50-53, which is fine. |
| 8 | `tests/conftest.py:14` is the `collect_ignore` entry for `sprint/test_property_based.py` (DF-12, Section 3) | `sed -n 12,16p` | VERIFIED. |
| 9 | `test.yml:12` job name, `:22` Python "3.10", `:29` xdist pin, `:47` `-n auto` (DF-05, DF-09, DF-26) | `sed -n` | VERIFIED. Line 47 also carries `--ignore=tests/cli/test_verify_sync_hooks.py` (see R2-M6). |
| 10 | `ORCA_AGENT = "claude"` at `seed-brief.md:64` (DF-11) | `sed -n 64p` | VERIFIED: "`orca agent launch --agent claude --worktree path:<abs> --surface terminal --prompt "/sc:issue --claim <int>" --json`". |
| 11 | `install_user_setup.py:35` `_ORCA_CLIS = ("orca-ide", "orca")`; `:216-219` probe shape (DF-10, DF-36) | `sed -n` | VERIFIED. |
| 12 | `main.py:547` swarm eager import; `:559-561` reflect import and `add_command`; `:564-565` `__main__` guard (DF-29, DF-34) | `sed -n` | VERIFIED. Every import line carries the `# noqa: E402,I001  # intentional: ...` suffix, which DF-29 copies. |
| 13 | `swarm/atomic.py:14` `write_prepared_bytes`; `:33` `except Exception` unlinks the tmp file; no directory fsync (DF-15, DF-30) | `sed -n` on `src/superclaude/cli/swarm/atomic.py` | VERIFIED. The tmp name is `<name>.<random>.tmp` in the same directory and the replace is `os.replace(tmp_name, str(path))`, so DF-15's C2 recipe (`dst` ends with `dispatch.json`) and the `dispatch.json.*.tmp` orphan are right. Only the file fsync exists, so DF-30's `_fsync_dir` is needed. Path note: the file is under `cli/swarm/`, not `src/superclaude/swarm/`. |
| 14 | `reflect/commands.py:222` `@reflect_group.command()`, docstring lines 4-5, `cli/__init__.py:13` `from .main import main`, `tests/cli/reflect/test_cli_smoke.py` lines 7, 17, 21, 46 (DF-26) | `sed -n` | VERIFIED (all lines match the described content). |
| 15 | task-builder SKILL.md 1186-1187 (intermediate gate under 5 rejected), 2140 (any gate under 6 FAIL CRITICAL), 2223 (`--diff {BASE}..HEAD`) (DF-07, DF-08) | `sed -n` on `~/.claude/skills/task-builder/SKILL.md` | VERIFIED. Also read 1149-1152: M4 "Minimum 2 fidelity agents", and 2363: final gate "standard: 7". |
| 16 | Makefile `test:13-15`, `lint:48-50`, `sync-dev:109`, `verify-sync:166`, `verify-deps:356-358` (Section 3 anchors) | `sed -n` | VERIFIED. `lint` is `lint: lint-architecture` then `uv run ruff check .`. |
| 17 | `.pre-commit-config.yaml` check-json line 15, detect-secrets 26-41, markdownlint 74-88, shellcheck 98-103 (DF-32) | `sed -n` on the end lines | VERIFIED. |
| 18 | `refs/claim.md:88` re-claim by editing the earlier comment (DF-16) | `sed -n 88p` | VERIFIED: "Edit the earlier claim comment with `gh api -X PATCH repos/<R>/issues/comments/<id> ...`". The file and `templates/claim-comment.md` (marker at line 23) are tracked under `src/superclaude/skills/sc-issue-protocol/`. |
| 19 | `uvx --offline ruff@0.15.20 --version` prints `ruff 0.15.20`; `.venv/bin/ruff` does not exist; local Python 3.11.15 (DF-09, G-5) | ran the commands | VERIFIED. `ruff` on PATH is `/usr/local/bin/ruff` 0.17.3. `uv run --offline --no-sync python --version` prints 3.11.15. |
| 20 | `/usr/bin/env` exists on this host (Table 1.4) | `ls` | VERIFIED. |
| 21 | Spec reason table has 52 names (DF-02) | count of S 330-358 by hand | VERIFIED (52). |
| 22 | S 136 FR-022, S 190-191 FR-026, S 213 NFR-005 (5 reruns), S 366 gates, S 379 "skipped with a reason" (DF-02, DF-03, DF-05, DF-15) | `sed -n` | VERIFIED. |
| 23 | D 441, 449, 502-503, 344, 351, 69, 93-102, 131-132, 137 (DF-13, 16, 17, 20, 22, 23) | `sed -n`, Read | VERIFIED. D 137 says "Absolute after expansion" for `state_dir`: see R2-M11. |
| 24 | D 237/238 import rules: `audit` imports nothing, `github` may import `runner`, `predicates` (DF-21, DF-30) | Read D 229-244 | VERIFIED (table rows 237 and 238). |
| 25 | D 295-302: `CrashingStore ... k-th write`, `RecordingLauncher(outcomes)`, `FakeClock(start, step)`, `Deps` fields (DF-15, DF-24) | Read | VERIFIED. D 525-531 crash table and D 776-780 seam table also match DF-15/DF-24. |
| 26 | D 697-722 audit schema, D 745 `slo_numbers(lines, doc, now)`, D 765 and D 780 committed bash stubs, D 785-791 test names (DF-02, 03, 10, 25) | Read | VERIFIED. |
| 27 | D 796-805 gate table and D 896 AC-23 say `make test`; AC-25 exists (DF-05, P9 "AC-1..AC-25") | Read | VERIFIED. |
| 28 | `plugins/superclaude/` holds `__init__.py` and `templates`, no `cli/` (DF-26) | `ls` | VERIFIED. |
| 29 | `.dev/brainstorms/20261107-064825-github-issue-watcher/` holds `spec-panel-review.md` and `base-selection.md`, so the prefix alone locates both (DF-26) | `ls`, `find` | PARTLY CONTRADICTED. `spec-panel-review.md` is at the top level; `base-selection.md` is at `.../adversarial/base-selection.md`. R2-M8. |
| 30 | `tests/conftest.py` has autouse `_pollution_snapshot` and `_redirect_reflexion_writes` (DF-39) | `grep -n` | VERIFIED (lines 29 and 83). |
| 31 | `tests/cli/test_verify_sync_hooks.py` rewrites real files under `src/superclaude/hooks/` (DF-05) | `sed -n 1,16p` | VERIFIED (docstring "DO NOT RUN WITH pytest-xdist ... mutate real repository files"). |
| 32 | DF-07 index state: no staged path under `.claude/`, `.dev/issues/`, `.dev/brainstorms/`; `pre-commit` absent (DF-07, DF-32) | `git diff --cached --name-only`, `command -v`, hooks dir | VERIFIED (83 staged, all under `.dev/tasks/`; no pre-commit; only `.sample` hooks). `tests/pr_submit/test_conflict_e2e.py` also exists (D 780 citation). |

Result: 30 of 32 fully verified; 2 have a citation slip (rows 5 and 29), none changes a decision.

## 4. Blocking findings in detail

### I-1 (IMPORTANT). 06 claims to be "the only decision source" but leaves thirteen 05/02 decisions without a DF id

Evidence:
- DF-40: "This file is the only decision source; the task cites DF ids." Header: "Do not cite research 02 `G1`..`G15`, research 05 `G-01`..`G-21` or `X1`..`X15` in task items."
- The first report's X-4 asked for "one merged decision table ... with an owner or default for each, referenced by index". Section 2.2 above shows 05 G-06, G-07, G-09, G-11, G-12, G-13, G-14, G-15, G-17, G-21 and 02 G9 (= 05 G-16) have no DF row, and 05 G-10 and G-18 are only partly covered (DF-25 handles `slo_numbers` but not `sweep`/`day_cap_count`; DF-23 gives a pure parser but not an injectable reader).
- 05 lines 431-451 hold a default for each, none conflicting with a DF row. So no contradiction, but an item author following 06 literally has no instruction for them.
- Four of them change behaviour or coverage, not just wording:
  - G-09: a second failure before any `pending` (`failed` to `failed`, attempts + 1) is not a T-row in D 7.3; without a decision the transition table raises on a normal retry path.
  - G-13: S 213 (NFR-005) lists "an account rename" as a required test; 06 has no test item for it.
  - G-12: DF-21 says "via the dual surface (D 791)" but not which path `test_marker_contract.py` reads; `.claude/skills` is absent here and `~/.claude` is absent in CI, so the test must read `src/superclaude/skills/sc-issue-protocol/refs/claim.md` and `.../templates/claim-comment.md` (both present and tracked, verified).
  - G-06: `audit.REASONS` is a frozenset (D 718) but cycle exit mapping and the kind of each reason (cycle, skip, entry, note, warning; S 330-358) are needed by `cycle.py`; no companion mapping is named.
- Also not carried: design-vs-spec deviations (02 G9 / 05 G-16: full-argv retry text, S1 reading, 3600 s clamp, `last_completed_cycle_at`, `status` exit 1). D 866 already lists owner questions Q1-Q4, but DF-40 defines the Open Questions list as the DEVIATION=yes rows of 06.

Fix (one edit to 06): add DF-41 and following rows that adopt the 05 defaults for G-06, G-07, G-09, G-11, G-12, G-13, G-14, G-15, G-17, G-21 and 02 G9, or replace the "only decision source" and "do not cite G-ids" sentences by "05 G-xx defaults not overridden here stand, cited as 'research 05 G-nn'". Complete DF-25 for `sweep`/`day_cap_count` (pure functions on `StoreDoc`) and say whether the mountinfo reader is injectable.

### I-2 (IMPORTANT). DF-18 requires `label` to be non-null for `renamed` events, which the G3 projection cannot supply

Evidence:
- DF-18: "G3: `id`, `event`, `created_at` non-null for every item; `label`, `actor_id`, `actor_login`, `actor_type` non-null only for `labeled`/`unlabeled`/`renamed`; else `events_unreadable`."
- `EVENTS_JQ` (D 545) projects `label: .label.name`. A `renamed` event is read by the predicates for its timestamp only (S 94: "no `renamed` event follows it"; D 660 T4). The projection contains no `rename` field, so for a `renamed` item `label` is null unless GitHub puts a `label` object on rename events. That GitHub behaviour is UNVERIFIED here; the design's own projection gives no reason to expect it.
- DF-18 states the principle "Fail closed only on fields a predicate reads". Requiring `label` on `renamed` breaks that principle: any issue with a rename in its history would be skipped as `events_unreadable`, including renames before the approval, which S 94 treats as harmless.
- The sentence is also ambiguous: one list governs four fields, so an implementer cannot tell whether `renamed` needs `label`, only the actor fields, or only `created_at`.

Fix: split DF-18's G3 rule per event type, for example `labeled`/`unlabeled` require `label`, `actor_id`, `actor_login`, `actor_type`; `renamed` requires `actor_id` and `created_at` only if a predicate reads the actor (otherwise `created_at` only); every other event type requires only `id`, `event`, `created_at`. Add a `renamed`-with-null-label case to the `test_github.py` plan.

## 5. Structured gap list

### CRITICAL
None.

### IMPORTANT (blocking)
| ID | Gap | Where | Fix owner |
|---|---|---|---|
| I-1 | 06 says it is the only decision source and bans G-ids, yet 02 G9 and 05 G-06, G-07, G-09, G-11, G-12, G-13, G-14, G-15, G-17, G-21 (plus the uncovered halves of G-10 and G-18) have no DF row; X-4 is therefore only PARTIALLY resolved | 06 DF-40 and header; 05 lines 431-451 | Add DF rows or a "05 defaults stand" clause (section 4) |
| I-2 | DF-18 requires `label` (and the other four fields) non-null for `renamed` events; the G3 projection (D 545) cannot supply `label` for a rename, and the predicates read only a timestamp from it | 06 DF-18; D 545, 660; S 94 | Split the rule per event type (section 4) |

### MINOR (non-blocking)
| ID | Gap | Where |
|---|---|---|
| R2-M1 | DF-08 quotes SKILL.md 2140 ("ANY QA gate ... fewer than 6 ... CRITICAL") and then defines a 2-agent M4 gate without saying why it is exempt (SKILL.md 1151 allows a minimum of 2 for M4). Also the six lenses are not mapped to the agent types the skill's intermediate floor lists (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative, SKILL.md 1164-1167). Add one sentence citing 1151 and the type mix | 06 DF-08, Table 1.6 |
| R2-M2 | DF-03 gives `operator_reset` the table kind `skip` but also writes it on a `warning` line (`reset --rate-limit`). D 718 only checks membership, so nothing breaks, but the kind column in any companion mapping (I-1, G-06) must allow both | 06 DF-03 |
| R2-M3 | DF-02 lists the triggers for `marker_unreadable` and `edits_unreadable` but not the repeated-`id` case on G4 (D 571) or the repeated or empty `endCursor` case on G5 (D 575, "incomplete"). Say they map to the same reasons | 06 DF-02 |
| R2-M4 | DF-01 says `launch.check_origin` passes `cwd=worktree`, but the design's argv is `git -C <abs> remote get-url origin` (D 843, also D 317/329), so cwd is redundant. State whether the recorded cwd for the `git` call is the worktree or none, because DF-10's stub log and `FakeRunner` both record cwd and a test may assert it | 06 DF-01 against D 843 |
| R2-M5 | P10 stages `.dev/tasks` once, before the commit. Task Log edits made afterwards (commit SHA, reflect report path) would be unstaged, against the rule that `.dev/tasks/` is always staged. `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/` is itself untracked at this moment. Add a closing `git add .dev/tasks` after the reflect step (staging only, no second commit unless asked) | 06 DF-07, P10 |
| R2-M6 | DF-05 says "the full suite runs in CI (`test.yml:47`, `-n auto`)". Line 47 ignores `tests/cli/test_verify_sync_hooks.py`; its comment says the lint job runs that file serially. Also S 366 lists `make test` as a gate, but DF-05's deviation row cites only D 896 and D 798 | 06 DF-05 |
| R2-M7 | DF-11 cites `test_model_alias_policy.py:140` for the model-id regex; it is `FULL_ID` at line 50, applied in the test starting at line 137. Conclusion unchanged | 06 DF-11 |
| R2-M8 | DF-26 says `base-selection.md` is cited "with the full `.dev/brainstorms/20261107-064825-github-issue-watcher/` prefix"; the file is under `adversarial/` inside that folder | 06 DF-26 |
| R2-M9 | P1 checkpoint says `uv run pytest tests/issue_watch/ -v` "collects 0 tests without error" while G-1 requires exit 0. Pytest exits with code 5 when nothing is collected (known pytest behaviour; not run here). Write "exit 5 (no tests collected) is the expected P1 result" so an executor does not loop | 06 section 2, P1 |
| R2-M10 | DF-35's one time helper parses `%Y-%m-%dT%H:%M:%SZ` only. The clock-skew check reads the HTTP `Date` header (D 503, 543) and the rate-limit path reads `Retry-After` and `x-ratelimit-reset` (D 598-599); no source, including 06, says how these are parsed, yet DF-22 adds a 61 s versus 60 s skew test | 06 DF-22, DF-35 |
| R2-M11 | DF-13 says values inside the JSON file are not `~`-expanded because D 137 requires an absolute path; D 137 literally says "Absolute after expansion" for `state_dir`. DF-13 is marked "no deviation"; either mark the `state_dir` reading as an interpretation or confirm with the owner | 06 DF-13 |

## 6. What holds up

- Every earlier X item except X-4 is closed by a DF row, and the 06 header makes the supersession explicit.
- The 52 to 56 reason pin, the 33-agent gate arithmetic and the DEVIATION list are internally consistent.
- Repo citations are accurate: 30 of 32 spot-checks match exactly, and the two slips (R2-M7, R2-M8) do not change a decision.
- The commit plan matches the repo state: origin/master exists, HEAD is its ancestor, no forbidden path is staged, no commit hook runs locally.

## 7. Limits of this check

- I read 06 and the first report in full. For 01-05 I read the sections that bear on each contradiction (05 lines 431-451 and its trap notes, 02's gap table, 01 and 03 on the runner, ruff and test-class lines) and used greps for the rest; I did not re-read every line of those 240 KB.
- I did not run `pytest`, `make` targets, `uv run ruff`, or any `gh` or `orca` command. The ruff and xdist facts rest on `uvx --offline ruff@0.15.20 --version`, file contents, and research 03's own measurements.
- GitHub API shapes (rename events, error text, GraphQL variables) are UNVERIFIED here, as 06 itself marks them. I-2 rests on the design's own projection and S 94, not on a live reply.

VERDICT: FAIL

Two IMPORTANT gaps block (I-1, I-2), none CRITICAL. Both are fixable with a short edit to `research/06-gap-fill-decisions.md` (a few added rows and one rewritten sentence in DF-18); the eleven MINOR items can ride along. After that edit a round-2 re-check should only need to confirm I-1 and I-2.

Report path: `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/qa/analyst-cross-validation-report-r2.md`
