"""Code-graph predicates for ``GateCriteria.code_assertions`` (R1.3 / §MVR §2).

This module is the roadmap-side companion to
``cli/pipeline/models.py:CodeAssertion``. The pipeline substrate declares
the slot; this module supplies the first concrete predicate plus its AST
helper, and is the natural home for further roadmap-specific assertions
introduced by R1.5 (``verify-implementation``).

Design source of truth:
``.dev/tasks/to-do/TASK-RF-20260531-042405/phase-outputs/plans/r1-3-codeassertion-design.md``

Master:§Flaw 1 invariant — the certify gate fails fast if
``build_certify_step()`` is not reachable from the production dispatch.
``assert_step_reachable`` operationalises BUILD-REQUEST §MVR §2 verbatim
("CodeAssertion guarantees no future step ships unwired").
"""

from __future__ import annotations

import ast
from pathlib import Path

from superclaude.cli.roadmap.envelope import PipelineEnvelope
from superclaude.cli.roadmap.models import Finding


def assert_step_reachable(
    envelope: PipelineEnvelope,
    repo_root: Path,
) -> Finding | None:
    """Verify ``certify`` step is reachable from a production dispatch path.

    Contract #2 requires the certify step to be reachable from a *production
    entry point*, not merely defined. The roadmap pipeline admits two
    legitimate dispatch shapes for the terminal certify step:

    1. **Static** — ``certify`` appears as a ``Step(id="certify", ...)``
       literal inside ``_build_steps`` (the primary dispatch map).
    2. **Dynamic** — ``build_certify_step()`` is *called* inside
       ``execute_roadmap`` (the pipeline driver), constructing the step
       after ``remediate`` passes. This is the step-count-budget-safe
       wiring chosen in design doc §7.3 (option a): it keeps
       ``_build_steps`` / ``ALL_GATES`` at 14 while still guaranteeing the
       step ships wired.

    The assertion PASSES if EITHER shape is present. It FAILS only when
    ``certify`` is unreachable by both — i.e. the master:§Flaw 1 state
    where ``build_certify_step`` exists but no production caller invokes
    it (the pre-R1.3 condition).

    The walker is intentionally conservative: only ``Constant`` string
    literals / ``JoinedStr`` static prefixes in ``Step(id=...)`` keywords
    are counted for shape 1, and only a direct ``build_certify_step(...)``
    ``Call`` within ``execute_roadmap``'s body satisfies shape 2.
    ``Step(id=...)`` calls *outside* ``_build_steps`` (e.g. the one inside
    ``build_certify_step`` itself) are NOT counted for shape 1 — that is
    the load-bearing semantic distinguishing "step defined" from "step
    reachable".

    Parameters
    ----------
    envelope:
        Current ``PipelineEnvelope``. Currently unused; reserved for
        future extensions that gate on envelope state.
    repo_root:
        Repository root used to locate ``src/superclaude/cli/roadmap/
        executor.py``.

    Returns
    -------
    Finding | None
        ``None`` on PASS (certify reachable via shape 1 or shape 2).
        A HIGH-severity ``Finding`` on FAIL referencing
        master:§Flaw 1 / Contract #2.
    """
    del envelope  # reserved; not consulted by this assertion
    executor_path = (
        repo_root / "src" / "superclaude" / "cli" / "roadmap" / "executor.py"
    )
    if not executor_path.is_file():
        return Finding(
            id="CA-DISPATCH-001",
            severity="HIGH",
            dimension="dispatch-reachability",
            description=(
                f"assert_step_reachable: executor.py not found at "
                f"{executor_path} (repo_root resolution failed)."
            ),
            location=str(executor_path),
            evidence="",
            fix_guidance="Verify repo_root passed to gate_passed is correct.",
        )

    tree = ast.parse(executor_path.read_text(encoding="utf-8"))
    step_ids = _extract_step_ids_from_build_steps(tree)
    static_reachable = "certify" in step_ids
    dynamic_reachable = _build_certify_step_has_production_caller(tree)

    if not (static_reachable or dynamic_reachable):
        return Finding(
            id="CA-DISPATCH-002",
            severity="HIGH",
            dimension="dispatch-reachability",
            description=(
                "CERTIFY_GATE dispatch-reachability: step 'certify' is not "
                "reachable from any production dispatch (Contract #2 / "
                f"master:§Flaw 1). _build_steps step ids: {sorted(step_ids)!r}; "
                "build_certify_step() has no production caller in executor.py. "
                "build_certify_step() defines the step but only a test invokes "
                "it."
            ),
            location=f"{executor_path}:_build_steps|build_certify_step-callers",
            evidence="",
            fix_guidance=(
                "Wire build_certify_step() into the production dispatch "
                "path: either add a Step(id='certify', ...) to _build_steps, "
                "or call build_certify_step() from execute_roadmap (directly "
                "or via a helper it invokes) post-execute_pipeline (design "
                "doc §7.3 option a), then re-run the gate."
            ),
        )

    return None


