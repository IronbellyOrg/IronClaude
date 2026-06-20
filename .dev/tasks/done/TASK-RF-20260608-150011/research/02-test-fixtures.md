# Research: Test fixtures

Status: Complete

Scope: Exact fixture code + existing-test idioms for two new sprint-recovery regression tests (diagnosis: `.dev/troubleshoot/sprint-merge-stranding-checkpoint-stale-20260608144847/REPORT.md`). The builder needs these so new tests integrate cleanly. All citations are exact `file:line` against the repo as of 2026-06-08.

---

## 1. `tests/sprint/test_recovery.py`

### 1.1 Imports (lines 1-21)

```python
"""Tests for sprint recovery bundle, audit log, and merge orchestration."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from superclaude.cli.sprint.recovery import (
    ManualNominator,
    RecoveryBundle,
    RecoveryBundleRef,
    RecoveryStatus,
    ReflectReportNominator,
    acquire_recovery_lock,
    compute_tasklist_sha256,
    merge_recovery_bundle,
    release_recovery_lock,
    retry_count_for_task,
    write_recovery_audit_log,
)
```

Note: `Phase, PhaseResult` are imported lazily *inside* a test (line 380), not at module top:
```python
from superclaude.cli.sprint.models import Phase, PhaseResult
```

### 1.2 `_seed_release` (lines 28-48) — FULL BODY

```python
def _seed_release(tmp_path: Path, phase: int = 7) -> tuple[Path, Path, Path]:
    """Create a minimal canonical release layout for merge tests.

    Returns ``(source_index, release_dir, results_dir)``. ``release_dir`` is
    ``tmp_path`` itself so ``_resolve_release_dir(source_index)`` resolves to
    it (index lives directly in the release dir, not under a ``tasklist/``
    subdir). Seeds a canonical ``phase-N-result.json`` so merge step 7 has a
    file to rewrite.
    """
    source_index = tmp_path / "tasklist-index.md"
    source_index.write_text(
        "# Sprint\n\n| # | File |\n|---|------|\n", encoding="utf-8"
    )
    results_dir = tmp_path / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    result_json = results_dir / f"phase-{phase}-result.json"
    result_json.write_text(
        json.dumps({"phase": phase, "task_results": [], "recovery_history": []}),
        encoding="utf-8",
    )
    return source_index, tmp_path, results_dir
```

Key facts:
- Return tuple: `(source_index, release_dir, results_dir)` where `source_index = tmp_path/"tasklist-index.md"`, `release_dir == tmp_path` (the index lives directly in the release dir), `results_dir = tmp_path/"results"`.
- Index body is a bare table header (no phase rows) — adequate for merge tests that don't exercise phase resolution.
- Seeds `results/phase-{phase}-result.json` with empty `task_results` + `recovery_history`.
- There is **NO** `_full_recovery_manifest` helper in `test_recovery.py` — that name lives only in `test_checkpoints.py` (§2.4).

### 1.3 `_bundle_with_sidecar` (lines 51-79) — FULL BODY

```python
def _bundle_with_sidecar(
    tmp_path: Path, *, bundle_id: str, phase: int, task_ids: list[str]
) -> RecoveryBundle:
    """Build a RecoveryBundle whose bundle dir holds a ``task-results.json``
    sidecar, so merge step 7 can refresh the affected tasks and settle SUCCESS.

    Without the sidecar the engine intentionally records a
    ``result-json-not-refreshed`` failure (no silent data loss), which
    downgrades the bundle to PARTIAL. The sidecar mirrors the serialized
    rerun ``PhaseResult.task_results`` that Phase 3's ``run_rerun_tasks``
    writes alongside the rerun transcripts.
    """
    bundle_dir = tmp_path / "bundles" / bundle_id
    bundle_dir.mkdir(parents=True, exist_ok=True)
    sidecar = bundle_dir / "task-results.json"
    sidecar.write_text(
        json.dumps([{"task": {"task_id": tid}, "status": "pass"} for tid in task_ids]),
        encoding="utf-8",
    )
    # artifacts_produced[0].parent resolves to bundle_dir (where the sidecar
    # lives); a placeholder transcript file anchors that parent.
    placeholder = bundle_dir / f"phase-{phase}-task-{task_ids[0]}-output.txt"
    placeholder.write_text("rerun output", encoding="utf-8")
    return RecoveryBundle(
        bundle_id=bundle_id,
        affected_phase=phase,
        affected_tasks=list(task_ids),
        artifacts_produced=[placeholder],
    )
```

