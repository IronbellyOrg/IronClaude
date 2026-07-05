"""T08.10 / TEST-002 -- INV remediation suite.

Consolidates the per-INV acceptance tests enumerated in
``tests/swarm/conftest.py::INV_COVERAGE_MAP`` (INV-001 manifest lens
rehydration, INV-002 Python-only dispatch, INV-003 custom-prompt-dir
guard, INV-005 worker-vs-pool guard, INV-007 empty-pool failure,
INV-010 resume merge regen, INV-014 escape-hatch isomorphism) into a
single suite entry point. Each INV case is represented by:

  1. A **coverage-matrix integrity** meta-test verifying the backing
     test file enumerated in ``INV_COVERAGE_MAP`` exists and declares
     ``pytestmark = pytest.mark.inv`` so ``pytest -m inv`` selects
     every test it carries.

  2. A **canonical-invariant smoke test** that exercises the
     underlying contract directly through the public swarm API
     (``preflight.resume_mode``, the swarm-package import surface,
     ``preflight.read_custom_prompt_dir``,
     ``preflight.check_pool_size`` / ``workers_exceed_pool``,
     ``preflight.check_empty_pool`` / ``emit_env_missing_contract``,
     ``reduce.regenerate_merge_on_resume``,
     ``preflight.enforce_injection_guard``). A regression in any of
     those public surfaces fails the suite even when the full backing
     matrix is filtered out.

The suite itself carries ``pytestmark = pytest.mark.inv`` at module
scope so:

  * ``pytest tests/swarm/test_inv_suite.py -v`` runs the consolidated
    entry point in isolation.
  * ``pytest -m inv --collect-only`` picks up the suite alongside
    the backing modules; the union covers every INV case enumerated
    in ``INV_COVERAGE_MAP``.

Acceptance criteria pinned (phase-8-tasklist T08.10):

  * Each INV remediation has a dedicated passing test (7 smoke tests
    below, plus 7 parametrized integrity tests over the backing
    modules).
  * Suite runnable via ``pytest -m inv`` (module-level marker).
  * All 7 INV cases (INV-001/002/003/005/007/010/014) listed.
  * Suite collection lists ≥7 tests
    (``pytest -m inv --collect-only`` requirement).
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

# T08.10 / TEST-002 INV remediation suite (T08.03 / NFR-007). Module-
# level marker so every test in this file is selected by ``pytest -m inv``.
pytestmark = pytest.mark.inv


SWARM_TEST_DIR = Path(__file__).resolve().parent
REPO_ROOT = SWARM_TEST_DIR.parents[1]
SWARM_PKG = REPO_ROOT / "src" / "superclaude" / "cli" / "swarm"


# Canonical phase-8 INV enumeration. Kept in lockstep with
# ``tests/swarm/conftest.py::INV_COVERAGE_MAP`` -- the integrity
# meta-test below trips if the two enumerations drift.
_EXPECTED_INV_CASES: tuple[str, ...] = (
    "INV-001",
    "INV-002",
    "INV-003",
    "INV-005",
    "INV-007",
    "INV-010",
    "INV-014",
)


# ---------------------------------------------------------------------------
# Coverage-matrix integrity -- verify the 7 INV cases enumerated in
# ``INV_COVERAGE_MAP`` each have a backing test file with the inv
# marker. A regression that drops or renames a backing module trips
# here before the underlying matrix runs.
# ---------------------------------------------------------------------------


def test_inv_coverage_map_has_seven_cases(
    inv_coverage_map: dict[str, str],
) -> None:
    """The canonical INV enumeration carries exactly the 7 phase-8 cases."""
    assert set(inv_coverage_map) == set(_EXPECTED_INV_CASES), (
        f"INV_COVERAGE_MAP keys {sorted(inv_coverage_map)} drift from "
        f"the phase-8 enumeration {sorted(_EXPECTED_INV_CASES)}; update "
        "conftest.INV_COVERAGE_MAP and this suite together."
    )


@pytest.mark.parametrize("inv_case", _EXPECTED_INV_CASES)
def test_inv_backing_module_exists_and_is_marked(
    inv_case: str, inv_coverage_map: dict[str, str]
) -> None:
    """Each INV case's backing test file exists and declares pytest.mark.inv."""
    backing_name = inv_coverage_map[inv_case]
    backing_path = SWARM_TEST_DIR / backing_name
    assert backing_path.is_file(), (
        f"{inv_case}: backing module {backing_name} missing from "
        f"{SWARM_TEST_DIR}; suite coverage matrix is broken."
    )
    source = backing_path.read_text(encoding="utf-8")
    assert "pytestmark = pytest.mark.inv" in source, (
        f"{inv_case}: backing module {backing_name} does not declare "
        "module-level pytestmark = pytest.mark.inv; -m inv would skip "
        "every test it carries."
    )


