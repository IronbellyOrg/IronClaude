# Research 02 — Reference Recovery Logic & Project Conventions

**Status: Complete**

Track 1 (single track). Topic: the in-repo recovery precedent to mirror (per-PHASE
`_determine_phase_status`) plus IronClaude build/test/sync gates.

Driving diagnosis: `/config/workspace/TUIBBS-scp/.dev/troubleshoot/phase6-gate-error-20260603/REPORT.md`
(read; confirms `_determine_phase_status @2067`, `detect_error_max_turns @37`,
`detect_prompt_too_long @64`).

Scope: `/config/workspace/IronClaude/src/superclaude/cli/sprint/{executor.py, monitor.py}`
+ IronClaude `Makefile` / `CLAUDE.md` / `pyproject.toml`.

---

## 1. `_determine_phase_status` — the reference recovery ladder

`src/superclaude/cli/sprint/executor.py:2067-2148` (full function). Signature
(lines 2067-2076):

```python
def _determine_phase_status(
    exit_code: int,
    result_file: Path,
    output_file: Path,
    *,
    config: SprintConfig | None = None,
    phase: Phase | None = None,
    started_at: float = 0.0,
    error_file: Path | None = None,
) -> PhaseStatus:
```

Documented priority ladder (docstring, lines 2079-2087):

```
1. Timeout (exit 124) -> TIMEOUT
2. Non-zero exit -> ERROR
3. Result file with EXIT_RECOMMENDATION: HALT -> HALT
4. Result file with EXIT_RECOMMENDATION: CONTINUE -> PASS
5. Result file with status: PASS/FAIL -> PASS/HALT
6. No result file but output exists -> PASS_NO_REPORT
7. No result file and no output -> ERROR
```

### The `exit_code != 0` branch (lines 2090-2111) — THE BRANCH TO MIRROR

```python
    if exit_code == 124:
        return PhaseStatus.TIMEOUT
    if exit_code != 0:
        # Path 1 — Specific: context exhaustion (Spec B S2)
        # detect_prompt_too_long reads NDJSON output for "Prompt is too long"
        if detect_prompt_too_long(output_file, error_path=error_file):
            # Check if the agent managed to write a result file before exhaustion
            result_status = _classify_from_result_file(result_file, started_at)
            if result_status is not None:
                return result_status
            # No valid result file — context exhausted without completing
            return PhaseStatus.INCOMPLETE

        # Path 2 — General: checkpoint inference (Spec A SOL-C)
        # Reads agent-written checkpoint files (pre-crash evidence)
        if config is not None and phase is not None:
            if _check_checkpoint_pass(config, phase):
                contaminated = _check_contamination(config, phase)
                _write_crash_recovery_log(config, phase, contaminated)
                if not contaminated:
                    return PhaseStatus.PASS_RECOVERED

        # Path 3 — Default: unchanged
        return PhaseStatus.ERROR
```

Three sub-branches inside `exit_code != 0`:
- **Path 1 — prompt-too-long → result-file classification.** Calls
  `detect_prompt_too_long(output_file, error_path=error_file)` (monitor.py:64).
  If context was exhausted, tries `_classify_from_result_file(result_file,
  started_at)`; returns that status if non-None, else `PhaseStatus.INCOMPLETE`.
- **Path 2 — checkpoint inference.** Only if `config` and `phase` were passed.
  `_check_checkpoint_pass` → `_check_contamination` → `_write_crash_recovery_log`
  → returns `PhaseStatus.PASS_RECOVERED` when checkpoint passed and no
  cross-phase contamination.
- **Path 3 — default.** `return PhaseStatus.ERROR`.

### The `exit_code == 0` branch (lines 2113-2148) — where `detect_error_max_turns` actually lives

```python
    if result_file.exists():
        content = result_file.read_text(errors="replace")
        ...
        has_continue = "EXIT_RECOMMENDATION: CONTINUE" in upper
        has_halt = "EXIT_RECOMMENDATION: HALT" in upper
        if has_halt:
            return PhaseStatus.HALT
        if has_continue:
            return PhaseStatus.PASS
        if re.search(r"status:\s*PASS\b", content, re.IGNORECASE):
            return PhaseStatus.PASS
        if re.search(r"status:\s*FAIL(?:ED|URE)?\b", content, re.IGNORECASE):
            return PhaseStatus.HALT
        if re.search(r"status:\s*PARTIAL\b", content, re.IGNORECASE):
            return PhaseStatus.HALT
        return PhaseStatus.PASS_NO_SIGNAL

    if output_file.exists() and output_file.stat().st_size > 0:
        # Check for budget exhaustion: a subprocess that exits 0 but hit
        # error_max_turns produced no useful result — reclassify as INCOMPLETE
        # to trigger HALT instead of silent continuation.
        if detect_error_max_turns(output_file):
            return PhaseStatus.INCOMPLETE
        return PhaseStatus.PASS_NO_REPORT

    return PhaseStatus.ERROR
```