Key facts:
- Sidecar path: `tmp_path/"bundles"/<bundle_id>/task-results.json`. The merge engine locates the sidecar via `artifacts_produced[0].parent` — so the placeholder transcript MUST live in the same dir as the sidecar.
- Sidecar JSON shape: a **list** of `{"task": {"task_id": tid}, "status": "pass"}` (note `status: "pass"` here — vs `"passed"` used in `_full_recovery_manifest` below; both forms appear in the suite).
- Presence of the sidecar is the precondition for `RecoveryStatus.SUCCESS`; absence forces `PARTIAL` (a `result-json-not-refreshed` failure).

### 1.4 `class TestMergeRecoveryBundle` (line 153) — method list

| Method | Line | What it asserts |
|--------|------|-----------------|
| `test_merge_writes_audit_log_entry` | 154 | merge appends one `merge_recovery_bundle` JSONL event to `results/recovery-audit.log`; event has `bundle_id`, `affected_phase`, `affected_tasks`, `status=="success"`, `timestamp`. |
| `test_merge_is_idempotent` | 179 | two merges → exactly 2 audit entries, 2 recovery_history refs, status never regresses (quote below). |
| `test_merge_failure_rolls_back_atomically` | 215 | patches `Path.write_text` to raise OSError on `phase-7-result.json.tmp`; canonical result-json byte-identical to pre-merge; bundle → `PARTIAL`. |
| `test_merge_refreshes_canonical_status_from_sidecar` | 246 | with sidecar: prior `fail_recoverable` entry REPLACED (not duplicated) by `pass`; 1 recovery_history; status `SUCCESS`. |
| `test_merge_without_sidecar_preserves_prior_and_partials` | 285 | no sidecar: prior entry PRESERVED (never dropped), status `PARTIAL`. |

### 1.5 `test_merge_is_idempotent` (lines 179-213) — representative pattern, FULL QUOTE

```python
    def test_merge_is_idempotent(self, tmp_path: Path):
        """Merging the same bundle twice does not corrupt state: each call adds
        exactly one audit entry and one recovery_history ref, and the bundle
        settles to a terminal-or-partial status both times (no exception)."""
        source_index, _release_dir, results_dir = _seed_release(tmp_path, phase=7)
        bundle = RecoveryBundle(
            bundle_id="rerun-idem",
            affected_phase=7,
            affected_tasks=["T07.11"],
        )
        merge_recovery_bundle(bundle, source_index)
        first_status = bundle.status
        merge_recovery_bundle(bundle, source_index)

        # Audit log accumulates one entry per merge call.
        audit_log = results_dir / "recovery-audit.log"
        merge_events = [
            json.loads(line)
            for line in audit_log.read_text(encoding="utf-8").splitlines()
            if line.strip() and json.loads(line).get("event") == "merge_recovery_bundle"
        ]
        assert len(merge_events) == 2

        # phase-N-result.json remains valid JSON and accumulates one ref per merge.
        result_json = results_dir / "phase-7-result.json"
        data = json.loads(result_json.read_text(encoding="utf-8"))
        refs = [
            r
            for r in data.get("recovery_history", [])
            if r.get("bundle_id") == "rerun-idem"
        ]
        assert len(refs) == 2
        # Second merge did not regress the status to a failure.
        assert bundle.status in (RecoveryStatus.SUCCESS, RecoveryStatus.PARTIAL)
        assert first_status in (RecoveryStatus.SUCCESS, RecoveryStatus.PARTIAL)
```

Pattern to copy:
- Call shape: `merge_recovery_bundle(bundle, source_index)` (positional; `release_dir` defaults to resolving from `source_index`). In `test_checkpoints.py` the call instead passes `release_dir=tmp_path` explicitly.
- Construct `RecoveryBundle` with only `bundle_id`, `affected_phase`, `affected_tasks` (other fields defaulted).
- Status assertions use `is`/`in` against `RecoveryStatus` members, never string literals.

### 1.6 How `recovery-audit.log` is read/parsed in existing assertions

Canonical idiom (lines 165-169, 194-199, 342-346):

```python
audit_log = results_dir / "recovery-audit.log"
lines = [
    json.loads(line)
    for line in audit_log.read_text(encoding="utf-8").splitlines()
    if line.strip()
]
merge_events = [e for e in lines if e.get("event") == "merge_recovery_bundle"]
```

