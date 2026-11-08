# Cross-Validation Report: research files 01-05 (task-builder track 1)

**Analysis type:** completeness-verification, lens: cross-validation
**Date:** 2026-11-07
**Scope:** `research/01-cli-package-conventions.md`, `02-integration-points-and-citation-check.md`, `03-test-and-verification.md`, `04-template-and-examples.md`, `05-work-breakdown.md`
**Track goal:** build an MDTM task file that implements the GitHub issue watcher exactly as designed in `docs/designs/issue-watcher.md`
**Status:** Complete. VERDICT: FAIL (0 CRITICAL, 6 IMPORTANT, 9 MINOR)

Method: read all five files in full (05 in two pages), read `research-notes.md`, then re-checked claims against the repo with Read/Grep/Bash. No research file was modified. No web research was used.

---

## 1. Repo spot-checks (target: at least 8; 30 done)

Tags: VERIFIED = repo matches the research claim; CONTRADICTED = repo differs; NOTE = matches with a caveat.

| # | Claim (source file) | Checked at | Result |
|---|---|---|---|
| 1 | `main.py` is 565 lines; reflect import at 559, `add_command` at 561, `if __name__` at 564 (01 F1, 02 X3, 05 1.9) | `src/superclaude/cli/main.py:545-565` | VERIFIED. Every import line carries `# noqa: E402,I001  # intentional: ...`. |
| 2 | `_find_orca` at `install_user_setup.py:198-221`, timeout 10 at 213, `except` at 217, `orca-cli` check at 219 outside the `try`; `_ORCA_CLIS` at 35 (02 C2, C19) | `install_user_setup.py:198-221`, grep line 35 | VERIFIED. Line 219 is outside the `try`. `topics=None` makes `for t in None` raise `TypeError`, and a string `topics` raises `AttributeError` at line 219. So 02's broader C19 reading is right and 05's "non-dict element" wording is narrower than the code. |
| 3 | `write_prepared_bytes(path, data) -> int` at `swarm/atomic.py:14`; no directory fsync; `except Exception` unlinks tmp then re-raises (02 C4, X14; 01 F8) | `swarm/atomic.py:1-39` | VERIFIED. |
| 4 | `parse_origin_url` at `origin_repo.py:86`; `_NAME` at 65; regexes without `IGNORECASE`; `_GITHUB_URL` is `IGNORECASE`; `read_origin` at 156 has `check=False` and no timeout (02 C3, E) | grep of `origin_repo.py` | VERIFIED. |
| 5 | Claim marker `<!-- sc:issue:claim -->` at `claim.md:29`, `claim.md:88`, `claim-comment.md:23`; `claim.md:26` has `gh api user -q .login`; `:41-42` owner rule; `:47` `--add-assignee @me` (02 C6, C7, E) | `refs/claim.md:24-49`, grep | VERIFIED. |
| 6 | `poll-augment-review.sh` `fetch_rest` at 48, 1000-page cap at 51, `length <= 100` at 57, `-lt 100` at 70, repeated-id check at 72 (02 C5, G13) | grep of the script | VERIFIED. |
| 7 | `pr_submit/ci.py:25` `classify_checks`, `:58` `_evidence_is_zero`, no `subprocess` under `pr_submit` (02 C1) | grep of `src/superclaude/pr_submit` | VERIFIED. |
| 8 | `contracts/__init__.py:302-313` `__all__` holds exactly ten names (01 F6, 02 C9) | `contracts/__init__.py:302-313` | VERIFIED. |
| 9 | Makefile: `test:13`, `lint:48`, `format:53`, `sync-dev:109`, `verify-sync:166`, `verify-deps:356`, `lint-architecture:362`, Check 11 at 467-476 scanning `src/superclaude/cli/` (01, 02, 03) | grep of `Makefile` | VERIFIED. |
| 10 | `test.yml`: Python 3.10 (lines 12, 22), xdist ad hoc (26-29), `-n auto` (47), ruff check (102), format check (106), verify-deps (123), verify-sync (131), lint-architecture (135) (02 C10-C13, 03 s6) | grep of `test.yml` | VERIFIED. |
| 11 | `pyproject.toml`: `requires-python` 16, `ruff==0.15.20` 54, `python_classes=["Test*"]` 110, `--strict-markers` 114, `property_based` 135, `thread_safety` 139 (01, 02, 03) | grep of `pyproject.toml` | VERIFIED. |
| 12 | `uv.lock` has click 8.5.1 (108-109) and ruff 0.15.20 (1563-1564); `.pre-commit-config.yaml` ruff `rev: v0.15.20` at 110 (01 F6) | grep | VERIFIED. |
| 13 | `tests/cli_portify/__init__.py` exists, so design C14's collision premise is false (02 C14 CONTRADICTED; 03 s9 "HOLDS"; 05 header and 1.0; research-notes line 24) | Glob, `ls` | 02 is RIGHT. 03 s9, 05 and research-notes repeat the false premise. Conflict, see X-6. |
| 14 | `tests/cli/test_cli_registration.py:31-49` `EXPECTED_TOP_LEVEL_COMMANDS` has 15 names, omits swarm and reflect (01 F7) | Read | VERIFIED. |
| 15 | No `cli.py` module exists under `src/superclaude` (01 F4) | Glob `**/cli.py` | VERIFIED (no match). |
| 16 | `src/superclaude/cli/issue_watch/` and `tests/issue_watch/` do not exist (all files) | `ls` | VERIFIED. |
| 17 | `.claude/templates` and `.claude/skills` are absent in this worktree (02 F, 03 s6, 04) | `ls` | VERIFIED. |
| 18 | 266 of 292 non-empty `.py` files under `cli/` have `from __future__ import annotations` (01 F5) | Bash count | VERIFIED (292 / 266). |
| 19 | No tracked executable under `tests/` (01 F6, 03 s2.1) | `git ls-files -s tests` | VERIFIED (none). |
| 20 | `reflect` has 4 `sys.exit(`; swarm exit-style count is 71 (01 F3) | grep | reflect VERIFIED. swarm: my pattern gives 73 against 01's 71. NOTE: a count-level difference, not material. |
| 21 | Local `ruff` is 0.17.3 (`/usr/local/bin/ruff`), not the 0.15.20 pin (03 s6) | `ruff --version`, `which -a` | VERIFIED. |
| 22 | `docs/designs/issue-watcher.md` is not tracked; `.dev/brainstorms/...issue-watcher` is not tracked (05 header, 02 G10) | `git ls-files --error-unmatch` | VERIFIED for the design. A fresh clone or CI lacks the spec and seed brief. |
| 23 | Design table has six rows and five command names; `reset` is one command (01 F2) | Design lines 112-121 | VERIFIED. |
| 24 | Seed brief line 64: `orca agent launch --agent <literal> --worktree path:<abs> ...` (02 E, G10; 05 header) | `seed-brief.md:60-67` | VERIFIED. Spec line 47 says the literal is "not repeated here" (PF-034). |
| 25 | Spec reason table, lines 334-358, has 52 names including `re-approved` and the two warning names (05 1.3) | Hand-count of spec lines 334-358 | VERIFIED (52). |
| 26 | Design 5.3 line 244 says `cli.py` is imported "lazily from `main.py`" (01 F1, 02 G11, 05 X14) | Design line 244 | VERIFIED. All three researchers correctly say this is inaccurate. |
| 27 | Design 8.4 line 625 says the runner is called with `cwd=worktree`, but the Protocol at 5.4 line 265 has no `cwd` (02 G1, 05 G-01, 01 F8 row 2) | Design lines 265, 625 | VERIFIED. The gap is real. |
| 28 | Design C21 (line 102) says `--method GET` is mandatory on "every G2 to G7 argv" (02 G2, 05 X9) | Design line 102 | VERIFIED as written. G2 is `gh issue list`, and G5/G6 are GraphQL. The sentence is wrong as stated. |
| 29 | `/usr/bin/orca-ide` exists here (symlink to `/opt/Orca/resources/bin/orca-ide`), and `/usr/bin/gh` exists | `ls -l` | NOTE. Relevant to X-3 below. 02 only mentions the `~/.local/bin` copy. |
| 30 | SKILL.md line 2140 says "If ANY QA gate has fewer than 6 agents, verdict is FAIL with severity CRITICAL"; the t2 sufficiency report applied it to the final gate only (04 B.5) | `SKILL.md:2136-2141`, `qa-qualitative-sufficiency-report.md:13-23` | VERIFIED. 04 describes the conflict accurately. |

