"""Contract #1 master-invariant recurrence regression suite (Step 13.3).

This module is the single steady-state gate that proves every documented
RECURRENT failure mode is now caught — or, where a failure mode is not
deterministically scanner-testable, that it is EXPLICITLY and auditably
skipped rather than silently dropped.

Contract #1 ("MUST FAIL pre-fix / PASS post-fix")
-------------------------------------------------
Contract #1's fail-before/pass-after property is attested **per-class at the
phase that landed the fix**: anti_instinct at R0.2 (Step 3.4 Findings),
id_containment at R0.1 (Step 2.5 Findings), retry_contract / fragility_stub /
threshold_registry / dispatch_reachability / spec_fidelity / verification at
R1.x (the R1.3/R1.5/R1.6 Findings). Phase 13 has **no pre-fix checkout** — it
runs against the post-fix tree only — so this suite asserts the *steady-state
PASS* (post-fix) for each dispatched class PLUS a no-silent-drop enumeration
invariant: every fixture under ``tests/roadmap/fixtures/recurrence/`` is either
dispatched against its real component, deferred with an auditable reason, or
recorded in the undispatched-class registry. A fixture that is none of these
FAILS ``test_every_fixture_enumerated_or_skipped``.

Anti-theater
------------
Each dispatch callable RUNS the real pipeline component against the fixture and
asserts the live output matches the ``.expected.json`` oracle. There are no
trivially-passing assertions: a class is absent from ``FAILURE_CLASS_DISPATCH``
only if every fixture in it is ``deferred:true`` or the class is in
``UNDISPATCHED_CLASSES`` with a recorded skip reason.

UV-only::

    uv run pytest tests/roadmap/test_recurrence_regression.py -v
"""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path

import pytest

# --- Real pipeline components under test -----------------------------------
from superclaude.cli.roadmap import gates as _gates
from superclaude.cli.roadmap.code_assertions import assert_step_reachable
from superclaude.cli.roadmap.envelope import PipelineEnvelope
from superclaude.cli.roadmap.id_registry import SpecIdRegistry, build_id_registry
from superclaude.cli.roadmap.obligation_scanner import scan_obligations
from superclaude.tools.arch_lint import scan_file

# The Contract #5 fragility-stub regex + cli-tree scanner live in a sibling
# test module; reuse them rather than re-deriving the pattern (single SoT).
from tests.roadmap.test_no_fragility_stubs import _FRAGILITY_STUB_RE, _cli_root

# ---------------------------------------------------------------------------
# Corpus discovery
# ---------------------------------------------------------------------------

_CORPUS_DIR = Path(__file__).resolve().parent / "fixtures" / "recurrence"
_REPO_ROOT = Path(__file__).resolve().parents[2]


def _discover_fixtures() -> list[tuple[str, str, Path, Path]]:
    """Glob every recurrence fixture as ``(failure_class, case, md, json)``.

    ``failure_class`` is the parent directory name (the corpus layout
    convention documented at ``fixtures/recurrence/README.md`` and the
    seeding map). Discovery is dynamic so a newly-added fixture is
    auto-enumerated by ``test_every_fixture_enumerated_or_skipped`` and
    cannot slip through as an implicit drop.
    """
    out: list[tuple[str, str, Path, Path]] = []
    for md_path in sorted(_CORPUS_DIR.glob("*/*.md")):
        expected_path = md_path.with_suffix(".expected.json")
        if not expected_path.is_file():
            # A bare .md with no oracle is itself a drop — surface it as a
            # discoverable fixture so the enumeration test fails loudly.
            out.append((md_path.parent.name, md_path.stem, md_path, expected_path))
            continue
        out.append((md_path.parent.name, md_path.stem, md_path, expected_path))
    return out


_FIXTURES = _discover_fixtures()