- Log path: `<results_dir>/recovery-audit.log` (i.e. `tmp_path/"results"/"recovery-audit.log"`).
- Format: JSONL — one `json.loads(line)` per non-blank line.
- Merge event filtered by `e.get("event") == "merge_recovery_bundle"`.
- Asserted fields (`test_merge_writes_audit_log_entry`, lines 173-177): `bundle_id`, `affected_phase`, `affected_tasks`, `status` (string value e.g. `"success"`), presence of `timestamp`.

---

## 2. `tests/sprint/test_checkpoints.py`

### 2.1 Imports (lines 1-40)

```python
from __future__ import annotations

import io
import json
from contextlib import redirect_stdout
from pathlib import Path

from click.testing import CliRunner

from superclaude.cli.sprint.checkpoints import (
    build_manifest,
    extract_checkpoint_paths,
    recover_missing_checkpoints,
    verify_checkpoint_files,
    write_manifest,
)
from superclaude.cli.sprint.commands import verify_checkpoints
from superclaude.cli.sprint.executor import _verify_checkpoints
from superclaude.cli.sprint.logging_ import SprintLogger
from superclaude.cli.sprint.models import (
    CheckpointEntry,
    Phase,
    PhaseStatus,
    SprintConfig,
)
from superclaude.cli.sprint.recovery import (
    RecoveryBundle,
    RecoveryStatus,
    merge_recovery_bundle,
)
```

### 2.2 `_seed_sprint` (lines 293-320) — FULL BODY

```python
def _seed_sprint(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    """Create a three-phase sprint workspace. Returns (index, p1, p2, p3)."""
    p1 = tmp_path / "phase-1-tasklist.md"
    p2 = tmp_path / "phase-2-tasklist.md"
    p3 = tmp_path / "phase-3-tasklist.md"
    index = tmp_path / "tasklist-index.md"
    index.write_text(
        "# Sprint\n\n"
        "| # | File |\n|---|------|\n"
        f"| 1 | {p1.name} |\n"
        f"| 2 | {p2.name} |\n"
        f"| 3 | {p3.name} |\n"
    )
    p1.write_text(
        "### Checkpoint: End of Phase 1\n"
        "Checkpoint Report Path: checkpoints/CP-P01-END.md\n"
    )
    p2.write_text("# Phase with no checkpoints\n### T02.01 Task body\n")
    p3.write_text(
        "### Checkpoint: Mid Phase 3\n"
        "Checkpoint Report Path: checkpoints/CP-P03-MID.md\n\n"
        "### Checkpoint: End of Phase 3\n"
        "Checkpoint Report Path: checkpoints/CP-P03-END.md\n"
        "**Verification:**\n"
        "- Configuration module loads\n"
        "- Utilities module works\n"
    )
    return index, p1, p2, p3
```

Key facts:
- Return tuple shape: `(index, p1, p2, p3)` — index + three phase tasklist paths. Files live directly in `tmp_path` (NOT under a `phases/` subdir; contrast `_build_phase` at line 160 which DOES use `phases/`).
- Phase 1: 1 checkpoint (`CP-P01-END.md`). Phase 2: 0 checkpoints. Phase 3: 2 checkpoints (`CP-P03-MID.md`, `CP-P03-END.md`); the End-of-Phase-3 checkpoint carries a `**Verification:**` block.
- Checkpoint report expected paths resolve to `tmp_path/"checkpoints"/<name>.md` (relative `checkpoints/...` resolved against `tmp_path`).
- For the Defect-2 stale-verdict test (REPORT.md line 75): after `_seed_sprint`, pre-seed `tmp_path/"checkpoints"/"CP-P03-END.md"` with stale `status: fail` frontmatter.

### 2.3 `class TestRecoverMissingCheckpoints` (line 407) — method list

| Method | Line | What it does |
|--------|------|--------------|
| `test_generates_file_with_auto_recovered_marker` | 408 | seeds `artifacts/D-0013`, `D-0014` evidence referencing T03.01/T03.02; `build_manifest` → `recover_missing_checkpoints(manifest, tmp_path/"artifacts", {3: p3})`; asserts both P3 entries `recovered`, body has `"Auto-Recovered"` + `"recovered: true"`. |
| `test_idempotent_second_run_does_not_overwrite` | 435 | runs recovery twice; snapshots bodies after run 1; asserts run-2 does not overwrite; second-run entries `exists`. |
| `test_does_not_overwrite_pre_existing_file` | 454 | pre-existing file kept verbatim; returned entry `exists=True` (quote §2.5). |
| `test_wave4_verification_block_copied_into_recovered_report` | 468 | Wave-4 `### T01.06 -- Checkpoint:` task; verification + exit criteria copied verbatim; no fallback sentinel. |
| `test_phase_without_tasklist_is_skipped` | 509 | phase absent from `phase_tasklists` map → file not written, `exists=False`, `recovered=False`. |

