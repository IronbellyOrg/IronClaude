# QA Report: interface-conformance lens (T179), impl-core gate

**Topic:** `/sc:sweep` Phase 1 core modules (`src/superclaude/cli/sweep/`) against DESIGN 7.1 to 7.5
**Date:** 2026-11-12
**Phase:** code gate, interface-conformance lens (report-only, `fix_authorization: false`)
**Design file read:** `docs/designs/orchestrator-mode.md` (sections 2.1, 7.1 to 7.5, 10, 11), with SPEC `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md` lines 227 to 262 for the SPEC field lists.
**Files read in full, in chunks of at most 150 lines:** `__init__.py`, `models.py`, `classify.py`, `probes.py`, `report.py`, `tests/sweep/conftest.py`, `tests/sweep/test_readonly.py`, `.gitignore` diff, `1.0a-facts.md`, `phase8-validation.md`, `step-1.4a-pytest.txt`, `gitignore-check.md`. `commands.py` does not exist yet and is outside this gate's file list.

---

## Findings

### F1 (MAJOR): `WorktreeState.frozen` is declared and consumed but never populated, so the FR-013 "frozen plan" condition cannot fire

- **Evidence:**
  - `src/superclaude/cli/sweep/probes.py:840` and `:862` set `frozen=None` on every `WorktreeState` that `collect` builds (`:862` carries the comment "no named source for a frozen plan in Phase 1").
  - `src/superclaude/cli/sweep/classify.py:486-487` (`removable`) returns `("no", "frozen plan")` only when `worktree.frozen is True`.
  - `classify.py:851-868` (`_prepare_worktrees`) never sets `frozen`, and `classify_all` (`:877-996`) computes `policy_of(row)` per row (`:957`) but never copies the result to the worktree that hosts the row.
  - `report.py:666` emits `w.frozen` into JSON, so the key is always `null` on a real run.
  - A named source does exist: `policy_of` (`classify.py:410-422`) returns `"frozen"` from the contract, and `OrcaObservation.worktree_path` links a row to its worktree.
- **Run evidence (inline smoke, read-only, `uv run python -I`):** one Orca row with `worktree_path="/w"`, a `failed` contract carrying `E-HALT-QA`, and a `WorktreeState("/w", ..., frozen=None)`. Result: `policy frozen | class waiting on a person b` and `worktree frozen: None | removable: could not determine | report read, open PR and unmerged commits not observable`. The row is frozen, its worktree is not.
- **What is wrong:** SPEC FR-013 (merged-requirements.md line 107) lists "a frozen plan" as a condition that makes a worktree `removable: no` with the condition named. The interface carries the field, the reader of it (`removable`) and the JSON key, but the producer side is a constant `None`. The call site exists and its result is dead. The "deferred / no named source" comment does not change that, because the named source (`policy_of` plus `worktree_path`) is already in the module. Only a hand-built `WorktreeState(frozen=True)` fixture reaches the branch, so a one-fixture-per-condition unit test would pass while the real pipeline never reports it.
- **Smallest fix:** in `classify_all`, before `_prepare_worktrees`, collect `frozen_paths = {_norm(o.worktree_path) for each Orca row whose SessionRow has policy_of(row) == "frozen" and o.worktree_path}` and pass it in, so `_prepare_worktrees` does `replace(w, frozen=True)` for a worktree whose `_norm(w.path)` is in the set (leave None otherwise, never False). Add one `test_classify.py` fixture that goes through `classify_all`, not a hand-built `WorktreeState`.

---

### Minor findings (notes only, never fail the gate)

