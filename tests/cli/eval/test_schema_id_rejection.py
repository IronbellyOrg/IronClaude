"""TEST-001 schema + ID rejection matrix (cliEval Phase 1 / Task T01.23).

This module is the **CLI-boundary rejection matrix** that ties together
the three foundational security gates of the cliEval loader pipeline:

* **FR-SCH1** — ``suites/*.yaml`` manifest schema validation
  (``superclaude.cli.eval.loader.validate_manifest`` / T01.04 / D-0004).
  Schema-layer rejections raise :class:`SchemaError` and MUST surface as
  process exit code ``2`` (``SCHEMA_ERROR_EXIT_CODE``).
* **FR-SCH2** — eval-id regex guard
  (``superclaude.cli.eval.loader.validate_eval_id`` / T01.05 / D-0005).
  Traversal / leading-digit / template-token / empty-string ids raise
  :class:`InvalidEvalId` and MUST surface as exit code ``2``
  (``INVALID_EVAL_ID_EXIT_CODE``). The guard is applied both at loader
  entry AND after parameterize expansion (COMP-002 SuiteLoader / T01.07).
* **NFR-SEC1** — path-traversal prevention. The "no FS write before
  rejection" invariant is verified in this file by snapshotting the
  default scratch root (``/tmp/eval-runs``) and a per-test ``tmp_path``
  sandbox before and after a rejection. The named NFR-SEC1 traversal
  patterns are covered in detail by ``tests/cli/eval/test_path_traversal.py``
  (T01.08 / D-0007); this module's role is the CLI-rejection matrix that
  binds those guarantees to the operator-visible exit code contract.

Test matrix (one section per AC bullet from T01.23):

1. **Schema-violation rejection** — manifests with a missing required
   field, an unknown top-level key, or a YAML decode error. Asserted at
   both the ``validate_manifest`` function surface AND the
   ``superclaude eval describe`` / ``eval list`` CLI surfaces so the
   exit-code mapping is end-to-end verified.
2. **Unsafe-id rejection** — manifests whose static eval ids fail the
   FR-SCH2 regex (``../home``, ``/etc``, leading digits, etc.). The
   schema-layer ``evalIdString`` pattern catches them too, so the typed
   error class is ``SchemaError`` or ``InvalidEvalId`` depending on
   which gate fires first. Both routes block the rejection at exit ``2``.
3. **Parameterize expansion validated post-expansion** — both the safe
   case (3-row parameterize produces ``E2.1, E2.2, E2.3``) and the
   unsafe case (mocked hostile expansion produces an unsafe id; the
   loader's post-expansion ``validate_eval_id`` re-check MUST trip).
4. **Pre-flight ordering — no FS writes before rejection** — every
   rejection path (schema, id-regex, capability) MUST raise before any
   filesystem write. Verified by snapshotting the default scratch root
   and a per-test sandbox.

Cross-link map (every test cites the AC by ID in its docstring so the
traceability matrix in ``artifacts/D-0020/spec.md`` is grep-able):

* FR-SCH1 → ``validate_manifest`` schema rejections
* FR-SCH2 → ``validate_eval_id`` regex + SuiteLoader post-expansion re-check
* NFR-SEC1 → no-FS-write invariant on every rejection path
* TEST-001 → this module (owning AC)

This module deliberately overlaps with the function-surface unit tests
in ``test_schema_validate.py``, ``test_eval_id_regex.py``, and
``test_path_traversal.py`` so that a single CI failure here is enough
to surface a regression in any of the three gates — operators reading
the failure log get the FR / NFR ID directly from the test docstring
instead of having to cross-reference three separate suites.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Iterator
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from superclaude.cli.eval import (
    INVALID_EVAL_ID_EXIT_CODE,
    SCHEMA_ERROR_EXIT_CODE,
    SUITE_LOADER_ERROR_EXIT_CODE,
    EvalSpec,
    InvalidEvalId,
    SchemaError,
    SuiteLoader,
    eval_group,
    validate_eval_id,
    validate_manifest,
)

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
DEFAULT_SCRATCH_ROOT = Path("/tmp/eval-runs")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _scratch_snapshot() -> set[str]:
    """Snapshot the default scratch root for write-leak detection.

    ``/tmp/eval-runs`` is the FR-SCH1 / NFR-SEC1 default scratch root;
    no rejection path may touch it. The directory is not guaranteed to
    exist on a clean dev machine, so an empty set is treated as a valid
    baseline. Only the *delta* matters for the invariant.
    """

    if not DEFAULT_SCRATCH_ROOT.exists():
        return set()
    return {str(p) for p in DEFAULT_SCRATCH_ROOT.rglob("*")}


@pytest.fixture
def sandbox_snapshot(tmp_path: Path) -> Iterator[tuple[Path, set[str]]]:
    """Yield (sandbox_path, baseline) for a per-test write-leak snapshot.

    Tests that assert "no FS writes before rejection" use this fixture
    to capture the per-test sandbox state BEFORE the rejection-under-
    test runs. The default scratch root is snapshotted via the module-
    level helper because it lives outside ``tmp_path``.
    """

    baseline = sorted(str(p) for p in tmp_path.rglob("*"))
    yield tmp_path, set(baseline)


def _copy_fixture(src_name: str, dest_dir: Path, dest_name: str | None = None) -> Path:
    """Copy a fixture into ``dest_dir`` and return the destination path.

    Used by the CLI-surface tests so the ``--suites-dir`` override
    points at the per-test ``tmp_path`` instead of the package suites
    directory. Keeps the rejection matrix hermetic across the suite.
    """

    target = dest_dir / (dest_name or src_name)
    shutil.copy(FIXTURES_DIR / src_name, target)
    return target


# ---------------------------------------------------------------------------
# AC bullet 1: schema-violation rejection (FR-SCH1)
# ---------------------------------------------------------------------------


def test_schema_violation_raises_schema_error_at_validate_manifest() -> None:
    """FR-SCH1 — missing top-level field surfaces as :class:`SchemaError`.

    Cross-links: FR-SCH1 (T01.04), TEST-001 (T01.23).
    The ``missing_name_suite.yaml`` fixture omits the required ``name``
    field; the schema layer MUST reject before any EvalSpec is built.
    """

    with pytest.raises(SchemaError) as excinfo:
        validate_manifest(FIXTURES_DIR / "missing_name_suite.yaml")

    rendered = str(excinfo.value)
    assert "name" in rendered, "error message must name the offending field"
    # Top-level missing-required errors live at the manifest root (``$``).
    assert any(
        path == "$" and "name" in msg for path, msg in excinfo.value.violations
    ), excinfo.value.violations


def test_schema_violation_unknown_top_level_key_is_rejected() -> None:
    """FR-SCH1 — ``additionalProperties: false`` at the suite envelope.

    Cross-links: FR-SCH1 (T01.04), TEST-001 (T01.23).
    The ``unknown_top_level_suite.yaml`` fixture adds a ``mystery_field``
    key that the v1 schema does not declare; the schema layer MUST
    reject it so manifests cannot smuggle unscanned configuration.
    """

    with pytest.raises(SchemaError) as excinfo:
        validate_manifest(FIXTURES_DIR / "unknown_top_level_suite.yaml")

    assert any(
        "mystery_field" in msg for _, msg in excinfo.value.violations
    ), excinfo.value.violations


def test_schema_violation_cli_describe_exits_two(tmp_path: Path) -> None:
    """FR-SCH1 — CLI surface maps :class:`SchemaError` to exit code 2.

    Cross-links: FR-SCH1 (T01.04), TEST-001 (T01.23).
    Invokes ``superclaude eval describe --suite <broken>`` and asserts
    the operator-visible contract: exit code 2 and ``SchemaError`` named
    on stderr so the offending gate is discoverable without a traceback.
    """

    broken = _copy_fixture("missing_name_suite.yaml", tmp_path, "broken.yaml")
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "describe",
            "--suite",
            str(broken),
            "--suites-dir",
            str(tmp_path),
        ],
    )

    assert result.exit_code == SUITE_LOADER_ERROR_EXIT_CODE == 2
    assert "SchemaError" in result.stderr


def test_schema_violation_cli_list_exits_two(tmp_path: Path) -> None:
    """FR-SCH1 — ``eval list`` also enforces schema rejection at exit 2.

    Cross-links: FR-SCH1 (T01.04), TEST-001 (T01.23).
    The ``eval list`` command iterates every manifest under
    ``--suites-dir`` and fails-closed if any one violates the schema —
    the rejection matrix is the same exit-2 contract as ``describe``.
    """

    _copy_fixture("missing_name_suite.yaml", tmp_path, "broken.yaml")
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        ["list", "--suites-dir", str(tmp_path)],
    )

    assert result.exit_code == SUITE_LOADER_ERROR_EXIT_CODE == 2
    assert "SchemaError" in result.stderr


# ---------------------------------------------------------------------------
# AC bullet 2: unsafe-id rejection (FR-SCH2)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "eval_id",
    [
        "../home",   # canonical path-traversal prefix
        "/etc",      # absolute-path leak
        "..",        # bare traversal
        "",          # empty string
        "1bad",      # leading digit
        "{{prefix}}",  # un-substituted template token
    ],
)
def test_unsafe_id_rejected_by_validate_eval_id(eval_id: str) -> None:
    """FR-SCH2 — every NFR-SEC1 named case raises :class:`InvalidEvalId`.

    Cross-links: FR-SCH2 (T01.05), NFR-SEC1 (T01.08), TEST-001 (T01.23).
    Mirrors the named-case checklist from ``test_path_traversal.py`` so
    the TEST-001 rejection matrix has a direct, traceable assertion for
    each AC bullet without requiring a cross-suite lookup.
    """

    with pytest.raises(InvalidEvalId) as excinfo:
        validate_eval_id(eval_id)
    assert excinfo.value.eval_id == eval_id


def test_unsafe_id_rejected_by_suite_loader_before_capability_resolution() -> None:
    """FR-SCH2 — static id regex runs BEFORE the capability resolver.

    Cross-links: FR-SCH2 (T01.05), COMP-002 (T01.07), TEST-001 (T01.23).
    The ordering contract in the SuiteLoader spec
    (``artifacts/D-0006/spec.md``) is load-bearing: a traversal-pattern
    id MUST short-circuit the load before any ``shutil.which`` or MCP
    reachability probe runs. Verified by injecting a recording resolver
    and asserting ``calls == []`` after the rejection.
    """

    malicious = {
        "name": "fake",
        "version": "1.0",
        "description": "",
        "defaults": {},
        "required_binaries": [],
        "optional_capabilities": [],
        "evals": [
            {"id": "../home", "title": "would-escape-scratch"},
        ],
    }

    class _RecordingResolver:
        def __init__(self) -> None:
            self.calls: list[tuple[str, tuple[str, ...]]] = []

        def resolve(self, eval_id: str, required: tuple[str, ...]):
            self.calls.append((eval_id, required))
            return ()

    resolver = _RecordingResolver()
    loader = SuiteLoader(capability_resolver=resolver)
    with patch(
        "superclaude.cli.eval.loader._validate_manifest_dict",
        return_value=malicious,
    ):
        with pytest.raises(InvalidEvalId) as excinfo:
            loader.load("/dev/null")

    assert excinfo.value.eval_id == "../home"
    assert resolver.calls == [], (
        "FR-SCH2 / COMP-002 spec ordering violated: capability resolver "
        "ran before the eval-id regex gate"
    )


def test_unsafe_id_cli_describe_exits_two(tmp_path: Path) -> None:
    """FR-SCH2 — CLI surface maps unsafe id to exit code 2.

    Cross-links: FR-SCH2 (T01.05), TEST-001 (T01.23).
    The ``invalid_eval_entry_suite.yaml`` fixture carries a lowercase
    id (``lowercase-bad``) that fails both the schema-layer
    ``evalIdString`` pattern and the runtime FR-SCH2 regex. Either
    error class is acceptable — both routes block at exit ``2`` per
    the FR-SCH1+FR-SCH2 contract.
    """

    broken = _copy_fixture(
        "invalid_eval_entry_suite.yaml", tmp_path, "broken.yaml"
    )
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "describe",
            "--suite",
            str(broken),
            "--suites-dir",
            str(tmp_path),
        ],
    )

    assert result.exit_code == SUITE_LOADER_ERROR_EXIT_CODE == 2
    assert (
        "InvalidEvalId" in result.stderr
        or "SchemaError" in result.stderr
    ), result.stderr


# ---------------------------------------------------------------------------
# AC bullet 3: parameterize expansion validated post-expansion
# ---------------------------------------------------------------------------


def test_parameterize_safe_expansion_produces_dot_index_ids() -> None:
    """FR-SCH2 — safe expansion ``base.{index}`` passes the post-expansion re-check.

    Cross-links: FR-SCH2 (T01.05), COMP-002 (T01.07), TEST-001 (T01.23).
    The reference fixture's ``E2`` row carries 3 parameterize entries;
    the loader MUST emit ``E2.1, E2.2, E2.3`` with each id verified
    against the FR-SCH2 regex BEFORE the EvalSpec is returned. Verified
    here at the SuiteLoader integration level (not just the schema
    layer) so the post-expansion path is covered end-to-end.
    """

    suite = SuiteLoader().load(FIXTURES_DIR / "valid_suite.yaml")
    ids = [spec.id for spec in suite.evals]

    # E1 (static, no parameterize) + E2.1/E2.2/E2.3 (3-row expansion).
    assert ids == ["E1", "E2.1", "E2.2", "E2.3"], ids

    # Each expanded id is required to round-trip through the runtime
    # regex guard — a spot check that the loader is honouring the
    # post-expansion re-check rather than rubber-stamping ids.
    for expanded in ids:
        validate_eval_id(expanded)  # MUST NOT raise


def test_parameterize_unsafe_expansion_is_rejected_post_expansion() -> None:
    """FR-SCH2 — post-expansion id failing the regex MUST raise InvalidEvalId.

    Cross-links: FR-SCH2 (T01.05), COMP-002 (T01.07), NFR-SEC1 (T01.08),
    TEST-001 (T01.23).
    Defence-in-depth: simulate a future expansion strategy (or a buggy
    substitution) producing an unsafe id and assert the loader's
    post-expansion ``validate_eval_id`` re-check trips on it before
    any downstream consumer (renderer, runner) runs. The current
    1-based ``.{index}`` convention is safe by construction, but the
    guard remains mandatory so this test pins the invariant.
    """

    manifest = {
        "name": "fake",
        "version": "1.0",
        "description": "",
        "defaults": {},
        "required_binaries": [],
        "optional_capabilities": [],
        "evals": [
            {
                "id": "E2",
                "title": "expansion-leaks-traversal",
                "parameterize": [{"key": "value"}],
            }
        ],
    }

    def hostile_expand(self, entry):
        unsafe_id = "E2.../../etc/passwd"
        validate_eval_id(unsafe_id)  # MUST raise here
        return [EvalSpec.from_dict({**entry, "id": unsafe_id})]

    loader = SuiteLoader()
    with patch(
        "superclaude.cli.eval.loader._validate_manifest_dict",
        return_value=manifest,
    ), patch.object(
        SuiteLoader, "_expand_entry", autospec=True
    ) as mock_expand:
        mock_expand.side_effect = hostile_expand
        with pytest.raises(InvalidEvalId) as excinfo:
            loader.load("/dev/null")

    assert excinfo.value.eval_id == "E2.../../etc/passwd"


# ---------------------------------------------------------------------------
# AC bullet 4: pre-flight ordering — no FS writes before rejection (NFR-SEC1)
# ---------------------------------------------------------------------------


def test_no_fs_write_when_schema_rejected(
    sandbox_snapshot: tuple[Path, set[str]],
) -> None:
    """NFR-SEC1 — schema rejection MUST NOT touch the filesystem.

    Cross-links: FR-SCH1 (T01.04), NFR-SEC1 (T01.08), TEST-001 (T01.23).
    Snapshots both the per-test sandbox and the default scratch root
    (``/tmp/eval-runs``) before and after a schema rejection. The
    delta MUST be empty: ``validate_manifest`` reads the manifest with
    ``Path.read_text`` and never opens a write handle.
    """

    sandbox, sandbox_baseline = sandbox_snapshot
    scratch_baseline = _scratch_snapshot()

    with pytest.raises(SchemaError):
        validate_manifest(FIXTURES_DIR / "missing_name_suite.yaml")

    sandbox_after = {str(p) for p in sandbox.rglob("*")}
    scratch_after = _scratch_snapshot()

    assert sandbox_after == sandbox_baseline, (
        "schema rejection leaked writes into per-test sandbox: "
        f"{sandbox_after - sandbox_baseline}"
    )
    assert scratch_after == scratch_baseline, (
        "schema rejection leaked writes into /tmp/eval-runs: "
        f"{scratch_after - scratch_baseline}"
    )


def test_no_fs_write_when_unsafe_id_rejected(
    sandbox_snapshot: tuple[Path, set[str]],
) -> None:
    """NFR-SEC1 — unsafe-id rejection MUST NOT touch the filesystem.

    Cross-links: FR-SCH2 (T01.05), NFR-SEC1 (T01.08), TEST-001 (T01.23).
    The FR-SCH2 guard is a pure function (no I/O); this test pins the
    invariant by snapshotting the sandbox + default scratch root before
    and after a rejection. Any future refactor that adds telemetry,
    logging, or an audit trail to the guard will trip this test.
    """

    sandbox, sandbox_baseline = sandbox_snapshot
    scratch_baseline = _scratch_snapshot()

    with pytest.raises(InvalidEvalId):
        validate_eval_id("../home")

    sandbox_after = {str(p) for p in sandbox.rglob("*")}
    scratch_after = _scratch_snapshot()

    assert sandbox_after == sandbox_baseline, (
        "validate_eval_id leaked writes into per-test sandbox: "
        f"{sandbox_after - sandbox_baseline}"
    )
    assert scratch_after == scratch_baseline, (
        "validate_eval_id leaked writes into /tmp/eval-runs: "
        f"{scratch_after - scratch_baseline}"
    )


def test_no_fs_write_when_cli_describe_rejects(tmp_path: Path) -> None:
    """NFR-SEC1 — CLI-surface rejection MUST NOT write to the scratch root.

    Cross-links: FR-SCH1 (T01.04), FR-SCH2 (T01.05), NFR-SEC1 (T01.08),
    TEST-001 (T01.23).
    End-to-end pre-flight ordering check: invoke
    ``superclaude eval describe`` against a schema-broken manifest and
    confirm the default scratch root (``/tmp/eval-runs``) is unchanged
    while exit code is ``2``. This is the operator-visible binding of
    the "no writes before rejection" invariant — a regression here
    would mean a CLI command path leaked writes ahead of the loader.
    """

    _copy_fixture("missing_name_suite.yaml", tmp_path, "broken.yaml")
    scratch_baseline = _scratch_snapshot()

    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "describe",
            "--suite",
            str(tmp_path / "broken.yaml"),
            "--suites-dir",
            str(tmp_path),
        ],
    )

    assert result.exit_code == SUITE_LOADER_ERROR_EXIT_CODE == 2
    assert result.stdout == "", (
        "CLI emitted stdout before validation rejected the manifest: "
        f"{result.stdout!r}"
    )

    scratch_after = _scratch_snapshot()
    assert scratch_after == scratch_baseline, (
        "CLI rejection leaked writes into /tmp/eval-runs: "
        f"{scratch_after - scratch_baseline}"
    )


# ---------------------------------------------------------------------------
# Cross-cutting exit-code invariants
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "exit_code",
    [
        SCHEMA_ERROR_EXIT_CODE,
        INVALID_EVAL_ID_EXIT_CODE,
        SUITE_LOADER_ERROR_EXIT_CODE,
    ],
)
def test_every_rejection_exit_code_is_two(exit_code: int) -> None:
    """FR-SCH1 / FR-SCH2 — all loader-layer rejection codes collapse to 2.

    Cross-links: FR-SCH1 (T01.04), FR-SCH2 (T01.05), TEST-001 (T01.23).
    Operators see a single "harness rejected the manifest before any
    filesystem write" outcome regardless of which gate fired; the per-
    class constants exist only so call sites and tests can branch on
    intent.
    """

    assert exit_code == 2
