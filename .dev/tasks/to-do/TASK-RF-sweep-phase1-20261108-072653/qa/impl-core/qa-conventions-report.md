# QA Report: Conventions lens (impl-core gate, T185)

**Date:** 2026-11-12
**Lens:** repository patterns copied (lazy `__getattr__`, conftest seam fakes), frozen dataclasses and tuples, no new dependency, no unused abstraction, no speculative option, one-line comment for every builder decision (OQ-11, OQ-14).
**fix_authorization:** false. No file was edited except this report.
**Scope read:** `src/superclaude/cli/sweep/{__init__,models,classify,probes,report}.py` (all lines, in chunks of at most 150), `tests/sweep/{__init__,conftest,test_readonly}.py`, `.gitignore` diff, DESIGN 2.1, 7.1 to 7.5, 10, 11 (`docs/designs/orchestrator-mode.md`), `1.0a-facts.md`, `gitignore-check.md`, `step-1.4a-pytest.txt`, `step-1.4-pytest.txt`, `phase8-validation.md`, plus the pattern files `src/superclaude/cli/recommend/__init__.py:12-20`, `src/superclaude/cli/tasklist/__init__.py:9-15` and `tests/cli/reflect/conftest.py`.

## Findings

### F1 (MAJOR): three time parsers where DESIGN allows one, and the speculative agentWait key list is copied into two modules

Pattern departed from: DESIGN `docs/designs/orchestrator-mode.md:470` ("One function, `probes.parse_time` ... applies this rule") and `models.py:3-6` ("Times are aware UTC `datetime` values (parsed by `probes.parse_time`)").

Evidence:
- `src/superclaude/cli/sweep/probes.py:335-359` `parse_time` is the DESIGN rule (rejects a naive ISO form with `T`, rejects date-only).
- `src/superclaude/cli/sweep/classify.py:111-127` `_as_utc` is a second parser with a different rule, and `classify.py:130-138` `_wait_time` plus `classify.py:97` `_WAIT_TIME_KEYS` use it (called at `classify.py:257`).
- `src/superclaude/cli/sweep/report.py:108-126` `_wait_time` is a third parser (it calls `now.fromisoformat` through an instance, with `# type: ignore` at lines 122 and 125), and `report.py:41` repeats the same six-key tuple as `classify.py:97`.
- I ran both against the same input (`uv run --no-sync python -c ...`, nothing written):
  - `"2026-11-08T07:00:00"`: `parse_time` gives `None`, `classify._as_utc` gives `2026-11-08 07:00:00+00:00`.
  - `"2026-11-08"`: `parse_time` gives `None`, `_as_utc` gives `2026-11-08 00:00:00+00:00`.
  - `{"since": {"at": "2026-11-08T07:00:00Z"}}`: `classify._wait_time` gives `None`, `report._wait_time` gives `2026-11-08 07:00:00+00:00`.

What is wrong: the same agentWait value is read by two pure modules with different results (classify decides the `timestamp in the future` note; report decides the Waiting (a) sort order), and neither follows the single time rule. The six candidate keys are guesses (`1.0a-facts.md` row 6: `agentWait` was absent from all five captured `worker-show` outputs), repeated in two places.

Smallest fix: parse the agentWait time once. Either add one helper in `models.py` (stdlib only, so both pure modules can import it) that applies the `parse_time` rule and holds the key tuple, then delete `classify._as_utc`, `classify._wait_time`, `report._wait_time` and one `_WAIT_TIME_KEYS`; or have `probes.parse_worker_show` set a `datetime` field from `parse_time` and let both modules read it.

### F2 (MINOR): byte-exact literals and class indexes duplicated between classify and report

- `classify.py:75` `NOTE_WC13` and `report.py:35` `WC13_NOTE` are the same string; `classify.py:65-67` `NOTE_COULD_NOT_JOIN` and `report.py:34` `COULD_NOT_JOIN` are the same string. `report._could_not_determine` (`report.py:347`) and `report._retained_problems` (`report.py:374`) match against `classification.notes`, so a one-sided edit silently stops the match.
- `report.py:26-27` picks classes with `CLASSES[5]` and `CLASSES[7]`, while `classify.py:39-48` unpacks all eight into named constants.

