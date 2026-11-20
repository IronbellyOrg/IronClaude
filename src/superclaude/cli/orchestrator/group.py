"""The click group ``superclaude orchestrator`` (design 5.1, decision ADD6).

The deterministic steps of the orchestrator skill are verbs of this group, so a
step that needs no model is code and not prose. Each verb lives in its own module
and is added below; a later piece adds its own line and its own module.

Two modules of the package are not verbs: ``limits`` (the refusal of 5.9) and
``names`` (the naming rule of 5.12). Every verb that runs ``gh``, ``git`` or
``orca`` does it through ``limits.GuardedRunner``.
"""

from __future__ import annotations

from pathlib import Path

import click

from .answer_check import answer_check_cmd
from .common import ROOT_ENV
from .idle_end import idle_end_cmd
from .lease import lease_group
from .plan_check import plan_check_cmd
from .repos_verb import repos_group
from .state_verb import state_group
from .wake_ack import wake_ack_cmd
from .wake_check import wake_check_cmd


@click.group(name="orchestrator")
@click.option(
    "--root",
    type=click.Path(file_okay=False, path_type=Path),
    envvar=ROOT_ENV,
    default=None,
    help="The orchestrator repo, the folder that holds .orchestrator/ "
    "(default: the current directory).",
)
@click.pass_context
def orchestrator_group(ctx: click.Context, root: Path | None) -> None:
    """The deterministic steps of /sc:orchestrator (state, and the verbs added to it)."""
    ctx.obj = {"root": root}


orchestrator_group.add_command(state_group)
orchestrator_group.add_command(wake_check_cmd)
orchestrator_group.add_command(wake_ack_cmd)
orchestrator_group.add_command(lease_group)
orchestrator_group.add_command(repos_group)
orchestrator_group.add_command(answer_check_cmd)
orchestrator_group.add_command(plan_check_cmd)
orchestrator_group.add_command(idle_end_cmd)
