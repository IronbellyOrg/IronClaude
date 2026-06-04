"""R1.5 ``verify-implementation`` terminal-step substrate (§MVR §4).

This module supplies the fail-closed, ``CodeAssertion``-only terminal gate
that **replaces** the legacy ``wiring-verification`` shadow step. It is the
roadmap-side companion to ``code_assertions.assert_step_reachable`` (R1.3):
where that assertion guards the *code graph* (a step ships wired), this one
guards the *requirement evidence chain* — every FR the run extracted from
the spec must resolve against the run's **own emitted artifacts** or an
accepted deviation.

Design source of truth:
``.dev/tasks/to-do/TASK-RF-20260531-042405/phase-outputs/plans/
r1-5-verify-implementation-design.md``

Master:§Flaw 1 invariant — a green pipeline must not certify a roadmap that
silently dropped a functional requirement. ``assert_all_frs_resolved`` is
fail-closed: an empty FR set or any unresolved FR yields a HIGH ``Finding``
(Contract #4 — no silent PASS on empty / wrong-target inputs).

**Runtime substrate (LOAD-BEARING, design §5).** FR resolution is checked
against the run's emitted tasklist/roadmap artifacts (recorded in
``envelope.artifacts``) plus the accepted-deviation channels — **never** the
pipeline's own ``src/`` source tree. Source-tree / ``importlib`` /
``fidelity_checker._scan_codebase`` resolution is CI-only (Step 10.3 test
scaffold), never the live runtime gate.
"""

from __future__ import annotations

import re
from pathlib import Path

from superclaude.cli.pipeline.models import GateCriteria, Step
from superclaude.cli.roadmap.envelope import PipelineEnvelope
from superclaude.cli.roadmap.models import Finding


def _fr_token_in_text(fr_id: str, text: str) -> bool:
    """Return True iff ``fr_id`` appears in ``text`` as a whole token.

    Token-boundary match so ``FR-1`` does not spuriously match inside
    ``FR-12`` (or ``XFR-1``). The boundary class ``[\\w-]`` rejects an
    adjacent word char or dash on either side — the canonical requirement-ID
    shape (``FR-001``) is dash-internal, so the negative look-around guards
    against both the longer-id and embedded-id false positives.
    """
    pattern = rf"(?<![\w-]){re.escape(fr_id)}(?![\w-])"
    return re.search(pattern, text) is not None