Result: 29 of 30 claims hold exactly; row 13 is a cross-file conflict. No fabricated citations found.

## 2. Overlap-by-overlap comparison

### 2.1 Module layout and `main.py` registration (01 vs 05, with 02)

AGREE. 01 F1/F8, 02 X3 and 05 1.9 give the same import path (`superclaude.cli.issue_watch.cli`), the same `issue_watch_group`, the same `name="issue-watch"`, and the same insertion point (after line 561, which I verified). All three also say the design's "lazy import" sentence (line 244) is wrong, because the registration is eager. File lists match design section 11: 8 modules plus `__init__.py` under `issue_watch/`, plus 19 test files (8 per-module, 11 cross-cutting). Module-level import rules (`TID252`, function-level imports counting for the AST test) are consistent across 01, 03 and 05. One prose slip: 05's Summary says "9 source files plus `__init__`", but its own order table and design section 11 list 8 modules (the 9th "file" is `main.py`). MINOR (X-11).

### 2.2 Verb count (01 vs 05, 03)

CONFLICT. 01 F2 says the design's "six verbs" are five Click commands (`once`, `status`, `check-config`, `init-state`, `reset`), because `reset` is one command with two modes. I verified the design table (lines 112-121): six rows, five names. 03 section 8 also lists five verb names. 05 says "six verbs" in four places (1.8, `test_cli.py` asserts "help lists six verbs", P8 checkpoint "lists six verbs", and 1.9 "`--help` lists six verbs"). A test or gate that expects six entries in `--help` can never pass. See X-1.