### 2.4 `_full_recovery_manifest` (lines 600-654) — FULL BODY

```python
def _full_recovery_manifest(tmp_path: Path) -> tuple[Path, RecoveryBundle]:
    """Seed a phase-3-filtered recovery workspace and a RecoveryBundle that,
    when merged, completes cleanly and yields ``RecoveryStatus.SUCCESS``.

    Layout mirrors the canonical SprintConfig: ``release_dir`` == tmp_path so
    ``_resolve_release_dir(index)`` (= index.parent for a top-level index)
    resolves results to ``<tmp_path>/results``. The prior phase-3 canonical
    artifacts (task output + result.json) are written so the 7-step merge has
    real files to rename/replace, and a ``task-results.json`` sidecar is placed
    in the bundle dir so Step 7 refreshes result-json without recording a
    failure — the precondition for a SUCCESS (not PARTIAL) terminal status.
    """
    index = tmp_path / "tasklist-index.md"
    p3 = tmp_path / "phase-3-tasklist.md"
    index.write_text(f"# Sprint\n\n| # | File |\n|---|------|\n| 3 | {p3.name} |\n")
    p3.write_text(
        "### Checkpoint: End of Phase 3\n"
        "Checkpoint Report Path: checkpoints/CP-P03-END.md\n"
    )

    results_dir = tmp_path / "results"
    results_dir.mkdir()
    # Prior canonical artifacts for the affected task (will be preserved as
    # .failed-<ts> and replaced by the rerun's produced output).
    (results_dir / "phase-3-task-T03.01-output.txt").write_text("stale output")
    (results_dir / "phase-3-result.json").write_text(
        json.dumps(
            {
                "phase": 3,
                "task_results": [
                    {"task": {"task_id": "T03.01"}, "status": "failed"},
                    {"task": {"task_id": "T03.02"}, "status": "passed"},
                ],
                "recovery_history": [],
            }
        )
        + "\n"
    )

    # Bundle dir holds the rerun's produced artifacts + the sidecar.
    bundle_dir = results_dir / "rerun-bundle"
    bundle_dir.mkdir()
    produced_output = bundle_dir / "phase-3-task-T03.01-output.txt"
    produced_output.write_text("fresh rerun output")
    (bundle_dir / "task-results.json").write_text(
        json.dumps([{"task": {"task_id": "T03.01"}, "status": "passed"}]) + "\n"
    )

    bundle = RecoveryBundle(
        bundle_id="rerun-20260602T000000Z",
        affected_phase=3,
        affected_tasks=["T03.01"],
        artifacts_produced=[produced_output],
    )
    return index, bundle
```

Key facts:
- Return tuple: `(index, bundle)`. `release_dir == tmp_path`, results at `tmp_path/"results"`.
- Bundle dir is `tmp_path/"results"/"rerun-bundle"` (nested under results/, unlike `_bundle_with_sidecar` which uses `tmp_path/"bundles"/<id>`). Sidecar `status` here is `"passed"` (vs `"pass"` in `_bundle_with_sidecar`).
- Prior canonical `phase-3-task-T03.01-output.txt` is preserved as `.failed-<ts>.txt` on merge; canonical replaced with `"fresh rerun output"`.
- Consumers: `class TestRecoverMissingReturnsRecoveryBundle` (line 657): `test_merge_sets_status_success_and_end_sha` (658), `test_merge_preserves_prior_output_and_writes_fresh` (667), `test_merge_refreshes_result_json_and_appends_history` (680). All call `merge_recovery_bundle(bundle, index, release_dir=tmp_path)` with explicit `release_dir=`.

### 2.5 `test_does_not_overwrite_pre_existing_file` (lines 454-466) — FULL QUOTE

```python
    def test_does_not_overwrite_pre_existing_file(self, tmp_path: Path):
        existing = tmp_path / "existing.md"
        existing.write_text("original body")
        entry = CheckpointEntry(
            phase=5,
            name="End of 5",
            expected_path=existing,
            exists=False,
        )
        result = recover_missing_checkpoints([entry], tmp_path, {})
        assert existing.read_text() == "original body"
        # The returned entry should now reflect exists=True.
        assert result[0].exists is True
```