def assert_envelope_artifacts_present(
    envelope: PipelineEnvelope,
    repo_root: Path,
) -> Finding | None:
    """Verify every artifact recorded in the envelope exists on disk.

    Envelope-coverage analogue of :func:`assert_step_reachable`: where the
    dispatch assertion guards the *code graph*, this one guards the
    *artifact graph*. The §MVR §1 substrate inversion makes the envelope
    the source of truth for cross-step state; a dangling ``ArtifactRef``
    (recorded in ``envelope.artifacts`` but missing on disk) means the
    envelope and the filesystem have diverged — exactly the master:§Flaw 3
    failure mode the envelope exists to prevent.

    For each ``(step_id, ArtifactRef)`` in ``envelope.artifacts`` whose
    ``path`` is relative, it is resolved against ``repo_root``; absolute
    paths are checked as-is. The first missing artifact yields a HIGH
    ``Finding``; an empty ``artifacts`` map (no steps recorded yet) is a
    PASS — coverage is vacuously satisfied.

    Parameters
    ----------
    envelope:
        The pipeline envelope whose recorded artifacts are checked.
    repo_root:
        Repository root used to resolve relative artifact paths.

    Returns
    -------
    Finding | None
        ``None`` when every recorded artifact exists.
        A HIGH-severity ``Finding`` naming the first missing artifact.
    """
    artifacts = getattr(envelope, "artifacts", None) or {}
    for step_id, ref in artifacts.items():
        ref_path = getattr(ref, "path", None)
        if ref_path is None:
            continue
        resolved = ref_path if ref_path.is_absolute() else (repo_root / ref_path)
        if not resolved.exists():
            return Finding(
                id="CA-ENVELOPE-001",
                severity="HIGH",
                dimension="envelope-coverage",
                description=(
                    "Envelope artifact coverage: artifact for step "
                    f"{step_id!r} recorded in envelope.artifacts but missing "
                    f"on disk at {resolved} (master:§Flaw 3 — envelope/"
                    "filesystem divergence)."
                ),
                location=str(resolved),
                evidence="",
                fix_guidance=(
                    "Ensure the step's post-extractor records the artifact "
                    "only after the artifact is written, or re-run the step "
                    "to regenerate the missing artifact."
                ),
            )
    return None


def assert_convergence_passed(
    envelope: PipelineEnvelope,
    repo_root: Path,
) -> Finding | None:
    """Verify the envelope's terminal convergence verdict is a PASS.

    Convergence-aware companion to the spec-fidelity gate (R1.6 / Contract #4
    / master:§Flaw 4). When the roadmap runs in convergence mode (the
    production default), spec-fidelity is decided by the convergence engine
    (``execute_fidelity_with_convergence``) and the terminal verdict is
    recorded on ``envelope.convergence`` (a :class:`ConvergenceResult`).
    Before R1.6 the spec-fidelity ``Step`` carried ``gate=None`` under
    convergence, so no ``GateCriteria``-level contract asserted that
    convergence actually reached a passing terminal state -- the fail-open
    seam this assertion closes by gating on the envelope SoT directly.

    This is a **runtime-safe** assertion (``ci_only=False``): it reads
    ``envelope.convergence`` and never touches the source tree, so it is
    dispatched in the live gate path whenever a caller plumbs the envelope.
    The live ``execute_pipeline`` path that omits the envelope falls through
    the documented envelope-None shim; in that path the terminal report's
    severity frontmatter (``high_severity_count`` / ``validation_complete`` /
    ``tasklist_ready``, written by ``_write_convergence_report``) is validated
    by the gate's ``semantic_checks`` tier, so a convergence FAIL cannot
    silently pass.

    Returns
    -------
    Finding | None
        ``None`` (PASS) when ``envelope.convergence`` is ``None`` (convergence
        did not run -- disabled or not yet reached, a vacuous pass) or when the
        recorded verdict is ``passed=True``. A HIGH-severity ``Finding`` when
        convergence ran and did not pass.
    """
    del repo_root  # not consulted; the verdict lives on the envelope
    convergence = getattr(envelope, "convergence", None)
    if convergence is None:
        return None
    if getattr(convergence, "passed", False):
        return None
    return Finding(
        id="CA-CONVERGENCE-001",
        severity="HIGH",
        dimension="spec-fidelity-convergence",
        description=(
            "Spec-fidelity convergence did not pass: envelope.convergence."
            "passed is False (halt_reason="
            f"{getattr(convergence, 'halt_reason', None)!r}). Contract #4 / "
            "master:§Flaw 4 -- the spec-fidelity step must not pass while the "
            "convergence engine reports an unresolved terminal state."
        ),
        location="envelope.convergence",
        evidence="",
        fix_guidance=(
            "Inspect the convergence halt_reason; resolve the outstanding HIGH "
            "findings (or record them as accepted deviations) so convergence "
            "reaches a passing terminal state, then re-run."
        ),
    )