### 2.3 PATH-stub pattern and the `test_conflict_e2e` / `test_conflict_scripts` citation (02 vs 03, with 01 and 05)

FACTS AGREE, RECOMMENDATIONS DIVERGE.
- Facts: 02 X13 and 03 sections 3 and 9 both say the PATH prepend lives in `test_conflict_scripts.py:167-179` and the e2e file only rewrites the stub. I verified `bin_dir` at 167, `os.pathsep` at 179, `_GH_STUB` at e2e:118, `chmod` at e2e:145, `_UV_STUB` at e2e:472. 01 F6 cites the e2e file for stub writing and gives the same lines. No contradiction.
- Both 02 and 03 say the existing pattern has no `shutil.which("gh")` guard and logs a flat `"$*"`; 03 adds that the design's exact-argv asserts need one record per argv element. 05 3.8 and the stub scenario format agree (JSON-line argv log).
- Divergence on stub names and PATH: see X-3. Divergence on committed versus runtime-written stubs: see X-9. Divergence on how `once` is invoked in e2e (CliRunner plus `monkeypatch.setenv`, per 02; `[sys.executable, "-m", "superclaude.cli.main", ...]` subprocess with `env=`, per 03): see X-9.
- `git` handling: 02 G5, 03 caveat 3 and 05 G-03 all raise it. Only 05 picks `stubs/git`; 02 and 03 leave "stub git or real tmp repo" open.

### 2.4 `Runner` `cwd` gap and the closed reason list (02 vs 05)

