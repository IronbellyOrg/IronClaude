"""cliEval canonical exit codes (design-spec §4 hierarchy).

All eval-module exit-code constants re-export from this module via descriptive
local names. If design-spec §4 conventions ever shift, the value change is a
one-file edit here, propagating to every re-export site.

Per CC2 / OQ-2 — exactly 4 canonical values. The descriptive ``*_EXIT_CODE``
names that consumers import are single-line re-exports defined alongside the
classes/functions they accompany, so locality-of-naming is preserved at each
call site.

Note on INTERRUPTED value: design-spec §4 (mirrored in
``tests/cli/eval/test_exit_codes.py`` docstring + ``signal_handler.EXIT_INTERRUPTED``)
pins interrupted = ``3``, not the POSIX signal+128 = 130 convention. The two
are conceptually equivalent (both mean "killed by signal") but the cliEval
process boundary is a documented ``3``. We track the codebase contract here.
"""

from __future__ import annotations

SUCCESS: int = 0
FAILURES: int = 1            # one or more eval failures
USAGE_ERROR: int = 2         # operator misuse / config / harness contract error
INTERRUPTED: int = 3         # SIGINT / SIGTERM cooperative cancellation