def _build_certify_step_has_production_caller(tree: ast.Module) -> bool:
    """Return True if ``build_certify_step(...)`` is called within executor.py.

    Walks the entire ``executor.py`` module AST for a ``Call`` whose
    ``.func`` is ``Name("build_certify_step")``, excluding any call that
    sits inside ``build_certify_step``'s own ``FunctionDef`` (a self-call
    would not constitute external wiring). Because ``executor.py`` is the
    production pipeline-driver module, any such call IS a production caller.

    This is the dynamic-dispatch shape for the terminal certify step
    (design doc §7.3 option a): ``build_certify_step()`` is invoked by
    ``execute_roadmap`` (directly or via the ``_run_certify_after_remediate``
    helper it calls), keeping ``_build_steps`` at the step-count budget
    while guaranteeing the step is reachable. The master:§Flaw 1 condition
    is precisely "build_certify_step has ZERO production callers (only a
    test in tests/ invokes it)"; this check parses only ``executor.py`` so
    a test-file call never satisfies it.
    """
    # Identify the line span of build_certify_step's own definition so we
    # can exclude self-referential calls (defensive — there are none today).
    def_node: ast.FunctionDef | None = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "build_certify_step":
            def_node = node
            break

    def_lineno = def_node.lineno if def_node is not None else -1
    def_end = getattr(def_node, "end_lineno", def_lineno) if def_node else -1

    for node in ast.walk(tree):
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "build_certify_step"
        ):
            continue
        call_line = getattr(node, "lineno", -1)
        # Skip calls inside build_certify_step's own body (self-reference).
        if def_node is not None and def_lineno <= call_line <= def_end:
            continue
        return True
    return False


def _extract_step_ids_from_build_steps(tree: ast.Module) -> set[str]:
    """Return literal ``id=`` values from ``Step(...)`` calls inside ``_build_steps``.

    Two-pass walk:

    1. Locate the ``FunctionDef`` named ``_build_steps``.
    2. Walk its body; collect every ``Call`` whose ``.func`` is
       ``Name("Step")`` and whose keyword ``id=`` is a ``Constant`` str
       or a ``JoinedStr`` whose leading components are static constants
       (the literal prefix is recorded).

    Dynamic ids without a static prefix (``id=some_var``) are skipped --
    the caller cares only about literal-id reachability, and dynamic
    ids would produce noisy false matches if normalized further.
    """
    ids: set[str] = set()
    for node in ast.walk(tree):
        if not (isinstance(node, ast.FunctionDef) and node.name == "_build_steps"):
            continue
        for inner in ast.walk(node):
            if not (
                isinstance(inner, ast.Call)
                and isinstance(inner.func, ast.Name)
                and inner.func.id == "Step"
            ):
                continue
            for kw in inner.keywords:
                if kw.arg != "id":
                    continue
                value = kw.value
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    ids.add(value.value)
                elif isinstance(value, ast.JoinedStr):
                    prefix_parts: list[str] = []
                    for part in value.values:
                        if isinstance(part, ast.Constant) and isinstance(
                            part.value, str
                        ):
                            prefix_parts.append(part.value)
                        else:
                            break
                    if prefix_parts:
                        ids.add("".join(prefix_parts))
    return ids
