"""A test-only failpoint for the restart test T5 (design 9.2; open question Q11).

T5 kills an orchestrator in the middle of each wave and checks that nothing is
done twice. To stop at an exact place, ``superclaude orchestrator state intent``
can end the process right after it has written an ``intent`` line and before it
prints anything, which leaves an ``intent`` with no ``done`` (design 5.5, rule 2).

The guard, stated once:

* the hook does nothing unless the environment variable
  ``SUPERCLAUDE_TEST_FAILPOINTS`` is exactly ``1``, and the variable
  ``SUPERCLAUDE_FAILPOINT`` names the place. A production session sets neither;
  the skill text never mentions them;
* there is one call site, in the ``state intent`` verb, after the line is saved,
  so the hook never changes what is written; it only ends the process;
* ``SUPERCLAUDE_FAILPOINT`` is ``after_intent`` (any step), ``after_intent:<step>``
  or ``after_intent:<wave>:<step>``;
* the process ends with exit code ``EXIT_CODE`` (86) through ``os._exit``, the way
  a killed session ends: no cleanup, no output on stdout.
"""

from __future__ import annotations

import os
import sys
from collections.abc import Callable, Mapping
from typing import Final

ENABLE_VAR: Final = "SUPERCLAUDE_TEST_FAILPOINTS"
POINT_VAR: Final = "SUPERCLAUDE_FAILPOINT"
EXIT_CODE: Final = 86
_POINT: Final = "after_intent"


def active_for(wave: int, step: str, env: Mapping[str, str]) -> bool:
    """True when the environment asks to stop after the intent line of ``wave``/``step``."""
    if env.get(ENABLE_VAR) != "1":
        return False
    name, *rest = env.get(POINT_VAR, "").split(":")
    if name != _POINT:
        return False
    if not rest:
        return True
    if len(rest) == 1:
        return rest[0] == step
    return len(rest) == 2 and rest[0] == str(wave) and rest[1] == step


def after_intent(
    wave: int,
    step: str,
    *,
    env: Mapping[str, str] | None = None,
    stop: Callable[[int], object] = os._exit,
) -> None:
    """End the process now when the failpoint is set for this intent line."""
    if active_for(wave, step, os.environ if env is None else env):
        sys.stderr.write("failpoint: stopped after an intent line\n")
        sys.stderr.flush()
        stop(EXIT_CODE)
