"""Swarm CLI commands -- concrete subcommand implementations.

This module hosts the real Click subcommands that replace the
``__init__.py`` placeholders one at a time as the Phase 2 / Phase 3
tasks land. The ``swarm_group`` itself remains in
``cli/swarm/__init__.py`` (divergence from sprint, documented there);
this file only declares the per-subcommand callables and lets
``__init__.py`` register them with ``swarm_group.add_command(...)`` so
the import order stays acyclic:

    ``__init__.py`` -> ``commands.py`` (one-way).

Currently implemented:

    * ``validate_cmd`` -- FR-007 / T02.19. Schema-checks a JobSpec JSON
      file against the DM-001 schema (``cli/swarm/schema.py``). Exits 0
      on a clean spec; exits non-zero with structured per-rule
      diagnostics on stderr otherwise. Supports a future-proofing
      ``--strict`` flag (current behavior identical -- the schema
      module is already strict; the flag is reserved for upcoming
      rule extensions that will gate on it).
    * ``validate_lenses_cmd`` -- FR-008 / T02.20. Runs the COMP-023
      lens validator (``cli/swarm/lenses/_validate.py::validate_all``)
      over the bundled :data:`LENSES` registry. Exits 0 when every
      non-custom entry passes its five assertions; exits non-zero with
      structured per-entry diagnostics on stderr otherwise. The
      ``--warning-mode`` flag flips the failure exit code to 0 (still
      printing warnings) for the OQ-010 warn-mode branch (pre-commit
      hooks and similar non-blocking callers).
"""

from __future__ import annotations

import json
import re
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Optional

import click

from superclaude.cli.swarm.lenses import LENS_NAMES, LENSES
from superclaude.cli.swarm.lenses._validate import (
    LensValidationFailure,
    validate_all,
)
from superclaude.cli.swarm.models import (
    JobSpec,
    LensEntry,
    SwarmState,
    SwarmStateValue,
    WorkerResult,
)
from superclaude.cli.swarm.schema import (
    CURRENT_SPEC_VERSION,
    SchemaValidationFailure,
    validate,
)

__all__ = [
    "attach_cmd",
    "auto_inject_guard_option",
    "discover_succeeded_slots",
    "kill_cmd",
    "logs_cmd",
    "run_cmd",
    "scaffold_cmd",
    "status_cmd",
    "validate_cmd",
    "validate_lenses_cmd",
]


# ---------------------------------------------------------------------------
# T07.04 / FR-002 -- ``swarm status`` subcommand state-file constant.
#
# The state filename is fixed by COMP-011 / DM-014; defining it as a
# module-level constant here (rather than importing from ``state.py``)
# keeps ``status_cmd`` lazy-import-light and lets the test suite assert
# on the named value without pulling in the full state module.
# ---------------------------------------------------------------------------
SWARM_STATE_FILENAME: str = ".swarm-state.json"
RESULT_CONTRACT_FILENAME: str = "return-contract.yaml"
TERMINAL_STATE_VALUE: str = "terminal"

# T07.05 / FR-003 -- ``swarm logs`` subcommand log-file constants.
#
# The dual-format Logger (COMP-012 / T03.04) writes its JSONL canonical
# surface and Markdown human-readable surface to ``execution-log.jsonl``
# and ``execution-log.md`` siblings of ``manifest.json`` inside the
# job's ``--output`` directory (see ``run_cmd``'s Logger instantiation).
# Defining the filenames as module-level constants here -- rather than
# importing from ``logging_.py`` -- keeps ``logs_cmd`` lazy-import-light
# and lets the test suite assert on the named values without pulling in
# the full logger module.
EXECUTION_LOG_JSONL_FILENAME: str = "execution-log.jsonl"
EXECUTION_LOG_MD_FILENAME: str = "execution-log.md"

# T07.08 / FR-005 -- ``swarm kill`` done-sentinel constants.
#
# DM-017 fixes ``done.json`` as the terminal marker filename. The kill
# path writes a sentinel carrying ``terminal_status="killed"`` -- a
# value that is intentionally NOT in :data:`models.ResultStatus`
# (locked to ``success`` / ``partial`` / ``failed`` by T01.25). A kill
# is operator-initiated termination, not an IMM-5 reduction outcome,
# so the kill writer bypasses the :class:`DoneSentinel` dataclass and
# emits the JSON shape directly. The dataclass docstring still
# describes the per-DM-017 field set; this constant simply names the
# additional terminal value the M7 kill flow needs.
DONE_SENTINEL_FILENAME: str = "done.json"
KILLED_TERMINAL_STATUS: str = "killed"


# ---------------------------------------------------------------------------
# T02.22 / FR-024 -- reusable ``--auto-inject-guard`` Click option.
#
# The option is defined as a module-level callable decorator so any
# future ``swarm`` subcommand that consumes ``--custom-prompt-dir``
# (notably the M3-M4 ``run`` command, currently a T01.08 placeholder)
# can attach it without duplicating the option definition. Defining the
# decorator here -- rather than inline on a specific subcommand -- keeps
# the operator-facing help text single-sourced and makes the flag
# discoverable from one location when the ``run`` command lands.
#
# Default ``False``: the absent-flag path preserves the full §11.5
# substring enforcement on the custom-prompt-dir reader. Setting the
# flag opts the caller into the
# :func:`preflight.read_custom_prompt_dir` backward-compat path that
# prepends :data:`schema.CANONICAL_INJECTION_GUARD_SENTENCE` to
# ``system.txt`` before the substring check fires.
#
# Subcommand wiring pattern::
#
#     @swarm_group.command("run")
#     @auto_inject_guard_option
#     def swarm_run(..., auto_inject_guard: bool) -> None:
#         system, user, meta = read_custom_prompt_dir(
#             custom_prompt_dir,
#             required_substring=spec.target.injection_guard.required_substring,
#             auto_inject_guard=auto_inject_guard,
#         )
#         ...
#
# The Click parameter name is ``auto_inject_guard`` so the bound
# subcommand keyword argument lines up byte-identically with the
# :func:`preflight.read_custom_prompt_dir` keyword, removing any
# rename hazard at the call site.
# ---------------------------------------------------------------------------


auto_inject_guard_option = click.option(
    "--auto-inject-guard",
    "auto_inject_guard",
    is_flag=True,
    default=False,
    show_default=True,
    help=(
        "FR-024 backward-compat: prepend the canonical §11.5 sentence to "
        "<custom-prompt-dir>/system.txt before the injection-guard "
        "substring check runs. Default is off so the §11.5 required-substring "
        "enforcement is preserved (no silent bypass). Use during migration "
        "from legacy custom-prompt-dir layouts that predate §11.5 framing."
    ),
)
"""FR-024 -- reusable ``--auto-inject-guard`` Click option.

Attach via ``@auto_inject_guard_option`` on any subcommand that calls
:func:`preflight.read_custom_prompt_dir`; the bound keyword argument
is ``auto_inject_guard: bool`` so it can be threaded straight through
to the reader (same parameter name, no rename hazard).
"""


# Exit codes for ``validate_cmd``. Lifted to module constants so the
# test suite can assert against named values rather than magic numbers
# and so the documented contract (FR-007) survives accidental edits.
#
# ``EXIT_OK``         -- spec passed every rule.
# ``EXIT_INVALID``    -- spec parsed but failed one or more schema /
#                        cross-field rules. Diagnostics printed on stderr.
# ``EXIT_USAGE``      -- spec file unreadable or not valid JSON. The
#                        2 code matches Click's convention for usage
#                        errors so shell scripts can distinguish
#                        "operator typo" (2) from "spec is wrong" (1).
EXIT_OK: int = 0
EXIT_INVALID: int = 1
EXIT_USAGE: int = 2


def _format_failure(failure: SchemaValidationFailure) -> str:
    """Render one structured failure on a single human-readable line.

    The format is deliberately grep-friendly and stable so operators
    and CI scripts can pattern-match on it: ``- <rule> @ <path>: <msg>``.
    ``rule`` is the stable identifier from ``schema.RULE_*`` constants,
    not the human-facing message, so test fixtures assert on the rule
    name rather than on prose that may evolve.
    """
    path = failure.path or "<root>"
    return f"  - {failure.rule} @ {path}: {failure.message}"


def _emit_failures(
    jobspec_path: Path,
    failures: list[SchemaValidationFailure],
) -> None:
    """Print the FR-007 structured diagnostics block on stderr.

    Separated from ``validate_cmd`` so future commands (preflight CLI
    wrapper, scaffold-then-validate) can reuse the exact same render
    surface without duplicating the format string.
    """
    click.echo(
        f"validate: {jobspec_path} FAILED ({len(failures)} rule(s))",
        err=True,
    )
    for failure in failures:
        click.echo(_format_failure(failure), err=True)


@click.command("validate")
@click.argument(
    "jobspec_path",
    type=click.Path(
        exists=True,
        dir_okay=False,
        readable=True,
        path_type=Path,
    ),
)
@click.option(
    "--strict",
    is_flag=True,
    default=False,
    help=(
        "Reserved for future stricter rule sets (FR-007 future-proofing). "
        "Currently a no-op: the bundled schema module is already strict."
    ),
)
def validate_cmd(jobspec_path: Path, strict: bool) -> None:
    """Schema-check a JobSpec JSON file (FR-007 / T02.19).

    Loads ``JOBSPEC_PATH`` as JSON and runs the DM-001 schema +
    cross-field validators from ``cli/swarm/schema.py``. Exits 0 with
    a one-line OK summary on stdout when the spec passes; exits 1 with
    a structured per-rule diagnostic block on stderr when it fails;
    exits 2 when the file is unreadable or not valid JSON.

    The ``--strict`` flag is accepted but currently a no-op. It exists
    so the operator surface is stable when later tasks add opt-in
    stricter rule sets (e.g., warn-only rules promoted to errors).
    """
    # ``strict`` is intentionally accepted-but-unused; document the
    # intent at call time so the linter doesn't drop the parameter and
    # so the operator-facing help string remains the source of truth.
    del strict

    try:
        raw_text = jobspec_path.read_text(encoding="utf-8")
    except OSError as exc:  # pragma: no cover -- click.Path(exists=True) catches most
        click.echo(
            f"validate: cannot read {jobspec_path}: {exc}",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)

    try:
        spec: Any = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        click.echo(
            f"validate: {jobspec_path} is not valid JSON "
            f"(line {exc.lineno}, col {exc.colno}): {exc.msg}",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)

    failures = validate(spec)
    if not failures:
        click.echo(f"validate: {jobspec_path} OK")
        raise click.exceptions.Exit(EXIT_OK)

    _emit_failures(jobspec_path, failures)
    raise click.exceptions.Exit(EXIT_INVALID)


# ---------------------------------------------------------------------------
# validate-lenses (FR-008 / T02.20)
# ---------------------------------------------------------------------------
#
# OQ-010 resolution -- ``swarm validate-lenses`` failure semantics.
#
# Branch chosen: **BLOCKING by default with selectable WARNING mode**.
#
#   - Default (no flag): exit 0 when every non-custom entry passes its
#     five COMP-023 assertions; exit ``EXIT_INVALID`` (1) when one or
#     more entries fail, with structured per-entry diagnostics printed
#     to stderr. This is the CI-gate default — a registry regression
#     hard-fails the pipeline, matching ``validate``'s blocking
#     behavior so operators learn one set of exit-code semantics for
#     both schema-time and registry-time validation surfaces.
#
#   - ``--warning-mode``: exit 0 even when failures exist, but still
#     emit the diagnostic block on stderr prefixed with ``WARNING:``.
#     This is the OQ-001 / OQ-010 pre-commit-hook opt-in: contributors
#     iterating on lens entries get the warnings without a hard block,
#     and CI gates that want a non-blocking advisory mode (e.g., a
#     "registry health" check that should not stop a release) can opt
#     in by flag rather than parsing exit codes.
#
# Rationale (recorded in docs/swarm/oq-resolutions.md OQ-010 section):
#
#   - The roadmap row (R-046 / FR-008) wires this gate into CI as the
#     authoritative lens-registry check. Defaulting to blocking matches
#     the spirit of the FR-008 acceptance criterion "exits 0 when
#     registry passes; reports first failure otherwise" -- "reports"
#     in a CI context means a non-zero exit so the pipeline stops.
#   - The flag is required by the T02.20 acceptance criterion
#     "Supports ``--warning-mode`` flag if OQ-010 resolves to
#     warning-mode" -- making warning-mode opt-in honors that wording
#     literally while keeping the strict default operators expect.
#   - Exit code 2 remains reserved for usage errors (Click convention),
#     matching the validate_cmd surface so operators have one mental
#     model for both subcommands.
#
# The command surface intentionally takes no positional argument: the
# bundled :data:`LENSES` registry is the validation subject by design
# (FR-008 -- "Validate bundled lens registry"). Callers that want to
# validate a fixture or experimental registry should call
# :func:`validate_all` directly; exposing a registry-path argument is
# tracked under a future task (no roadmap row yet) and is intentionally
# out of scope for T02.20.


def _format_lens_failure(failure: LensValidationFailure) -> str:
    """Render one structured lens failure on a single human-readable line.

    Format mirrors :func:`_format_failure` for schema diagnostics so
    operators learn one parsing convention for both subcommands:
    ``- <rule> @ <path>: <message> (lens=<lens_name>)``. The
    ``lens=<name>`` suffix is the FR-008-required entry-name identifier
    (the AC says "reports first failure with entry name otherwise").
    Tests assert on the rule identifier (the stable
    ``_validate.RULE_*`` constants), not on the prose, so message
    phrasing can evolve.
    """
    path = failure.path or "<root>"
    return (
        f"  - {failure.rule} @ {path}: {failure.message} "
        f"(lens={failure.lens_name})"
    )


def _emit_lens_failures(
    failures: list[LensValidationFailure],
    warning_mode: bool,
) -> None:
    """Print the FR-008 structured diagnostics block on stderr.

    Header prefix flips between ``validate-lenses:`` (blocking default)
    and ``validate-lenses: WARNING:`` (warning-mode opt-in) so log
    consumers can grep one or the other without inspecting exit codes.
    Failure lines themselves are identical in both modes -- only the
    header tone changes -- so the diagnostic surface is structurally
    stable across the two OQ-010 branches.
    """
    prefix = "validate-lenses: WARNING:" if warning_mode else "validate-lenses:"
    click.echo(
        f"{prefix} {len(failures)} lens entry/entries failed validation",
        err=True,
    )
    for failure in failures:
        click.echo(_format_lens_failure(failure), err=True)