| Id | file:line | Note | Smallest fix |
|---|---|---|---|
| M1 | `__init__.py:4`, `:12` | DESIGN 7.1 gives `def __getattr__(name: str) -> object`; the code has no return annotation. `__all__ = ["sweep_group"]` is not in the design, and with `commands.py` absent, `hasattr(pkg, "sweep_group")` and `from superclaude.cli.sweep import *` raise `ModuleNotFoundError`, not `AttributeError`. Resolves itself when `commands.py` lands. | Add `-> object`; drop `__all__` or keep it once `commands.py` exists. |
| M2 | `report.py:566`, `:599` | `sanitize(text: object)` and `cell(text: object)`; DESIGN 7.1 says `text: str`. Wider parameter, same return type. | Optional: narrow to `str`, or note the widening. |
| M3 | `report.py:542` | `SECTIONS` has no annotation; DESIGN 7.1 gives `tuple[Callable[[SweepResult, SweepContext], str], ...]`. Contents and order match (12 functions). | Add the annotation. |
| M4 | `probes.py:549`, `:691`, `:772` | `read_ledger`, `read_contract` and `read_transcript_tail` take an extra optional `root: Path \| None = None`; DESIGN 7.1 shows `(path)` only. Backward compatible. | Note the extra parameter in the design, or keep as is. |
| M5 | `probes.py:94-97`, `:222`, `:268` | `OrcaResult.data` for `ok` is the envelope's `result` object (and a `str` Run id for `run-current`); DESIGN 7.1 comment says "parsed JSON for ok". The code comment states it, and it matches the captured fixtures (`.result.workers`, `.result.dispatch`). | Align the design comment. |
| M6 | `probes.py:990` | Three source rows per Run: `orca worker-list <run>`, `orca task-list <run>` and an extra `orca task-list --ready <run>`. DESIGN 7.4 names two. `classify._origin_unknown` reads only the first two, so no behaviour breaks; a prefix test on `orca task-list` would see two names. | Note the third row in DESIGN 7.4. |
| M7 | `models.py:230`; `classify.py:962-977` | `SweepResult.summary` is a `dict` (and `counts` a nested `dict`) inside a frozen dataclass, while the models docstring (`models.py:3`) says "collections are tuples". A frozen dataclass holding a dict is unhashable. | Accept, or use a small frozen `Summary` type. |
| M8 | `models.py:125-134` | `SessionRow` has nine dimension fields plus an extra `freshness_age_s`; DESIGN 7.2 says "the ten #409 dimensions". The tenth, `Policy`, is printed from `ClassifiedRow.policy` (`report.py:400`). This is the recorded OQ-11 builder decision; the dimension names never reach JSON (see C11). | None. |
| M9 | `report.py:34-35`, `:41`; `classify.py:65`, `:75`, `:97` | `COULD_NOT_JOIN`, `WC13_NOTE` and `_WAIT_TIME_KEYS` are defined twice, once per pure module. Equal today, so a drift risk only. | Have `report.py` import them from `classify.py`, or from `models.py`. |
| M10 | `tests/sweep/conftest.py:149-157` | `sweep_home` only moves `HOME` and `XDG_STATE_HOME`; DESIGN 11 line 753 also lists a layout holding packages, contracts, transcripts and an `orca-tabs/` folder. Later test files can build it. | Extend when the first consumer is written. |
| M11 | `probes.py:397`, `:399`; `models.py:70` | `status` and `dispatch_status` both come from `dispatch.status`, so Rule 5 (`status == "in_progress"`) cannot match; `1.0a-facts.md` row 6 records exactly this ("Rule 5 cannot match; rows fall to the fallback"). `OrcaObservation.unsupervised` and `ContractRecord.report_path` / `artifacts` are populated or declared but no rule or report reads them. All follow the SPEC field list; informational. | None. |

---

## Check detail