# ---------------------------------------------------------------------------
# INV-001 -- resume rehydrates lens from manifest, not live LENSES
# ---------------------------------------------------------------------------


def test_inv001_resume_mode_rehydrates_from_manifest(tmp_path: Path) -> None:
    """INV-001: resume_mode reads lens-derived fields from the manifest.

    Build a minimal Manifest carrying a pinned ``ResolvedLensEntry``,
    persist it via ``write_manifest``, then install a mutated lens
    resolver that would overwrite every field. ``resume_mode`` must
    return a JobSpec carrying the manifest's snapshot values, and the
    mutated resolver must not be invoked.
    """
    from superclaude.cli.swarm.models import (
        JobSpec,
        LensEntry,
        Manifest,
        PreflightSummary,
        ResolvedLensEntry,
    )
    from superclaude.cli.swarm.preflight import (
        resume_mode,
        set_lens_resolver,
        write_manifest,
    )
    from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE

    snapshot_fragment = (
        "SUITE-PINNED snapshot prompt fragment. " + CANONICAL_INJECTION_GUARD_SENTENCE
    )
    snapshot = ResolvedLensEntry(
        name="bare-review",
        system_prompt_fragment=snapshot_fragment,
        user_template="SUITE user template: {{target}}",
        recipe_name="bare-review-v1",
        default_workers=3,
        suspect=True,
        tier="T2",
        recommended_next_command_template="sc:reflect on {job_id}",
        stability="stable",
    )
    manifest = Manifest(
        contract_version="1.0",
        job_id="job-inv-suite-001",
        resolved_lens_entry=snapshot,
        preflight=PreflightSummary(
            target_checksum="a" * 64,
            workers_requested=3,
            transport_kind="openai_compat",
        ),
    )
    manifest_path = write_manifest(manifest, tmp_path)

    resolver_calls: list[str] = []

    def mutated_resolver(name: str) -> LensEntry:
        resolver_calls.append(name)
        return LensEntry(
            name="bare-review",
            description="mutated lens registry entry",
            system_prompt_fragment=(
                "MUTATED fragment. " + CANONICAL_INJECTION_GUARD_SENTENCE
            ),
            user_template="MUTATED user template: {{target}}",
            output_template_path="/abs/path/to/mutated-template.j2",
            recipe_name="verdict-only-v1",
            normalizer_strategy="passthrough",
            default_workers=5,
            default_target_line_cap=6000,
            suspect=False,
            tier="T3",
            recommended_next_command_template="sc:troubleshoot {job_id}",
            acceptance_notes="mutated",
            stability="experimental",
        )

    previous = set_lens_resolver(mutated_resolver)
    try:
        spec = resume_mode(manifest_path)
    finally:
        set_lens_resolver(previous)

    assert isinstance(spec, JobSpec)
    assert spec.lens == "bare-review"
    assert spec.prompt.system == snapshot_fragment
    assert spec.prompt.user_template == "SUITE user template: {{target}}"
    assert spec.normalization.recipe == "bare-review-v1"
    # The mutated registry must NOT have been consulted on the default
    # (manifest-driven) resume path. INV-001's load-bearing assertion.
    assert resolver_calls == []


# ---------------------------------------------------------------------------
# INV-002 -- Python-only dispatch (no shell-out family in swarm package)
# ---------------------------------------------------------------------------


_INV002_FORBIDDEN_IMPORT_ROOTS: frozenset[str] = frozenset(
    {"subprocess", "shlex", "pty", "pexpect"}
)

# The INV-002 invariant pins the **dispatch surface** specifically --
# Wave-1 concurrency must route through Python (``ParallelExecutor`` ->
# threaded ``httpx``) rather than shelling out via ``swarm_dispatch.sh``.
# tmux / detached-mode OS-orchestration glue (``tmux.py``, the
# ``commands.py`` tmux helper) is unrelated to dispatch routing and is
# allowed to shell out for session control; the canonical backing test
# (``test_concurrency_python_only.py``) handles the package-wide audit.
# The smoke test scopes to the load-bearing dispatch modules so a
# regression that puts ``import subprocess`` into the dispatch path
# trips here independently of the package-wide audit's state.
# Roots scanned for INV-002. Each entry is a path relative to
# ``src/superclaude/cli/swarm/`` and may be either a single ``.py`` file
# or a subpackage directory (every ``.py`` underneath is scanned).
_INV002_DISPATCH_SURFACE: tuple[str, ...] = (
    "dispatch.py",
    "reduce.py",
    "preflight.py",
    "transports",
)