- `cwd` gap: AGREE on the defect and on the fix (optional `cwd` on `Runner.run`, `FakeRunner` records it). 02 G1 and 05 G-01/X11 are the same finding. 01 F8 row 2 lists the Protocol without `cwd` and does not mention the gap, and 03's `FakeRunner` description records argv only. These are propagation gaps only (MINOR, X-12).
- Closed reason list: PARTIAL. Both verify the spec table. 05 counts 52 names and I confirmed 52 (spec lines 334-358). 02 G3 reports that the table has no reason for a failed or incomplete marker read (G4) or a failed edit-timestamp read (G5), and that `audit.line` raises on any unknown reason. 05 never mentions this gap: its G-04 (no reason for `reset`), G-06 (`re-approved`) and G-07 do not cover it, and 05 1.4 only says "marker unknown". See X-4.

### 2.5 Gates and test names (03 vs 05)

- Test names and counts AGREE (design section 11/12 names; 19 files). 03 section 8's AC mapping is labelled INFERRED and matches 05's mapping except for small differences in which files carry a given AC (harmless).
- Gate list: 05 has 8 gates (adds `git diff --exit-code pyproject.toml Makefile` and a staging check) over 03's 7 design gates. That is a compatible superset. The commands themselves diverge from 03's findings: see X-7 (ruff pin) and X-8 (`make test`, `-n auto`).
- 03 notes `tests/conftest.py` has autouse `_pollution_snapshot` and `_redirect_reflexion_writes`, and `property_based` is registered but tied to hypothesis. 05 does not mention the first two and tags a test with `property_based` (X-10).

## 3. Checklist results

| # | Check | Result | Basis |
|---|---|---|---|
| 1 | Cross-file consistency | PARTIAL | Layout, registration, module order, test-file names and counts, Python 3.10 floor, eager-import fact and the `swarm.atomic` / `_ORCA_CLIS` reuse agree across files. Failures are X-1, X-2, X-3, X-6, X-7, X-8 below. |
| 2 | No contradictory claims | FAIL | Direct contradictions: verb count (X-1), C14 premise (X-6, 02 against 03/05), agent-literal handling (X-2), `property_based` tagging (X-10). |
| 3 | Shared dependencies documented consistently | PARTIAL | Python 3.10, xdist and hypothesis absent locally, ruff pin, click floor, `fcntl`/Linux-only are consistent where they appear. The xdist-absent and ruff-skew facts (02, 03) are not carried into 05's gate and checkpoint text (X-7, X-8). The `fromisoformat` / `Z` trap exists only in 05 (X-13). |
| 4 | Integration-point descriptions match | PASS with notes | `main.py`, `write_prepared_bytes`, `_find_orca`, `parse_origin_url`, claim marker and dual-surface read are described the same way. 02 is more exact than 05 on `_find_orca` failure inputs (X-14) and on the `cwd` signature (X-12). |
| 5 | Builder-must-resolve conflicts listed in one place or traceable | FAIL | No single register exists. 02 has G1-G15, 05 has G-01..G-21 and X1-X15, 04 has conflicts (a)-(e), 01 has three "design inconsistencies", and 03 has its own gap list. Several items appear in only one file. `research-notes.md` says "AMBIGUITIES_FOR_USER: None", which is inconsistent with the number of H-severity decisions. The consolidated register below is the fix. |

---

## 4. Register of conflicts and open decisions the builder must resolve

IDs here are this report's X-n. "Source" gives the research items; "Where it bites" says what breaks if unresolved.

### Blocking (IMPORTANT)

**X-1. Verb count: five Click commands versus "six verbs".** (01 F2 and 03 s8 against 05 1.8, `test_cli.py` row, P8 checkpoint, 1.9; design lines 177 and 759 also say six.)
Evidence: design table lines 112-121 has six rows, five names; `reset` is one command with optional `N`, `--forfeit-guarantee`, `--rate-limit`.
Where it bites: a `--help` assertion or P8 checkpoint "lists six verbs" fails forever; an item that says "implement six verbs" sends the implementer looking for a sixth.
Resolution to carry: five `@issue_watch_group.command(...)` functions; `reset` validates its own flag combination (`click.UsageError` gives exit 2); `--help` lists five names; say "six rows of the verb table" wherever the design number is quoted.