Smallest fix: put the two notes in `models.py` next to `CLASSES` and import them in both modules; expose `C_IDLE` and `C_UNKNOWN` from `models.py` instead of indexing by position.

### F3 (MINOR): six public readers that nothing calls, with a `root` option nothing passes

Evidence: `probes.py:549` `read_ledger`, `:606` `read_packages`, `:691` `read_contract`, `:772` `read_transcript_tail`, `:805` `read_tab_map` and `:901` `read_worktree` are thin wrappers over `_ledger`, `_packages`, `_contract`, `_transcript`, `_tab_map` and `_read_worktree`. `collect` calls only the underscore twins (`probes.py:595, 879, 1191, 1200, 1248, 1288`). A repository search found no caller of any wrapper in `src/` or `tests/`. `read_ledger`, `read_contract` and `read_transcript_tail` also take a `root: Path | None = None` that DESIGN 7.1 (`orchestrator-mode.md:398-400`) does not list and no caller passes. `read_worktree` (`probes.py:901-904`) discards the package rows that `_read_worktree` returns, so it is not equivalent to what `collect` uses.

Mitigation, so this stays MINOR: DESIGN 7.1 and the section 11 test plan name these functions, and Phase 10 tests are expected to call `read_transcript_tail`.

Smallest fix: drop the `root` parameter from the three wrappers, or make `collect` call the public names so one path exists.

### F4 (MINOR): a field nobody reads, and a field added without the DESIGN mark or a comment

- `models.py:232` `SweepResult.context` is written at `classify.py:988` and read nowhere in `src/`; `render` and `to_json` take `ctx` as a separate argument (DESIGN 7.1 `orchestrator-mode.md:431-432`). DESIGN 7.2 line 468 lists "carried header data from `SweepInput`", which does not include the context.
- `models.py:130` `SessionRow.freshness_age_s` is not in DESIGN 7.2 (line 451 says the design "adds only the items marked (design)") and has no comment. It is read at `report.py:389-390` and written at `classify.py:934`.

Smallest fix: delete `SweepResult.context`. Add a one-line builder-decision comment on `freshness_age_s` in the style of `models.py:213`.

### F5 (MINOR): conftest carries dead fallbacks and task-item numbers that go stale

Pattern departed from: `tests/cli/reflect/conftest.py:58-80` (a seam fake with no conditional on code that does not exist yet).

Evidence: `tests/sweep/conftest.py:95-97` and `:129` say `probes.OrcaResult` and `_orca` exist "once item 8.10" or "from item 8.10"; `:116-118` does `getattr(probes, "check_orca_argv", None)` "added by item 8.10"; `:123` does `getattr(probes, "OrcaResult", None) or SimpleNamespace`. Both names now exist (`probes.py:93` and `probes.py:186`), so the `None` branch and the `SimpleNamespace` import (`conftest.py:15`) are dead. `tests/sweep/test_readonly.py:91` has the same kind of comment ("Item 10.4 re-points this ..."). A task checklist item number is meaningless once the package moves to `done/`.

Smallest fix: call `probes.check_orca_argv(tuple(args))` and `probes.OrcaResult(...)` directly, delete the `SimpleNamespace` import, and reword the comments without item numbers.

### F6 (MINOR): `JOIN_PATH` is a one-value switch that is only half wired

Evidence: `classify.py:37` `JOIN_PATH = "B"` is read once, at `classify.py:755` (`path_b = JOIN_PATH == "B"`, used at `:760-764`). The path A join at `classify.py:682-691` runs whatever `JOIN_PATH` says, and path B matching at `:692-697` runs after it. `1.0a-facts.md` row 1 says the question is CLOSED and "path A cannot apply".

Mitigation: DESIGN 11 (`orchestrator-mode.md:760`) still lists path A fixtures, so the constant may be the intended test switch.