def _collect_inv002_surface_sources() -> list[Path]:
    """Resolve ``_INV002_DISPATCH_SURFACE`` entries to concrete ``.py`` files."""
    sources: list[Path] = []
    for rel in _INV002_DISPATCH_SURFACE:
        candidate = SWARM_PKG / rel
        if candidate.is_file():
            sources.append(candidate)
        elif candidate.is_dir():
            sources.extend(
                p
                for p in candidate.rglob("*.py")
                if p.is_file() and "__pycache__" not in p.parts
            )
    return sources


def test_inv002_dispatch_surface_has_no_shell_dispatch_imports() -> None:
    """INV-002: dispatch-path modules import no shell-out family.

    Parses ``dispatch.py`` / ``reduce.py`` / ``preflight.py`` and every
    ``.py`` under the ``transports/`` subpackage -- the concurrency-
    dispatch surface the INV-002 invariant pins -- and asserts none of
    them import ``subprocess`` / ``shlex`` / ``pty`` / ``pexpect``. The
    fuller AST-based audit (with call-target detection + mutation
    guards across every swarm source) lives in
    ``test_concurrency_python_only.py``; this smoke test guards the
    load-bearing dispatch leg so a regression that re-introduces
    shell-out at the Wave-1 routing path fails at the suite level
    before the full matrix runs.

    tmux / detached-mode OS-orchestration helpers are intentionally
    out of scope -- they shell out for tmux session control, not for
    Wave-1 concurrency dispatch -- so this smoke test does not flag
    them. The canonical backing test handles the package-wide audit
    with whatever allowlist policy applies to non-dispatch modules.
    """
    missing = [
        rel for rel in _INV002_DISPATCH_SURFACE if not (SWARM_PKG / rel).exists()
    ]
    assert missing == [], (
        f"swarm dispatch surface missing modules/subpackages {missing}; "
        "the INV-002 audit would be vacuously green -- this smoke test "
        "must fail loudly when the dispatch surface is misrouted."
    )

    sources = _collect_inv002_surface_sources()
    assert sources, (
        "swarm dispatch surface resolved to zero Python sources; the "
        "INV-002 audit would be vacuously green."
    )

    hits: list[tuple[str, int, str]] = []
    for source_path in sources:
        rel = str(source_path.relative_to(SWARM_PKG))
        tree = ast.parse(
            source_path.read_text(encoding="utf-8"), filename=str(source_path)
        )
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".", 1)[0]
                    if root in _INV002_FORBIDDEN_IMPORT_ROOTS:
                        hits.append((rel, node.lineno, alias.name))
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                root = module.split(".", 1)[0]
                if root in _INV002_FORBIDDEN_IMPORT_ROOTS:
                    hits.append((rel, node.lineno, module))

    assert hits == [], (
        "INV-002 violation: forbidden shell-dispatch imports found in "
        "the swarm concurrency-dispatch surface: "
        + ", ".join(f"{rel}:{lineno} ({name})" for rel, lineno, name in hits)
    )


# ---------------------------------------------------------------------------
# INV-003 -- custom-prompt-dir guard delegates to enforce_injection_guard
# ---------------------------------------------------------------------------


def test_inv003_custom_prompt_dir_rejects_missing_substring(
    tmp_path: Path,
) -> None:
    """INV-003: read_custom_prompt_dir raises on §11.5 substring miss.

    Drives a system.txt that lacks the §11.5 canonical sentence through
    the custom-prompt-dir reader. The reader must raise
    :class:`PreflightError` carrying :data:`RULE_INJECTION_GUARD` with
    ``reason="injection-guard"`` -- the same shape the lens path
    emits, satisfying the INV-003 identical-guard property.
    """
    from superclaude.cli.swarm.preflight import (
        RULE_INJECTION_GUARD,
        PreflightError,
        read_custom_prompt_dir,
    )
    from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE

    cpd = tmp_path / "custom_prompt"
    cpd.mkdir()
    # ``system.txt`` deliberately omits the §11.5 canonical sentence so
    # the guard rejects it; the other two required files are present so
    # the only surfaced failure is the injection-guard one.
    (cpd / "system.txt").write_text(
        "You are a code reviewer. (no §11.5 framing present)\n",
        encoding="utf-8",
    )
    (cpd / "user.txt").write_text("Review {{target}}\n", encoding="utf-8")
    (cpd / "meta.yaml").write_text("variables: {}\n", encoding="utf-8")

    with pytest.raises(PreflightError) as exc_info:
        read_custom_prompt_dir(
            cpd,
            required_substring=CANONICAL_INJECTION_GUARD_SENTENCE,
            auto_inject_guard=False,
        )

    failures = exc_info.value.failures
    guard_failures = [f for f in failures if f.rule == RULE_INJECTION_GUARD]
    assert len(guard_failures) == 1, (
        "INV-003 violation: custom-prompt-dir reader did not emit a "
        f"{RULE_INJECTION_GUARD} failure for a system.txt missing the "
        f"§11.5 substring; surfaced failures: {failures!r}."
    )
    assert guard_failures[0].reason == "injection-guard"
    assert guard_failures[0].path == "custom_prompt_dir/system.txt"