| Id | What was compared | Result and evidence |
|---|---|---|
| C1 | `__init__.py` against DESIGN 7.1 (`__getattr__`, lazy `sweep_group`) | Name and lazy import match (`__init__.py:4-9`); annotation and `__all__` differences are M1. |
| C2 | Every `models.py` dataclass against DESIGN 7.2 and SPEC lines 229 to 243 | All 15 types present and frozen (introspection run): `SweepContext`, `OrcaObservation`, `ContractRecord`, `TranscriptTail`, `TabMapEntry`, `SessionRow`, `StatusParse`, `PackageRecord`, `WorktreeState`, `Classification`, `SafeToClose`, `SourceCoverage`, `SweepInput`, `ClassifiedRow`, `SweepResult`. Field names, order and `\| None` types match, including the R3-B1 fields (`dispatch_started`, `dispatch_ended`, `dispatch_status`, `first_record_ts`, `tail_complete`) and `upstream_note`. |
| C3 | Constants in `models.py` | `JSON_SCHEMA_VERSION = 1`; `CLASSES` has the 8 names in DESIGN order; `PACKAGE_STATES` has the 6 names in precedence order; `SAFE_VALUES` is `yes`, `no`, `could not determine` (`models.py:16-39`). |
| C4 | `ClassifiedRow` shape | Exactly `row`, `classification`, `policy`, `safe` (`models.py:214-219`); introspection prints those four names, in that order. |
| C5 | `classify.py` public signatures against DESIGN 7.1 | `Rule(name, match)` frozen; `classify(row, ctx) -> Classification`; `policy_of(row) -> str \| None`; `package_state(pkg) -> str`; `mark_shared_packages(worktrees) -> tuple[WorktreeState, ...]`; `safe_to_close(row, worktree) -> SafeToClose`; `removable(worktree) -> tuple[str, str]`; `classify_all(inp, ctx) -> SweepResult`. All match. |
| C6 | `RULES` order, names, count | Runtime print: `blocked_contract, orca_exit_proof, fenced, waiting_signal, working, finished, idle, person_active, fallback`, 9 entries, same as the DESIGN 7.2 table. |
| C7 | `probes.py` seams and classes against DESIGN 7.1 | `Budget(shows=50, total_s=90.0, per_call_s=10.0, clock=time.monotonic)` with `share_shows`, `take_show`, `call_timeout`, `cut`; `OrcaResult(kind, data, reason)` frozen; `BindingError`, `GitCallFailed`; `orca_binary()`; `check_orca_argv`; `check_git_args`; `_orca(*args, timeout)`; `_git(cwd, *args, timeout)`; `bind_run(budget) -> str`. Defaults and return types match. |
| C8 | `probes.py` parsers, readers and `collect` | `parse_time`, `parse_worker_show(run, list_row, show)`, `collect(ctx, runs, root, budget) -> SweepInput`, `read_worktree(path, budget) -> tuple[WorktreeState, SourceCoverage]`, `parse_status(raw)`, `read_packages(worktree)`, `read_tab_map(state_dir)`, `read_orca_version(path=ORCA_VERSION_FILE)` all match. `read_ledger`, `read_contract` and `read_transcript_tail` carry one extra optional parameter (M4). No design name is missing. |
| C9 | DESIGN 7.3 constants | `ORCA_BINARY_DEFAULT`, `ALLOWED_ORCA` (10 templates, same order and tokens), `FORBIDDEN_TOKENS`, `ALLOWED_GIT`, `ORCA_VERSION_FILE`, `OUTPUT_LIMIT`, `CONTRACT_LIMIT = LEDGER_LIMIT`, `LEDGER_SPLIT`, `TRANSCRIPT_TAIL`, `WORKER_LIST_PAGE` present with the design values (`probes.py:37-69`); `RUN_ID_RE` and `DISPATCH_ID_RE` match `1.0a-facts.md` row 2. The over-limit ledger read searches the tail only, which matches GQ-105 ("head and tail are read and the tail is searched"). |
| C10 | `report.py` public names against DESIGN 7.1 | `CHECKED_ORCA_VERSION: str = "1.4.245"`, `CELL_MAX: int = 200`, `SECTIONS` (12 functions), `sanitize`, `cell`, `render(result, ctx) -> str`, `to_json(result, ctx, report_path) -> dict[str, object]`. Parameter and annotation differences are M2 and M3. |
| C11 | JSON v1 key set against DESIGN 7.4, and no dimension field in it | Runtime print of `to_json`: top keys `collected, observed_at, orca_available, report_path, rows, schema_version, scope, sources, summary, waiting, window, worktrees` (12); row keys `class, evidence, notes, person_started, policy, row_id, rule, safe_to_close, waiting_kind` (9); summary keys `bound_reached, counts, historical, total, total_is_lower_bound, visible`; `counts` has exactly the `CLASSES` names. The intersection of the row keys with `lifecycle, phase, health, approval, freshness, freshness_age_s, result, admission, evidence_packet, tests_review` is the empty set. Worktree and package key lists read at `report.py:659-678` match DESIGN 7.4 (the smoke input had no worktree, so those were checked by reading, not by a run). |
| C12 | Report layout (DESIGN 7.5) | Runtime print of the `## ` headings in render order: Source coverage, Waiting (a), Waiting (b), Could not determine, Retained problems, Sessions, Worktrees, Historical sessions, Shift Brief, What I could not determine; render ends with `Report complete\n`. Fixed lines (`READ ONLY . observed`, `Orca lock risk`, `BOUND_LINE`, `PAGE_LINE`, `WORKTREES_LINE`, `SP24_LINE`, the (a) table headers) match the DESIGN text on reading. |
| C13 | Caller-liveness: every interface field that a consumer reads is set by a producer | `WorktreeState.frozen` fails: always `None` (F1). Other consumed fields checked and live: `unpushed`, `upstream_note`, `dev_tasks_unsaved`, `PackageRecord.active`, `shared_package_ids`, `removable`, `removable_reason`, `session_join`, `dispatch_started`, `dispatch_ended`, `dispatch_status`, `first_record_ts`, `tail_complete`, `gate_policy`, `task_spec_text`. |
| C14 | `.gitignore` lines (item 8.6, DESIGN section 10) | `git diff .gitignore` shows exactly the comment line plus `.dev/sweeps/`, two insertions after the `.dev/sprint-state/` entry; `gitignore-check.md` records `check-ignore` 0 for `.dev/sweeps/x.md` and 1 for `.dev/tasks/to-do/x.md`. `.dev/tasks/` is not covered. |
| C15 | `tests/sweep` scaffolding against DESIGN 11 | `conftest.py` has the autouse process guard (respects the function-level `integration` mark), `patch_git`, `patch_orca`, `fixed_now`, `sweep_home`; `test_readonly.py` has the four step-1.4a cases, and the names they use (`probes._git`, `probes.check_git_args`, `probes.ALLOWED_GIT`, `probes.subprocess.run`) all exist. Re-run now: `uv run pytest tests/sweep -q -p no:cacheprovider` gives 4 passed, matching `step-1.4a-pytest.txt` and `phase8-validation.md`. `sweep_home` layout gap is M10. |
| C16 | Parser field paths against the live capture (`1.0a-facts.md` and `tests/sweep/fixtures/captured-*.json`) | `result.dispatch.{assigneeHandle, dispatchedAt, completedAt, status}`, `result.projection.liveness.verdict`, `result.projection.outcome`, `result.terminal.worktreePath`, list-row `dispatchId`, `result.workers`, `result.page`, `result.worktrees[].path` all exist in the fixtures (jq key listings). The two time forms in the facts file are accepted by `parse_time`. |
| C17 | Purity and import list | `models.py` imports only `dataclasses`, `datetime`, `pathlib`; `classify.py` imports `re`, `collections.abc`, `dataclasses`, `datetime`, `pathlib` and `.models`; `report.py` imports `re`, `unicodedata` and `.models`. None of `subprocess`, `click`, `os`, `shutil` appears in `classify.py` or `report.py` (import blocks read at `classify.py:10-33`, `report.py:11-21`). `subprocess` is imported only in `probes.py:15`. |
| C18 | Extra, renamed or missing names | Missing: none. Renamed: none (`ClassifiedRow` and the `Rule.name` values are the DESIGN names). Extra public names: `classify.JOIN_PATH`, `C_*`, `NOTE_*`, `REASON_*`, `POLICY_*`; `probes.ReadFailed`, `RUN_ID_RE`, `DISPATCH_ID_RE`, `Budget.orca_calls`, `Budget.budget_reason`, `Budget.show_cap_reason`; `report.NO_RECORDS`, `DISTINCT`, `BOUND_LINE`, `PAGE_LINE`, `WORKTREES_LINE`, `NEXT_INSPECTION`. All are constants or helpers that the design implies; the two Run-id regexes are named in DESIGN 7.3. No extra field appears in the JSON key set. |