**X-2. How to handle the `ORCA_AGENT` literal.** (02 G10 against 05 T-F, G-20 and the 1.6 header.)
02 says state the value (`claude`, verified at `seed-brief.md:64`) in the task file, with a pin test holding the literal, because the PF-034 ban covers the spec and design text only. 05 says task items and docs must say "the seed-brief agent token", cites a "Project/user constraint: no model name in any file", and keeps the literal only in `launch.py` plus its pin test. Spec line 47 says only that the literal is "not repeated here" in the spec. I found no source for 05's "no model name in any file" rule in the CLAUDE.md files I was given or in `research-notes.md`; treat it as UNVERIFIED.
Where it bites: the `launch.py` item and the `test_launch.py` pin-test item cannot be written actionably without either the literal or an instruction to read an untracked file. `launch_argv` equality (AC-8, T10) also needs the value.
Resolution to carry: decide once whether task items may print `claude`. If not, the item must tell the executor to read `seed-brief.md:64` and the pin test must still hold the literal inline (never read `.dev/` from a test; the file is untracked and absent in CI, as 02 G10 and 05 T-G both say).

**X-3. PATH stubs do not isolate the real `orca-ide` (and the real `git`).** (02 G5 against 05 file list, P8, T-J; 01 and 03 do not address it.)
Evidence: `_ORCA_CLIS = ("orca-ide", "orca")` (`install_user_setup.py:35`), so `find_orca` tries `orca-ide` first. On this host `orca-ide` is at `/home/coder/.local/bin/orca-ide`, and also `/usr/bin/orca-ide` and `/bin/orca-ide` (I checked; 02 names only the first). 05 T-J proposes "PATH = stub dir + `/usr/bin:/bin`" and a guard "`which("orca-ide")` is None or stub". With `/usr/bin/orca-ide` present, that PATH still finds the real binary and the guard is false on this host. A stub named only `orca` is never reached. 05's file list also omits an `orca-ide` stub.
Where it bites: the e2e test could probe and then launch against the real Orca runtime, which contradicts design section 12 ("No test runs a real `gh`, `orca`, `git`") and NFR-003/NFR-001 intent.
Resolution to carry: use 02's rule: stubs named `orca-ide` and `orca` that both log argv; guards for `gh`, `orca-ide`, `orca` (and `git` if stubbed) using `shutil.which(name, path=env["PATH"])`; or a PATH holding only the stub directory plus symlinks to required tools (03 cites the precedent at `test_conflict_scripts.py:1555-1571`). Pick one PATH recipe (prepend, 02/03; replace, 05) and state it. Decide `git`: stub (05 G-03) or real tmp repo (03/02).

**X-4. Decisions that appear in one register only; no consolidated register; reason-list gap missing from 05.** (02 G3, G4, G8, G12, G13, G14 against 05 G-xx; 05 G-04, G-05, G-06, G-07, G-09, G-10, G-11, G-13, G-14, G-17..G-19, G-21 against 02.)
Items only in 02: G3 (no reason in the closed list for a failed or incomplete marker read G4 or edit-timestamp read G5; `audit.line` raises on unknown reasons; severity H), G4 (`marker_time` is never defined; define as `max(created_at, updated_at)`), G8 (skip the migration save in dry-run), G12 (event field null handling: every key is projected, so a field is `null` not missing), G13 (page longer than 100 is unreadable), G14 (label names with commas; `gh issue list --label` is a comma-splitting `strings` flag).
Items only in 05: G-04 (`reset` audit line has no reason), G-05 (`stderr_fallback` signature), G-06 (`REASONS` needs a companion mapping; `re-approved`), G-07 (`last_reason` enum versus `record` not importing `audit`), G-09 (`failed` to `failed` is not a T-row), G-10 (`sweep`/`day_cap_count` take store or doc), G-11 (owner module of `Deps`/`CycleResult`), G-13 (account-rename test), G-14 (`FakeRunner` value type), G-17 (FR-028 120 s case only on G1), G-18 (network-FS check reads `/proc/self/mountinfo`), G-19 (`reset N` with no entry), G-21 (`init-state` network-FS check).
Where it bites: `github.py`/`cycle.py` items will each hit a reason-enum decision (G3) that no item text resolves, and the executor either invents names or fails `test_audit`. `research-notes.md` states there are no ambiguities.
Resolution to carry: one merged decision table in the task file's Execution Context or Open Questions, with an owner or default for each, referenced from the items by index (TB-Add-3). For G3, 02's two options are to map onto `events_unreadable` / `events_incomplete`, or to add `marker_unreadable`/`edits_unreadable` to `REASONS` and to the test that pins `REASONS` to the spec table; 02 says to treat it as an owner question.

