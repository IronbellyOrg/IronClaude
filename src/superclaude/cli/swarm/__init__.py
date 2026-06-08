"""Swarm CLI module -- multi-model swarm orchestration.

Exposes the ``swarm_group`` Click group registered as the top-level
``superclaude swarm`` verb (AC-002). Subcommand placeholders land in
T01.08; the Click group itself is intentionally minimal here so the
registration test (T01.02) can lock in top-level placement before the
Click adoption task (T01.04) wires real options.

Module shape mirrors ``cli/sprint/`` (AC-003 / NFR-015) so operators
who know the sprint layout can navigate the swarm tree without a
second mental model. Counterparts:

    cli/sprint/commands.py    -> cli/swarm/commands.py
    cli/sprint/config.py      -> cli/swarm/config.py
    cli/sprint/models.py      -> cli/swarm/models.py
    cli/sprint/logging_.py    -> cli/swarm/logging_.py
    cli/sprint/tmux.py        -> cli/swarm/tmux.py
    cli/sprint/tui.py         -> cli/swarm/tui.py
    cli/sprint/preflight.py   -> cli/swarm/preflight.py
        (T02.02 -- shared name, divergent concrete roles. Sprint:
        phase-step subprocess executor. Swarm: Wave 0 gate that runs
        schema validation, lens resolution + materialization, and the
        §11.5 / IMM-4 / INV-005 / INV-007 guards before emitting the
        Manifest. Both share the "pre-execution validation" abstract
        role so they occupy the same counterpart slot.)

Documented divergences (swarm-specific, no sprint analogue):

* ``state.py`` -- carries DM-014 ``SwarmState`` and DM-015
  ``EventRecord`` persistence. Sprint folds run-state into
  ``executor.py``; swarm separates it because resume (M6) reads it
  independently.
* ``schema.py`` -- DM-001 JobSpec JSON Schema + §11.5 cross-field
  validators (Wave 0 preflight gate; COMP-005 / T02.01). Sprint has
  no equivalent because its tasklist surface is bespoke MDTM, not a
  schema-validated job spec.
* ``dispatch.py`` -- COMP-007 Wave 1 dispatcher (T03.01 wiring +
  reference body; T03.02 replaces with the
  :class:`ParallelExecutor`-driven fan-out per AC-004 / NFR-001 /
  IMM-3). Sprint routes phases sequentially through ``executor.py``,
  so there is no parity file.
* ``normalize.py`` -- COMP-008 Wave 2 normalize dispatcher (T04.01).
  Selects a recipe from ``recipes.REGISTRY`` per
  ``NormalizationSpec.recipe``, applies it per worker, writes the
  normalized body atomically to ``final_path`` and the provenance
  meta sidecar to ``meta_path``. Sprint has no amalgamation step, so
  there is no parity file.
* ``reduce.py`` -- COMP-009 Wave 3 reduce orchestrator (T05.01).
  Runs IMM-5 success-first status determination, dispatches over the
  three :data:`AmalgamationMode` values (raw / normalize /
  normalize+merge), invokes the mechanical merge module (T05.02) on
  ``normalize+merge`` runs when M >= ``StatusPolicy.floor``, and emits
  the final :class:`ResultContract` (DM-012) to ``return-contract.yaml``
  atomically. Sprint has no reduce/contract step, so there is no
  parity file.
* ``merge.py`` -- COMP-010 mechanical merge module (T05.02 / FR-012).
  ``normalize+merge`` mode's sole concat surface: orders ``WorkerResult``
  sections by slot index and prepends one ``## From {model_label}
  ({elapsed_ms}ms)`` provenance header per section. Body capped at
  <=30 LOC (NFR-008 / T05.08) and protected by four structural guards
  (docstring contract, LOC ceiling test, PR-review discipline,
  3-worker boundary test -- see ``merge.py`` docstring). All scoring /
  ranking / dedup / rewrite stays in ``/sc:adversarial``; sprint has
  no merge counterpart.
* ``transports/`` -- swarm fans a prompt across heterogeneous workers,
  so a Transport Protocol + concrete impls (openai_compat, stub) live
  in a sub-package. Sprint shells out via ``process.py`` instead.
* ``lenses/`` -- swarm registers the eight LensEntry records (DM-010);
  sprint has no lens concept.
* ``recipes/`` -- normalization recipe modules (DM-006); sprint has no
  amalgamation step.

Documented sprint-only files with no swarm analogue (and why):

* ``executor.py`` -- swarm uses a fan-out worker pool driven by the
  transport layer, not a phased step executor.
* ``monitor.py``, ``summarizer.py``, ``checkpoints.py``,
  ``retrospective.py``, ``classifiers.py``, ``diagnostics.py``,
  ``debug_logger.py``, ``kpi.py``, ``notify.py``, ``process.py`` --
  sprint-specific phasing / KPI / shell-out concerns that the swarm
  ResultContract (DM-012), Manifest (DM-016), and DoneSentinel
  (DM-017) replace end-to-end.
"""

