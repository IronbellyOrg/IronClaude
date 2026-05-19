# QA Report — PG-2 task-integrity (Phase 2)

**Topic:** sprint-state-migration — Phase 2 source-edit verification
**Date:** 2026-05-19
**Phase:** task-integrity (PG-2)
**Fix cycle:** 1 (initial gate)
**Task:** TASK-RF-track-1-20260518-231708
**Branch:** feat/sprint-state-migration

---

## Overall Verdict: PASS

All six acceptance criteria (AC1..AC6) verified directly against the working-tree source files. Zero discrepancies between the aggregation report's claimed diffs and what is on disk. Zero regressions vs. baseline. All 11 tests in `tests/sprint/test_tmux.py` pass when re-executed.

---

## Per-AC Verdicts

| AC | Verdict | Severity (if FAIL) | Summary |
|----|---------|--------------------|---------|
| AC1 | PASS | — | `state_dir` field + sentinel derivation + `_derive_tasklist_id` present at models.py:399 / 401-413 / 466-471 with exact spec |
| AC2 | PASS | — | `load_sprint_config()` accepts `state_dir: Path \| None = None` (config.py:288) and forwards as `state_dir if state_dir is not None else Path("")` (config.py:356) |
| AC3 | PASS | — | `--state-dir` Click option (commands.py:182-188), `state_dir_override` param (206), env-var resolution (223-227), threading to load_sprint_config (242), re-derivation block with original_release_dir_name captured BEFORE mutation (251-268) |
| AC4 | PASS | — | executor.py:1751-1758 has 3-line state_dir block + comment + original try/except; tmux.py:166 reader migrated to `config.state_dir` |
| AC5 | PASS | — | tests/sprint/test_tmux.py:99-102 writes to `config.state_dir` after `mkdir(parents=True, exist_ok=True)` |
| AC6 | PASS | — | Ruff delta = 0 (11/11), pytest delta = 0 (57f/1350p/1s), all 11 `test_tmux.py` tests pass (re-verified live) |

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | AC1 — state_dir field present | PASS | models.py:399 `state_dir: Path = field(default_factory=lambda: Path(""))` (exact) |
| 2 | AC1 — _derive_tasklist_id helper | PASS | models.py:401-413; preference order release_dir.name → index_path.parent.name → index_path.stem → "default" matches spec |
| 3 | AC1 — sentinel derivation in __post_init__ | PASS | models.py:466-471 `if self.state_dir == Path(""): object.__setattr__(self, "state_dir", Path(".dev/sprint-state") / self._derive_tasklist_id())` |
| 4 | AC1 — PipelineConfig.__post_init__ claim | PASS | pipeline/models.py:180 class PipelineConfig declared with NO __post_init__ method (verified by grep) — aggregation report's note 1 is accurate |
| 5 | AC2 — load_sprint_config signature | PASS | config.py:288 `state_dir: Path \| None = None,` |
| 6 | AC2 — forwarded to SprintConfig | PASS | config.py:356 `state_dir=state_dir if state_dir is not None else Path(""),` exact-match |
| 7 | AC3 — --state-dir Click option | PASS | commands.py:182-188; type click.Path(file_okay=False, path_type=Path), default=None, dest `state_dir_override` |
| 8 | AC3 — run() signature param | PASS | commands.py:206 `state_dir_override: Path \| None,` |
| 9 | AC3 — env-var resolution | PASS | commands.py:223-227 uses `Path(os.environ["SPRINT_STATE_DIR"]) if os.environ.get("SPRINT_STATE_DIR") else None` and `import os` present at commands.py:9 |
| 10 | AC3 — threaded to load_sprint_config | PASS | commands.py:242 `state_dir=state_dir,` |
| 11 | AC3 — re-derivation block + ordering | PASS | commands.py:251 `original_release_dir_name = config.release_dir.name` captured BEFORE `object.__setattr__(config, "release_dir", resolved)` at line 253. Condition on lines 259-263 matches spec (`state_dir is None AND config.state_dir == Path(".dev/sprint-state") / original_release_dir_name`). Re-derivation at 264-268. |
| 12 | AC4 — executor.py 3-line block | PASS | executor.py:1751-1758 — comment includes "state_dir (non-tracked transient path)"; lines 1754-1756 are exact 3-line block; lines 1753+1757 are original `try: ... except OSError: pass` wrapping |
| 13 | AC4 — tmux.py reader | PASS | tmux.py:166 `sentinel = config.state_dir / ".sprint-exitcode"` (exact); other release_dir uses at tmux.py:58, 60, 87 intentionally retained |
| 14 | AC5 — test_tmux.py fixture migration | PASS | test_tmux.py:99-102 contains `config.state_dir.mkdir(parents=True, exist_ok=True)` then `sentinel = config.state_dir / ".sprint-exitcode"` then `sentinel.write_text("0\n")` |
| 15 | AC6 — ruff delta | PASS | baseline-summary.md = 11 errors; phase2-summary.md = 11 errors; delta 0; none in target files |
| 16 | AC6 — pytest delta | PASS | baseline = 57f/1350p/1s; phase2 = 57f/1350p/1s; identical failing-test set per aggregation report |
| 17 | AC6 — 11 tests in test_tmux.py pass | PASS (re-verified live) | `uv run pytest tests/sprint/test_tmux.py -v` = 11 passed in 0.11s |