def _run_validate_lenses(
    registry: Mapping[str, LensEntry],
    warning_mode: bool,
) -> int:
    """Run :func:`validate_all` over ``registry`` and return an exit code.

    Pulled out of :func:`validate_lenses_cmd` so the exit-code policy
    (OQ-010 blocking vs warning-mode) is testable without invoking the
    Click runner. Returns the integer exit code so the caller can
    ``raise click.exceptions.Exit(code)``; tests can assert on the
    integer directly.

    Both branches print the success summary on stdout when the registry
    is clean; only the failure branch differs by mode (blocking ->
    EXIT_INVALID, warning -> EXIT_OK with warnings on stderr).
    """
    failures = validate_all(registry)
    if not failures:
        click.echo(
            f"validate-lenses: registry OK ({len(registry)} entries inspected, "
            f"{sum(1 for e in registry.values() if e.name != 'custom')} validated)"
        )
        return EXIT_OK
    _emit_lens_failures(failures, warning_mode=warning_mode)
    return EXIT_OK if warning_mode else EXIT_INVALID


@click.command("validate-lenses")
@click.option(
    "--warning-mode",
    is_flag=True,
    default=False,
    help=(
        "OQ-010 warning branch: emit per-entry diagnostics on stderr but "
        "exit 0 even when entries fail. Use for pre-commit hooks and "
        "non-blocking CI advisories. Default is blocking (exit 1 on any "
        "failure)."
    ),
)
def validate_lenses_cmd(warning_mode: bool) -> None:
    """Validate the bundled LENSES registry (FR-008 / T02.20).

    Runs the COMP-023 five-assertion lens validator over every entry in
    :data:`superclaude.cli.swarm.lenses.LENSES`. The ``custom`` escape
    hatch (COMP-026) is intentionally skipped — its prompt body flows in
    from ``--custom-prompt-dir`` at preflight and is validated on that
    path (T02.05 / T02.07).

    Exit codes (OQ-010 resolution -- see module docstring):

        * 0 -- every non-custom entry passes its five COMP-023
          assertions, OR ``--warning-mode`` is set and failures are
          emitted as warnings rather than errors.
        * 1 -- one or more entries failed validation and
          ``--warning-mode`` is not set (default blocking branch).
        * 2 -- reserved for future usage errors (no path argument
          accepted today, but kept consistent with :func:`validate_cmd`
          for a future ``--registry-path`` opt-in).

    Output:

        * Success: one-line OK summary on stdout naming the registry
          size and the count of inspected (non-custom) entries.
        * Failure: structured per-entry diagnostic block on stderr,
          one line per failing entry, format
          ``- <rule> @ <path>: <message> (lens=<lens_name>)``.
    """
    exit_code = _run_validate_lenses(LENSES, warning_mode=warning_mode)
    raise click.exceptions.Exit(exit_code)


# ---------------------------------------------------------------------------
# T03.01 / FR-001 -- ``superclaude swarm run`` subcommand.
#
# ``run_cmd`` is the COMP-002 ``run`` subcommand wiring. It accepts a
# JobSpec via three mutually-exclusive input modes (spec file argument,
# ``--stdin``, ``--lens`` shortcut), runs Wave 0 (preflight) via
# :func:`run_preflight`, then dispatches Wave 1 via
# :func:`dispatch_wave1`, and emits a return-contract stub on stdout.
#
# Scope split with downstream tasks:
#
#     * T03.02 replaces the T03.01 sequential reference body of
#       :func:`dispatch_wave1` with the real
#       :class:`ParallelExecutor`-driven fan-out (AC-004 / IMM-3).
#       :func:`run_cmd` does not change.
#     * T03.05 / T03.07 land the concrete ``openai_compat`` and
#       ``stub`` :class:`Transport` implementations consumed via
#       ``--transport``.
#     * T03.08 (FR-001) deepens the ``--lens`` shortcut path with
#       lens-driven defaults (FR-020) so the spec is preflight-valid
#       without a separate spec file. T03.01 leaves the ``--lens``
#       path as a minimal stub that builds a ``{"lens": NAME}`` dict
#       -- preflight will reject it on the other required fields, but
#       the input-mode resolution surface is in place for T03.08 to
#       extend.
#     * M5 replaces the return-contract emission stub with the full
#       :class:`ResultContract` writer (DM-012 + ``return-contract.yaml``).
#
# OQ-008 / INV-007 -- the env-missing failure branch is already wired
# end-to-end by :func:`run_preflight`: when the configured model pool
# is empty, preflight writes ``return-contract.yaml`` and raises
# :class:`PreflightError` with ``env_missing_contract_path`` populated.
# :func:`run_cmd` surfaces the contract path on stderr so operators
# can locate the structured failure envelope without parsing the
# diagnostic block.
# ---------------------------------------------------------------------------


# Transport ``kind`` choices accepted on ``--transport``. The literal
# pair mirrors :data:`superclaude.cli.swarm.models.TransportKind`
# (Phase-1 reference transports per FR-022 / FR-023). Listed here as a
# tuple so :func:`click.Choice` and the help text stay in sync without
# importing the typing.Literal at module load.
_TRANSPORT_KINDS: tuple[str, ...] = ("openai_compat", "stub")


def _resolve_run_transport(
    transport_kind: str,
    *,
    models: Any = (),
    env: Any = None,
) -> Any:
    """F-P3-1 -- construct the concrete :class:`Transport` for a run.

    Historically ``run_cmd`` (and the resume redispatch path) passed
    ``transport=None`` into :func:`dispatch_wave1`, which short-circuits to
    an empty result list -- so ``swarm run`` recorded ``transport.kind`` on
    the manifest but dispatched **zero** workers (the F-P3-1 critical no-op:
    ``swarm run --transport stub`` produced ``results=0`` with no worker
    artifacts or dispatch log events). This resolver constructs the concrete
    transport so dispatch actually fans out.

    Resolution:

    * ``stub``          -- a deterministic, network-free :class:`StubTransport`
      bound to the first configured model id (falling back to the stub
      default when no model is supplied). No env contract is consulted.
    * ``openai_compat`` -- reads the T2 proxy env contract (AC-017) via
      :func:`read_env` and binds a single :class:`OpenAICompatTransport` to
      the first configured model. ``read_env`` raises :class:`TransportEnvError`
      when the contract is incomplete; callers surface that as a structured
      env-missing failure (``EXIT_INVALID``) rather than dispatching nothing.

    A single transport is shared across all N worker slots because
    :func:`dispatch_wave1` accepts one transport for the whole wave. Per-slot
    model differentiation (one ``OpenAICompatTransport`` per ``T2Model0N``
    slot) is intentionally **out of scope** for the no-op fix; it would
    require extending the dispatch signature and is tracked separately.

    Args:
        transport_kind: the resolved ``transport.kind`` (one of
            :data:`_TRANSPORT_KINDS`). Taken from
            ``manifest.preflight.transport_kind`` on the inline run path and
            from the manifest / ``--transport`` override on resume.
        models: optional iterable of model identifiers. For ``stub`` the
            first non-empty entry becomes the stub ``model_id`` so per-worker
            results carry a stable model label; for ``openai_compat`` the
            wire models come from the env contract, so this is ignored.
        env: optional environment mapping forwarded to :func:`read_env`
            (defaults to ``os.environ``). Exposed for deterministic tests.

    Returns:
        A concrete object satisfying the ``Transport`` protocol
        (``send(prompt, timeout) -> WorkerResult``).

    Raises:
        TransportEnvError: ``openai_compat`` selected but the T2 env contract
            is incomplete.
        ValueError: ``transport_kind`` is not a recognised kind.
    """
    if transport_kind == "stub":
        from superclaude.cli.swarm.transports.stub import StubTransport

        model_id = next((m for m in (models or ()) if m), None) or "stub-model-00"
        return StubTransport(model_id=model_id)
    if transport_kind == "openai_compat":
        from superclaude.cli.swarm.transports.openai_compat import (
            OpenAICompatTransport,
            read_env,
        )

        config = read_env(env)
        return OpenAICompatTransport(
            base_url=config.base_url,
            api_key=config.api_key,
            model=config.models[0],
        )
    raise ValueError(
        f"swarm run: unknown transport kind {transport_kind!r}; "
        f"expected one of {_TRANSPORT_KINDS}"
    )


def _write_swarm_state(
    output_dir: Path,
    state_value: SwarmStateValue,
    job_id: str,
) -> None:
    """F-P3-3 -- persist ``.swarm-state.json`` for a lifecycle transition.

    Writes ``<output_dir>/.swarm-state.json`` via the atomic COMP-011
    :func:`~superclaude.cli.swarm.state.write_state` writer (tmp-file +
    :func:`os.replace`), confined to ``output_dir`` (NFR-013 / AC-014) so a
    target outside the ``--output`` root raises
    :class:`OutputConfinementError` before any side effect.

    Before F-P3-3 the production ``swarm run`` path built an in-memory
    :class:`SwarmState` in preflight but never wrote it to disk, so a real
    run left no ``.swarm-state.json`` and ``swarm status`` reported
    ``EXIT_USAGE`` ("no state file") even though the job had run. This helper
    is invoked at each wave-level transition (``preflight_ok`` ->
    ``dispatching`` -> ``terminal``) on the inline run path and at resume
    terminal, so ``swarm status`` and the resume reader observe the live
    phase. Detached runs re-enter ``swarm run`` inline inside the tmux
    session (the child argv carries no ``--detached``), so they inherit the
    identical state behaviour without a separate write site.

    Each call constructs a fresh :class:`SwarmState`; ``updated`` is stamped
    by the writer, so callers do not manage the timestamp.
    """
    from superclaude.cli.swarm.state import write_state as _write_state

    _write_state(
        output_dir / SWARM_STATE_FILENAME,
        SwarmState(state=state_value, job_id=job_id),
        output_dir=output_dir,
    )


def _build_spec_from_lens(lens_name: str) -> dict[str, Any]:
    """Expand a ``--lens NAME`` shortcut into a full JobSpec dict (FR-020).

    T03.08 -- promotes the T03.01 minimal stub (``{"lens": NAME}``) into
    a fully populated JobSpec dict so a bare ``--lens NAME`` invocation
    plus ``--target`` / ``--output`` is preflight-valid without a
    companion JSON spec file. Every field the DM-001 schema marks as
    required is populated either:

        * from the :class:`LensEntry` registry entry (``prompt.system``,
          ``prompt.user_template``, ``normalization.recipe``,
          ``normalization.template_path``, ``workers.count``,
          ``target.truncation.line_cap``,
          ``recommended_next_command_template``, ``output.lens_name``);
        * from sensible static defaults that match the parent-spec
          §4.2 lens-defaulting table (``transport.kind=stub`` for
          lens-shortcut quick dispatch, ``runtime.mode=inline``,
          ``status_policy`` floor/threshold values from the M3
          reference fixture in ``test_commands_run.py``); or
        * left as a placeholder that the operator MUST override via
          the CLI (``target.path`` and ``output.dir``) -- if neither
          override is supplied, preflight surfaces the structured
          target/output rule on stderr so the failure mode is the same
          actionable diagnostic operators see for spec-file mode.

    The transport defaults to ``stub`` because the lens shortcut is the
    quick-dispatch surface (FR-001 / FR-020 framing); operators who want
    to drive the T2 proxy via the shortcut must pass
    ``--transport openai_compat`` explicitly. The ``base_url_env`` /
    ``api_key_env`` placeholders match the AC-017 contract regardless of
    transport kind so schema validation passes on either branch.

    Unknown lens names are not resolved here: the caller
    (:func:`_resolve_input_mode`) filters out ``custom`` (escape hatch,
    no defaults to expand from) and unknown names before invoking this
    helper, so reaching this function implies ``lens_name`` is a
    well-known non-custom entry.
    """
    entry = LENSES[lens_name]
    workers_count = max(1, int(entry.default_workers or 1))
    return {
        "spec_version": CURRENT_SPEC_VERSION,
        "job_id": f"lens-{lens_name}-{uuid.uuid4().hex[:8]}",
        "created": datetime.now(timezone.utc).isoformat(),
        "caller": {
            "skill": None,
            "skill_version": None,
            "invocation_label": f"swarm-run-lens-{lens_name}",
            "kind": "cli",
        },
        "lens": lens_name,
        "custom_prompt_dir": None,
        "workers": {
            "count": workers_count,
            # Models is required by the schema; supply per-slot
            # placeholders so the spec passes schema validation. When
            # the operator wants real model IDs they should provide a
            # spec file. The openai_compat transport reads the
            # ``T2Model0N`` env contract at Wave 0 (T03.05 / T03.21)
            # so these placeholder strings never reach the wire.
            "models": [f"lens-default-model-{i}" for i in range(workers_count)],
            "timeout_sec": 180,
            "temperature": 0.2,
            "retry": {
                "on_5xx": True,
                "on_5xx_backoff_sec": 2,
                "on_4xx": False,
                "on_timeout": False,
            },
        },
        "transport": {
            # Default to stub so the lens shortcut path is a safe
            # quick-dispatch surface that never reaches the wire by
            # accident. ``--transport openai_compat`` opts in.
            "kind": "stub",
            "base_url_env": "T2ProxyUrl",
            "api_key_env": "T2ProxyKey",
        },
        "prompt": {
            "system": entry.system_prompt_fragment,
            "user_template": entry.user_template,
            "variables": {},
        },
        "target": {
            "kind": "file",
            # Placeholder; operator MUST override via ``--target``.
            # An empty/unreadable path surfaces the schema/preflight
            # target rule on stderr -- same diagnostic as spec-file mode.
            "path": "",
            "truncation": {
                "line_cap": entry.default_target_line_cap,
                "byte_floor": 50,
            },
            "delimiters": {
                "open": "<<<TARGET>>>",
                "close": "<<<END TARGET>>>",
            },
            "injection_guard": {
                "enabled": True,
                # The §11.5 substring is embedded in the lens
                # ``system_prompt_fragment`` (COMP-023 assertion 5),
                # so the required_substring mirror is set to the same
                # canonical sentence carried by the lens entry. Reading
                # the substring back off the lens body keeps the two
                # surfaces byte-identical without duplicating the
                # canonical constant here.
                "required_substring": _lens_injection_substring(entry),
            },
        },
        "normalization": {
            "recipe": entry.recipe_name,
            "template_path": entry.output_template_path,
            "schema_version": "1.0",
            "recipe_args": {},
            "on_parse_error": {"salvage": True, "retain_raw": True},
        },
        "output": {
            # Placeholder; operator MUST override via ``--output``.
            "dir": "",
            "filename_template": "{lens}-{index:02d}-{model_slug}.md",
            "lens_name": lens_name,
            "atomic_write": True,
            "emit_meta_sidecar": True,
        },
        "amalgamation_mode": "normalize+merge",
        "status_policy": {
            "floor": 2,
            "success_first": True,
            "partial_threshold": 2,
        },
        "recommended_next_command_template": (
            entry.recommended_next_command_template
        ),
        "recommended_next_command_substitutions": {},
        "runtime": {
            "mode": "inline",
            "log_level": "info",
            "on_completion": {
                "write_done_sentinel": True,
                "print_contract_to_stdout": True,
            },
        },
    }