Closest existing pattern to the Defect-2 regression test: hand-builds one `CheckpointEntry` (not via `build_manifest`), calls `recover_missing_checkpoints([entry], <artifacts_dir>, <phase_tasklists>)`, asserts on-disk content + the returned entry's `exists`. **Critical baseline for Defect 2:** when the file already exists, `recover_missing_checkpoints` returns it UNCHANGED with `exists=True` and never reads frontmatter/verdict — exactly the no-op the new test must prove gets fixed.

### 2.6 `build_manifest` + `recover_missing_checkpoints` invocation idiom

`build_manifest`:
```python
manifest = build_manifest(index, tmp_path)        # (index_path, release_dir)
```
- Signature (`checkpoints.py:138`): `build_manifest(index, release_dir) -> list[CheckpointEntry]`.

`recover_missing_checkpoints`:
```python
recovered = recover_missing_checkpoints(manifest, tmp_path / "artifacts", {3: p3})
```
- Signature (`checkpoints.py:213-219`):
```python
def recover_missing_checkpoints(
    manifest: list[CheckpointEntry],
    artifacts_dir: Path,
    phase_tasklists: dict[int, Path],
    *,
    return_bundle: bool = False,
) -> list[CheckpointEntry] | RecoveryBundle:
```
- 3rd positional `phase_tasklists` maps phase number → phase tasklist path; phases absent from the map are SKIPPED. Returns a NEW list (input not mutated). `return_bundle=True` wraps the result in a `RecoveryBundle`.

### 2.7 Artifacts/evidence dir seeding idiom (`artifacts/D-####/<file>`)

From `test_generates_file_with_auto_recovered_marker` (lines 409-418):
```python
index, _, _, p3 = _seed_sprint(tmp_path)
# Evidence referencing phase 3 tasks.
(tmp_path / "artifacts" / "D-0013").mkdir(parents=True)
(tmp_path / "artifacts" / "D-0013" / "config.md").write_text(
    "Task T03.01 delivered configuration module."
)
(tmp_path / "artifacts" / "D-0014").mkdir()
(tmp_path / "artifacts" / "D-0014" / "util.md").write_text(
    "Task T03.02 delivered utilities."
)
```
- Evidence lives under `tmp_path/"artifacts"/"D-####"/<file>.md`; body text references the phase's task IDs (e.g. `T03.01`) so the recoverer associates the artifact with the phase. The `artifacts_dir` arg passed is `tmp_path/"artifacts"`.

---

## 3. RecoveryBundle constructor — required vs defaulted (cross-check)

Source: `src/superclaude/cli/sprint/recovery.py:76-114` (dataclass).

```python
@dataclass
class RecoveryBundle:
    bundle_id: str                                              # REQUIRED
    affected_phase: int                                         # REQUIRED
    verb: str = "rerun-tasks"                                   # default
    affected_tasks: list[str] = field(default_factory=list)    # default []
    artifacts_produced: list[Path] = field(default_factory=list)   # default []
    artifacts_replaced: dict[Path, Path] = field(default_factory=dict)  # default {}
    source_tasklist_sha256: str = ""                           # default ""
    end_tasklist_sha256: Optional[str] = None                  # default None
    status: RecoveryStatus = RecoveryStatus.DRYRUN             # default DRYRUN
    rerun_attempt: int = 1                                      # default 1
```

- **Required (no default):** `bundle_id`, `affected_phase`.
- **Defaulted:** `verb`, `affected_tasks`, `artifacts_produced`, `artifacts_replaced`, `source_tasklist_sha256`, `end_tasklist_sha256`, `status`, `rerun_attempt`.
- The kwargs used by the test helpers (`bundle_id`, `affected_phase`, `affected_tasks`, `artifacts_produced`) are all valid fields. No `add_entry()` method — state accrues by appending to `affected_tasks` / `artifacts_produced`; merge engine flips `status` + `end_tasklist_sha256` (per `test_recovery.py:103-114`).

### RecoveryStatus enum (recovery.py:58-68)
```python
class RecoveryStatus(Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    DRYRUN = "dryrun"
    @property
    def is_terminal(self) -> bool:
        return self in (RecoveryStatus.SUCCESS, RecoveryStatus.FAILED)
```
`PARTIAL` and `DRYRUN` are NOT terminal.