---

## Verification evidence

### Tool engagement (all verifications mapped to specific ACs)

- Read calls: 8 (aggregation report; baseline + phase2 summaries; models.py:390-480 (2 ranges); config.py:280-365; commands.py:170-280; executor.py:1745-1764; tmux.py:160-180; test_tmux.py:1-50 + 85-115)
- Grep calls: 7 (state_dir in each of the 6 source files + os import in commands.py)
- Bash calls: 4 (wc -l for all 6 files; test-function counter; PipelineConfig grep; live pytest re-run)

Total tool calls (Read+Grep+Bash) = 19; total verification items = 17. Tool count ≥ item count, so the verification floor is satisfied per the QA tool-engagement minimum.

### Cited file:line lookups

**AC1 evidence:**
- `src/superclaude/cli/sprint/models.py:399` — `state_dir: Path = field(default_factory=lambda: Path(""))` ✓ exact-match with aggregation hunk
- `src/superclaude/cli/sprint/models.py:398` — preceded by the documentation comment that mentions SPRINT_STATE_DIR env var override
- `src/superclaude/cli/sprint/models.py:401-413` — `_derive_tasklist_id` helper exists with the documented preference order; lines 408-409 implement release_dir guard (`!= Path(".")` AND name not in ("", "."))
- `src/superclaude/cli/sprint/models.py:463-471` — sentinel derivation block inside `__post_init__`, comparing against `Path("")` and writing through `object.__setattr__`
- `src/superclaude/cli/pipeline/models.py:180` — `class PipelineConfig:` declared but `grep -n "def __post_init__\|class PipelineConfig" pipeline/models.py` returns ONLY the class line (no __post_init__), confirming aggregation note 1 is accurate

**AC2 evidence:**
- `src/superclaude/cli/sprint/config.py:288` — `state_dir: Path | None = None,` exact-match
- `src/superclaude/cli/sprint/config.py:290-294` — docstring augmented with state_dir description
- `src/superclaude/cli/sprint/config.py:356` — `state_dir=state_dir if state_dir is not None else Path(""),` exact-match with hunk

**AC3 evidence:**
- `src/superclaude/cli/sprint/commands.py:9` — `import os` present (required for `os.environ.get("SPRINT_STATE_DIR")`)
- `src/superclaude/cli/sprint/commands.py:182-188` — `--state-dir` Click option matches spec (dest `state_dir_override`, type click.Path(file_okay=False, path_type=Path), default=None, help text mentions $SPRINT_STATE_DIR and .dev/sprint-state/<tasklist-id>/)
- `src/superclaude/cli/sprint/commands.py:206` — `state_dir_override: Path | None,` exact param
- `src/superclaude/cli/sprint/commands.py:223-227` — env var resolution: `state_dir = state_dir_override or (Path(os.environ["SPRINT_STATE_DIR"]) if os.environ.get("SPRINT_STATE_DIR") else None)` exact-match
- `src/superclaude/cli/sprint/commands.py:242` — `state_dir=state_dir,` threaded into load_sprint_config call
- `src/superclaude/cli/sprint/commands.py:250` — `if release_dir_override is not None:` branch
- `src/superclaude/cli/sprint/commands.py:251` — `original_release_dir_name = config.release_dir.name` — **captured BEFORE** mutation
- `src/superclaude/cli/sprint/commands.py:252-254` — release_dir + work_dir mutations come AFTER the capture
- `src/superclaude/cli/sprint/commands.py:259-268` — re-derivation block: condition `state_dir is None and config.state_dir == Path(".dev/sprint-state") / original_release_dir_name`; setter writes `Path(".dev/sprint-state") / resolved.name`
- Ordering check: line 251 (capture) < line 253 (mutation) ✓ — the "capture before mutation" requirement in AC3 is structurally satisfied

**AC4 evidence:**
- `src/superclaude/cli/sprint/executor.py:1751` — leading comment: `# Write sentinel exit code file in state_dir (non-tracked transient path) so tmux caller can read the outcome` — contains the required "state_dir (non-tracked transient path)" phrase
- `src/superclaude/cli/sprint/executor.py:1753-1758` — full try/except block:
  - Line 1753: `try:`
  - Line 1754: `state_dir = config.state_dir`
  - Line 1755: `state_dir.mkdir(parents=True, exist_ok=True)`
  - Line 1756: `(state_dir / ".sprint-exitcode").write_text(str(_exitcode))`
  - Line 1757: `except OSError:`
  - Line 1758: `pass  # best-effort; do not mask the real exit`
  All three new lines are inside the original try/except — verified.