def _lens_injection_substring(entry: LensEntry) -> str:
    """Return the §11.5 canonical sentence to mirror into ``injection_guard``.

    The lens entry is required (by COMP-023 assertion 5) to carry the
    canonical sentence in ``system_prompt_fragment``. Importing the
    constant directly from :mod:`schema` would couple this helper to
    the schema module's exact phrasing; instead we keep the lens body
    as the single source of truth and import the canonical constant on
    demand. The two surfaces stay in sync because they originate from
    the same canonical string in :mod:`schema`.
    """
    from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE

    # The lens fragment always contains the canonical sentence; the
    # injection_guard.required_substring field demands the canonical
    # form so the schema's RULE_INJECTION_SUBSTRING enforcement matches
    # byte-for-byte regardless of which prompt path produced the spec.
    if CANONICAL_INJECTION_GUARD_SENTENCE in entry.system_prompt_fragment:
        return CANONICAL_INJECTION_GUARD_SENTENCE
    # Fallback: even if a future lens variant elides the canonical
    # sentence, the required_substring field still has to be a string;
    # surface the canonical constant so preflight can produce a
    # well-formed diagnostic instead of an opaque schema error.
    return CANONICAL_INJECTION_GUARD_SENTENCE


def _resolve_input_mode(
    spec_path: Optional[Path],
    stdin_mode: bool,
    lens: Optional[str],
) -> tuple[str, Any]:
    """Resolve the three input modes into a (mode_label, spec_dict) pair.

    Returns the parsed JobSpec dict alongside a short identifier for
    the chosen mode (``"spec-file"`` / ``"stdin"`` / ``"lens"``); the
    label feeds into the operator-facing error messages so a wrong
    input shape is grep-friendly. Exits with :data:`EXIT_USAGE` on
    mutually-exclusive option conflicts and on invalid JSON.

    Mode precedence (highest first; mutually exclusive):
        1. Positional ``SPEC_PATH`` argument (spec-file mode).
        2. ``--stdin`` flag (stdin mode -- reads ``sys.stdin``).
        3. ``--lens NAME`` shortcut (lens mode -- T03.08 extends).

    The mutually-exclusive enforcement raises a Click usage error when
    more than one mode is requested so operators see a single
    actionable diagnostic instead of a cascade of downstream
    PreflightFailure rules.
    """
    modes_set = [
        bool(spec_path is not None),
        bool(stdin_mode),
        bool(lens),
    ]
    if sum(modes_set) > 1:
        click.echo(
            "swarm run: SPEC_PATH, --stdin, and --lens are mutually exclusive",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)
    if sum(modes_set) == 0:
        click.echo(
            "swarm run: provide a SPEC_PATH argument, --stdin, or --lens NAME",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)

    if spec_path is not None:
        try:
            raw_text = spec_path.read_text(encoding="utf-8")
        except OSError as exc:  # pragma: no cover -- click.Path(exists) covers most
            click.echo(
                f"swarm run: cannot read {spec_path}: {exc}",
                err=True,
            )
            raise click.exceptions.Exit(EXIT_USAGE)
        try:
            return "spec-file", json.loads(raw_text)
        except json.JSONDecodeError as exc:
            click.echo(
                f"swarm run: {spec_path} is not valid JSON "
                f"(line {exc.lineno}, col {exc.colno}): {exc.msg}",
                err=True,
            )
            raise click.exceptions.Exit(EXIT_USAGE)

    if stdin_mode:
        raw_text = sys.stdin.read()
        try:
            return "stdin", json.loads(raw_text)
        except json.JSONDecodeError as exc:
            click.echo(
                f"swarm run: stdin is not valid JSON "
                f"(line {exc.lineno}, col {exc.colno}): {exc.msg}",
                err=True,
            )
            raise click.exceptions.Exit(EXIT_USAGE)

    # lens mode -- T03.08 (FR-020) expands the shortcut into a fully
    # lens-defaulted JobSpec so a bare ``--lens NAME`` invocation plus
    # ``--target`` / ``--output`` is preflight-valid without a
    # companion spec file. ``custom`` is rejected here -- its prompt
    # body flows in from ``--custom-prompt-dir`` at preflight per
    # FR-021 / INV-003, so the shortcut path has nothing to expand and
    # the operator must use spec-file mode (or supply ``--stdin``).
    assert lens is not None  # exhaustive: covered by the count guard above
    if lens == "custom":
        click.echo(
            "swarm run: --lens custom is not a shortcut (FR-021 escape "
            "hatch); supply a spec file with custom_prompt_dir set instead",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)
    if lens not in LENSES:
        known = ", ".join(n for n in LENS_NAMES if n != "custom")
        click.echo(
            f"swarm run: unknown lens {lens!r}; known lenses: {known}",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)
    return "lens", _build_spec_from_lens(lens)


# ---------------------------------------------------------------------------
# T07.11 / FR-014 -- detached-launch staging helper.
#
# ``_launch_detached_run`` factors the tmux launch out of :func:`run_cmd`
# so the body of the detached branch is a single well-typed call. The
# helper:
#
#     1. Probes :func:`tmux.is_tmux_available` -- absence is EXIT_USAGE,
#        not a silent fallback to inline (operators who passed --detached
#        explicitly opted in; surfacing the missing-tmux diagnostic up
#        front beats a confusing inline run that contradicts the flag).
#     2. Validates the resolved ``job_id`` against the tmux session-name
#        rules so a malformed id surfaces as a clear CLI diagnostic
#        instead of a downstream tmux complaint.
#     3. Resolves ``output.dir`` (which holds the staged snapshot AND
#        the eventual three-layer durable monitoring set per NFR-004)
#        and writes the resolved spec atomically to
#        ``<output_dir>/.swarm-detached-spec.json`` via tmp+os.replace
#        (mirrors the IMM-6 / NFR-002 atomic-write discipline used by
#        the rest of the swarm surface).
#     4. Builds the child argv via ``sys.executable -m superclaude.cli.main`` running ``swarm
#        run <snapshot>`` so the launch works regardless of whether the
#        ``superclaude`` console script is on PATH inside the tmux
#        session. Operators who customize the launcher path should
#        monkeypatch :func:`tmux.launch_detached` -- this helper does
#        not expose a launcher override because the canonical
#        re-invocation surface is the same for every operator.
#     5. Delegates to :func:`tmux.launch_detached` and surfaces the
#        deterministic ``swarm-<job_id>`` session name on stdout next to
#        the job_id so the operator can pipe both into a follow-up
#        ``swarm attach`` / ``swarm status`` / ``swarm kill`` call.
# ---------------------------------------------------------------------------


DETACHED_SPEC_SNAPSHOT_FILENAME: str = ".swarm-detached-spec.json"


def _launch_detached_run(*, spec_dict: dict[str, Any], input_mode: str) -> None:
    """T07.11 -- stage a snapshot and launch ``swarm run`` inside tmux.

    See the module-level T07.11 block above for the staged contract.
    Raises ``click.exceptions.Exit`` on every terminal branch so the
    calling subcommand never needs to inspect the return value.
    """
    from superclaude.cli.swarm import tmux as swarm_tmux

    if not swarm_tmux.is_tmux_available():
        click.echo(
            "swarm run --detached: tmux is not available "
            "(missing on PATH or already nested inside a tmux session); "
            "detached mode requires tmux",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)

    job_id_value = spec_dict.get("job_id")
    if not isinstance(job_id_value, str) or not job_id_value:
        click.echo(
            "swarm run --detached: resolved spec is missing a non-empty "
            "job_id; supply ``job_id`` in the spec or use --lens to "
            "synthesize one",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)

    try:
        target_session = swarm_tmux.session_name(job_id_value)
    except ValueError as exc:
        click.echo(
            f"swarm run --detached: invalid job_id for tmux: {exc}",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)

    output_section = spec_dict.get("output", {}) or {}
    output_dir_value = output_section.get("dir", "") if isinstance(
        output_section, dict
    ) else ""
    if not isinstance(output_dir_value, str) or not output_dir_value:
        click.echo(
            "swarm run --detached: output.dir is required to stage the "
            "detached spec snapshot; set --output <dir> or output.dir in "
            "the spec",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)

    output_path = Path(output_dir_value)
    try:
        output_path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        click.echo(
            f"swarm run --detached: cannot create output dir {output_path}: {exc}",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)

    snapshot_path = output_path / DETACHED_SPEC_SNAPSHOT_FILENAME
    body = json.dumps(spec_dict, indent=2, sort_keys=False) + "\n"
    tmp_path = snapshot_path.with_suffix(snapshot_path.suffix + ".tmp")
    try:
        tmp_path.write_text(body, encoding="utf-8")
        import os as _os

        _os.replace(tmp_path, snapshot_path)
    except OSError as exc:
        click.echo(
            f"swarm run --detached: cannot stage spec snapshot "
            f"{snapshot_path}: {exc}",
            err=True,
        )
        try:
            tmp_path.unlink()
        except FileNotFoundError:
            pass
        raise click.exceptions.Exit(EXIT_USAGE)

    child_argv: list[str] = [
        sys.executable,
        "-m",
        "superclaude.cli.main",
        "swarm",
        "run",
        str(snapshot_path),
    ]

    import subprocess as _subprocess

    try:
        session = swarm_tmux.launch_detached(
            job_id_value, child_argv, cwd=output_path
        )
    except swarm_tmux.TmuxUnavailableError as exc:
        # Race: tmux disappeared between availability check and launch.
        click.echo(f"swarm run --detached: {exc}", err=True)
        raise click.exceptions.Exit(EXIT_USAGE)
    except ValueError as exc:
        # Empty command argv (defensive -- argv is always non-empty here).
        click.echo(f"swarm run --detached: {exc}", err=True)
        raise click.exceptions.Exit(EXIT_USAGE)
    except RuntimeError as exc:
        # A live session with this job_id already exists -- refusing to
        # clobber is the launcher's job (idempotency belongs to kill).
        click.echo(
            f"swarm run --detached: cannot launch session "
            f"{target_session!r}: {exc}",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_INVALID)
    except _subprocess.CalledProcessError as exc:
        click.echo(
            f"swarm run --detached: tmux launch failed (exit "
            f"{exc.returncode}): {exc}",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_INVALID)

    click.echo(
        f"swarm run: detached job_id={job_id_value} session={session} "
        f"mode={input_mode}"
    )
    raise click.exceptions.Exit(EXIT_OK)


def _emit_preflight_failures(
    failures: list[Any],  # list[PreflightFailure] but typed loosely for import locality
    env_missing_contract_path: Optional[str],
) -> None:
    """Print the FR-007-shaped structured diagnostics for preflight failures.

    Mirrors the :func:`_emit_failures` shape from ``validate`` so
    operators learn one diagnostic format for both Wave-0 surfaces
    (``swarm validate`` and ``swarm run`` preflight). When the
    env-missing contract was written, the path is surfaced as the
    last line so callers can locate the structured envelope without
    parsing.
    """
    click.echo(
        f"swarm run: preflight FAILED ({len(failures)} rule(s))",
        err=True,
    )
    for failure in failures:
        path = getattr(failure, "path", "") or "<root>"
        rule = getattr(failure, "rule", "<unknown>")
        message = getattr(failure, "message", "")
        click.echo(f"  - {rule} @ {path}: {message}", err=True)
    if env_missing_contract_path:
        click.echo(
            f"swarm run: env-missing return-contract: {env_missing_contract_path}",
            err=True,
        )