### CheckpointEntry dataclass (models.py:486-514)
```python
@dataclass
class CheckpointEntry:
    phase: int                              # REQUIRED
    name: str                               # REQUIRED
    expected_path: Path                     # REQUIRED
    exists: bool                            # REQUIRED
    recovered: bool = False                 # default
    recovery_source: Optional[str] = None   # default
```
First four required positionals; tests build it as `CheckpointEntry(phase=5, name="End of 5", expected_path=existing, exists=False)`.

---

## 4. Checkpoint report frontmatter / verdict key (Defect 2 relevance)

The recovered checkpoint report rendered by `recover_missing_checkpoints` uses YAML frontmatter keys `checkpoint:`, `phase:`, `recovered: true`, `generated_at:` and a `## Result` body section (`checkpoints.py:415-439`):

```python
return (
    "---\n"
    f"checkpoint: {entry.name}\n"
    f"phase: {entry.phase}\n"
    "recovered: true\n"
    f"generated_at: {timestamp}\n"
    "---\n\n"
    "## Note: Auto-Recovered\n\n"
    ...
    "## Result\n\n"
    "`UNKNOWN` — recovered without live verification. Re-run the phase or\n"
    "manually inspect the evidence artifacts listed above to confirm the\n"
    "acceptance criteria were met.\n"
)
```

- The recovered report does NOT use a `status:` or `verdict:` frontmatter key — the verdict is a markdown body token (`` `UNKNOWN` ``) under `## Result`, never auto-`PASS` (REPORT.md line 69 cites `checkpoints.py:436-437` for the never-auto-PASS rule).
- **Per the diagnosis (REPORT.md line 75):** the Defect-2 regression test must seed an EXISTING `CP-P03-END.md` with a stale `status: fail` frontmatter key (stale agent-written verdict), then assert that verdict does NOT survive untouched after recovery. Existing tests inspect the recovered body via `e.expected_path.read_text()` and assert substrings (`"Auto-Recovered"`, `"recovered: true"`, `"**Verification:**"`, negative `"no verification block found" not in body`) — same idiom the new test should follow. REPORT.md line 45 notes a reusable verdict regex `PASS|FAIL|...|BLOCKED|SKIP` at `summarizer.py:69`. There is currently NO existing test that reads `status:`/`verdict:` from an existing checkpoint file; that is the NEW behavior being introduced.

---

## Summary for the builder

- **Test A (Defect 1, stranded deliverables)** → `tests/sprint/test_recovery.py::TestMergeRecoveryBundle` (or sibling). Reuse `_seed_release` / `_bundle_with_sidecar`, or `test_checkpoints.py::_full_recovery_manifest` for a richer layout. Audit-log assertion idiom: read `results/recovery-audit.log` as JSONL, filter `event == "merge_recovery_bundle"`, assert `status`/`failures`. Merge call: `merge_recovery_bundle(bundle, source_index)` or with explicit `release_dir=tmp_path`.
- **Test B (Defect 2, stale verdict)** → `tests/sprint/test_checkpoints.py::TestRecoverMissingCheckpoints`. Model after `test_does_not_overwrite_pre_existing_file` (line 454): hand-build a `CheckpointEntry` OR use `_seed_sprint` + pre-seed `checkpoints/CP-P03-END.md` with stale `status: fail` frontmatter; call `recover_missing_checkpoints(manifest, tmp_path/"artifacts", {3: p3})`; assert stale verdict is re-stamped (not left verbatim) when tasks pass, plus a paired negative test (tasks still failing ⇒ FAIL preserved). Evidence dirs: `tmp_path/"artifacts"/"D-####"/<file>.md` referencing the phase's task IDs.
- `RecoveryBundle` required kwargs: `bundle_id`, `affected_phase` only; rest defaulted. `CheckpointEntry` required: `phase`, `name`, `expected_path`, `exists`.
- Sidecar status string is inconsistent across helpers (`"pass"` in `_bundle_with_sidecar`, `"passed"` in `_full_recovery_manifest`) — match whichever helper you reuse.
- Recovered-report frontmatter keys: `checkpoint:`, `phase:`, `recovered: true`, `generated_at:`; verdict is a body token under `## Result` (`UNKNOWN`), never auto-PASS. No `status:`/`verdict:` frontmatter is written today — reading a stale `status:`/`verdict:` from an existing file is NEW behavior for Defect 2.