- `src/superclaude/cli/sprint/tmux.py:166` — `sentinel = config.state_dir / ".sprint-exitcode"` — exact-match single-line change
- Other release_dir uses in tmux.py confirmed intentionally retained: lines 58 (`def session_name(release_dir: Path) -> str:`), 60 (hashing for session name), 87 (`name = session_name(config.release_dir)`) — these are NOT exit-code-sentinel uses

**AC5 evidence:**
- `tests/sprint/test_tmux.py:87-103` — `TestThreePaneLayout::test_launch_creates_three_panes` at line 88, fixture migration at lines 99-102:
  - Line 99: `# Make the sentinel read succeed with exit 0 so launch returns cleanly.`
  - Line 100: `config.state_dir.mkdir(parents=True, exist_ok=True)` ← preceding mkdir confirmed
  - Line 101: `sentinel = config.state_dir / ".sprint-exitcode"`
  - Line 102: `sentinel.write_text("0\n")`
- Test is at ~line 100 as claimed.

**AC6 evidence:**
- `phase-outputs/test-results/baseline-summary.md:13-17` — 11 ruff errors, all in pre-existing files (tests/sprint/diagnostic, conftest), none in target files
- `phase-outputs/test-results/baseline-summary.md:21-35` — 57 pytest failures all share `AttributeError: ... has no attribute 'stdin'` root cause
- `phase-outputs/test-results/phase2-summary.md:14` — Ruff: 11 errors, 0 delta
- `phase-outputs/test-results/phase2-summary.md:20` — Pytest: 57 failed / 1350 passed / 1 skipped, 0 delta
- `phase-outputs/test-results/phase2-summary.md:32-35` — Regression check: 0 previously-passing now failing, 0 previously-failing now passing, 0 new ruff, 0 new pytest failures
- Live re-verification: `uv run pytest tests/sprint/test_tmux.py -v --tb=short` returned `11 passed in 0.11s` with all 11 tests enumerated explicitly (TestSessionHelpers x4, TestThreePaneLayout x2, TestUpdateTailPane x2, TestUpdateSummaryPane x3 = 11)
- File-level test count: `grep -c "def test_" tests/sprint/test_tmux.py` returns 11 ✓

### Adversarial sanity checks performed (looking for what could be wrong)

1. **Hunk vs. on-disk line numbers** — aggregation claimed `state_dir` at line 397 area. On disk it's at line 399 (after the `total_tasks: int = 0` at line 397). The 2-line drift is from the field added on line 399 and the doc comment on line 398 itself. Hunk content matches; minor displacement is expected and immaterial.
2. **Capture-before-mutation requirement (AC3)** — verified by reading lines 251 vs. 253 sequentially. Line 251 captures `original_release_dir_name`, line 253 mutates `release_dir`. ORDER IS CORRECT.
3. **try/except integrity (AC4)** — verified all three new lines are between `try:` at 1753 and `except OSError:` at 1757. The mkdir IS inside the try block, so OSError on mkdir is also swallowed (matches spec intent of best-effort).
4. **No leftover release_dir.sprint-exitcode references** — grep of executor.py and tmux.py for `release_dir.*sprint-exitcode` returned no hits. Migration is complete in both producer and consumer.
5. **Sentinel-collision guard** — confirmed `Path("") != Path(".")` semantics work: empty Path string is the sentinel; release_dir's `Path(".")` default does NOT collide. This is what AC1's documentation comment in models.py:464 explicitly guards against.
6. **commands.py imports** — `import os` is present at line 9, so the `os.environ` lookup at line 224 is valid (would have been a NameError otherwise).
7. **Live test execution** — re-ran `pytest tests/sprint/test_tmux.py` independently of the phase2-summary.md report; confirmed 11/11 pass and the migrated test (`test_launch_creates_three_panes`) is among the passing set, not skipped/xfail.
8. **PipelineConfig parent class** — verified the aggregation report's claim that no `super().__post_init__()` is needed by grepping for `def __post_init__` in pipeline/models.py — none exists. The omission in models.py:415 is correct.

---

## Summary

- Checks passed: 17 / 17
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0 (fix authorization was false; none needed)

## Issues Found

None.

## Actions Taken

No source modifications (verification-only gate; `fix_authorization: false`). Verdict report written to `/config/workspace/IronClaude-T1-sprint/.dev/tasks/to-do/TASK-RF-track-1-20260518-231708/phase-outputs/reviews/pg2-rf-qa-report.md`.

---

## Confidence

- **Verified:** 17 / 17
- **Unverifiable:** 0
- **Unchecked:** 0
- **Confidence:** 100.0%
- **Tool engagement:** Read: 8 | Grep: 7 | Bash: 4

Confidence threshold (≥95%) satisfied. Tool engagement exceeds the per-item floor (19 ≥ 17). Every PASS verdict cites a specific file:line and an exact textual match against the AC text.

## Recommendations

Green light for Phase 3 (bootstrap_scan.sh patch + 40-sentinel purge + sync-dev). No remediation required.

## QA Complete