@click.command("run")
@click.argument(
    "spec_path",
    required=False,
    type=click.Path(
        exists=True,
        dir_okay=False,
        readable=True,
        path_type=Path,
    ),
)
@click.option(
    "--stdin",
    "stdin_mode",
    is_flag=True,
    default=False,
    help="Consume the JobSpec JSON document from stdin instead of a file.",
)
@click.option(
    "--lens",
    "lens",
    type=str,
    default=None,
    help=(
        "Shortcut: dispatch with the named lens (e.g. bare-review). "
        "Expands lens defaults (system/user prompts, recipe, workers, "
        "line_cap, next-command template) into a full JobSpec per "
        "FR-020. Requires --target and --output to point at concrete "
        "files. Pass --transport openai_compat to drive the T2 proxy; "
        "the default is stub for safe quick-dispatch. ``custom`` and "
        "unknown lens names are rejected with EXIT_USAGE."
    ),
)
@click.option(
    "--resume",
    "resume_job_id",
    type=str,
    default=None,
    help=(
        "T06.04 / FR-015 -- resume a prior swarm job from its manifest. "
        "Requires --output <dir> pointing at the original job's output "
        "directory (the one carrying manifest.json). Skips workers whose "
        "*.meta.json sidecar reports status=success, re-dispatches the "
        "remainder, re-runs Wave 2 normalize on the redispatched slots, "
        "and regenerates merged.md when amalgamation_mode==normalize+merge "
        "via reduce_wave3(resume=True). Mutually exclusive with SPEC_PATH "
        "/ --stdin / --lens. INV-001 / INV-016: the lens snapshot is "
        "rehydrated verbatim from manifest.resolved_lens_entry; live "
        "LENSES edits between runs are ignored unless --force-relens "
        "(T06.07) is passed."
    ),
)
@click.option(
    "--target",
    "target_path",
    type=click.Path(path_type=Path),
    default=None,
    help=(
        "Override target.path on the resolved JobSpec. Useful with "
        "--lens to point a shortcut invocation at a specific file."
    ),
)
@click.option(
    "--output",
    "output_dir",
    type=click.Path(path_type=Path, file_okay=False),
    default=None,
    help=(
        "Override output.dir on the resolved JobSpec. The preflight "
        "manifest and (eventually) the M5 return-contract are written "
        "under this directory. Required when --resume is set: the "
        "resume branch locates the prior job's manifest under this dir."
    ),
)
@click.option(
    "--transport",
    "transport_kind",
    type=click.Choice(list(_TRANSPORT_KINDS)),
    default=None,
    help=(
        "Override transport.kind on the resolved JobSpec. "
        "``openai_compat`` (default, FR-022) routes through the T2 "
        "proxy; ``stub`` (FR-023) is the deterministic in-process "
        "transport used by tests and dry runs."
    ),
)
@click.option(
    "--force-relens",
    "force_relens",
    is_flag=True,
    default=False,
    help=(
        "T06.07 / FR-025 -- on resume, re-resolve the lens from the "
        "current LENSES registry instead of consuming the manifest's "
        "resolved_lens_entry snapshot. The default resume path is "
        "manifest-driven (INV-001 / INV-016) so registry edits made "
        "between runs are silently ignored; this flag is the opt-in "
        "override for operators who explicitly want the live lens "
        "values applied to the redispatched workers. The lens name + "
        "workers.count + transport.kind still come from the manifest; "
        "only the lens body (system prompt, user template, recipe, "
        "next-command template) is re-resolved. Requires --resume."
    ),
)
@click.option(
    "--detached",
    "detached",
    is_flag=True,
    default=False,
    help=(
        "T07.11 / FR-014 -- launch the run inside a detached tmux "
        "session named ``swarm-<job_id>`` so it survives caller exit "
        "(AC-008). Returns immediately after the session is launched, "
        "printing the job_id on stdout. The resolved JobSpec (with "
        "CLI overrides applied) is staged to "
        "``<output_dir>/.swarm-detached-spec.json`` and the child "
        "tmux process re-invokes ``swarm run`` against that snapshot. "
        "Requires tmux on PATH and a resolvable output.dir; mutually "
        "exclusive with --resume. Use ``swarm attach <job_id>`` to "
        "re-attach and ``swarm kill <job_id>`` to terminate."
    ),
)
@auto_inject_guard_option
def run_cmd(
    spec_path: Optional[Path],
    stdin_mode: bool,
    lens: Optional[str],
    resume_job_id: Optional[str],
    target_path: Optional[Path],
    output_dir: Optional[Path],
    transport_kind: Optional[str],
    force_relens: bool,
    detached: bool,
    auto_inject_guard: bool,
) -> None:
    """Run a swarm job: Wave 0 preflight -> Wave 1 dispatch (T03.01 / FR-001).

    Four mutually-exclusive input modes:

        * Positional ``SPEC_PATH`` -- a JobSpec JSON file on disk.
        * ``--stdin`` -- read the JobSpec JSON document from stdin.
        * ``--lens NAME`` -- shortcut for a single bundled lens.
          T03.08 / FR-020 expands the shortcut into a fully
          lens-defaulted JobSpec so a bare ``--lens NAME --target ...
          --output ...`` is preflight-valid without a spec file.
        * ``--resume JOB_ID`` -- T06.04 / FR-015 resume mode. Loads
          ``manifest.json`` from ``--output``, rehydrates the JobSpec
          via :func:`preflight.resume_mode` (lens snapshot taken
          verbatim per INV-001 / INV-016), skips succeeded workers via
          their on-disk meta sidecars, re-dispatches the remainder,
          re-runs Wave 2 normalize on the redispatched slots, and
          regenerates ``merged.md`` via :func:`reduce_wave3` with
          ``resume=True``.

    Flow (non-resume modes):

        1. Resolve the input mode into a JobSpec dict.
        2. Apply ``--target`` / ``--output`` / ``--transport``
           overrides on the dict in place.
        3. Run :func:`run_preflight` (Wave 0). On failure, emit the
           structured rule block on stderr and exit with
           :data:`EXIT_INVALID`. The INV-007 env-missing contract
           path (when written) is surfaced as the last stderr line.
        4. Run :func:`dispatch_wave1` (Wave 1) with the selected
           :class:`Transport`. The T03.01 path is a sequential
           reference body; T03.02 swaps in the real
           :class:`ParallelExecutor`-driven fan-out.
        5. Emit a return-contract stub on stdout (M5 replaces this
           with the full :class:`ResultContract` writer).
    """
    # Imports are deferred so the module load surface stays light and
    # circular-import-free; preflight + dispatch both pull in many
    # downstream pieces (schema, lenses, transports) that are not
    # needed for ``validate`` / ``validate-lenses`` invocations.
    from superclaude.cli.swarm.dispatch import dispatch_wave1
    from superclaude.cli.swarm.preflight import PreflightError, run_preflight

    # F-P2-1 -- ``--auto-inject-guard`` is threaded into ``run_preflight``
    # below so the FR-021 custom-prompt-dir reader can auto-prepend the
    # canonical §11.5 sentence to a legacy ``system.txt`` that lacks it.
    # The flag is a no-op on the lens-driven / inline-prompt paths.

    # T06.04 / FR-015 -- resume branch. Mutually exclusive with the
    # three preflight-driven input modes (spec_path / stdin / lens).
    # When --resume is set, the resume orchestrator owns the full
    # pipeline; preflight does not re-run (INV-001 / INV-016 -- the
    # manifest is the durable source-of-truth).
    if resume_job_id is not None:
        if any([spec_path is not None, stdin_mode, lens is not None]):
            click.echo(
                "swarm run --resume: --resume is mutually exclusive with "
                "SPEC_PATH, --stdin, and --lens",
                err=True,
            )
            raise click.exceptions.Exit(EXIT_USAGE)
        if detached:
            click.echo(
                "swarm run --resume: --resume is mutually exclusive with "
                "--detached (resume orchestrates its own pipeline inline)",
                err=True,
            )
            raise click.exceptions.Exit(EXIT_USAGE)
        if output_dir is None:
            click.echo(
                "swarm run --resume: --output <dir> is required to locate "
                "the prior job's manifest.json",
                err=True,
            )
            raise click.exceptions.Exit(EXIT_USAGE)
        _run_resume_branch(
            job_id=resume_job_id,
            output_dir=output_dir,
            transport_kind_override=transport_kind,
            force_relens=force_relens,
        )
        return  # _run_resume_branch raises click.exceptions.Exit on terminal status.

    # T06.07 / FR-025 -- --force-relens only has meaning under --resume;
    # outside that branch the manifest snapshot does not exist yet so the
    # flag is a no-op trap. Surface that as EXIT_USAGE with an actionable
    # diagnostic instead of silently ignoring the operator's intent.
    if force_relens:
        click.echo(
            "swarm run: --force-relens requires --resume; it re-resolves "
            "the lens from the current registry on the resume path only",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)

    mode, spec_dict = _resolve_input_mode(spec_path, stdin_mode, lens)

    # T07.11 / FR-014 -- detached branch. Resolve overrides on the spec
    # snapshot so the child tmux invocation sees the same effective spec
    # as inline mode would have, then hand off to the tmux launcher. The
    # detached path NEVER runs Wave 0 / Wave 1 in the parent process --
    # the operator gets the job_id immediately and the full pipeline
    # executes inside the detached tmux session.
    if detached:
        if not isinstance(spec_dict, dict):
            click.echo(
                "swarm run --detached: resolved spec must be a JSON object, "
                f"got {type(spec_dict).__name__}",
                err=True,
            )
            raise click.exceptions.Exit(EXIT_USAGE)
        if target_path is not None:
            spec_dict.setdefault("target", {})["path"] = str(target_path)
        if output_dir is not None:
            spec_dict.setdefault("output", {})["dir"] = str(output_dir)
        if transport_kind is not None:
            spec_dict.setdefault("transport", {})["kind"] = transport_kind
        # Stamp runtime.mode so the staged snapshot, manifest, and any
        # downstream consumer agree on the detached lifecycle.
        spec_dict.setdefault("runtime", {})["mode"] = "detached"
        _launch_detached_run(spec_dict=spec_dict, input_mode=mode)
        return  # _launch_detached_run raises click.exceptions.Exit.

    # Apply CLI overrides on the spec dict so the same internal
    # JobSpec is produced regardless of input mode. ``--target`` /
    # ``--output`` / ``--transport`` are operator ergonomics; the
    # canonical source-of-truth remains the spec dict feeding
    # preflight. Each override is no-op when not supplied.
    if not isinstance(spec_dict, dict):
        click.echo(
            f"swarm run: resolved spec must be a JSON object, got {type(spec_dict).__name__}",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)
    if target_path is not None:
        spec_dict.setdefault("target", {})["path"] = str(target_path)
    if output_dir is not None:
        spec_dict.setdefault("output", {})["dir"] = str(output_dir)
    if transport_kind is not None:
        spec_dict.setdefault("transport", {})["kind"] = transport_kind

    try:
        preflight_result = run_preflight(
            spec_dict,
            output_dir=output_dir,
            auto_inject_guard=auto_inject_guard,
        )
    except PreflightError as err:
        _emit_preflight_failures(
            list(err.failures),
            env_missing_contract_path=err.env_missing_contract_path,
        )
        raise click.exceptions.Exit(EXIT_INVALID)

    # Wave 1 -- dispatch. The transport selector is the resolved
    # JobSpec ``transport.kind``; T03.05 / T03.07 land the concrete
    # implementations. The T03.01 wiring path passes ``transport=None``
    # so the dispatch wave is a no-op while the call site is in place;
    # tests inject a real :class:`Transport` via ``--transport stub``
    # once T03.07 lands.
    #
    # T03.10 / FR-045 -- when an output directory is in play, instantiate
    # the dual-format Logger so dispatch emits ``execution-log.jsonl``
    # (canonical, append-only) and ``execution-log.md`` (human-readable)
    # side-by-side. The two files are siblings of ``manifest.json``
    # inside ``--output``; preflight has already mkdir'd the directory.
    logger: Optional["Logger"] = None
    # F-P3-3 -- the output root for the durable ``.swarm-state.json``. Set
    # only when an ``--output`` directory is in play (same gate as the
    # manifest / logger); ``None`` for the spec-only smoke path that runs
    # without a materialised output directory.
    state_output_dir: Optional[Path] = None
    if preflight_result.manifest_path:
        from superclaude.cli.swarm.logging_ import Logger as _Logger

        manifest_dir = Path(preflight_result.manifest_path).parent
        state_output_dir = manifest_dir
        logger = _Logger(
            jsonl_path=manifest_dir / "execution-log.jsonl",
            md_path=manifest_dir / "execution-log.md",
            # F-P3-6 -- pass the ``--output`` root so the logger confines both
            # log paths via ``confine_path`` at construction (NFR-013 / AC-014);
            # the production path previously omitted ``output_dir``, bypassing
            # the confinement branch entirely.
            output_dir=manifest_dir,
        )
        # F-P3-3 -- persist the post-preflight state so ``swarm status`` and
        # the resume reader observe ``preflight_ok`` immediately after Wave 0,
        # even if the process dies before dispatch. The in-memory
        # ``preflight_result.state`` is already stamped ``preflight_ok``.
        _write_swarm_state(
            state_output_dir,
            preflight_result.state.state,
            preflight_result.manifest.job_id,
        )

    # F-P3-1 -- construct the concrete transport before dispatch. Passing
    # ``transport=None`` here is the historical no-op (dispatch returns an
    # empty list, so ``swarm run`` recorded the transport kind but never
    # fanned out a single worker). The resolver builds a deterministic
    # ``StubTransport`` for ``stub`` and an ``OpenAICompatTransport`` bound
    # to the T2 env contract for ``openai_compat``.
    from superclaude.cli.swarm.transports.openai_compat import TransportEnvError

    resolved_transport_kind = preflight_result.manifest.preflight.transport_kind
    workers_section = (
        spec_dict.get("workers", {}) if isinstance(spec_dict, dict) else {}
    )
    resolved_models = (
        workers_section.get("models", [])
        if isinstance(workers_section, dict)
        else []
    )
    try:
        run_transport = _resolve_run_transport(
            resolved_transport_kind, models=resolved_models
        )
    except TransportEnvError as exc:
        click.echo(
            f"swarm run: cannot construct {resolved_transport_kind!r} "
            f"transport -- {exc}",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_INVALID)

    # F-P3-3 -- transition to ``dispatching`` before Wave 1 fans out, so a
    # crash mid-dispatch leaves the state file at ``dispatching`` (not the
    # stale ``preflight_ok``) for resume / status triage.
    if state_output_dir is not None:
        _write_swarm_state(
            state_output_dir,
            "dispatching",
            preflight_result.manifest.job_id,
        )

    worker_results = dispatch_wave1(
        preflight_result, transport=run_transport, logger=logger
    )

    # F-P3-3 -- Wave 1 is the terminal wave for this T03.01 run body (the
    # M5 normalize/reduce pipeline is wired separately); flip the state to
    # ``terminal`` so ``swarm status`` reports completion and ``swarm kill``
    # finds an already-terminal record.
    if state_output_dir is not None:
        _write_swarm_state(
            state_output_dir,
            "terminal",
            preflight_result.manifest.job_id,
        )

    # Return-contract emission stub -- M5 replaces this with the real
    # :class:`ResultContract` writer (DM-012). For T03.01 we emit a
    # single grep-friendly line on stdout so the smoke test has a
    # stable success signal independent of the M5 writer landing.
    click.echo(
        f"swarm run: dispatched job (mode={mode}, "
        f"workers={preflight_result.manifest.preflight.workers_requested}, "
        f"results={len(worker_results)})"
    )
    raise click.exceptions.Exit(EXIT_OK)


# ---------------------------------------------------------------------------
# T06.04 / FR-015 -- ``swarm run --resume`` end-to-end orchestration.
#
# The resume branch is intentionally implemented as a self-contained helper
# rather than threaded through the preflight-driven ``run_cmd`` body. The
# distinction is structural: preflight runs once at job-acceptance time and
# stamps ``manifest.json`` as the durable source-of-truth (INV-001 / INV-016);
# resume MUST NOT re-run preflight because doing so would re-consult the live
# LENSES registry and break the manifest-as-source-of-truth invariant. The
# resume orchestrator therefore reads the manifest, rehydrates the JobSpec
# via :func:`preflight.resume_mode` (no live LENSES lookup), and drives
# dispatch + normalize + reduce directly.
#
# Slot-state discovery:
#   The dispatcher writes a ``*.meta.json`` sidecar per worker (see
#   :func:`normalize._emit_meta`). The filename encodes the slot index in
#   the ``-NN-`` position derived from ``OutputSpec.filename_template``
#   (``{lens}-{index:02d}-{model_slug}.md`` → ``…-NN-….meta.json``).
#   ``discover_succeeded_slots`` parses the filename, reads the sidecar's
#   ``status`` field, and returns a ``{slot_index: WorkerResult}`` map for
#   workers whose status survived to ``success``. Workers whose sidecars
#   are missing or report a non-success status are scheduled for redispatch.
#
# Redispatch:
#   The orchestrator builds a synthetic :class:`PreflightResult` whose
#   ``workers_requested`` is the count of remaining slots, then calls
#   :func:`dispatch_wave1`. The returned :class:`WorkerResult` list is
#   reindexed onto the original slot positions so subsequent normalize /
#   reduce / merge stages see slot-aligned indices. The synthetic manifest
#   preserves ``resolved_lens_entry`` and ``preflight.transport_kind`` from
#   the original manifest verbatim (INV-016).
# ---------------------------------------------------------------------------