**X-7. `ruff` skew not carried into the gates.** (03 s6 against 05 final gates 2-3, 04 C.4 and Part D.)
Evidence: local `ruff` is 0.17.3 (`/usr/local/bin/ruff`, verified), pin is 0.15.20 (`pyproject.toml:54`, `uv.lock:1563-1564`, `.pre-commit-config.yaml:110`). 03 measured `ruff format --check src/ tests/` with 0.17.3 as "12 files would be reformatted" (all Markdown), but clean with the pinned version. I did not re-run `uv run ruff`; this rests on 03's measurement plus my confirmation of the binary version.
05 gate 3 writes `uv run ruff format --check src/ tests/` and labels it "ruff 0.15.20"; gate 2 `make lint` calls `uv run ruff check .`; 04 recommends scoped `uv run ruff check`/`format --check`. None says the local binary is a different version.
Where it bites: the validation item reports a failure unrelated to the task, and the fix-until-green clause may reformat unrelated files.
Resolution to carry: use 03's form `uvx --offline ruff@0.15.20 format --check src/ tests/` and `... check src/ tests/` (or scope to the changed files per 04 EX-A) and state the reason in the item.

**X-8. `make test` and `-n auto` as written are not runnable or not safe here.** (03 s1, s5, s6 and 02 s A against 05 final gate 4, P5 checkpoint, T-B.)
Evidence: xdist is not installed locally (02 A, 03 s1; CI installs it ad hoc at `test.yml:26-29`), so 05's "`uv run pytest tests/issue_watch/ -n auto`" and the P5 checkpoint "lock cases pass under `-n auto`" fail with an unrecognised-option error unless run as `uv run --with "pytest-xdist>=3.5,<4" pytest -n auto ...` (02's untested command). `make test` is the whole suite (17,096 tests collected) and includes `tests/cli/test_verify_sync_hooks.py`, whose docstring (verified, lines 7-15) says it mutates real files in `src/superclaude/hooks/` and `install_hooks.py`; 03 recommends the affected subset instead. 05 leaves "runtime for research 03 to size" and 03 answers "unknown".
Where it bites: either an unrunnable item, or an unbounded item that rewrites source files in the worktree.
Resolution to carry: name the exact commands (xdist via `--with`; affected-subset command from 03 s6), state that the full `make test` is a CI-side gate, or record an owner decision to run it. Design section 13 and AC-23 still list it as a gate, so say which wins.

### Non-blocking (MINOR)

**X-5. QA gate size at `qa_intensity: standard`.** (04 B.5/Part D against `SKILL.md` lines 1186-1187, 2140, 2299, 2363.)
04 recommends 3-agent intermediate gates, citing template I22 and the t2 precedent whose sufficiency report passed. The skill text says "an intermediate gate with fewer than 5 agents will be REJECTED during task file validation" (line 1186-1187) and "If ANY QA gate has fewer than 6 agents, verdict is FAIL with severity CRITICAL" (line 2140). The t2 report applied the rule only to the final gate (report lines 22-23). 04 flags this in its own Gaps (a) but still leaves the choice open. 05 says nothing about gate size. Record the decision and the risk (a CRITICAL from the A.10.5 sufficiency lens would cost a fix cycle).