def assert_all_frs_resolved(
    envelope: PipelineEnvelope,
    repo_path: Path | None = None,
) -> Finding | None:
    """Verify every FR resolves against the run's own emitted artifacts.

    For each ``fr_id`` in ``envelope.spec_ids.fr_ids`` (the dataclass
    **accessor** — never ``envelope.spec_ids[FR]``, which raises
    ``TypeError``), the FR is **resolved** iff at least one of (design §5.1):

    (a) the FR id appears as a whole token in one of the run's emitted
        artifacts (``envelope.artifacts`` — the tasklist/roadmap markdown
        this run produced), OR
    (b) the FR id is in ``envelope.spec_ids.accepted_deviation_ids``, OR
    (c) the FR id matches an ``envelope.accepted_deviations`` record's ``id``.

    Fail-closed semantics (Contract #4, design §6):

    - **Empty ``fr_ids`` → HIGH ``Finding``** (NOT a silent PASS). This is the
      deliberate inverse of ``assert_envelope_artifacts_present``'s
      empty-map=PASS precedent: an FR token set is a *consumed input* the gate
      emits PASS over, so ``len(fr_ids) > 0`` is the Contract #4 precondition.
    - Any unresolved FR → HIGH ``Finding`` (all unmatched FRs aggregated into
      one Finding's evidence). There is **no fail-open ``found=True`` default**.

    Parameters
    ----------
    envelope:
        The live ``PipelineEnvelope`` for this run. Its ``spec_ids.fr_ids``,
        ``artifacts``, ``spec_ids.accepted_deviation_ids`` and
        ``accepted_deviations`` are the *only* substrate consulted.
    repo_path:
        Accepted for signature-parity with ``assert_step_reachable`` and the
        ``gate_passed`` dispatch contract. **Not used to resolve FRs against
        the source tree** (design §4.1 / §5.2). It is consulted *only* to
        normalise a relative artifact path recorded in the envelope (path
        normalisation, not source-tree scanning).

    Returns
    -------
    Finding | None
        ``None`` when every FR resolves (PASS). A HIGH-severity ``Finding``
        otherwise (FAIL): empty ``fr_ids``, or one naming the unresolved FRs.
    """
    fr_ids = tuple(envelope.spec_ids.fr_ids)  # ACCESSOR — never subscript.

    # Contract #4 empty-input guard: empty fr_ids is a FAIL, not a silent PASS.
    if not fr_ids:
        return Finding(
            id="CA-VERIFY-IMPL-000",
            severity="HIGH",
            dimension="fr-resolution",
            description=(
                "verify-implementation: envelope.spec_ids.fr_ids is empty — the "
                "run never extracted any functional requirements to verify. "
                "Contract #4 forbids a silent PASS on an empty FR token set "
                "(master:§Recurrence #3 silent-PASS-on-empty-input)."
            ),
            location="envelope.spec_ids.fr_ids",
            evidence="fr_ids == ()",
            fix_guidance=(
                "Confirm the extract step populated the spec-id registry. An "
                "empty FR set after extraction indicates the spec parser found "
                "no FR-family identifiers, or the envelope was not initialised "
                "from build_id_registry()."
            ),
        )

    # Accepted-deviation channels (b) + (c): ID-only tuple ∪ full records.
    accepted_ids: set[str] = set(envelope.spec_ids.accepted_deviation_ids)
    accepted_ids.update(dev.id for dev in envelope.accepted_deviations)

    # Channel (a) substrate: the run's OWN emitted artifacts (NOT src/).
    artifact_texts: list[str] = []
    artifacts = getattr(envelope, "artifacts", None) or {}
    for ref in artifacts.values():
        ref_path = getattr(ref, "path", None)
        if ref_path is None:
            continue
        # Path normalisation ONLY (not source-tree resolution): a relative
        # artifact path is resolved against repo_path when provided.
        resolved = ref_path
        if not ref_path.is_absolute() and repo_path is not None:
            resolved = repo_path / ref_path
        try:
            artifact_texts.append(resolved.read_text(encoding="utf-8"))
        except OSError:
            # A missing/unreadable artifact contributes no resolution
            # evidence. It does NOT fail-open — an FR resolvable only via a
            # missing artifact stays unresolved (fail-closed).
            continue

    unresolved: list[str] = []
    for fr_id in fr_ids:
        if fr_id in accepted_ids:
            continue
        if any(_fr_token_in_text(fr_id, text) for text in artifact_texts):
            continue
        unresolved.append(fr_id)

    if unresolved:
        return Finding(
            id="CA-VERIFY-IMPL-001",
            severity="HIGH",
            dimension="fr-resolution",
            description=(
                "verify-implementation: "
                f"{len(unresolved)} of {len(fr_ids)} functional requirement(s) "
                "did not resolve against the run's own emitted artifacts or any "
                "accepted deviation (Contract #2 + #4 / master:§Flaw 1 evidence "
                f"chain). Unresolved: {', '.join(sorted(unresolved))}."
            ),
            location="envelope.artifacts | envelope.accepted_deviations",
            evidence=(
                f"unresolved_frs={sorted(unresolved)!r}; "
                f"artifacts_scanned={sorted(artifacts.keys())!r}; "
                f"accepted_deviation_ids={sorted(accepted_ids)!r}"
            ),
            fix_guidance=(
                "Each FR must appear in the run's emitted tasklist/roadmap "
                "artifact (carried through merge), or be recorded as an "
                "accepted deviation. An unresolved FR means the requirement was "
                "extracted from the spec but dropped from the plan — re-run the "
                "merge/spec-fidelity steps, or accept the deviation explicitly."
            ),
        )

    return None


# ---------------------------------------------------------------------------
# Gate definition is owned by gates.py (the pure-data gate registry); the
# Step builder lives here next to its assertion. gates.py imports
# ``assert_all_frs_resolved`` from this module and constructs
# ``VERIFY_IMPLEMENTATION_GATE``.
# ---------------------------------------------------------------------------


def build_verify_implementation_step(
    config: object,
    gate: GateCriteria | None = None,
) -> Step:
    """Construct the terminal ``verify-implementation`` Step.

    The step is dispatched dynamically after ``certify`` (design §2), mirroring
    the ``build_certify_step`` pattern. Its gate is the
    ``CodeAssertion``-only ``VERIFY_IMPLEMENTATION_GATE``; the gate is passed
    in (rather than imported) to keep this module free of a gates.py import
    cycle — ``gates.py`` already imports :func:`assert_all_frs_resolved` here.

    The output file is a small machine-written report (``verify-implementation
    .md``). It exists only to satisfy the STRICT-tier ``gate_passed``
    file-existence precondition; the gate verdict is owned entirely by the
    ``all_frs_resolved`` code assertion, NOT by the file's content.

    Parameters
    ----------
    config:
        A ``RoadmapConfig`` exposing ``output_dir``.
    gate:
        The ``VERIFY_IMPLEMENTATION_GATE`` (injected by the executor). When
        ``None`` the caller is responsible for setting the gate; the builder
        does not import gates.py to avoid an import cycle.
    """
    out = Path(config.output_dir)
    return Step(
        id="verify-implementation",
        prompt="",  # code-assertion-only step; no LLM invocation
        output_file=out / "verify-implementation.md",
        gate=gate,
        timeout_seconds=60,
        inputs=[out / "roadmap.md"],
        retry_limit=0,
    )