Smallest fix: either make `JOIN_PATH` gate the path A block as well so it is a real switch, or delete the constant and the dead branch and update the DESIGN 11 path A fixtures in the same change.

### F7 (MINOR): autouse fixture name does not follow the repo's naming

`tests/sweep/conftest.py:21` `no_subprocess` is autouse and public. The repo's autouse fixtures are underscore-prefixed: `tests/conftest.py:29` `_pollution_snapshot`, `tests/conftest.py:83` `_redirect_reflexion_writes`, `tests/sprint/conftest.py:33` `_stub_phase_narrative`. Fix: rename to `_no_subprocess` (no test requests it by name in this phase).

### F8 (MINOR): "collections are tuples" is not true of two members

- `models.py:3` says collections are tuples. `models.py:230` `SweepResult.summary` is a `dict[str, object]` holding a nested `counts` dict (`classify.py:962-977`), so a frozen row still contains mutable state.
- `report.py:44` `NEXT_INSPECTION` is a mutable module-level `dict`.
- Private accumulators `probes._OrcaState` (`probes.py:957`) and `classify._Joins` (`classify.py:609`) are non-frozen dataclasses. This is fine because they are working state outside `models.py`.

Smallest fix: either reword `models.py:3` ("collections are tuples, except `summary`, which is a JSON-shaped dict") or hold `summary` as a tuple of pairs; wrap `NEXT_INSPECTION` in `types.MappingProxyType`.

### F9 (MINOR): builder decisions that are not marked in one line

- OQ-11 and OQ-14 are marked (see C17 and C18). The OQ-11 comment at `models.py:123-124` runs two lines.
- The key that joins a contract to an Orca row is a builder decision (DESIGN names none). It is built from two regexes at `probes.py:937-954` with only a "what" docstring. Its twin `classify.py:596` says "DESIGN names no key between a contract and its row; see the final report", and `classify.py:830-831` ends "(see the final report)". The final report is not in the repo, so the reason is lost.
- `classify.py:965` `historical = counts[C_IDLE]` (Historical means the `idle` class) has no comment.

Smallest fix: replace "see the final report" with the actual rule in one line, add the same one-line comment above `_CONTRACT_PATH_RE`, and comment `classify.py:965`.

### F10 (MINOR): nine `# type: ignore` in report.py come from typing parameters as `object`

`report.py:80, 84, 122, 125, 137, 161, 207, 376, 684`. `_iso`, `_window_text`, `_wait_time` and `_distinct` take `object` so that only `re`, `unicodedata` and `models` are imported (`report.py:3-6`), but `datetime` and `timedelta` are stdlib and `models.py` already imports them. `pyproject.toml` sets `warn_unused_ignores = true`, `mypy` is not installed in the venv and no workflow or Makefile target runs it, so these ignores are unchecked. A count over `src/superclaude/cli` finds 64 `type: ignore` in 23 files; `report.py` has 9, the second highest after `issue_watch/cycle.py` (19). Fix: type the parameters as `datetime`/`timedelta` and drop the ignores.

## Notes outside the lens (for the tests lens, not graded here)

- `tests/sweep/test_readonly.py:90-99` `test_one_git_argv_per_worktree` calls `probes._git` once per path it builds itself and then asserts the call count equals the path count, so it cannot fail; the comment at line 91 admits this until `collect` is wired.
- `tests/sweep/conftest.py:69-70` `GitFake` rebuilds the `--no-optional-locks` argv and `GIT_OPTIONAL_LOCKS=0` env itself, so a test that reads `GitFake.calls` checks the fake's copy, not `probes._git`. The `test_readonly.py` tests avoid this by patching `probes.subprocess.run`, which is correct.
- `sweep_group` (`sweep/__init__.py:6`) raises `ModuleNotFoundError` today because `commands.py` does not exist yet. The `__getattr__` body is identical to the pattern, so this is expected until the command item lands.

## Checks