# ---------------------------------------------------------------------------
# INV-005 -- workers.count vs configured model-pool size guard
# ---------------------------------------------------------------------------


def test_inv005_check_pool_size_stop_policy_emits_failure() -> None:
    """INV-005: check_pool_size with policy="stop" rejects oversize fan-out.

    Detection-only helper contract -- the OQ-007 V2 STOP branch must
    surface :data:`RULE_WORKERS_EXCEED_POOL` whenever
    ``workers_count > len(pool)`` (and the pool is non-empty).
    ``policy="warn"`` is detection-only and returns ``[]`` even on
    oversize so the run_preflight clamp + warning path can run.
    """
    from superclaude.cli.swarm.preflight import (
        RULE_WORKERS_EXCEED_POOL,
        check_pool_size,
        workers_exceed_pool,
    )

    # workers_exceed_pool is the pure detection predicate.
    assert workers_exceed_pool(5, ["a", "b", "c"]) is True
    assert workers_exceed_pool(3, ["a", "b", "c"]) is False

    stop_failures = check_pool_size(5, ["a", "b", "c"], policy="stop")
    assert len(stop_failures) == 1, (
        "INV-005 violation: check_pool_size(policy='stop') did not "
        "emit exactly one failure for workers=5 over pool=['a','b','c']."
    )
    assert stop_failures[0].rule == RULE_WORKERS_EXCEED_POOL
    assert stop_failures[0].reason == "workers-exceed-pool"

    warn_failures = check_pool_size(5, ["a", "b", "c"], policy="warn")
    assert warn_failures == [], (
        "INV-005 violation: check_pool_size(policy='warn') must be "
        "detection-only and return []; the clamp + WARNING wiring "
        "lives in run_preflight."
    )

    # Empty pool is INV-007's job; check_pool_size must stay silent.
    assert check_pool_size(5, [], policy="stop") == []


# ---------------------------------------------------------------------------
# INV-007 -- empty configured model pool emits env-missing contract
# ---------------------------------------------------------------------------


def test_inv007_check_empty_pool_emits_env_missing_contract() -> None:
    """INV-007: check_empty_pool emits the env-missing failure shape.

    Detection-only helper contract -- the empty-pool case must surface
    :data:`RULE_EMPTY_POOL` with ``reason="env-missing"`` so
    :func:`emit_env_missing_contract` (the structured writer) wires the
    ``failed`` / ``env-missing`` contract per OQ-008.
    """
    from superclaude.cli.swarm.preflight import (
        ENV_MISSING_REASON,
        RULE_EMPTY_POOL,
        check_empty_pool,
        emit_env_missing_contract,
    )

    # Empty list AND list-of-empty-strings both fall under INV-007.
    for empty_pool in ([], ["", ""]):
        failures = check_empty_pool(empty_pool)
        assert len(failures) == 1, (
            f"INV-007 violation: check_empty_pool({empty_pool!r}) did "
            f"not emit exactly one failure; surfaced: {failures!r}."
        )
        assert failures[0].rule == RULE_EMPTY_POOL
        assert failures[0].reason == ENV_MISSING_REASON

    # Non-empty pool stays silent.
    assert check_empty_pool(["model-a"]) == []

    # The structured-contract writer is part of the INV-007 wiring; if
    # the symbol disappears the contract surface is broken even when
    # the detection helper still trips.
    assert callable(emit_env_missing_contract)


# ---------------------------------------------------------------------------
# INV-010 -- resume regenerates merged.md unconditionally (normalize+merge)
# ---------------------------------------------------------------------------