def _load_expected(expected_path: Path) -> dict:
    if not expected_path.is_file():
        return {}
    return json.loads(expected_path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Dispatch callables — each RUNS the real component + asserts the oracle.
# Signature: (md_path: Path, expected: dict) -> None ; raises AssertionError.
# ---------------------------------------------------------------------------


def _slice_section(text: str, heading: str) -> str:
    """Return the H2 section body (heading exclusive → next H2 exclusive).

    Mirrors ``test_spec_roadmap_id_containment._slice_section`` so the
    spec_fidelity phantom-ID fixture is sliced identically to the
    id_containment fixtures it shares the ``_roadmap_ids_within_spec``
    mechanism with.
    """
    marker = f"\n## {heading}\n"
    if marker not in text:
        marker = f"## {heading}\n"
    start = text.index(marker) + len(marker)
    rest = text[start:]
    nxt = rest.find("\n## ")
    return rest if nxt == -1 else rest[:nxt]


def dispatch_anti_instinct(md_path: Path, expected: dict) -> None:
    """Contract #10 — run ``scan_obligations`` on the fixture.

    FP cases (``expected_high_findings`` present) assert the documented
    historical false positive is now absorbed by the Layer 6 allowlist; the
    genuine-obligation case asserts the allowlist did NOT over-broaden.
    """
    content = md_path.read_text(encoding="utf-8")
    report = scan_obligations(content)
    high = [o for o in report.obligations if o.severity == "HIGH"]

    if "expected_min_high_findings" in expected:
        # valid_obligation_case — anti-regression lower-bound guard.
        assert report.total_obligations >= expected["expected_min_total_obligations"], (
            f"{expected['fixture']}: allowlist OVER-BROADENED — expected ≥"
            f"{expected['expected_min_total_obligations']} obligations, got "
            f"{report.total_obligations}"
        )
        assert len(high) >= expected["expected_min_high_findings"], (
            f"{expected['fixture']}: allowlist OVER-BROADENED — expected ≥"
            f"{expected['expected_min_high_findings']} HIGH, got {len(high)}"
        )
        assert (
            report.undischarged_count >= expected["expected_min_undischarged_count"]
        ), (
            f"{expected['fixture']}: allowlist OVER-BROADENED — expected ≥"
            f"{expected['expected_min_undischarged_count']} undischarged, got "
            f"{report.undischarged_count}"
        )
        return

    # FP / imperative-override cases — exact counts.
    assert report.total_obligations == expected["expected_total_obligations"], (
        f"{expected['fixture']}: expected {expected['expected_total_obligations']} "
        f"total obligations, got {report.total_obligations}. Findings: "
        f"{[(o.term, o.context) for o in report.obligations]}"
    )
    assert len(high) == expected["expected_high_findings"], (
        f"{expected['fixture']}: expected {expected['expected_high_findings']} HIGH, "
        f"got {len(high)}. Findings: {[(o.term, o.context) for o in high]}"
    )
    assert report.undischarged_count == expected["expected_undischarged_count"], (
        f"{expected['fixture']}: expected {expected['expected_undischarged_count']} "
        f"undischarged, got {report.undischarged_count}"
    )


def dispatch_id_containment(md_path: Path, expected: dict) -> None:
    """Contract #9 — build the registry from ``## spec`` and run the
    ``_roadmap_ids_within_spec`` MERGE_GATE check on ``## roadmap``.
    """
    _run_roadmap_ids_within_spec(md_path, expected)


def dispatch_spec_fidelity(md_path: Path, expected: dict) -> None:
    """Contract #9 / Contract #4 — spec-fidelity class.

    Two shapes share this class:
    * ``phantom_id_*`` — exercises ``_roadmap_ids_within_spec`` (same
      mechanism as id_containment) via the ``verified_component`` chain.
    * ``deviation_unclassified_*`` — exercises ``_no_ambiguous_deviations``.
    The expected.json's ``verified_component`` selects the right component.
    """
    component = expected.get("verified_component", "")
    if "_no_ambiguous_deviations" in component:
        content = md_path.read_text(encoding="utf-8")
        result = _gates._no_ambiguous_deviations(content)
        assert result is expected["expected_check_result_on_fixture"], (
            f"{expected['fixture']}: _no_ambiguous_deviations on the "
            f"{expected['fixture_ambiguous_deviations_value']}-ambiguous fixture "
            f"returned {result!r}, expected "
            f"{expected['expected_check_result_on_fixture']!r} (fail-closed)."
        )
        # Companion oracles — clean report passes; stale ambiguous_count-only
        # report still fails closed (proves the GATE_FIELD_NAMES SoT fix).
        canonical = expected["canonical_field_name"]
        clean_fm = f"---\n{canonical}: 0\n---\nbody\n"
        assert (
            _gates._no_ambiguous_deviations(clean_fm)
            is expected["expected_check_result_if_zero"]
        ), f"{expected['fixture']}: clean {canonical}:0 report should PASS the gate"
        stale_fm = "---\nambiguous_count: 0\n---\nbody\n"
        assert (
            _gates._no_ambiguous_deviations(stale_fm)
            is expected["expected_check_result_if_old_ambiguous_count_field_only"]
        ), (
            f"{expected['fixture']}: a stale ambiguous_count-only report must "
            f"fail closed (canonical field absent), proving the field-name fix."
        )
        return

    # phantom_id_* — _roadmap_ids_within_spec containment check.
    _run_roadmap_ids_within_spec(md_path, expected)


def _run_roadmap_ids_within_spec(md_path: Path, expected: dict) -> None:
    """Shared driver: slice ``## spec`` / ``## roadmap``, build registry +
    sidecar, run the live ``_gates._roadmap_ids_within_spec`` check.
    """
    case_text = md_path.read_text(encoding="utf-8")
    spec_body = _slice_section(case_text, expected.get("spec_section_heading", "spec"))
    roadmap_body = _slice_section(
        case_text, expected.get("roadmap_section_heading", "roadmap")
    )

    tmp = md_path.parent / f".{md_path.stem}.spec.tmp.md"
    sidecar = md_path.parent / f".{md_path.stem}.sidecar.tmp.json"
    try:
        tmp.write_text(spec_body, encoding="utf-8")
        registry = build_id_registry(tmp)

        # Sanity: the registry matches the fixture's expected spec IDs.
        exp_ids = expected["expected_spec_ids"]
        assert sorted(registry.fr_ids) == sorted(exp_ids["fr_ids"]), (
            f"{expected['fixture']}: fr_ids {sorted(registry.fr_ids)} != "
            f"{sorted(exp_ids['fr_ids'])}"
        )
        assert sorted(registry.nfr_ids) == sorted(exp_ids["nfr_ids"]), (
            f"{expected['fixture']}: nfr_ids drift"
        )
        assert sorted(registry.d_ids) == sorted(exp_ids["d_ids"]), (
            f"{expected['fixture']}: d_ids drift"
        )
        if "md_ids" in exp_ids:
            assert sorted(registry.md_ids) == sorted(exp_ids["md_ids"]), (
                f"{expected['fixture']}: md_ids drift"
            )

        sidecar.write_text(
            json.dumps(registry.to_dict(), indent=2, sort_keys=True),
            encoding="utf-8",
        )
        _gates.set_id_registry_sidecar_path(sidecar)
        result = _gates._roadmap_ids_within_spec(roadmap_body)

        expected_type = expected["expected_semantic_check_result_type"]
        if expected_type == "str":
            assert isinstance(result, str), (
                f"{expected['fixture']}: expected failure string (phantom IDs); "
                f"got {result!r}"
            )
            substr = expected["expected_failure_substring"]
            assert substr in result, (
                f"{expected['fixture']}: failure message {result!r} missing "
                f"expected substring {substr!r}"
            )
        else:
            assert result is True, (
                f"{expected['fixture']}: expected PASS (no phantom IDs); got {result!r}"
            )

        # contains() oracle when the fixture pins it.
        if "expected_contains_fr_1" in expected:
            assert registry.contains("FR-1") is expected["expected_contains_fr_1"]
        if "expected_contains_fr_99" in expected:
            assert registry.contains("FR-99") is expected["expected_contains_fr_99"]

        # Load-bearing recurrence assertion for the milestone fixture: the R5 MD
        # family must resolve every M{n}-D{nn} ID distinctly — NONE may collapse
        # into the bare-D phantom set (that collapse IS master:§Recurrence #4).
        if expected.get("expected_milestone_ids_resolve_distinctly"):
            from superclaude.cli.roadmap.id_registry import extract_roadmap_ids

            phantoms = extract_roadmap_ids(roadmap_body) - registry.union_of_known()
            md_in_phantoms = {p for p in phantoms if "-D" in p and p[0] == "M"}
            assert not md_in_phantoms, (
                f"{expected['fixture']}: milestone IDs collapsed into the phantom "
                f"set {sorted(md_in_phantoms)} — master:§Recurrence #4 MD-collapse "
                f"regression (the R5 fix should resolve them distinctly)."
            )
            assert sorted(phantoms) == sorted(
                expected["expected_phantom_violations"]
            ), (
                f"{expected['fixture']}: phantom set {sorted(phantoms)} != oracle "
                f"{sorted(expected['expected_phantom_violations'])}"
            )
    finally:
        _gates.set_id_registry_sidecar_path(None)
        tmp.unlink(missing_ok=True)
        sidecar.unlink(missing_ok=True)


def dispatch_retry_contract(md_path: Path, expected: dict) -> None:
    """Contract #7 — AST-lint the live roadmap source tree for deterministic
    identical-input retries; assert the post-fix oracle (zero violations).
    """
    import ast

    roadmap_dir = _REPO_ROOT / "src" / "superclaude" / "cli" / "roadmap"
    if not roadmap_dir.is_dir():
        pytest.skip(
            f"CI-only source-tree lint: {roadmap_dir} absent "
            "(pipx-installed package, no src/ tree)."
        )

    transient = expected["expected_transient_annotation"]
    steps_seen = 0
    violations: list[str] = []
    for py_file in sorted(roadmap_dir.glob("*.py")):
        source = py_file.read_text(encoding="utf-8")
        src_lines = source.splitlines()
        tree = ast.parse(source)
        for call in ast.walk(tree):
            if not (
                isinstance(call, ast.Call)
                and isinstance(call.func, ast.Name)
                and call.func.id == "Step"
            ):
                continue
            steps_seen += 1
            kwargs = {kw.arg: kw.value for kw in call.keywords if kw.arg}
            retry_node = kwargs.get("retry_limit")
            retry_val = (
                retry_node.value
                if isinstance(retry_node, ast.Constant)
                and isinstance(retry_node.value, int)
                else None
            )
            if retry_val is None or retry_val <= 0:
                continue
            prompt_node = kwargs.get("prompt")
            is_deterministic = (
                isinstance(prompt_node, ast.Constant) and prompt_node.value == ""
            )
            if not is_deterministic:
                continue
            start = call.lineno - 1
            end = getattr(call, "end_lineno", call.lineno)
            span = "\n".join(src_lines[start:end])
            if transient in span:
                continue
            violations.append(f"{py_file.name}:{call.lineno}: deterministic retry")

    assert steps_seen > 0, "Step-detection regression — lint would pass vacuously."
    assert len(violations) == expected["expected_deterministic_retry_violations"], (
        f"{expected['fixture']}: expected "
        f"{expected['expected_deterministic_retry_violations']} deterministic-retry "
        f"violations, got {len(violations)}: {violations}"
    )


def dispatch_dispatch_reachability(md_path: Path, expected: dict) -> None:
    """Contract #2 — run ``assert_step_reachable`` against the LIVE executor.py
    AST (verification_against says "live executor.py, not this .md").

    Post-fix oracle: ``build_certify_step()`` (and ``_run_verify_implementation``)
    have production callers in ``execute_roadmap``, so the dynamic-dispatch shape
    makes the terminal step reachable and the assertion returns ``None``.
    """
    spec_ids = SpecIdRegistry(
        fr_ids=("FR-1",),
        nfr_ids=(),
        sc_ids=(),
        g_ids=(),
        d_ids=(),
        md_ids=(),
        accepted_deviation_ids=(),
        spec_hash="0" * 16,
        spec_path=Path("spec.md"),
    )
    envelope = PipelineEnvelope.empty(
        release_id="recurrence-regression",
        spec_hash="0" * 16,
        spec_ids=spec_ids,
    )
    finding = assert_step_reachable(envelope, _REPO_ROOT)

    # The oracle records ``expected_assert_step_reachable_returns: null`` (JSON
    # null -> Python None): post-fix the terminal step IS reachable via the
    # dynamic dispatch shape, so the assertion returns None / no Finding.
    expected_return = expected.get("expected_assert_step_reachable_returns", None)
    if expected_return is None:
        assert finding is None, (
            f"{expected['fixture']}: assert_step_reachable returned a Finding "
            f"({finding!r}) — certify/verification terminal step is UNREACHABLE "
            f"in the live executor.py (Contract #2 / master:§Flaw 1 regression)."
        )
    else:
        assert finding is not None, (
            f"{expected['fixture']}: expected a Finding but got None"
        )


def dispatch_threshold_registry(md_path: Path, expected: dict) -> None:
    """Contract #8 — extract the pre-fix snippet from the fixture and run the
    live ``arch_lint.scan_file`` against it; assert exactly one ``name-rebind``
    violation on the canonical constant.
    """
    from superclaude.tools.arch_lint import _load_canonical_constants

    text = md_path.read_text(encoding="utf-8")
    pre_fix = _extract_first_fenced_python(text)
    post_fix = _extract_python_block_containing(text, "from superclaude.contracts")
    canonical_names, canonical_bodies = _load_canonical_constants()

    pre_path = md_path.parent / f".{md_path.stem}.prefix.tmp.py"
    post_path = md_path.parent / f".{md_path.stem}.postfix.tmp.py"
    try:
        pre_path.write_text(pre_fix, encoding="utf-8")
        pre_violations = scan_file(pre_path, canonical_names, canonical_bodies)
        rebinds = [
            v
            for v in pre_violations
            if v.kind == expected["pre_fix_expected_violation_kind"]
            and v.name == expected["pre_fix_expected_violation_name"]
        ]
        assert len(rebinds) == expected["pre_fix_expected_violation_count"], (
            f"{expected['fixture']}: expected "
            f"{expected['pre_fix_expected_violation_count']} "
            f"{expected['pre_fix_expected_violation_kind']} violation(s) on "
            f"{expected['pre_fix_expected_violation_name']}, got "
            f"{[(v.kind, v.name) for v in pre_violations]}"
        )

        if post_fix:
            post_path.write_text(post_fix, encoding="utf-8")
            post_violations = scan_file(post_path, canonical_names, canonical_bodies)
            assert (
                len(post_violations) == expected["post_fix_expected_violation_count"]
            ), (
                f"{expected['fixture']}: post-fix (import) snippet should emit "
                f"{expected['post_fix_expected_violation_count']} violations, got "
                f"{[(v.kind, v.name) for v in post_violations]}"
            )
    finally:
        pre_path.unlink(missing_ok=True)
        post_path.unlink(missing_ok=True)


def dispatch_fragility_stub(md_path: Path, expected: dict) -> None:
    """Contract #5 — two assertions:

    1. The pre-fix snippet IS matched by the Contract #5 fragility-stub regex
       (proves the regex actually catches the documented stub shape).
    2. The LIVE ``src/superclaude/cli`` tree contains ZERO fragility-commented
       ``return True`` stubs (R1.6 deleted them).
    """
    snippet = expected["pre_fix_snippet"]
    assert (
        bool(_FRAGILITY_STUB_RE.search(snippet))
        is expected["pre_fix_expected_regex_match"]
    ), (
        f"{expected['fixture']}: the Contract #5 fragility-stub regex did not "
        f"match the documented pre-fix stub {snippet!r} — detection regression."
    )

    cli_root = _cli_root()
    if not cli_root.is_dir():
        pytest.skip(
            f"CI-only source-tree scan: {cli_root} absent (pipx-installed package)."
        )
    offenders: list[str] = []
    for py_file in sorted(cli_root.rglob("*.py")):
        body = py_file.read_text(encoding="utf-8")
        for m in _FRAGILITY_STUB_RE.finditer(body):
            line_no = body[: m.start()].count("\n") + 1
            offenders.append(f"{py_file}:{line_no}: {m.group().strip()!r}")
    assert len(offenders) == expected["post_fix_expected_cli_tree_offender_count"], (
        f"{expected['fixture']}: expected "
        f"{expected['post_fix_expected_cli_tree_offender_count']} fragility stubs in "
        f"src/superclaude/cli, found {len(offenders)}:\n" + "\n".join(offenders)
    )


def dispatch_verification(md_path: Path, expected: dict) -> None:
    """Contract #4 — run ``_spec_fidelity_validation_complete_true`` on the
    fixture; assert it fails closed on ``validation_complete:false``.
    """
    content = md_path.read_text(encoding="utf-8")
    result = _gates._spec_fidelity_validation_complete_true(content)
    assert result is expected["expected_check_result_on_fixture"], (
        f"{expected['fixture']}: _spec_fidelity_validation_complete_true returned "
        f"{result!r} on the validation_complete:"
        f"{expected['fixture_validation_complete_field']} fixture, expected "
        f"{expected['expected_check_result_on_fixture']!r} (fail-closed)."
    )
    # Flip-true oracle: a genuinely-passing report returns True.
    flipped = content.replace("validation_complete: false", "validation_complete: true")
    assert (
        _gates._spec_fidelity_validation_complete_true(flipped)
        is expected["expected_check_result_if_flipped_true"]
    ), (
        f"{expected['fixture']}: flipping validation_complete:true should PASS the "
        f"gate (load-bearing PASS/FAIL bit)."
    )


# ---------------------------------------------------------------------------
# Snippet extraction helpers (threshold_registry fixture parses fenced code)
# ---------------------------------------------------------------------------


def _iter_fenced_python(text: str) -> list[str]:
    blocks: list[str] = []
    lines = text.splitlines()
    inside = False
    buf: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not inside and stripped.startswith("```python"):
            inside = True
            buf = []
            continue
        if inside and stripped.startswith("```"):
            inside = False
            blocks.append("\n".join(buf) + "\n")
            continue
        if inside:
            buf.append(line)
    return blocks


def _extract_first_fenced_python(text: str) -> str:
    blocks = _iter_fenced_python(text)
    assert blocks, "fixture has no ```python fenced block (pre-fix snippet)"
    return blocks[0]


def _extract_python_block_containing(text: str, needle: str) -> str:
    for block in _iter_fenced_python(text):
        if needle in block:
            return block
    return ""


# ---------------------------------------------------------------------------
# (1) Extensible dispatch registry
# ---------------------------------------------------------------------------

FAILURE_CLASS_DISPATCH: dict[str, Callable[[Path, dict], None]] = {
    "anti_instinct": dispatch_anti_instinct,
    "id_containment": dispatch_id_containment,
    "retry_contract": dispatch_retry_contract,
    "spec_fidelity": dispatch_spec_fidelity,
    "dispatch_reachability": dispatch_dispatch_reachability,
    "threshold_registry": dispatch_threshold_registry,
    "fragility_stub": dispatch_fragility_stub,
    "verification": dispatch_verification,
}

# Classes whose every fixture is a documented DEFER stub and which have no
# runtime component to dispatch. Each maps to a recorded skip reason. A class
# may be absent from FAILURE_CLASS_DISPATCH only if it is here OR every fixture
# in it carries ``deferred:true``. ``deferred/`` is the catch-all stub area for
# runtime-resource / out-of-scope / meta rows (#10, #16, #17, #20, #21);
# ``merge_completeness`` (#15) has no incorporation-completeness component
# post-R1 (verified Step 13.2). Both contain only ``deferred:true`` fixtures, so
# they are skipped per-fixture via the expected.json reason; they are listed
# here as well so the enumeration invariant treats a (future) reason-less
# fixture in these dirs as an explicit skip rather than an implicit drop.
UNDISPATCHED_CLASSES: dict[str, str] = {
    "deferred": (
        "Catch-all stub area for non-scanner-testable RECURRENT rows "
        "(#10 generator/validator asymmetry meta-pattern, #16 telemetry "
        "text-regex, #17 context-window/OOM runtime-resource, #20 truncation, "
        "#21 sprint-executor out-of-scope). No deterministic roadmap-pipeline "
        "component consumes these fixtures; each carries an auditable "
        "deferred:true reason (seeding-map §Deferral)."
    ),
    "merge_completeness": (
        "Recurrence #15 (adversarial findings dropped at merge): no "
        "incorporation-completeness component exists post-R1 — MERGE_GATE "
        "semantic_checks and _validate_merge_completeness check structural "
        "completeness only, not findings reconciliation (verified Step 13.2). "
        "Retained as an auditable deferred:true stub."
    ),
}


# ---------------------------------------------------------------------------
# (2) Invariant tests
# ---------------------------------------------------------------------------


def test_every_fixture_enumerated_or_skipped():
    """No-silent-drop master invariant.

    Every fixture under ``tests/roadmap/fixtures/recurrence/*/*.md`` must be
    EITHER (a) ``deferred:true`` in its expected.json, OR (b) in a dispatched
    failure_class, OR (c) in ``UNDISPATCHED_CLASSES``. A fixture that is none
    of these is an implicit drop and FAILS here. Also asserts every dispatched
    class has at least one real (non-deferred) fixture.
    """
    assert _FIXTURES, "No recurrence fixtures discovered — corpus glob regression."

    dropped: list[str] = []
    real_per_class: dict[str, int] = {k: 0 for k in FAILURE_CLASS_DISPATCH}

    for failure_class, case, md_path, expected_path in _FIXTURES:
        ident = f"{failure_class}/{case}"
        assert md_path.is_file(), f"{ident}: fixture .md missing on disk"
        assert expected_path.is_file(), (
            f"{ident}: expected.json missing — every fixture needs an oracle "
            f"or a deferred:true stub (no bare .md drops)."
        )
        expected = _load_expected(expected_path)

        if expected.get("deferred") is True:
            assert (expected.get("reason") or "").strip(), (
                f"{ident}: deferred:true with no reason — deferrals must be "
                f"auditable (seeding-map §Provenance guarantee)."
            )
            continue
        if failure_class in FAILURE_CLASS_DISPATCH:
            real_per_class[failure_class] += 1
            continue
        if failure_class in UNDISPATCHED_CLASSES:
            continue
        dropped.append(ident)

    assert not dropped, (
        "Implicit fixture drop(s) — neither dispatched, deferred, nor in "
        "UNDISPATCHED_CLASSES:\n" + "\n".join(dropped)
    )

    empty = [cls for cls, n in real_per_class.items() if n == 0]
    assert not empty, (
        "Dispatched class(es) with ZERO real (non-deferred) fixtures — the "
        "dispatch callable would never run, a vacuous-pass regression: "
        f"{empty}"
    )


@pytest.mark.parametrize(
    ("failure_class", "case", "md_path", "expected_path"),
    _FIXTURES,
    ids=[f"{fc}/{case}" for fc, case, _md, _ej in _FIXTURES],
)
def test_dispatched_fixture_matches_expected(
    failure_class, case, md_path, expected_path
):
    """Run each fixture's real component (or skip it auditably).

    deferred:true → ``pytest.skip(reason)``. Dispatched class → run the real
    component and assert the oracle. UNDISPATCHED_CLASSES → ``pytest.skip``.
    Anything else → ``pytest.fail`` (implicit drop).
    """
    expected = _load_expected(expected_path)
    ident = f"{failure_class}/{case}"

    assert expected, f"{ident}: expected.json missing or empty"

    if expected.get("deferred") is True:
        pytest.skip(f"deferred: {expected.get('reason', '(no reason recorded)')}")

    if failure_class in FAILURE_CLASS_DISPATCH:
        FAILURE_CLASS_DISPATCH[failure_class](md_path, expected)
        return

    if failure_class in UNDISPATCHED_CLASSES:
        pytest.skip(f"undispatched class: {UNDISPATCHED_CLASSES[failure_class]}")

    pytest.fail(f"implicit drop: {ident} (no dispatch, no deferral, no skip registry)")