Evidence for the PASS rows: `sweep/__init__.py:1-12` against `recommend/__init__.py:12-20` and `tasklist/__init__.py:9-15`; `git diff HEAD --stat -- pyproject.toml uv.lock Makefile` printed nothing; `git diff HEAD -- .gitignore` shows only the two added lines after `.dev/sprint-state/`; `ruff check --no-cache` and `ruff format --no-cache --check` over `src/superclaude/cli/sweep tests/sweep` gave "All checks passed!" and "9 files already formatted"; import lists of `models.py`, `classify.py` and `report.py` hold only stdlib and `.models`; the ten `ALLOWED_ORCA` templates, `ALLOWED_GIT`, `FORBIDDEN_TOKENS` and the byte limits at `probes.py:37-69` match DESIGN 7.3 (`orchestrator-mode.md:524-550`).

| Check | What it tests | Result |
|---|---|---|
| C1 | `sweep/__init__.py` is the lazy `__getattr__` pattern of `recommend` and `tasklist` (import inside the branch, `AttributeError` otherwise, `__all__`) | PASS |
| C2 | `tests/sweep/__init__.py` present as in `tests/__init__.py` and `tests/cli/reflect/__init__.py` | PASS |
| C3 | conftest seam fakes patch the module seam with `monkeypatch.setattr`, import `probes` inside the fixture, and name fixtures `patch_git` / `patch_orca` as `tests/cli/reflect/conftest.py:58-80` does | PASS |
| C4 | conftest has no conditional on code that does not exist (F5) | FAIL |
| C5 | autouse fixture name follows the repo's underscore prefix (F7) | FAIL |
| C6 | every `models.py` type is a frozen dataclass | PASS |
| C7 | collections in models are tuples as `models.py:3` states (F8) | FAIL |
| C8 | `models.py`, `classify.py` and `report.py` import only stdlib and `.models`; none imports `subprocess`, `click`, `os` or `shutil` | PASS |
| C9 | no dependency added (pyproject and lock unchanged, all imports stdlib or pytest) | PASS |
| C10 | `.gitignore` gets the two lines of DESIGN 10 after `.dev/sprint-state/`, nothing else | PASS |
| C11 | allowlist constants match DESIGN 7.3 token for token | PASS |
| C12 | one time-parsing rule, as DESIGN 7.2 line 470 says (F1) | FAIL |
| C13 | no literal or class index duplicated between the pure modules (F2) | FAIL |
| C14 | no unused abstraction in `probes.py` (F3) | FAIL |
| C15 | no unused field in `models.py` and no unmarked addition to DESIGN 7.2 (F4) | FAIL |
| C16 | no speculative option (F6 for `JOIN_PATH`; the agentWait key list is counted in F1) | FAIL |
| C17 | OQ-11 comment present (`models.py:123-124`, `report.py:400`) | PASS |
| C18 | OQ-14 comment present (`models.py:213`, matches DESIGN line 468) | PASS |
| C19 | every other builder decision carries a one-line comment (F9) | FAIL |
| C20 | no avoidable `type: ignore` noise (F10) | FAIL |
| C21 | `ruff check` and `ruff format --check` clean on the new files | PASS |

## Self-audit

- Read in full, in chunks of at most 150 lines: `models.py` (239), `classify.py` (996), `probes.py` (1294), `report.py` (692), `conftest.py` (157), `test_readonly.py` (166), `sweep/__init__.py` (12), and the two pattern files. DESIGN 2.1, 7.1 to 7.3, 7.5 (headings), 10 and 11 were read; 7.4 was read as a schema only.
- Not run: `pytest` (the task's own recorded runs, `step-1.4a-pytest.txt`, `step-1.4-pytest.txt` and `phase8-validation.md`, all show 4 passed; I did not re-run them, so that is reliance, not verification). `mypy` is not installed in the venv, so the `type: ignore` comments could not be checked.
- The only Python I ran was a read-only `-c` snippet with `PYTHONDONTWRITEBYTECODE=1` that called `parse_time`, `_as_utc` and the two `_wait_time` functions and read `sweep_group`; it wrote no file.
- Possible blind spot: DESIGN sections 7.4 and 7.5 were checked for names and structure, not for every rendered string; that belongs to the correctness lenses.

Verdict: FAIL
Blocking count: 1