def test_inv010_resume_regenerates_merge_unconditionally(tmp_path: Path) -> None:
    """INV-010: regenerate_merge_on_resume deletes stale merged.md.

    Filesystem-only helper contract -- a pre-existing ``merged.md``
    must be unlinked when the amalgamation mode is ``"normalize+merge"``,
    and left untouched (return ``None``) for ``"raw"`` / ``"normalize"``
    modes that never write ``merged.md`` in the first place.
    """
    from superclaude.cli.swarm.reduce import (
        MERGED_FILENAME,
        regenerate_merge_on_resume,
    )

    # normalize+merge -> stale merged.md is deleted.
    stale = tmp_path / MERGED_FILENAME
    stale.write_text("stale pre-crash merge body\n", encoding="utf-8")
    deleted = regenerate_merge_on_resume(tmp_path, "normalize+merge")
    assert deleted == stale
    assert not stale.exists(), (
        "INV-010 violation: regenerate_merge_on_resume did not unlink "
        f"{stale}; a stale pre-crash merge body would survive resume."
    )

    # Idempotent: a second call on a missing merged.md returns None.
    assert regenerate_merge_on_resume(tmp_path, "normalize+merge") is None

    # raw / normalize -- never write merged.md, so the helper must
    # stay silent even when one happens to exist on disk.
    stale_raw = tmp_path / MERGED_FILENAME
    stale_raw.write_text("survives raw-mode resume\n", encoding="utf-8")
    assert regenerate_merge_on_resume(tmp_path, "raw") is None
    assert stale_raw.exists(), (
        "INV-010 violation: regenerate_merge_on_resume must be a no-op "
        "when mode != 'normalize+merge'; raw-mode resume deleted the file."
    )
    assert regenerate_merge_on_resume(tmp_path, "normalize") is None
    assert stale_raw.exists()


# ---------------------------------------------------------------------------
# INV-014 -- escape-hatch isomorphism (lens path ↔ custom-prompt-dir path)
# ---------------------------------------------------------------------------


def test_inv014_enforce_injection_guard_path_isomorphism() -> None:
    """INV-014: enforce_injection_guard produces isomorphic failures.

    The lens path (``path_label="prompt.system"``) and the
    custom-prompt-dir path (``path_label="custom_prompt_dir/system.txt"``)
    feed the same enforcement helper. Both must surface
    :data:`RULE_INJECTION_GUARD` with ``reason="injection-guard"`` and
    a message body that differs only in the path-label substring --
    i.e. byte-identical modulo the path field. INV-014 declares this
    bijection load-bearing: a guard regression on only one path would
    break the parity and surface here.
    """
    from superclaude.cli.swarm.preflight import (
        RULE_INJECTION_GUARD,
        enforce_injection_guard,
    )

    system = "this fragment lacks the required substring"
    required = "REQUIRED-SUBSTRING-SENTINEL"

    lens_failures = enforce_injection_guard(
        system=system,
        required_substring=required,
        path_label="prompt.system",
    )
    cpd_failures = enforce_injection_guard(
        system=system,
        required_substring=required,
        path_label="custom_prompt_dir/system.txt",
    )

    assert len(lens_failures) == 1 and len(cpd_failures) == 1, (
        "INV-014 violation: enforce_injection_guard must emit exactly "
        f"one failure per path; lens={lens_failures!r}, cpd={cpd_failures!r}."
    )

    lens_only, cpd_only = lens_failures[0], cpd_failures[0]

    # Identical structural tokens -- the load-bearing parity.
    assert lens_only.rule == cpd_only.rule == RULE_INJECTION_GUARD
    assert lens_only.reason == cpd_only.reason == "injection-guard"

    # Path labels legitimately differ; both must be present on their
    # own failure and absent from the sibling's.
    assert lens_only.path == "prompt.system"
    assert cpd_only.path == "custom_prompt_dir/system.txt"

    # Normalized message bodies (path label substituted out) must
    # match byte-for-byte -- the isomorphism core.
    sentinel = "<PATH_LABEL>"
    lens_msg_norm = lens_only.message.replace(lens_only.path, sentinel)
    cpd_msg_norm = cpd_only.message.replace(cpd_only.path, sentinel)
    assert lens_msg_norm == cpd_msg_norm, (
        "INV-014 violation: normalised failure messages diverge; the "
        f"escape-hatch path bypasses the shared enforcement template.\n"
        f"  lens : {lens_msg_norm!r}\n"
        f"  cpd  : {cpd_msg_norm!r}"
    )