## Checks

| Check | Result |
|---|---|
| C1 | PASS |
| C2 | PASS |
| C3 | PASS |
| C4 | PASS |
| C5 | PASS |
| C6 | PASS |
| C7 | PASS |
| C8 | PASS |
| C9 | PASS |
| C10 | PASS |
| C11 | PASS |
| C12 | PASS |
| C13 | FAIL (F1) |
| C14 | PASS |
| C15 | PASS |
| C16 | PASS |
| C17 | PASS |
| C18 | PASS |

## Summary

- Checks passed: 17 / 18. Checks failed: 1 (C13).
- Findings: 1 MAJOR (F1), 11 MINOR (M1 to M11, notes only).
- Name, signature, default and return-type conformance to DESIGN 7.1 to 7.3 is complete: no missing or renamed public name, and no differently typed one beyond the minor widenings in M2 to M5.
- `ClassifiedRow` is `row`, `classification`, `policy`, `safe`; no dimension field is in the JSON key set.
- Not checked by this lens: rule semantics, join behaviour and sanitizer completeness (other gates); `commands.py` (not yet written).
- Tool engagement (approximate): Read about 38 | Grep 9 | Glob 4 | Bash about 17 (introspection, smoke runs, jq key listings, pytest re-run, git diff). Each call maps to a check above. No web lookups.
- Files written: this report only. The smoke runs used `python -I` with `PYTHONDONTWRITEBYTECODE=1` and `-p no:cacheprovider`.

Verdict: FAIL
Blocking count: 1