**X-6. False premise of design C14 repeated.** 02 C14 is right: `tests/cli_portify/__init__.py` exists (verified), so a rootless `tests/issue_watch/test_cli.py` does not collide. 03 s9 says C14 "HOLDS", 05 1.0 repeats the collision claim, and `research-notes.md` line 24 repeats it. The conclusion (add `tests/issue_watch/__init__.py`) is unchanged. Give the real reason in the item (package convention; `tests/pr_submit` and `tests/cli_portify` are packages) or the item text will contain a false statement that an evidence-quality lens may flag.

**X-9. Stub materialisation, e2e invocation and lock-test mechanism are decided differently.** (a) Committed executable stubs (design 11, 05 3.8) versus copy-then-`chmod` into `tmp_path/bin` (03, to avoid a lost exec bit and xdist sharing; 01 adds shellcheck at warning severity for committed shebang files). (b) `CliRunner` with `monkeypatch.setenv("PATH", ...)` (02 X13) versus subprocess `-m superclaude.cli.main` with `env=` (03). (c) Design's `multiprocessing` two-process test (05) versus 03's `subprocess.Popen` + `fcntl.flock` form, which has repo precedent (`tests/unit/test_ccsession_tag.py:4496-4518`) and an `-n auto` risk note. Pick one of each and state it in the items.

**X-10. `property_based` tag.** Design C12 and 05 (`test_security_invariants`) tag the prompt-regex property test `property_based`. 03 recommends not tagging, because the marker text says "using hypothesis" (verified at `pyproject.toml:135`) and its only user is in `collect_ignore`. Both are legal under `--strict-markers`.

**X-11. Prose count.** 05 Summary says "9 source files plus `__init__`"; the order table and design section 11 list 8 modules plus `__init__` (the ninth entry is `main.py`). Fix wording to avoid a prose-versus-checklist mismatch (rf-qa check 19).

**X-12. `cwd` not propagated.** Even though 02 and 05 agree on the fix, 01 F8 row 2 (runner signature), 03's `FakeRunner` and 05 1.1/3.3 all still show argv-only. The task must state the final signature once (for example `Runner.run(argv, timeout, cwd=None)`) and use it in the `runner.py`, `launch.py`, `conftest.py` and `test_launch.py` items. Also note `LaunchOutcome`/retry rely on the stored `launch_cwd`.

**X-13. Python 3.10 self-check grep is incomplete.** 03 s5 gives `grep -rnE 'tomllib|datetime\.UTC|StrEnum|import Self|ExceptionGroup|asyncio\.timeout'`. 05 T-A / `record` trap 7 adds that `datetime.fromisoformat` rejects a trailing `Z` before 3.11 (the repo uses `fromisoformat` elsewhere, e.g. `sprint/models.py:244`, with its own data). Add `fromisoformat` to the grep or the executor will not catch it locally (local Python is 3.11.15).

**X-14. `find_orca` parity table scope.** 05 2.2 says exclude "the non-dict element" input. Per the code (verified), the original also raises uncaught `TypeError` for `topics: null`, and `AttributeError` for a string or dict `topics` (02 C19). The parity test's excluded set must cover every input where `topics` is not a list of dicts.

**X-15. Gap-ID collisions.** 02 uses `G1`-`G15`, 05 uses `G-01`-`G-21`, and the design uses `G1`-`G7` for argv builders and `C1`-`C22` / `S1` for citation rows (05 also uses `X1`-`X15`). "G3" can mean reason-enum gap, stubs/git (`G-03`) or the events REST call. Use this report's X-n, or prefix by file, in task-file references.

## 5. What holds up