**Critical observation (executor.py:2144):** `detect_error_max_turns(output_file)`
is invoked ONLY on the **exit_code == 0** path, and there it maps to
`INCOMPLETE` (NOT a recovery — it is a no-result-found pessimistic
reclassification: "exited 0 but really hit the budget, treat as incomplete →
HALT"). On the **non-zero** branch there is no `detect_error_max_turns` call at
all. This is the gap the per-task fix must close differently: in the T06.15 case
the subprocess exited NON-zero with `error_max_turns` AFTER writing a valid
result, so the correct task outcome is a SUCCESS-like recovery, not INCOMPLETE.

How callers thread the args (executor.py:1502-1510, the per-PHASE call site):

```python
status = _determine_phase_status(
    exit_code=exit_code,
    result_file=config.result_file(phase),
    output_file=config.output_file(phase),
    config=config,
    phase=phase,
    started_at=started_at.timestamp(),
    error_file=config.error_file(phase),
)
```

The per-task analog would pass `config.task_output_file(phase, task)` and
`config.task_error_file(phase, task)` (models.py:502-506) in place of the
phase-level `output_file`/`error_file`.

---

## TL;DR for the builder

- The reference recovery logic is `_determine_phase_status` at
  `src/superclaude/cli/sprint/executor.py:2067-2148`. It handles a non-zero
  exit (`exit_code != 0`) in a 3-path ladder (lines 2090-2111), and ALSO has a
  separate `error_max_turns` reclassification on the **exit_code==0** branch
  (lines 2140-2146).
- **IMPORTANT NUANCE the builder must not miss:** the per-PHASE path does NOT
  call `detect_error_max_turns` on its `exit_code != 0` branch. On a non-zero
  exit it relies on `detect_prompt_too_long` + checkpoint inference, then
  defaults to `ERROR`. The `detect_error_max_turns` call lives on the
  exit_code==0 path. So "mirror the per-PHASE exit!=0 branch" alone would NOT
  fix the T06.15 case (which is exit!=0). The per-TASK fix must ADD a
  `detect_error_max_turns(task_output_file)` check to the non-zero-exit branch —
  combining the structure of the per-PHASE non-zero ladder with the
  `detect_error_max_turns` detector that today only runs on the zero-exit path.
- Detectors to call live in `monitor.py`: `detect_error_max_turns(output_path)`
  @37 and `detect_prompt_too_long(output_path, *, error_path=None)` @64.
- Per-task output/error file paths ALREADY EXIST:
  `config.task_output_file(phase, task)` and `config.task_error_file(phase, task)`
  in `models.py:502-506`. No new plumbing of file paths is required to call the
  detectors. (There is NO `task_result_file` method — see §3 caveat.)
- `TaskStatus` (models.py:39) has `PASS / FAIL / INCOMPLETE / SKIPPED` — so the
  per-task path can reclassify to `TaskStatus.INCOMPLETE` (the task-level analog
  of the phase-level `INCOMPLETE`). There is no `TaskStatus.PASS_RECOVERED`.
- Verification gates: `uv run pytest tests/sprint/` (or `make test`),
  `make lint` (ruff check), `make format`. `make sync-dev` / `make verify-sync`
  are for `.claude/` mirror of skills/agents/commands/hooks/templates — they do
  NOT cover `src/superclaude/cli/` Python, so a pure-`cli/sprint` edit does not
  require sync-dev, but verify-sync should still pass (no drift introduced).

---

## 2. Detectors in `monitor.py` (the functions the per-task fix will call)

### `detect_error_max_turns(output_path)` — `monitor.py:37-61`

```python
def detect_error_max_turns(output_path: Path) -> bool:
    """Check if the last NDJSON line indicates budget exhaustion.

    Scans the last non-empty line of the output file for the
    ``"subtype":"error_max_turns"`` pattern, which signals that a
    subprocess exhausted its turn budget.

    Returns True if error_max_turns is detected, False otherwise.
    """
    try:
        content = output_path.read_text(errors="replace")
    except (FileNotFoundError, OSError):
        return False

    if not content.strip():
        return False

    # Get last non-empty line
    lines = content.strip().splitlines()
    for line in reversed(lines):
        line = line.strip()
        if line:
            return bool(ERROR_MAX_TURNS_PATTERN.search(line))

    return False
```

- **Signature:** `(output_path: Path) -> bool`. Single positional arg, no kwargs.
- **File read:** `output_path` — the NDJSON stream-json output file. For the
  per-task path, pass `config.task_output_file(phase, task)`.
- **Pattern matched:** `ERROR_MAX_TURNS_PATTERN = re.compile(r'"subtype"\s*:\s*"error_max_turns"')`
  (monitor.py:33). Scans ONLY the **last non-empty line** (the final result
  envelope). This matches the REPORT's T06.15 EOF envelope
  `{"type":"result","subtype":"error_max_turns",...,"is_error":true,"num_turns":101}`.
- **Return:** `bool`. `False` on missing/empty/unreadable file (safe default).

### `detect_prompt_too_long(output_path, *, error_path=None)` — `monitor.py:64-107`

```python
def detect_prompt_too_long(
    output_path: Path, *, error_path: Path | None = None
) -> bool:
    """Check if NDJSON output contains a prompt-too-long error.

    Scans the last 10 non-empty lines of the output file for the
    ``"Prompt is too long"`` pattern...
    If ``error_path`` is provided, the same last-10-lines scan is also
    applied to that file. Returns True if the pattern is found in either file.
    """

    def _scan(path: Path) -> bool:
        try:
            content = path.read_text(errors="replace")
        except (FileNotFoundError, OSError):
            return False
        if not content.strip():
            return False
        lines = content.strip().splitlines()
        count = 0
        for line in reversed(lines):
            line = line.strip()
            if not line:
                continue
            if PROMPT_TOO_LONG_PATTERN.search(line):
                return True
            count += 1
            if count >= 10:
                break
        return False

    if _scan(output_path):
        return True
    if error_path is not None and _scan(error_path):
        return True
    return False
```

- **Signature:** `(output_path: Path, *, error_path: Path | None = None) -> bool`.
  `error_path` is keyword-only.
- **Files read:** `output_path`, plus `error_path` if given. For per-task:
  `config.task_output_file(phase, task)` + `config.task_error_file(phase, task)`.
- **Pattern matched:** `PROMPT_TOO_LONG_PATTERN = re.compile(r'"Prompt is too long"')`
  (monitor.py:34). Scans the last **10** non-empty lines of each file.
- **Return:** `bool`.

Both are already imported into executor.py (used by `_determine_phase_status`).
Confirm import line before adding a per-task call (grep `from .monitor import`
in executor.py — they are in scope at module level since `_determine_phase_status`
calls them unqualified).

---

## 3. Recovery helpers in `executor.py` — signatures + reuse analysis

### `_classify_from_result_file(result_file, started_at)` — `executor.py:1774-1808`

```python
def _classify_from_result_file(
    result_file: Path,
    started_at: float,
) -> PhaseStatus | None:
```
- Inputs: `result_file: Path`, `started_at: float` (epoch seconds; staleness
  guard — file must have `mtime >= started_at`).
- Returns `PhaseStatus | None`. Maps `status: PASS` / `EXIT_RECOMMENDATION:
  CONTINUE` → `PASS_RECOVERED`; `HALT` / `status: FAIL` → `HALT`; `PARTIAL` →
  `INCOMPLETE`; otherwise `None`.
- **Per-task reuse caveat:** this returns a **PhaseStatus**, not a TaskStatus,
  and reads a *result file*. There is **no `config.task_result_file()` method**
  (models.py has `task_output_file`/`task_error_file` only — lines 502-506).
  The per-task subprocess writes its structured result into its NDJSON output
  stream (the `task_complete` / `result:"Pass"` envelope per the REPORT), not a
  separate `*-result.md`. So `_classify_from_result_file` is NOT directly
  reusable for the per-task path without (a) a new task-result file path, or
  (b) reworking it to read the task output stream. The simpler, lower-risk
  per-task fix is: on non-zero exit, if `detect_error_max_turns(task_output)` is
  True, reclassify FAIL → a success-like/INCOMPLETE task status WITHOUT calling
  `_classify_from_result_file`. (researcher-01 owns the exact reclassification
  target enum; this researcher flags the available values: `TaskStatus.PASS`,
  `TaskStatus.INCOMPLETE`.)

### `_check_checkpoint_pass(config, phase)` — `executor.py:1894-1905`

```python
def _check_checkpoint_pass(config: SprintConfig, phase: Phase) -> bool:
    """Return True if the end-of-phase checkpoint file exists with status PASS."""
    checkpoint_path = (
        config.release_dir / "checkpoints" / f"CP-P{phase.number:02d}-END.md"
    )
```
- Inputs: `config: SprintConfig`, `phase: Phase`. Reads
  `<release_dir>/checkpoints/CP-P{NN}-END.md`; True if it contains
  `STATUS: PASS` or `**RESULT**: PASS`.
- **Per-task reuse:** this is **phase-granular** (one end-of-phase checkpoint per
  phase, keyed on `phase.number`). It is NOT task-granular and is the wrong
  precedent for per-task recovery — a single task overrunning does not have a
  per-task `CP-*-END.md`. Do not reuse for the per-task path.

### `_check_contamination(config, phase)` — `executor.py:1908-1924`

```python
def _check_contamination(config: SprintConfig, phase: Phase) -> list[str]:
    """Return list of artifact files containing cross-phase task ID patterns."""
```
- Inputs: `config`, `phase`. Scans `<release_dir>/artifacts/**/*.md` for
  next-phase task IDs (`T{phase+1:02d}.\d\d`). Returns list of contaminated files.
- **Per-task reuse:** phase-level cross-phase contamination guard, not relevant
  to a single-task budget overrun. Do not reuse.

### `_write_crash_recovery_log(config, phase, contaminated)` — `executor.py:1927-1951`

```python
def _write_crash_recovery_log(
    config: SprintConfig,
    phase: Phase,
    contaminated: list[str],
) -> None:
```
- Inputs: `config`, `phase`, `contaminated: list[str]`. Appends a
  `## Phase N — PASS_RECOVERED Recovery` entry to
  `<results_dir>/crash_recovery_log.md`. Side-effect only (returns None).
- **Per-task reuse:** optional. The per-task fix could append an analogous
  audit entry (e.g. "Task T06.15 — error_max_turns after completion, recovered")
  to the same log for traceability, but the function as written hardcodes
  phase-level wording. Reuse is cosmetic, not required for correctness.

### Reuse summary

| Helper | Granularity | Reusable for per-task? |
|---|---|---|
| `_classify_from_result_file` | reads a `*-result.md` | NO directly — no task_result_file; task result is in the NDJSON stream |
| `_check_checkpoint_pass` | per-phase `CP-PNN-END.md` | NO — phase-granular |
| `_check_contamination` | per-phase artifact scan | NO — phase-granular |
| `_write_crash_recovery_log` | per-phase audit append | Optional/cosmetic only |
| `detect_error_max_turns` (monitor) | reads any output file | YES — call on `task_output_file(phase, task)` |
| `detect_prompt_too_long` (monitor) | reads any output/error file | YES — call on task output/error files |

**Net:** the durable, low-risk per-task fix reuses the **monitor detectors**
(§2), NOT the phase-granular executor helpers. The structural pattern to mirror
is the *shape* of the `exit_code != 0` ladder (§1: detect → reclassify-before-
defaulting-to-failure), applied with `detect_error_max_turns` on the per-task
output file, reclassifying to a non-FAIL `TaskStatus`.

---

## 4. Project conventions & verification gates

### Test runner (pyproject.toml:101-110, UV-only)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = ["-v", "--strict-markers", "--tb=short"]
```
- Markers are `--strict-markers` (pyproject.toml:108) — any new test must use a
  registered marker (registry at pyproject.toml:111-135; e.g. `unit`,
  `diagnostic_l1`, `backward_compat`) or none.
- Sprint tests live in `tests/sprint/`. Existing relevant files (researcher-03
  owns tests; listed here only as gate context): `test_executor.py`,
  `test_monitor.py`, `test_regression_gaps.py`, `test_phase8_halt_fix.py`,
  `test_backward_compat_regression.py`.

**Exact verification commands (UV only — never `pytest`/`python` bare):**
```bash
uv run pytest tests/sprint/                          # focused sprint suite
uv run pytest tests/sprint/test_executor.py -v       # executor-specific
uv run pytest tests/sprint/test_monitor.py -v        # detector-specific
make test                                            # full suite (uv run pytest)
make lint                                            # uv run ruff check .
make format                                          # uv run ruff format .
```

### Sync model (CLAUDE.md:16-33, Makefile sync-dev/verify-sync)

- Source of truth is `src/superclaude/`; `.claude/{skills,commands,agents,hooks,
  templates}/*` is **gitignored sync-dev output** (CLAUDE.md:18). Only
  `.claude/settings.json` is tracked.
- `make sync-dev` (Makefile:109-163) copies skills/agents/commands/hooks/
  templates from `src/superclaude/` → `.claude/`. It does **NOT** touch
  `src/superclaude/cli/` Python modules.
- `make verify-sync` (Makefile:166-353) checks drift between `src/` and
  `.claude/` for those same component dirs (CI-friendly, exits 1 on drift).
- **Implication for THIS fix:** the edit is to `src/superclaude/cli/sprint/
  executor.py` (and possibly `monitor.py`/`models.py`), which are plain Python
  modules, NOT synced components. Therefore `make sync-dev` is **not required**
  for the code change to take effect, and the change introduces no `.claude/`
  drift. Still run `make verify-sync` as a no-regression gate (it should report
  "All components in sync" unchanged). **Do NOT** `git add` any `.claude/` path
  (CLAUDE.md:20-29 — absolute rule; `git add -f` on `.claude/` is the "violation
  siren").

### Git / branch conventions (CLAUDE.md:245-252)

- Branch structure: `master` ← `integration` ← `feature/*`, `fix/*`, `docs/*`.
- Feature-branch only; create from `integration`:
  `git checkout -b fix/<name>` (this is a fix → `fix/` prefix). Conventional
  commits (`fix: ...`). Never commit to `master`/`integration` directly.
- PRs target the fork: `gh pr create --repo IronbellyOrg/IronClaude --base master
  --head <branch>` (CLAUDE.md:35-60) — NEVER upstream.

### Recommended verification sequence for the builder
```bash
uv run pytest tests/sprint/test_executor.py tests/sprint/test_monitor.py -v
uv run pytest tests/sprint/          # broader sprint regression
make lint                            # ruff check
make format                          # ruff format (or check formatting)
make verify-sync                     # confirm no .claude/ drift (should pass unchanged)
```

---

## Summary

- **Reference recovery site:** `_determine_phase_status` @ `executor.py:2067-2148`.
  Its `exit_code != 0` branch (2090-2111) is the structural pattern to mirror:
  detect a recoverable condition (prompt-too-long / checkpoint) and reclassify
  BEFORE the default `return PhaseStatus.ERROR`.
- **Verified key nuance:** `detect_error_max_turns` is currently called ONLY on
  the **exit_code == 0** path (executor.py:2144 → `INCOMPLETE`). The non-zero
  branch never calls it. T06.15 exited NON-zero with `error_max_turns` after
  completing — so the per-task fix must ADD `detect_error_max_turns` to a
  non-zero-exit classification, not literally copy either existing branch.
- **Detectors (monitor.py):** `detect_error_max_turns(output_path) -> bool` @37
  (last-line `"subtype":"error_max_turns"`); `detect_prompt_too_long(output_path,
  *, error_path=None) -> bool` @64 (last-10-lines `"Prompt is too long"`). Both
  already imported into executor.py.
- **File paths already exist:** `config.task_output_file(phase, task)` and
  `config.task_error_file(phase, task)` (models.py:502-506) — feed these to the
  detectors. NO `task_result_file` exists.
- **Helper reuse verdict:** the phase-level executor helpers
  (`_classify_from_result_file`, `_check_checkpoint_pass`, `_check_contamination`,
  `_write_crash_recovery_log`) are phase-granular / result-file-dependent and are
  NOT cleanly reusable for per-task. The reusable pieces are the two monitor
  detectors. Reclassification target enum values available: `TaskStatus.PASS`,
  `TaskStatus.INCOMPLETE` (no `TaskStatus.PASS_RECOVERED`).
- **Gates:** `uv run pytest tests/sprint/` + `make lint` (ruff check) +
  `make format`; `make verify-sync` should pass unchanged (edit is to
  `cli/sprint/` Python, not a synced `.claude/` component — `make sync-dev` NOT
  required). Feature/`fix/` branch off `integration`, conventional commits,
  PRs `--repo IronbellyOrg/IronClaude`. UV-only; never stage `.claude/`.