# Slot-index pattern: filenames produced by the canonical
# ``{lens}-{index:02d}-{model_slug}.md`` template land at
# ``…-NN-….meta.json``. The capture group extracts the slot index; the
# trailing slug is non-greedy so multi-segment model slugs (``-1-5-pro``)
# still match a single ``NN`` pair at the leftmost position.
_META_SLOT_INDEX_RE: re.Pattern[str] = re.compile(
    r"-(\d+)-[^/\\]+\.meta\.json$"
)


def discover_succeeded_slots(
    output_dir: Path,
    workers_requested: int,
) -> dict[int, WorkerResult]:
    """T06.04 -- scan ``output_dir`` for succeeded worker meta sidecars.

    Returns ``{slot_index: WorkerResult}`` for every ``*.meta.json``
    sidecar whose ``status`` field is ``"success"``. The slot index is
    extracted from the filename via :data:`_META_SLOT_INDEX_RE` (the
    ``-NN-`` segment between the lens prefix and the model slug). Slots
    outside ``[0, workers_requested)`` are ignored so a stale sidecar
    from a prior run with a different ``workers.count`` cannot influence
    the resume decision.

    The reconstructed :class:`WorkerResult` carries:

        * ``index`` -- the slot the sidecar names.
        * ``meta_path`` -- absolute path to the on-disk sidecar.
        * ``final_path`` -- absolute path to the sibling
          ``…-NN-….final.md`` body when it exists; empty string when
          absent (a sidecar without a final body still counts as
          succeeded but downstream merge gates on ``final_path``).
        * ``raw_path`` -- absolute path to the sibling
          ``…-NN-….raw.md`` when it exists.
        * ``status`` -- ``"success"`` (the only branch admitted here).
        * ``model_label`` -- harvested from the model-slug segment of
          the filename so merge provenance survives resume.
        * ``bytes`` -- mirrored from the sidecar's ``bytes`` field.

    Args:
        output_dir: the original job's output directory. Must contain
            ``manifest.json`` and any per-worker sidecars. The function
            tolerates a missing directory (returns ``{}``) so a clean
            preflight that crashed before any worker landed surfaces
            as "redispatch everything".
        workers_requested: N from ``manifest.preflight.workers_requested``.
            Sidecars naming a slot outside ``[0, N)`` are ignored.

    Returns:
        Mapping from slot index to :class:`WorkerResult`. Empty when no
        sidecar reports success.
    """
    succeeded: dict[int, WorkerResult] = {}
    if not output_dir.is_dir():
        return succeeded
    for meta_file in sorted(output_dir.glob("*.meta.json")):
        match = _META_SLOT_INDEX_RE.search(meta_file.name)
        if match is None:
            continue
        slot_index = int(match.group(1))
        if slot_index < 0 or slot_index >= workers_requested:
            continue
        try:
            payload = json.loads(meta_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            # Corrupt or unreadable sidecar -- treat as "not succeeded"
            # so the slot is redispatched. Defensive: do not crash the
            # whole resume on a single bad file.
            continue
        if not isinstance(payload, dict):
            continue
        if payload.get("status") != "success":
            continue

        stem = meta_file.name[: -len(".meta.json")]
        final_candidate = meta_file.parent / f"{stem}.final.md"
        raw_candidate = meta_file.parent / f"{stem}.raw.md"
        # Recover the model_label from the filename segment between the
        # slot index and the ``.meta.json`` suffix. The capture's tail
        # is the model_slug; we surface it verbatim so merge provenance
        # carries the same label the original run stamped.
        slug_tail = meta_file.name[match.end(1) + 1 : -len(".meta.json")]
        bytes_written = payload.get("bytes", 0)
        try:
            bytes_int = int(bytes_written)
        except (TypeError, ValueError):
            bytes_int = 0
        succeeded[slot_index] = WorkerResult(
            index=slot_index,
            path=str(final_candidate) if final_candidate.exists() else "",
            raw_path=str(raw_candidate) if raw_candidate.exists() else "",
            meta_path=str(meta_file),
            final_path=str(final_candidate) if final_candidate.exists() else "",
            model_id=slug_tail,
            model_label=slug_tail,
            bytes=bytes_int,
            status="success",
        )
    return succeeded


def _run_resume_branch(
    *,
    job_id: str,
    output_dir: Path,
    transport_kind_override: Optional[str],
    force_relens: bool = False,
) -> None:
    """T06.04 -- orchestrate ``swarm run --resume <job_id>``.

    Steps:

        1. Locate ``<output_dir>/manifest.json`` and rehydrate the
           :class:`JobSpec` via :func:`preflight.resume_mode` (INV-001
           manifest source-of-truth; live LENSES never consulted).
        2. Validate ``manifest.job_id == job_id`` so a wrong-job-id
           invocation is surfaced as :data:`EXIT_USAGE` instead of
           silently rewriting the wrong output directory.
        3. Discover succeeded slots from per-worker sidecars; remaining
           slots are the redispatch set.
        4. Build a synthetic :class:`PreflightResult` carrying
           ``workers_requested=len(remaining)`` plus the original
           manifest's ``resolved_lens_entry`` and ``preflight.target_checksum``
           verbatim so dispatch + downstream stages see an INV-016-aligned
           view of the lens binding.
        5. Call :func:`dispatch_wave1` for the remaining slots. Reindex
           the returned :class:`WorkerResult` instances to the original
           slot positions so merge provenance respects slot order.
        6. Call :func:`normalize_wave2` on the redispatched workers only
           (succeeded workers already have on-disk meta + final bodies).
        7. Combine succeeded + redispatched, sort by slot index, and
           call :func:`reduce_wave3` with ``resume=True`` so a stale
           ``merged.md`` from the crashed prior run is deleted before
           the regenerated body lands (INV-010 / T06.02).
        8. Emit a grep-friendly success line on stdout (mode=resume,
           workers, skipped, redispatched counts) and exit 0.

    Args:
        job_id: the prior job identifier the operator wants to resume.
            Must match :attr:`Manifest.job_id`.
        output_dir: directory containing the prior job's
            ``manifest.json`` and per-worker sidecars.
        transport_kind_override: optional ``--transport`` override.
            When omitted, the manifest's recorded ``transport_kind``
            is used (INV-016 source-of-truth). When supplied, the
            override wins so operators can switch transport between
            runs without re-creating the manifest.
        force_relens: T06.07 / FR-025 opt-in. When ``True``, the
            rehydrated JobSpec AND the synthetic manifest's
            ``resolved_lens_entry`` are taken from the live LENSES
            registry instead of the persisted snapshot, so the
            redispatched workers see the freshly-edited lens body
            (system prompt, user template, recipe, next-command
            template). The lens NAME, ``workers_requested``, and
            ``transport_kind`` still come from the manifest; only the
            lens body is re-resolved. Surfaces an EXIT_USAGE error
            when the lens name is no longer registered.
    """
    from superclaude.cli.swarm.dispatch import dispatch_wave1
    from superclaude.cli.swarm.models import (
        Manifest as _Manifest,
    )
    from superclaude.cli.swarm.models import (
        PreflightSummary as _PreflightSummary,
    )
    from superclaude.cli.swarm.models import (
        SwarmState as _SwarmState,
    )
    from superclaude.cli.swarm.normalize import normalize_wave2
    from superclaude.cli.swarm.preflight import (
        PreflightResult as _PreflightResult,
    )
    from superclaude.cli.swarm.preflight import (
        resume_mode,
    )
    from superclaude.cli.swarm.reduce import reduce_wave3

    output_path = Path(output_dir)
    manifest_path = output_path / "manifest.json"
    if not manifest_path.is_file():
        click.echo(
            f"swarm run --resume: manifest.json not found under {output_path}",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)

    # Load the manifest into a Manifest dataclass (for downstream
    # synthetic-PreflightResult construction) AND rehydrate a JobSpec
    # via resume_mode (for normalization recipe + amalgamation_mode).
    try:
        manifest_payload = manifest_path.read_text(encoding="utf-8")
        manifest_dict = json.loads(manifest_payload)
    except (OSError, json.JSONDecodeError) as exc:
        click.echo(
            f"swarm run --resume: cannot read manifest at {manifest_path}: {exc}",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)

    from superclaude.cli.swarm.models import from_dict as _from_dict

    try:
        manifest_obj: _Manifest = _from_dict(_Manifest, manifest_dict)
    except (TypeError, ValueError) as exc:
        click.echo(
            f"swarm run --resume: manifest at {manifest_path} is malformed: {exc}",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)

    if manifest_obj.job_id != job_id:
        click.echo(
            f"swarm run --resume: job_id mismatch -- requested {job_id!r}, "
            f"manifest carries {manifest_obj.job_id!r}",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)

    try:
        rehydrated_spec: JobSpec = resume_mode(
            manifest_path, force_relens=force_relens
        )
    except KeyError as exc:
        click.echo(
            f"swarm run --resume --force-relens: lens "
            f"{manifest_obj.resolved_lens_entry.name!r} is no longer "
            f"registered in the live LENSES registry: {exc}",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)

    # T06.07 / FR-025 -- when --force-relens is set, the synthetic
    # manifest fed into dispatch must carry the freshly-resolved lens
    # snapshot so the redispatched workers see the live body (system
    # prompt, user template, recipe). The default path keeps the
    # persisted snapshot verbatim (INV-001 / INV-016 manifest immunity).
    if force_relens:
        from superclaude.cli.swarm.models import (
            ResolvedLensEntry as _ResolvedLensEntry,
        )
        from superclaude.cli.swarm.preflight import resolve_lens as _resolve_lens

        resolved_lens_entry_for_dispatch = _ResolvedLensEntry.from_lens(
            _resolve_lens(manifest_obj.resolved_lens_entry.name)
        )
    else:
        resolved_lens_entry_for_dispatch = manifest_obj.resolved_lens_entry

    workers_requested = manifest_obj.preflight.workers_requested
    resolved_transport_kind = (
        transport_kind_override
        if transport_kind_override
        else manifest_obj.preflight.transport_kind
    )
    amalgamation_mode = rehydrated_spec.amalgamation_mode
    recipe_name = rehydrated_spec.normalization.recipe

    # ----- Slot-state discovery ---------------------------------------------
    succeeded = discover_succeeded_slots(output_path, workers_requested)
    remaining_indices: list[int] = [
        index for index in range(workers_requested) if index not in succeeded
    ]

    # ----- Wave 1 redispatch (remaining slots only) -------------------------
    redispatched: list[WorkerResult] = []
    if remaining_indices:
        synthetic_manifest = _Manifest(
            contract_version=manifest_obj.contract_version,
            job_id=manifest_obj.job_id,
            resolved_lens_entry=resolved_lens_entry_for_dispatch,
            preflight=_PreflightSummary(
                target_checksum=manifest_obj.preflight.target_checksum,
                workers_requested=len(remaining_indices),
                transport_kind=resolved_transport_kind,
            ),
        )
        synthetic_state = _SwarmState(
            state="preflight_ok", job_id=manifest_obj.job_id
        )
        synthetic_preflight = _PreflightResult(
            manifest=synthetic_manifest, state=synthetic_state
        )

        # F-P3-1 -- construct the concrete transport for the resume
        # redispatch (previously ``transport=None``, the no-op that made
        # resume re-dispatch zero workers). The transport kind comes from
        # the manifest (or the ``--transport`` override resolved above);
        # ``stub`` needs no env, ``openai_compat`` reads the T2 contract.
        from superclaude.cli.swarm.transports.openai_compat import (
            TransportEnvError as _TransportEnvError,
        )

        try:
            resume_transport = _resolve_run_transport(
                resolved_transport_kind,
                models=list(rehydrated_spec.workers.models),
            )
        except _TransportEnvError as exc:
            click.echo(
                f"swarm run --resume: cannot construct "
                f"{resolved_transport_kind!r} transport -- {exc}",
                err=True,
            )
            raise click.exceptions.Exit(EXIT_INVALID)
        raw_redispatched = dispatch_wave1(
            synthetic_preflight, transport=resume_transport, logger=None
        )

        # Reindex returned slots (0..K-1) onto the original slot
        # positions so merge provenance and reduce M-counting honour
        # the original fan-out shape.
        for new_pos, worker in enumerate(raw_redispatched):
            if new_pos >= len(remaining_indices):
                # Defensive: dispatch returned more results than slots
                # we asked for. Drop the surplus rather than overwrite
                # a succeeded slot.
                break
            target_index = remaining_indices[new_pos]
            worker.index = target_index
            redispatched.append(worker)

    # ----- Wave 2 normalize (redispatched workers only) ---------------------
    if redispatched and recipe_name:
        try:
            redispatched = normalize_wave2(
                redispatched,
                recipe_name=recipe_name,
            )
        except KeyError as exc:
            click.echo(
                f"swarm run --resume: normalize recipe {recipe_name!r} "
                f"not registered: {exc}",
                err=True,
            )
            raise click.exceptions.Exit(EXIT_INVALID)

    # ----- Combine + sort by slot index -------------------------------------
    redispatched_by_index = {w.index: w for w in redispatched}
    combined: list[WorkerResult] = []
    for index in range(workers_requested):
        if index in succeeded:
            combined.append(succeeded[index])
        elif index in redispatched_by_index:
            combined.append(redispatched_by_index[index])
        # else: slot unfilled (dispatch returned fewer than requested);
        # reduce_wave3 will classify the overall run as partial/failed
        # via IMM-5 based on M/N.

    # ----- Wave 3 reduce with resume=True (merge regen per INV-010) ---------
    reduce_wave3(
        combined,
        mode=amalgamation_mode,
        output_dir=output_path,
        workers_requested=workers_requested,
        status_policy=rehydrated_spec.status_policy,
        job_id=manifest_obj.job_id,
        resume=True,
    )

    # F-P3-3 -- resume reached its terminal wave; persist the terminal state
    # so ``swarm status`` on the resumed job reports completion (confined to
    # the ``--output`` root via the same atomic writer the inline path uses).
    _write_swarm_state(output_path, "terminal", manifest_obj.job_id)

    click.echo(
        f"swarm run --resume: job_id={manifest_obj.job_id} "
        f"workers={workers_requested} "
        f"skipped={len(succeeded)} "
        f"redispatched={len(remaining_indices)}"
    )
    raise click.exceptions.Exit(EXIT_OK)


# ---------------------------------------------------------------------------
# T07.04 / FR-002 -- ``superclaude swarm status`` subcommand.
#
# ``status_cmd`` is the COMP-013 operator surface for inspecting a job's
# current wave-level phase and (when terminal) the
# :class:`ResultContract` status. It reads ``.swarm-state.json`` via the
# state module, so the source-of-truth for "what wave is this job in"
# stays single-sourced in :class:`SwarmState`. When the state reports
# ``terminal``, the command additionally consults
# ``return-contract.yaml`` for the IMM-5-determined
# ``success``/``partial``/``failed`` status so the exit code reflects
# the run outcome (acceptance: "Returns exit code per terminal state").
#
# Exit codes:
#
#     * 0 -- non-terminal phase (job still running), OR terminal phase
#       with contract status ``success``, OR terminal phase with no
#       contract on disk (degraded but not a status-known failure --
#       operator should consult logs).
#     * 1 -- terminal phase with contract status ``partial`` or
#       ``failed`` (non-success terminal).
#     * 2 -- usage error: ``--output`` directory missing, state file
#       missing, corrupt JSON, or ``--job`` mismatch with the state's
#       recorded job_id.
#
# ``--watch`` polls every ``--watch-interval`` seconds and refreshes
# stdout until the state reaches ``terminal`` (or KeyboardInterrupt).
# A bounded ``--watch-max-iterations`` keeps the test surface fast and
# bounds the worst case for runaway jobs.
# ---------------------------------------------------------------------------


def _format_status_line(state: Any, contract_status: Optional[str]) -> str:
    """Render the grep-friendly status line.

    Shape: ``status: phase=<phase> job_id=<id> updated=<ts>[ terminal_status=<s>]``.
    Operators and CI scripts pattern-match on ``phase=`` and
    ``terminal_status=`` as stable identifiers. The optional suffix is
    present only when ``state.state == "terminal"`` and the contract
    resolved a status; otherwise it is omitted so non-terminal lines
    stay short.
    """
    base = (
        f"status: phase={state.state} "
        f"job_id={state.job_id or '<unset>'} "
        f"updated={state.updated or '<unset>'}"
    )
    if contract_status is not None:
        base += f" terminal_status={contract_status}"
    return base


def _read_terminal_status(output_dir: Path) -> Optional[str]:
    """Best-effort lookup of ``ResultContract.status`` from disk.

    Returns ``None`` when the contract is absent or unreadable -- the
    caller treats a missing contract as "status unknown" rather than a
    failure (the run may have crashed before reduce emitted it). When
    the contract is present, the lightweight YAML parse extracts the
    top-level ``status`` field without importing the full
    :class:`ResultContract` round-trip, keeping ``swarm status`` cheap
    enough to poll under ``--watch``.

    The contract is YAML by emission (``emit_contract`` writes via
    ``yaml.safe_dump``). PyYAML is already a transport dependency, so
    importing it here is safe; we import inside the function to keep
    the module-load surface light for ``validate`` / ``validate-lenses``
    invocations that never touch the contract.
    """
    contract_path = output_dir / RESULT_CONTRACT_FILENAME
    if not contract_path.is_file():
        return None
    try:
        import yaml

        payload = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 -- defensive: any parse error -> unknown
        return None
    if not isinstance(payload, dict):
        return None
    status = payload.get("status")
    if not isinstance(status, str):
        return None
    return status


def _read_status_once(
    output_dir: Path,
    job_id: Optional[str],
) -> tuple[int, str]:
    """Load state + contract once and return ``(exit_code, line)``.

    Pulled out of :func:`status_cmd` so the watch loop can reuse the
    exact same resolution logic and so the unit tests can pin the
    one-shot path without invoking the Click runner. On a usage error
    (missing dir, missing state, corrupt JSON, job_id mismatch) the
    function returns ``(EXIT_USAGE, <stderr-message>)`` so the caller
    routes it to stderr. On success the returned line is the stdout
    payload.
    """
    if not output_dir.is_dir():
        return (
            EXIT_USAGE,
            f"swarm status: output directory not found: {output_dir}",
        )

    state_path = output_dir / SWARM_STATE_FILENAME
    from superclaude.cli.swarm.state import read_state

    try:
        state = read_state(state_path)
    except json.JSONDecodeError as exc:
        return (
            EXIT_USAGE,
            f"swarm status: {state_path} is not valid JSON "
            f"(line {exc.lineno}, col {exc.colno}): {exc.msg}",
        )
    except ValueError as exc:
        return (
            EXIT_USAGE,
            f"swarm status: {state_path} has invalid SwarmState shape: {exc}",
        )

    if state is None:
        return (
            EXIT_USAGE,
            f"swarm status: state file not found: {state_path}",
        )

    if job_id is not None and state.job_id != job_id:
        return (
            EXIT_USAGE,
            f"swarm status: job_id mismatch -- requested {job_id!r}, "
            f"state carries {state.job_id!r}",
        )

    contract_status: Optional[str] = None
    if state.state == TERMINAL_STATE_VALUE:
        contract_status = _read_terminal_status(output_dir)

    line = _format_status_line(state, contract_status)

    # Exit code policy: only a terminal-with-non-success contract is a
    # non-zero. Non-terminal phases (job still running) and terminal
    # phases without a readable contract (degraded but unknown) report
    # 0 so CI scripts can distinguish "definitely failed" from "still
    # running or unknown" via the exit code alone.
    if state.state == TERMINAL_STATE_VALUE and contract_status in {
        "partial",
        "failed",
    }:
        return EXIT_INVALID, line
    return EXIT_OK, line


@click.command("status")
@click.option(
    "--output",
    "output_dir",
    type=click.Path(path_type=Path, file_okay=False),
    required=True,
    help=(
        "Directory containing the prior job's .swarm-state.json. "
        "Typically the same directory passed to ``swarm run --output``."
    ),
)
@click.option(
    "--job",
    "job_id",
    type=str,
    default=None,
    help=(
        "Optional job_id to verify against the state file. When set, a "
        "mismatch with .swarm-state.json's recorded job_id is surfaced "
        "as EXIT_USAGE so a wrong-directory invocation fails loudly "
        "instead of silently reporting a different job's phase."
    ),
)
@click.option(
    "--watch",
    "watch",
    is_flag=True,
    default=False,
    help=(
        "Poll .swarm-state.json on an interval and refresh stdout until "
        "the state reaches ``terminal`` (or Ctrl-C). Each poll emits the "
        "same single-line summary the one-shot mode produces, so log "
        "consumers see a stable, grep-friendly stream."
    ),
)
@click.option(
    "--watch-interval",
    "watch_interval",
    type=click.FloatRange(min=0.01),
    default=2.0,
    show_default=True,
    help="Seconds between polls when --watch is set.",
)
@click.option(
    "--watch-max-iterations",
    "watch_max_iterations",
    type=click.IntRange(min=1),
    default=None,
    help=(
        "Optional ceiling on poll iterations under --watch. Primarily a "
        "test-surface lever; production callers omit it so the loop "
        "runs until terminal or interrupted."
    ),
)
def status_cmd(
    output_dir: Path,
    job_id: Optional[str],
    watch: bool,
    watch_interval: float,
    watch_max_iterations: Optional[int],
) -> None:
    """Report a swarm job's phase + status (T07.04 / FR-002).

    Reads ``<output_dir>/.swarm-state.json`` and reports the wave-level
    phase (``preflight_ok`` / ``dispatching`` / ``normalizing`` /
    ``reducing`` / ``terminal``). When the phase is ``terminal``, also
    reads ``return-contract.yaml`` for the IMM-5-determined run status
    (``success`` / ``partial`` / ``failed``) and adjusts the exit code:

        * 0 -- non-terminal phase OR terminal+success OR terminal with
          unreadable contract (status unknown).
        * 1 -- terminal+partial or terminal+failed.
        * 2 -- usage error (directory missing, state missing, corrupt
          JSON, job_id mismatch).

    The ``--watch`` flag polls the state file on ``--watch-interval``
    seconds and re-emits the status line until ``terminal`` is reached
    or the operator interrupts. Each iteration writes a fresh line to
    stdout, so non-TTY callers (CI / monitor scripts) get a stable
    JSONL-adjacent stream they can parse line-by-line.
    """
    output_path = Path(output_dir)

    if not watch:
        exit_code, line = _read_status_once(output_path, job_id)
        stream = sys.stderr if exit_code == EXIT_USAGE else sys.stdout
        click.echo(line, file=stream)
        raise click.exceptions.Exit(exit_code)

    # --watch path: poll until terminal (or max-iterations) is reached.
    # The last observed exit code is the command's exit code so CI
    # scripts that loop on `swarm status --watch` still see the right
    # success/failed signal at the end of the run.
    last_exit_code = EXIT_OK
    iterations = 0
    try:
        while True:
            exit_code, line = _read_status_once(output_path, job_id)
            stream = sys.stderr if exit_code == EXIT_USAGE else sys.stdout
            click.echo(line, file=stream)
            last_exit_code = exit_code

            if exit_code == EXIT_USAGE:
                # Usage errors are not recoverable mid-watch (missing
                # dir, missing state, job_id mismatch). Stop polling so
                # the operator sees the diagnostic once instead of
                # spinning at watch_interval.
                break

            if "phase=" + TERMINAL_STATE_VALUE in line:
                break

            iterations += 1
            if (
                watch_max_iterations is not None
                and iterations >= watch_max_iterations
            ):
                break
            time.sleep(watch_interval)
    except KeyboardInterrupt:
        # Operator-initiated stop is a clean exit -- the last status
        # line is already on stdout. Propagate the last observed exit
        # code so the CI surface still distinguishes terminal-failed
        # from "user gave up".
        pass

    raise click.exceptions.Exit(last_exit_code)


# ---------------------------------------------------------------------------
# T07.05 / FR-003 -- ``superclaude swarm logs`` subcommand.
#
# ``logs_cmd`` is the COMP-013 operator surface for reading the
# dual-format event log produced by the T03.04 Logger (COMP-012). It
# supports two output formats and two read modes:
#
#   --md (default)   read ``execution-log.md`` -- human-readable.
#   --jsonl          read ``execution-log.jsonl`` -- canonical, machine-parseable.
#
#   one-shot (default)  read the file once and dump to stdout.
#   --follow / -f       poll-and-print appended lines until terminal
#                       state or the operator interrupts (Ctrl-C).
#
# Convenience flag ``--tail`` is shorthand for ``--jsonl --follow``,
# matching the T07.05 validation example ``swarm logs --job <id>
# --tail`` (follows the JSONL surface) and the AC wording "Tails JSONL
# or dumps markdown log as flag indicates".
#
# Exit codes:
#
#     * 0 -- file read successfully (one-shot) OR follow loop reached
#       a terminal state / max-iterations / KeyboardInterrupt cleanly.
#     * 2 -- usage error: ``--output`` directory missing, log file
#       missing, ``--job`` mismatch with the state's recorded job_id.
#
# Like ``status_cmd``, follow mode is bounded by
# ``--watch-max-iterations`` for the test surface; production callers
# omit it so the loop runs until terminal or interrupted.
# ---------------------------------------------------------------------------


def _validate_job_id(
    output_dir: Path,
    job_id: Optional[str],
) -> Optional[str]:
    """Return an error message when ``--job`` mismatches the state file.

    When ``job_id`` is ``None`` the function returns ``None`` (no
    validation requested). When the state file is missing we likewise
    return ``None`` -- the caller will fail loudly on the log-file path
    instead, and a state file is not required to read logs (operators
    may inspect a partial job that never reached the state-write stage).
    When ``job_id`` is supplied AND the state file is present AND its
    recorded job_id does not match, the function returns an error
    string for the caller to surface as :data:`EXIT_USAGE`.
    """
    if job_id is None:
        return None
    state_path = output_dir / SWARM_STATE_FILENAME
    if not state_path.is_file():
        return None
    from superclaude.cli.swarm.state import read_state

    try:
        state = read_state(state_path)
    except (json.JSONDecodeError, ValueError):
        # A corrupt state file is the status surface's problem, not
        # ours. The log file may still be intact and useful for
        # post-mortem; surface the corruption only when --job pins it.
        return (
            f"swarm logs: {state_path} is unreadable; cannot verify --job "
            f"{job_id!r}"
        )
    if state is None:
        return None
    if state.job_id != job_id:
        return (
            f"swarm logs: job_id mismatch -- requested {job_id!r}, "
            f"state carries {state.job_id!r}"
        )
    return None


def _is_state_terminal(output_dir: Path) -> bool:
    """Best-effort check for ``.swarm-state.json`` reaching terminal.

    Used by :func:`_follow_log` so the follow loop exits cleanly once
    the job has wrapped up rather than spinning forever on a stable log
    file. Returns ``False`` when the state file is missing / unreadable
    / non-terminal -- a missing state file means "no signal yet, keep
    polling", which is the right behaviour for a job that crashed
    before writing state.
    """
    state_path = output_dir / SWARM_STATE_FILENAME
    if not state_path.is_file():
        return False
    from superclaude.cli.swarm.state import read_state

    try:
        state = read_state(state_path)
    except (json.JSONDecodeError, ValueError):
        return False
    if state is None:
        return False
    return state.state == TERMINAL_STATE_VALUE


def _dump_log_file(log_path: Path, lines_tail: Optional[int]) -> int:
    """Load ``log_path`` once and echo it on stdout. Returns exit code.

    When ``lines_tail`` is set, only the last N lines are emitted so
    operators can sample a long log without flooding the terminal.
    ``None`` dumps the full file.
    """
    try:
        text = log_path.read_text(encoding="utf-8")
    except OSError as exc:
        click.echo(
            f"swarm logs: cannot read {log_path}: {exc}",
            err=True,
        )
        return EXIT_USAGE
    if lines_tail is not None and lines_tail > 0:
        all_lines = text.splitlines()
        text = "\n".join(all_lines[-lines_tail:])
        if text:
            text += "\n"
    # ``click.echo`` adds its own trailing newline; strip exactly one so
    # the file's natural terminator survives unchanged.
    click.echo(text, nl=False)
    return EXIT_OK


def _follow_log(
    output_dir: Path,
    log_path: Path,
    *,
    lines_tail: Optional[int],
    watch_interval: float,
    watch_max_iterations: Optional[int],
) -> int:
    """Tail ``log_path`` for appended lines until terminal or interrupted.

    Opens the file once, seeks to ``EOF - lines_tail*avg_line`` when a
    seed is requested (or to byte zero when ``lines_tail`` is ``None``
    so the entire current contents are emitted as the seed), then polls
    on ``watch_interval`` seconds reading any new bytes that appended
    since the last read. Exits cleanly when ``.swarm-state.json``
    reports ``terminal`` or the operator hits Ctrl-C. Bounded by
    ``watch_max_iterations`` for the test surface (None = unbounded).

    The seed phase prints the file's current contents (or the trailing
    ``lines_tail`` lines) so the operator sees context before the live
    stream begins -- matching ``tail -f``'s default behaviour.
    """
    if not log_path.is_file():
        click.echo(
            f"swarm logs: log file not found: {log_path}",
            err=True,
        )
        return EXIT_USAGE

    # Seed: print existing contents (full file or last N lines) so the
    # operator has context before the follow loop blocks on new data.
    try:
        existing = log_path.read_text(encoding="utf-8")
    except OSError as exc:
        click.echo(
            f"swarm logs: cannot read {log_path}: {exc}",
            err=True,
        )
        return EXIT_USAGE
    if lines_tail is not None and lines_tail > 0:
        seed_lines = existing.splitlines()[-lines_tail:]
        seed_text = "\n".join(seed_lines)
        if seed_text:
            seed_text += "\n"
    else:
        seed_text = existing
    if seed_text:
        click.echo(seed_text, nl=False)

    # Track the byte position we've already emitted so the polling loop
    # only sees the newly-appended tail. Re-stat the file each iteration
    # to handle the rare case of truncation (we restart from byte zero
    # if the file shrinks, mirroring ``tail -F``).
    last_pos = len(existing.encode("utf-8"))
    iterations = 0
    try:
        while True:
            if _is_state_terminal(output_dir):
                # Drain any final bytes the writer landed between our
                # last poll and the terminal-state observation so the
                # follow surface never misses the closing events.
                _drain_appended(log_path, last_pos)
                break

            iterations += 1
            if (
                watch_max_iterations is not None
                and iterations > watch_max_iterations
            ):
                break

            time.sleep(watch_interval)

            try:
                size = log_path.stat().st_size
            except OSError:
                # File disappeared mid-follow; surface as usage error
                # so callers see a definite signal rather than spinning.
                click.echo(
                    f"swarm logs: log file vanished mid-follow: {log_path}",
                    err=True,
                )
                return EXIT_USAGE

            if size < last_pos:
                # Truncation -- restart from byte zero (``tail -F``
                # semantics). Re-emit nothing here; the next read will
                # pick up the new contents.
                last_pos = 0

            if size > last_pos:
                last_pos = _drain_appended(log_path, last_pos)
    except KeyboardInterrupt:
        # Operator-initiated stop is a clean exit. The follow surface
        # has already streamed everything it observed.
        pass

    return EXIT_OK


def _drain_appended(log_path: Path, start_pos: int) -> int:
    """Emit bytes appended since ``start_pos`` and return the new EOF position.

    Reads from ``start_pos`` to end-of-file, decodes as UTF-8, and
    writes to stdout via :func:`click.echo` (``nl=False`` so embedded
    newlines pass through unchanged). Returns the post-read byte
    position so the follow loop can resume from the new EOF on the next
    poll.
    """
    try:
        with open(log_path, "rb") as fh:
            fh.seek(start_pos)
            chunk = fh.read()
            new_pos = fh.tell()
    except OSError:
        return start_pos
    if chunk:
        try:
            text = chunk.decode("utf-8")
        except UnicodeDecodeError:
            # Drop the partial multi-byte tail; the next poll will pick
            # it up once the writer finishes the codepoint.
            text = chunk.decode("utf-8", errors="replace")
        click.echo(text, nl=False)
    return new_pos


@click.command("logs")
@click.option(
    "--output",
    "output_dir",
    type=click.Path(path_type=Path, file_okay=False),
    required=True,
    help=(
        "Directory containing execution-log.jsonl / execution-log.md. "
        "Typically the same directory passed to ``swarm run --output``."
    ),
)
@click.option(
    "--job",
    "job_id",
    type=str,
    default=None,
    help=(
        "Optional job_id to verify against ``.swarm-state.json``. When "
        "set, a mismatch with the state's recorded job_id is surfaced "
        "as EXIT_USAGE so a wrong-directory invocation fails loudly. A "
        "missing state file is tolerated (logs may exist for a partial "
        "run that never reached the state-write stage)."
    ),
)
@click.option(
    "--jsonl/--md",
    "use_jsonl",
    default=False,
    show_default=True,
    help=(
        "Use the JSONL canonical surface (--jsonl) or the Markdown "
        "human-readable surface (--md, default). The two files share "
        "the same record stream so the choice is purely cosmetic -- "
        "use --jsonl when piping into ``jq`` or downstream parsers."
    ),
)
@click.option(
    "--follow",
    "-f",
    "follow",
    is_flag=True,
    default=False,
    help=(
        "Live-tail the log file: poll on --watch-interval seconds and "
        "emit appended lines until the job reaches terminal state or "
        "the operator interrupts (Ctrl-C). Default is one-shot dump."
    ),
)
@click.option(
    "--tail",
    "tail_shortcut",
    is_flag=True,
    default=False,
    help=(
        "Shorthand for ``--jsonl --follow``: live-tail the canonical "
        "JSONL surface. Matches the AC wording 'tails JSONL' so the "
        "common monitoring invocation is one flag instead of two."
    ),
)
@click.option(
    "--lines",
    "lines_tail",
    type=click.IntRange(min=1),
    default=None,
    help=(
        "Show only the last N lines of the log (instead of the full "
        "file). Applies to both one-shot dump and the seed phase of "
        "--follow. Omit to dump the entire log."
    ),
)
@click.option(
    "--watch-interval",
    "watch_interval",
    type=click.FloatRange(min=0.01),
    default=0.5,
    show_default=True,
    help="Seconds between polls when --follow / --tail is set.",
)
@click.option(
    "--watch-max-iterations",
    "watch_max_iterations",
    type=click.IntRange(min=1),
    default=None,
    help=(
        "Optional ceiling on poll iterations under --follow / --tail. "
        "Primarily a test-surface lever; production callers omit it so "
        "the loop runs until terminal state or KeyboardInterrupt."
    ),
)
def logs_cmd(
    output_dir: Path,
    job_id: Optional[str],
    use_jsonl: bool,
    follow: bool,
    tail_shortcut: bool,
    lines_tail: Optional[int],
    watch_interval: float,
    watch_max_iterations: Optional[int],
) -> None:
    """Dump or tail a swarm job's execution log (T07.05 / FR-003).

    Reads ``<output_dir>/execution-log.md`` (default) or
    ``<output_dir>/execution-log.jsonl`` (``--jsonl``). One-shot dump is
    the default; ``--follow`` / ``--tail`` polls for appended lines
    until the job reaches terminal state or the operator interrupts.

    Modes:

        * default          -- dump execution-log.md to stdout.
        * ``--jsonl``      -- dump execution-log.jsonl to stdout.
        * ``--follow``     -- live-tail the selected surface (default
                              md unless ``--jsonl`` also set).
        * ``--tail``       -- shorthand for ``--jsonl --follow``.

    The ``--lines N`` option caps the dump (and the follow-mode seed)
    to the last N lines so operators can sample a long log without
    flooding the terminal.

    Exit codes:

        * 0 -- log read successfully OR follow loop exited cleanly
          (terminal state, max-iterations, or Ctrl-C).
        * 2 -- usage error: ``--output`` missing, log file missing,
          ``--job`` mismatch.
    """
    output_path = Path(output_dir)

    if not output_path.is_dir():
        click.echo(
            f"swarm logs: output directory not found: {output_path}",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)

    # ``--tail`` is the convenience shorthand. Resolve it to the
    # underlying flags so the rest of the function has a single
    # mode-decision surface (use_jsonl + follow).
    if tail_shortcut:
        use_jsonl = True
        follow = True

    job_mismatch = _validate_job_id(output_path, job_id)
    if job_mismatch is not None:
        click.echo(job_mismatch, err=True)
        raise click.exceptions.Exit(EXIT_USAGE)

    log_filename = (
        EXECUTION_LOG_JSONL_FILENAME if use_jsonl else EXECUTION_LOG_MD_FILENAME
    )
    log_path = output_path / log_filename

    if follow:
        exit_code = _follow_log(
            output_path,
            log_path,
            lines_tail=lines_tail,
            watch_interval=watch_interval,
            watch_max_iterations=watch_max_iterations,
        )
        raise click.exceptions.Exit(exit_code)

    if not log_path.is_file():
        click.echo(
            f"swarm logs: log file not found: {log_path}",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)

    exit_code = _dump_log_file(log_path, lines_tail)
    raise click.exceptions.Exit(exit_code)


# ---------------------------------------------------------------------------
# T07.07 / FR-004 -- ``superclaude swarm attach`` subcommand.
#
# ``attach_cmd`` is the COMP-014 operator surface for re-attaching to a
# detached tmux job launched via ``swarm run --detached`` (T07.11). It is
# a thin Click wrapper over :func:`tmux.attach`:
#
#     1. Validate tmux is available (``shutil.which`` + nested-session
#        check). Missing tmux is an operator-configuration error (the
#        job could not have been launched detached on this host) and
#        surfaces as EXIT_USAGE.
#     2. Probe for the live session via ``tmux.has_session(job_id)``. A
#        missing session is the AC "exits gracefully" branch: emit a
#        single grep-friendly stderr line and exit 0 so a script that
#        wraps ``swarm attach`` after ``swarm run`` does not error out
#        when the job has already terminated.
#     3. Delegate to :func:`tmux.attach`, which calls ``tmux
#        attach-session`` synchronously and blocks until the operator
#        detaches or the session ends. The tmux subprocess return code
#        propagates through to ``attach_cmd``'s exit code so an upstream
#        wrapper can distinguish "operator detached" (0) from "tmux
#        attach errored" (non-zero from tmux itself).
#
# Exit codes:
#
#     * 0 -- attached cleanly (tmux returned 0), OR session not present
#       (graceful no-op per AC: "Exits gracefully if no detached session
#       present").
#     * non-zero -- tmux returned a non-zero exit from attach-session
#       (propagated verbatim).
#     * 2 -- usage error: tmux not installed / nested tmux session.
#
# The positional ``JOB_ID`` matches the validation example in the task
# row (``swarm attach <id>``); :func:`tmux.session_name` validates the
# tmux-illegal characters before any subprocess fires, so a malformed
# job_id surfaces as EXIT_USAGE with a clear diagnostic instead of an
# opaque tmux complaint.
# ---------------------------------------------------------------------------


@click.command("attach")
@click.argument("job_id", type=str, required=True)
def attach_cmd(job_id: str) -> None:
    """Re-attach to a detached swarm tmux session (T07.07 / FR-004).

    Looks up the live ``swarm-<JOB_ID>`` tmux session, then runs
    ``tmux attach-session`` synchronously so the operator's terminal is
    re-bound to the detached job. Blocks until the operator detaches
    (Ctrl-b d by default) or the session ends.

    Exit codes:

        * 0 -- attached and detached cleanly, OR no live session for
          ``JOB_ID`` (graceful no-op so wrapper scripts can poll without
          erroring).
        * non-zero -- propagated from the tmux ``attach-session``
          subprocess when tmux itself reports a failure.
        * 2 -- usage error: tmux is not installed or the caller is
          already nested inside a tmux session, OR ``JOB_ID`` carries
          tmux-illegal characters.
    """
    # Import inside the function so the module-load surface stays light
    # for ``validate`` / ``validate-lenses`` invocations on hosts that
    # never touch the tmux integration.
    from superclaude.cli.swarm import tmux as swarm_tmux

    # Validate JOB_ID shape before any tmux call so a malformed id is
    # surfaced as a usage error rather than an opaque tmux complaint.
    try:
        target = swarm_tmux.session_name(job_id)
    except ValueError as exc:
        click.echo(f"swarm attach: invalid job_id: {exc}", err=True)
        raise click.exceptions.Exit(EXIT_USAGE)

    if not swarm_tmux.is_tmux_available():
        click.echo(
            "swarm attach: tmux is not available "
            "(missing on PATH or already nested inside a tmux session); "
            "detached jobs require tmux",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)

    if not swarm_tmux.has_session(job_id):
        # AC: "Exits gracefully if no detached session present." A
        # missing session is reported on stderr (so the stdout stream
        # stays clean for any subsequent pipeline stage) and exits 0.
        click.echo(
            f"swarm attach: no live tmux session for job_id={job_id!r} "
            f"(looked for {target!r})",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_OK)

    try:
        rc = swarm_tmux.attach(job_id)
    except swarm_tmux.TmuxUnavailableError as exc:
        # Race: tmux disappeared between is_tmux_available() and
        # attach(). Surface as EXIT_USAGE for symmetry with the
        # pre-flight check.
        click.echo(f"swarm attach: {exc}", err=True)
        raise click.exceptions.Exit(EXIT_USAGE)
    except swarm_tmux.TmuxSessionMissingError as exc:
        # Race: session ended between has_session() and attach().
        # Treat as the graceful "no session" branch.
        click.echo(f"swarm attach: {exc}", err=True)
        raise click.exceptions.Exit(EXIT_OK)

    raise click.exceptions.Exit(rc)


# ---------------------------------------------------------------------------
# T07.08 / FR-005 -- ``superclaude swarm kill`` subcommand.
#
# ``kill_cmd`` is the COMP-014 operator surface for terminating a
# detached tmux job launched via ``swarm run --detached`` (T07.11). It
# layers three concerns on top of :func:`tmux.kill`:
#
#     1. tmux session termination -- :func:`tmux.kill` is idempotent
#        on its own; calling it on a missing session returns False
#        rather than raising.
#     2. Terminal state write -- when ``--output`` is supplied, the
#        run's ``.swarm-state.json`` is flipped to ``state="terminal"``
#        via the same atomic :func:`write_state` writer the executor
#        uses, so a polling reader (``swarm status``) observes the
#        killed state without any partial-file window.
#     3. Done sentinel emission -- ``done.json`` is written via
#        tmp+os.replace with ``terminal_status="killed"``. This is the
#        signal the FR-029 polling pattern (``until [ -f done.json ]``)
#        consumes. The shape mirrors :class:`models.DoneSentinel` but
#        the writer bypasses the dataclass: ``ResultStatus`` (locked to
#        ``success`` / ``partial`` / ``failed`` by T01.25) does NOT
#        admit ``killed`` because a kill is operator-initiated, not an
#        IMM-5 reduction outcome.
#
# Exit codes:
#
#     * 0 -- session terminated cleanly OR no session was present
#       (idempotent no-op per the AC "Idempotent (kill twice no-op)").
#     * 2 -- usage error: tmux not installed / nested tmux session,
#       JOB_ID carries tmux-illegal characters, or ``--output`` points
#       at an existing non-directory.
#
# Idempotency: a second ``swarm kill`` invocation against the same
# job_id finds no live tmux session AND finds the state already
# terminal AND finds ``done.json`` already on disk. The state writer
# becomes a no-op transition (still atomically re-stamps the
# ``updated`` field, which is a desirable refresh) and the done
# sentinel writer skips overwrite when the target already exists --
# preserving byte-for-byte equality of the first sentinel.
# ---------------------------------------------------------------------------


def _emit_killed_done_sentinel(output_dir: Path) -> Path:
    """Atomically write ``done.json`` with ``terminal_status="killed"``.

    Idempotent on rerun: when the target already exists, the writer is
    a no-op and the existing bytes are preserved. This keeps the AC
    "Idempotent (kill twice no-op)" honest -- a second kill leaves the
    first sentinel intact rather than rewriting it with a fresh
    timestamp.

    The shape mirrors :class:`models.DoneSentinel` (DM-017) field set
    so a future :func:`reduce.emit_done_sentinel` consumer can parse
    both flavours uniformly. ``contract_path`` is the empty string
    because killed jobs do not produce a :class:`ResultContract` --
    the executor was interrupted before reduce could emit one.

    Uses the tmp + :func:`os.replace` idiom (IMM-6 / NFR-002) so a
    mid-write kill leaves no partial sentinel. The matching
    enforcement test lives in ``tests/swarm/test_imm6_atomic_write.py``
    which sweeps the swarm package for any line writing ``done.json``
    without ``os.replace(`` in the same module.
    """
    import os as _os

    target = output_dir / DONE_SENTINEL_FILENAME
    if target.is_file():
        # Idempotent: preserve the first sentinel's bytes verbatim.
        return target

    payload = {
        "atomic_write": True,
        "terminal_status": KILLED_TERMINAL_STATUS,
        "contract_path": "",
    }
    body = json.dumps(payload, sort_keys=True, indent=2) + "\n"
    tmp = target.with_suffix(target.suffix + ".tmp")
    tmp.write_text(body, encoding="utf-8")
    _os.replace(tmp, target)
    return target


def _write_killed_terminal_state(output_dir: Path, job_id: str) -> None:
    """Flip ``.swarm-state.json`` to ``state="terminal"`` for the killed job.

    When the state file is absent (kill invoked before the executor
    wrote one) a stub is materialised so ``swarm status`` still has a
    consistent terminal record to read. When the existing state's
    ``job_id`` mismatches the kill target the state is overwritten --
    the operator deliberately invoked ``swarm kill JOB_ID --output
    DIR``, naming both halves; the kill flow trusts that pairing over
    the on-disk record.
    """
    from superclaude.cli.swarm.state import read_state, write_state

    state_path = output_dir / SWARM_STATE_FILENAME
    try:
        existing = read_state(state_path)
    except (json.JSONDecodeError, ValueError):
        # Corrupt prior state must not block the kill flow; rewrite it
        # with a fresh terminal stub so the artifact set stays
        # consistent for downstream readers.
        existing = None

    if existing is not None and existing.state == TERMINAL_STATE_VALUE:
        # Already terminal: refresh the ``updated`` stamp atomically
        # but keep the recorded job_id (the executor's record wins
        # when the state already reached terminal naturally).
        # F-P3-3 -- confine the write to the ``--output`` root (NFR-013 /
        # AC-014) so the kill flow cannot escape the directory it was given.
        write_state(state_path, existing, output_dir=output_dir)
        return

    # F-P3-3 -- output-confined terminal write (see above).
    write_state(
        state_path,
        SwarmState(state=TERMINAL_STATE_VALUE, job_id=job_id),
        output_dir=output_dir,
    )


@click.command("kill")
@click.argument("job_id", type=str, required=True)
@click.option(
    "--output",
    "output_dir",
    type=click.Path(path_type=Path, file_okay=False),
    default=None,
    help=(
        "Directory carrying the killed job's observability artifacts. "
        "When supplied, the kill flow flips ``.swarm-state.json`` to "
        "``state=terminal`` and emits ``done.json`` with "
        "``terminal_status=killed`` so polling consumers (the FR-029 "
        "``until [ -f done.json ]`` pattern) observe the terminated "
        "job. When omitted, only the tmux session is torn down."
    ),
)
def kill_cmd(job_id: str, output_dir: Optional[Path]) -> None:
    """Terminate a detached swarm tmux session (T07.08 / FR-005).

    Tears down the live ``swarm-<JOB_ID>`` tmux session via
    :func:`tmux.kill`. When ``--output`` is supplied, also writes the
    terminal-state artifacts (``.swarm-state.json`` flipped to
    ``terminal``; ``done.json`` carrying ``terminal_status=killed``)
    so the three-layer durable monitoring set (NFR-004) stays
    consistent across the four artifacts.

    Exit codes:

        * 0 -- session terminated cleanly OR no live session was
          present (the AC "Idempotent (kill twice no-op)" branch --
          calling kill on an already-terminated job is a clean no-op).
        * 2 -- usage error: tmux is not installed, the caller is
          already nested inside a tmux session, ``JOB_ID`` carries
          tmux-illegal characters, or ``--output`` points at a
          non-directory.
    """
    # Lazy import keeps the module-load surface light for
    # ``validate`` / ``validate-lenses`` callers that never touch the
    # tmux integration.
    from superclaude.cli.swarm import tmux as swarm_tmux

    # Validate JOB_ID shape before any tmux subprocess fires so a
    # malformed id surfaces as EXIT_USAGE with a clear diagnostic
    # rather than an opaque tmux complaint downstream.
    try:
        target_name = swarm_tmux.session_name(job_id)
    except ValueError as exc:
        click.echo(f"swarm kill: invalid job_id: {exc}", err=True)
        raise click.exceptions.Exit(EXIT_USAGE)

    if not swarm_tmux.is_tmux_available():
        click.echo(
            "swarm kill: tmux is not available "
            "(missing on PATH or already nested inside a tmux session); "
            "detached jobs require tmux",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)

    try:
        killed = swarm_tmux.kill(job_id)
    except swarm_tmux.TmuxUnavailableError as exc:
        # Race: tmux disappeared between is_tmux_available() and kill().
        click.echo(f"swarm kill: {exc}", err=True)
        raise click.exceptions.Exit(EXIT_USAGE)

    if killed:
        click.echo(
            f"swarm kill: terminated tmux session {target_name!r} "
            f"for job_id={job_id!r}",
            err=True,
        )
    else:
        # AC "Idempotent (kill twice no-op)" branch: no live session.
        # Report on stderr so stdout stays clean for any downstream
        # pipeline stage, and still flow through the terminal-state
        # writes when --output is supplied so the observability
        # artifact set remains consistent.
        click.echo(
            f"swarm kill: no live tmux session for job_id={job_id!r} "
            f"(looked for {target_name!r}); treating as already-terminated",
            err=True,
        )

    if output_dir is not None:
        # ``click.Path(file_okay=False)`` already rejected an existing
        # regular file; materialise the directory tree so the writers
        # below can target it without a prior ``mkdir -p``.
        output_dir.mkdir(parents=True, exist_ok=True)
        _write_killed_terminal_state(output_dir, job_id)
        _emit_killed_done_sentinel(output_dir)

    raise click.exceptions.Exit(EXIT_OK)


# ---------------------------------------------------------------------------
# T07.09 / FR-006 -- ``swarm scaffold`` subcommand.
#
# Emits a fully-populated starter JobSpec for the named lens so operators
# get a valid baseline they can edit (target.path, output.dir, model IDs,
# transport env contract) instead of authoring the DM-001 surface from
# scratch. Reuses :func:`_build_spec_from_lens` -- the same helper the
# ``swarm run --lens`` shortcut path uses -- so the scaffold output is
# byte-identical to what a bare ``swarm run --lens NAME`` would synthesize
# internally; a single helper guarantees scaffold-then-validate-then-run
# stays consistent without duplicating lens-defaulting logic.
#
# Output mode:
#
#     * Default -- pretty-printed JSON emitted to stdout so operators can
#       pipe straight into ``swarm validate`` or redirect to a file with
#       their shell of choice.
#     * ``--output PATH`` -- write the JSON document to ``PATH`` atomically
#       (tmp + ``os.replace``) so partial writes never leave a malformed
#       spec on disk. A confirmation line lands on stderr so stdout stays
#       clean for callers that combine the flag with a piped consumer.
#
# Lens guards:
#
#     * ``custom`` is rejected with :data:`EXIT_USAGE` -- the FR-021
#       escape hatch has no registry defaults to expand from; its prompts
#       flow in from ``--custom-prompt-dir`` at preflight, so a starter
#       spec for ``custom`` is meaningless.
#     * Unknown lens names are rejected with :data:`EXIT_USAGE` and the
#       list of well-known non-custom lenses, mirroring the
#       ``swarm run --lens`` diagnostic so operators learn one error
#       shape for both surfaces.
# ---------------------------------------------------------------------------


def _scaffold_spec_payload(lens_name: str) -> str:
    """Render the starter JobSpec for ``lens_name`` as pretty JSON text.

    Pretty-printing (2-space indent, trailing newline) is chosen so the
    emitted document is human-editable straight out of the box --
    scaffold output is meant to be opened in ``$EDITOR``, not stored
    compactly. The trailing newline matches POSIX text-file conventions
    so the file plays nicely with version control and ``cat``.
    """
    spec = _build_spec_from_lens(lens_name)
    return json.dumps(spec, indent=2, sort_keys=False) + "\n"


def _write_scaffold_atomic(output_path: Path, payload: str) -> None:
    """Atomic-write ``payload`` to ``output_path`` via ``tmp + os.replace``.

    Mirrors the atomic-write discipline used elsewhere in the swarm
    surface (NFR-002 / DM-014 state writes) so an interrupted scaffold
    never leaves a half-written file on disk. The temp file lives in the
    same directory as the target so ``os.replace`` is guaranteed to be
    atomic (same-filesystem rename).
    """
    import os
    import tempfile

    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{output_path.name}.",
        suffix=".tmp",
        dir=str(output_path.parent),
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(payload)
        os.replace(tmp_path, output_path)
    except BaseException:
        # Best-effort cleanup; surface the original exception to the caller.
        try:
            tmp_path.unlink()
        except FileNotFoundError:
            pass
        raise


@click.command("scaffold")
@click.option(
    "--lens",
    "lens_name",
    type=str,
    required=True,
    help=(
        "Lens to scaffold a starter JobSpec for (e.g. bare-review). "
        "Expands lens defaults (system/user prompts, recipe, workers, "
        "line_cap, next-command template) into a full DM-001 JobSpec "
        "the operator can edit. ``custom`` and unknown lens names are "
        "rejected -- ``custom`` is the FR-021 escape hatch whose prompts "
        "flow in from --custom-prompt-dir at preflight, so it has no "
        "registry defaults to expand from."
    ),
)
@click.option(
    "--output",
    "-o",
    "output_path",
    type=click.Path(dir_okay=False, path_type=Path),
    default=None,
    help=(
        "Write the starter JobSpec to PATH atomically (tmp + os.replace). "
        "When omitted, the JSON document is emitted to stdout so it can "
        "be piped straight into ``swarm validate`` or redirected with "
        "the shell of choice."
    ),
)
def scaffold_cmd(lens_name: str, output_path: Optional[Path]) -> None:
    """Emit a starter JobSpec for the named lens (FR-006 / T07.09).

    Generates a fully-populated DM-001 JobSpec for ``--lens NAME`` so
    operators have a valid baseline they can edit instead of authoring
    the spec from scratch. The emitted spec passes ``swarm validate``
    out of the box -- the only fields the operator MUST override before
    invoking ``swarm run`` are ``target.path`` (placeholder ``""``) and
    ``output.dir`` (placeholder ``""``). Model IDs are filled with
    ``lens-default-model-<i>`` placeholders that schema-validate but
    never reach the wire (the transport defaults to ``stub`` for the
    same safe-quick-dispatch reasoning as ``swarm run --lens``).

    Exit codes:

        * 0 -- starter spec rendered successfully (to stdout, or to
          ``--output`` when supplied).
        * 2 -- usage error: lens unknown, lens is the ``custom`` escape
          hatch (no registry defaults to expand from), or ``--output``
          path is unwritable.
    """
    # ``custom`` is the FR-021 escape hatch: prompts flow in from
    # --custom-prompt-dir at preflight, so the registry carries no
    # defaults to expand from. Reject explicitly so operators learn the
    # same diagnostic shape ``swarm run --lens custom`` produces.
    if lens_name == "custom":
        click.echo(
            "swarm scaffold: --lens custom is not scaffoldable (FR-021 "
            "escape hatch); author a spec by hand with custom_prompt_dir "
            "set and validate via ``swarm validate``",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)

    if lens_name not in LENSES:
        known = ", ".join(n for n in LENS_NAMES if n != "custom")
        click.echo(
            f"swarm scaffold: unknown lens {lens_name!r}; "
            f"known lenses: {known}",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)

    payload = _scaffold_spec_payload(lens_name)

    if output_path is None:
        # Stdout mode -- the JSON document is the entire stdout payload
        # so pipelines (``swarm scaffold --lens NAME | swarm validate ...``)
        # see a clean JSON stream. ``click.echo`` adds its own newline,
        # but the payload already terminates with ``\n``; pass
        # ``nl=False`` so the document is not double-newline-terminated.
        click.echo(payload, nl=False)
        raise click.exceptions.Exit(EXIT_OK)

    try:
        _write_scaffold_atomic(output_path, payload)
    except OSError as exc:
        click.echo(
            f"swarm scaffold: cannot write {output_path}: {exc}",
            err=True,
        )
        raise click.exceptions.Exit(EXIT_USAGE)

    # Confirmation lands on stderr so stdout stays clean for callers
    # that combine ``--output`` with a piped consumer.
    click.echo(
        f"swarm scaffold: wrote starter spec for lens "
        f"{lens_name!r} to {output_path}",
        err=True,
    )
    raise click.exceptions.Exit(EXIT_OK)