- Citation accuracy is high. All 29 spot-checked file:line citations hold (section 1). The three that research files call "contradicted" (02 C14, C21 scope, X13 guard) are genuine design defects, not research errors; I confirmed C14 and the C21 wording myself.
- The five files cover the whole scope: package conventions (01), integration points and citation checks (02), test and gate infrastructure (03), template and examples (04), and a module-by-module breakdown with FR/NFR traceability (05). Every researcher states Status Complete, a Summary and a Gaps section.
- Where researchers overlap on facts (registration text, `write_prepared_bytes` reuse and missing directory fsync, `_ORCA_CLIS` import, `parse_origin_url` copy plus parity test, eager registration, Python 3.10, UV-only, no new marker, no new dependency), they agree, and the repo agrees with them.

## 6. Structured gap list

### CRITICAL
None.

### IMPORTANT (blocking)
| ID | Gap | Files | Fix owner |
|---|---|---|---|
| X-1 | "Six verbs" versus five Click commands; 05's `--help` assertion and P8 checkpoint cannot pass | 01, 03 against 05 | Correct 05 (or add a reconciliation note the builder reads) |
| X-2 | Agent-literal handling contradicts: 02 G10 says state `claude` in the task file; 05 T-F says never print it; 05's "no model name" source is unverified | 02 against 05 | Builder decision recorded in the task file; 05 to cite a source or drop the rule |
| X-3 | Stub plan does not isolate `orca-ide`; 05 T-J PATH recipe still reaches `/usr/bin/orca-ide` on this host; no `orca-ide` stub in 05's file list | 02 G5 against 05 | Correct 05 file list, PATH recipe and guards; decide `git` stub or real tmp repo |
| X-4 | No consolidated decision register; 02 G3/G4/G8/G12/G13/G14 are absent from 05, 05 G-04..G-21 absent from 02; `research-notes.md` says no ambiguities | 02, 05, research-notes | Merge into one register (this report's section 4 can serve as the base) |
| X-7 | Pinned-ruff versus local 0.17.3 skew not carried into 05's gates or 04's validation items | 03 against 05, 04 | Add pinned-ruff commands to 05 gate list |
| X-8 | `-n auto` and unqualified `make test` are not runnable or not safe as written (xdist absent locally; `test_verify_sync_hooks` rewrites source files) | 02, 03 against 05 | Correct 05 gate 4 and P5 checkpoint; name affected-subset command |

### MINOR (non-blocking)
X-5 (gate-size rule text versus 3-agent precedent), X-6 (C14 false premise repeated in 03 s9, 05, research-notes), X-9 (stub materialisation, e2e invocation and lock-test mechanism), X-10 (`property_based` tagging), X-11 ("9 source files" prose), X-12 (`cwd` signature not propagated into 01/03/05 module text), X-13 (3.10 grep lacks `fromisoformat`), X-14 (`find_orca` parity exclusions too narrow in 05), X-15 (gap-ID collisions across files). Also noted: swarm exit-idiom count is 73 by my pattern against 01's 71 (count-level difference only).

## 7. Limits of this check

- I did not run `uv run ruff`, `pytest`, `make` targets or any `gh`/`orca` command. Findings on ruff skew and xdist rest on the research files' own measurements plus my confirmation of binary versions and file contents.
- I did not re-verify every one of 02's 45 [CODE-VERIFIED] rows (for example help-output quotes for `gh` and `orca`); I re-checked the 29 repo-file citations listed in section 1.
- I did not read `tests/pr_submit/test_conflict_scripts.py` beyond the cited lines, the t2 and detection-contract task files, or `rf-qa.md` TB-Add text beyond the grep hits; 04's claims about them are not re-verified except where noted (row 30).

VERDICT: FAIL

Six IMPORTANT cross-file issues (X-1, X-2, X-3, X-4, X-7, X-8) block, none CRITICAL. All can be fixed by a short reconciliation addendum (or a corrected 05 plus the merged register in section 4) before the builder starts writing items. Report path: `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/qa/analyst-cross-validation-report.md`