from __future__ import annotations

import click

# AC-006 (T01.04): pyproject pins ``click>=8.0.0``. The decorator
# ``@click.group(...)`` returns a ``click.Group`` instance, satisfying
# the spec wording ``swarm_group = click.Group(...)`` while keeping the
# idiomatic Click 8 form. ``context_settings`` adds the standard
# ``-h`` alias and lets subcommands inherit help-option naming.
_SWARM_CONTEXT_SETTINGS: dict[str, object] = {
    "help_option_names": ["-h", "--help"],
    "max_content_width": 100,
}


@click.group("swarm", context_settings=_SWARM_CONTEXT_SETTINGS)
def swarm_group() -> None:
    """Orchestrate multi-model swarm execution.

    Fan a single prompt across N heterogeneous OpenAI-compatible workers,
    normalize and amalgamate results through lens recipes, and emit a
    caller-facing ResultContract. See ``docs/swarm/`` for the full
    specification.
    """


# ---------------------------------------------------------------------------
# Subcommand placeholders (T01.08 / COMP-001).
#
# Eight placeholder subcommands land here so ``superclaude swarm --help``
# advertises the operator surface from M1 onward while each milestone's
# real implementation lands in later phases:
#
#   run               -- fan a prompt across N workers (M3-M4)
#   status            -- inspect SwarmState for a job_id (M3)
#   logs              -- tail the JSONL event log (M3)
#   attach            -- reattach to a detached tmux job (M7)
#   kill              -- terminate a running job (M7)
#   scaffold          -- write starter JobSpec / lens files (M2)
#   validate          -- schema-check a JobSpec file (M2)
#   validate-lenses   -- schema-check LENSES dict + template fragments (M2)
#
# Each placeholder echoes a clear "not yet implemented" message on stderr
# and exits with a non-zero code (2), so tests and operators catch
# premature invocation. ``--help`` still renders normally because Click
# only runs the callback after argument parsing succeeds.
# ---------------------------------------------------------------------------

assert isinstance(swarm_group, click.Group), (
    "swarm_group must be a click.Group instance for AC-006 compliance"
)


_PLACEHOLDER_EXIT_CODE = 2


def _not_yet_implemented(subcommand: str) -> None:
    """Echo a uniform "not yet implemented" notice and exit non-zero."""
    click.echo(
        f"superclaude swarm {subcommand}: not yet implemented",
        err=True,
    )
    raise click.exceptions.Exit(_PLACEHOLDER_EXIT_CODE)


# T02.19 (FR-007) / T02.20 (FR-008) / T03.01 (FR-001) / T07.04 (FR-002) /
# T07.05 (FR-003) / T07.07 (FR-004) / T07.08 (FR-005) / T07.09 (FR-006) --
# the ``validate``, ``validate-lenses``, ``run``, ``status``, ``logs``,
# ``attach``, ``kill``, and ``scaffold`` placeholders have been replaced
# by the real implementations in ``commands.py``. Imported here at module
# load so ``swarm_group.commands["validate"]`` / ``["validate-lenses"]`` /
# ``["run"]`` / ``["status"]`` / ``["logs"]`` / ``["attach"]`` /
# ``["kill"]`` / ``["scaffold"]`` resolve to the concrete commands for
# ``--help`` discovery and CLI dispatch. The imports live at the bottom
# of the file to keep the placeholder block above contiguous;
# ``commands.py`` does not import from ``__init__.py``, so this is acyclic.
from superclaude.cli.swarm.commands import (  # noqa: E402
    attach_cmd,
    kill_cmd,
    logs_cmd,
    run_cmd,
    scaffold_cmd,
    status_cmd,
    validate_cmd,
    validate_lenses_cmd,
)

swarm_group.add_command(attach_cmd, name="attach")
swarm_group.add_command(kill_cmd, name="kill")
swarm_group.add_command(logs_cmd, name="logs")
swarm_group.add_command(run_cmd, name="run")
swarm_group.add_command(scaffold_cmd, name="scaffold")
swarm_group.add_command(status_cmd, name="status")
swarm_group.add_command(validate_cmd, name="validate")
swarm_group.add_command(validate_lenses_cmd, name="validate-lenses")


# Names registered in this module -- consumed by the T01.08 placement test.
_PLACEHOLDER_SUBCOMMANDS: tuple[str, ...] = (
    "run",
    "status",
    "logs",
    "attach",
    "kill",
    "scaffold",
    "validate",
    "validate-lenses",
)


__all__ = ["swarm_group"]
