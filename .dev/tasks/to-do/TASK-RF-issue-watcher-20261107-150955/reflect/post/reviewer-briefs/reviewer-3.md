# Reviewer brief 3 (persona lens: refactorer / structure, duplication, boundaries, security hygiene)

## T1 card excerpt

(Verbatim slice of the Tier-1 card, "Structural and tech-debt". Unverified claims; confirm or refute.)

#### Structural and tech-debt (card section)

- **Module boundaries:** cycle.py is 1369 lines (config, mountinfo parser, approvers, deadline, cycle, status and SLO in one module; fixed by NFR-014's module list). Two boundary leaks the walker cannot see: cli -> cycle.format_utc (cli.py:319) and cycle -> launch._ORCA_CLIS, a private name (cycle.py:1225-1230).
- **Duplication:**
  - OPERATION_ID_PATTERN x2.
  - The issue bound x3, plus 2 digit encodings.
  - The login regex x2 (cycle.py:468, github.py:134).
  - The UTC format string x3.
  - ENTRY_STATES x2 (pinned by literal in test_audit.py:473).
  - Exit constants in cli.py:34-38 vs REASON_TABLE (audit.stderr_fallback checks membership only, audit.py:393-401).
- **Dead code:** the A8 list.
- **Wall-clock reads:** audit.py:396 only, plus runner's monotonic. SystemClock is the one sanctioned reader.
- **Doc/code drift:** D:239 and D:242 (imports). D lacks cycle_complete, cycle_crashed and the once exit 1 (D:114). S has 52 names, the code 59, the runbook 59. The task file is stale (C7).
- **Risk register (blast radius):**
  - R1: real gh/Orca shapes differ from the fixtures. Every launch then stops loudly or reads wrongly (whole feature; gated by the live test).
  - R2: the A6 pipe hang makes all launches `unknown` (whole feature, fail-closed).
  - R3: A1 clock step, cap exceeded (bounded by human approvals).
  - R4: A5, lost operation_id (one issue).
  - R5: A10, one issue never launches.
  - R6: `reset --forfeit-guarantee` is the only path to a second launch (by design).
- **Untested invariants:**
  - launch bound == predicates bound
  - cycle._LOGIN == github._LOGIN_RE
  - a DISABLED re-check after the origin call
  - the day cap under a backward clock
  - an exception after the spawn (only launcher exceptions are tested, T/test_crash_injection.py:327)
  - `status` on a dangling DISABLED
  - the six root-skipped paths when run as root

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-08T04:40:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher

### .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/post/artifacts/reuse-audit.yaml

```yaml
stage: post
candidates_scanned: 12
neighbours_found: 20
max_overlap: 0.98
degraded: ["neighbour-search:auggie_unavailable"]   # no auggie tool in this run; codegraph + Grep + Read used; every tier capped at maybe-related; C_aug dropped and S_reuse renormalized over C_cap/C_shape
sampled: false
findings:
  - candidate: "record.py FileStore.save (record.py:370)"
    capability_tag: "atomic JSON store write: tmp + fsync + replace, then chmod 0600 and directory fsync. The atomic core already delegates to swarm.atomic.write_prepared_bytes through a lazy import (record.py:372); only chmod and directory fsync are added here"
    neighbours:
      - ref: "src/superclaude/cli/swarm/atomic.py:14"
        snippet: "def write_prepared_bytes(path: Path, data: bytes) -> int:"
      - ref: "src/superclaude/cli/install_hooks.py:485"
        snippet: "def _atomic_write_json(target: Path, payload: dict) -> None:"
      - ref: "src/superclaude/cli/install_codegraph.py:79"
        snippet: "def _write_private(path: Path, text: str) -> None:"
    C_cap: 0.75
    C_shape: 0.55
    C_aug: 0.0
    S_reuse: 0.66
    confidence: 0.80
    tier: maybe-related
    verdict: reuse-by-import        # already satisfied for the atomic core; the allowed edge is superclaude.cli.swarm.atomic from record
    shape_divergence: false
    consolidation: { N: 1, recommend_centralize: false, centralize_target: null }
    evidence_grounded: true

  - candidate: "record.py FileStore.lock (record.py:381)"
    capability_tag: "non-blocking exclusive flock on a pre-created lock file, opened O_NOFOLLOW, with a regular-file/uid check and an inode re-check after locking. Negative evidence: Grep for flock|fcntl across src/superclaude finds it only in issue_watch/record.py; the O_NOFOLLOW opens elsewhere (archive_workspace.py:451, install_retired_mcp.py:345, install_codegraph.py:212) are read or create paths with no lock"
    neighbours: []
    C_cap: 0.10
    C_shape: 0.20
    C_aug: 0.0
    S_reuse: 0.14
    confidence: 0.85
    tier: distinct
    verdict: distinct
    shape_divergence: false
    consolidation: { N: 1, recommend_centralize: false, centralize_target: null }
    evidence_grounded: true

  - candidate: "launch.py find_orca (launch.py:163) with _lists_orca_cli (launch.py:144)"
    capability_tag: "prove a PATH binary is the Orca CLI by running `skills list --json` and requiring a topic named orca-cli. Same probe, same _ORCA_CLIS candidate order. Differences: runner and which are injected, a non-absolute which() result is skipped, and a malformed reply returns False instead of raising. Tier capped at maybe-related by the degraded substrate; uncapped S_reuse would pass the 0.82 floor"
    neighbours:
      - ref: "src/superclaude/cli/install_user_setup.py:198"
        snippet: "def _find_orca() -> str | None:"
      - ref: "src/superclaude/cli/install_user_setup.py:219"
        snippet: "if probe.returncode == 0 and any(t.get(\"name\") == \"orca-cli\" for t in topics):"
    C_cap: 0.95
    C_shape: 0.80
    C_aug: 0.0
    S_reuse: 0.88
    confidence: 0.90
    tier: maybe-related
    verdict: mirror-shape           # launch.py:7-8 allows only the standard library, runner and _ORCA_CLIS; the _find_orca import is banned, so import is downgraded to a mirror (NFR-import-ban). tests/issue_watch/test_find_orca_parity.py exists
    shape_divergence: false
    consolidation: { N: 2, recommend_centralize: false, centralize_target: null }
    evidence_grounded: true

  - candidate: "launch.py parse_origin (launch.py:200) and check_origin (launch.py:218)"
    capability_tag: "parse owner/repo from a GitHub origin URL with two anchored patterns (https and git@), strip .git, reject '.' and '..'; check_origin runs `git remote get-url origin` and compares the result to one repo. parse_origin is a line-for-line copy of parse_origin_url (the launch.py:191-192 comment says so). check_origin matches read_origin apart from the Runner seam, timeout and comparison. Tier capped at maybe-related by the degraded substrate; uncapped S_reuse would pass the 0.82 floor"
    neighbours:
      - ref: "src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:86"
        snippet: "def parse_origin_url(url: str) -> str | None:"
      - ref: "src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:66"
        snippet: "re.compile(rf\"^https://github\\.com/(?P<owner>{_NAME})/(?P<repo>{_NAME})/?$\"),"
      - ref: "src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:156"
        snippet: "def read_origin() -> str:"
    C_cap: 1.0
    C_shape: 0.95
    C_aug: 0.0
    S_reuse: 0.98
    confidence: 0.95
    tier: maybe-related
    verdict: mirror-shape           # the neighbour is an installed skill script outside the package, and launch.py:7-8 bans the import; tests/issue_watch/test_origin_parity.py exists
    shape_divergence: false
    consolidation: { N: 2, recommend_centralize: false, centralize_target: null }
    evidence_grounded: true

  - candidate: "runner.py SubprocessRunner (runner.py:67) and CommandResult (runner.py:20)"
    capability_tag: "run one argv with shell=False, a timeout and stdin closed, and fold timeout / spawn failure / capped stderr into a typed result. Prior art is only ad hoc subprocess.run call sites, each with its own try/except and none returning a result type. No shared wrapper exists in src/superclaude. install_codegraph.py:43 Runner is a bare Callable alias with a different shape"
    neighbours:
      - ref: "src/superclaude/cli/install_user_setup.py:209"
        snippet: "probe = subprocess.run("
      - ref: "src/superclaude/cli/install_ccsession.py:107"
        snippet: "subprocess.run("
      - ref: "src/superclaude/cli/sprint/summarizer.py:339"
        snippet: "proc = subprocess.run("
    C_cap: 0.45
    C_shape: 0.35
    C_aug: 0.0
    S_reuse: 0.41
    confidence: 0.70
    tier: distinct
    verdict: distinct
    shape_divergence: false
    consolidation: { N: 1, recommend_centralize: false, centralize_target: null }
    evidence_grounded: true

  - candidate: "audit.py AuditLog.append / rotate_if_needed (audit.py:130, 141)"
    capability_tag: "append-only JSONL: one os.write on an O_APPEND fd, then size-triggered rotation .1 to .4 with a directory fsync. Other JSONL appenders exist (listed) but they are plain open('a') writes (generic CRUD guardrail 2). No rotation prior art: Grep for 'rotat' (case-insensitive) finds none outside issue_watch except account-rotation text"
    neighbours:
      - ref: "src/superclaude/pr_submit/run_log.py:133"
        snippet: "with self.jsonl_path.open(\"a\", encoding=\"utf-8\") as fh:"
      - ref: "src/superclaude/cli/swarm/logging_.py:155"
        snippet: "with open(self.jsonl_path, \"a\") as jsonl_fh:"
      - ref: "src/superclaude/cli/recommend/telemetry.py:61"
        snippet: "with events_path.open(\"a\", encoding=\"utf-8\") as fh:"
    C_cap: 0.45
    C_shape: 0.35
    C_aug: 0.0
    S_reuse: 0.41
    confidence: 0.75
    tier: distinct
    verdict: distinct
    shape_divergence: false
    consolidation: { N: 1, recommend_centralize: false, centralize_target: null }
    evidence_grounded: true

  - candidate: "predicates.py parse_utc / format_utc (predicates.py:27, 42)"
    capability_tag: "render an aware datetime as YYYY-MM-DDTHH:MM:SSZ (format_utc, with a naive-datetime refusal) and strictly parse that shape (parse_utc). The format half has the same input and output as three existing helpers. The parse half has no neighbour, and none of the three validates tzinfo"
    neighbours:
      - ref: "src/superclaude/cli/swarm/recipes/_primitives.py:15"
        snippet: "def format_timestamp(value: datetime) -> str:"
      - ref: "src/superclaude/cli/swarm/state.py:127"
        snippet: "def _utc_now_iso() -> str:"
      - ref: "src/superclaude/cli/eval/disk_budget.py:495"
        snippet: "return time.strftime(\"%Y-%m-%dT%H:%M:%SZ\", time.gmtime())"
    C_cap: 0.85
    C_shape: 0.60
    C_aug: 0.0
    S_reuse: 0.74
    confidence: 0.65
    tier: maybe-related
    verdict: mirror-shape           # predicates.py:4 says it imports nothing from superclaude, so the import is banned; the swarm helper is also a private leaf
    shape_divergence: false
    consolidation: { N: 2, recommend_centralize: false, centralize_target: null }
    evidence_grounded: true

  - candidate: "github.py classify / _rest_read / _graphql_read (github.py:345, 592, 645)"
    capability_tag: "classify a gh CLI reply (timeout, auth, scope, rate limit, transient, non-JSON) and page REST / GraphQL reads under a call budget. Negative evidence: the only literal \"gh\" argv in src/superclaude is github.py; pr_submit mentions gh only in evidence filenames (contract_setup/evidence.py:12-14)"
    neighbours: []
    C_cap: 0.10
    C_shape: 0.15
    C_aug: 0.0
    S_reuse: 0.12
    confidence: 0.85
    tier: distinct
    verdict: distinct
    shape_divergence: false
    consolidation: { N: 1, recommend_centralize: false, centralize_target: null }
    evidence_grounded: true

  - candidate: "cycle.py load_config (cycle.py:195) / validate_approvers (cycle.py:298)"
    capability_tag: "strict closed-key JSON config load with typed field checks, absolute-path rules and a network-filesystem refusal. Only generic JSON load and unknown-key checks exist elsewhere (for example pr_submit/conflicts.py unknown-field handling, a different artifact), which guardrail 2 excludes"
    neighbours: []
    C_cap: 0.25
    C_shape: 0.30
    C_aug: 0.0
    S_reuse: 0.27
    confidence: 0.70
    tier: distinct
    verdict: distinct
    shape_divergence: false
    consolidation: { N: 1, recommend_centralize: false, centralize_target: null }
    evidence_grounded: true

  - candidate: "cycle.py Deadline (cycle.py:383) / CallBudget (github.py:437) / Clock Protocol (cycle.py:361)"
    capability_tag: "per-cycle time budget from an injected monotonic clock: timeout_for returns min(configured, time left), or None under a 5 s floor. The closest prior art is _orca_timeout in a one-shot installer (a different, one-way clamp with no floor-to-None, no launch cutoff and no clock seam). CallBudget and Clock have no neighbour; the repo's other budgets count tokens (audit/budget.py, cli_portify/convergence.py) and were not Read"
    neighbours:
      - ref: "src/superclaude/cli/install_user_setup.py:224"
        snippet: "def _orca_timeout(deadline: float | None) -> float:"
    C_cap: 0.50
    C_shape: 0.45
    C_aug: 0.0
    S_reuse: 0.48
    confidence: 0.70
    tier: distinct
    verdict: distinct
    shape_divergence: false
    consolidation: { N: 1, recommend_centralize: false, centralize_target: null }
    evidence_grounded: true

  - candidate: "cli.py issue_watch_group wiring (cli.py:94, registered at main.py:565)"
    capability_tag: "Click group plus deferred add_command registration in main.py. Framework boilerplate (guardrail 5), excluded. It follows the established reflect_group registration idiom, including the noqa comment, so there is no shape divergence"
    neighbours:
      - ref: "src/superclaude/cli/reflect/commands.py:53"
        snippet: "@click.group(\"reflect\")"
      - ref: "src/superclaude/cli/main.py:561"
        snippet: "main.add_command(reflect_group, name=\"reflect\")"
    C_cap: 0.30
    C_shape: 0.90
    C_aug: 0.0
    S_reuse: 0.56
    confidence: 0.80
    tier: distinct
    verdict: distinct
    shape_divergence: false
    consolidation: { N: 1, recommend_centralize: false, centralize_target: null }
    evidence_grounded: true

  - candidate: "record.py MIGRATIONS / migrate (record.py:247, 251)"
    capability_tag: "schema_version migration chain: version-to-version pure steps with strict result checks. Negative evidence: Grep for MIGRATIONS|def migrate across src/superclaude finds only issue_watch/record.py, plus cycle.py:1207 which reads it"
    neighbours: []
    C_cap: 0.10
    C_shape: 0.15
    C_aug: 0.0
    S_reuse: 0.12
    confidence: 0.85
    tier: distinct
    verdict: distinct
    shape_divergence: false
    consolidation: { N: 1, recommend_centralize: false, centralize_target: null }
    evidence_grounded: true
```

### docs/designs/issue-watcher.md:229-246

```markdown
### 5.3 Dependency rules (NFR-014)

Allowed intra-package imports. Anything not listed is forbidden; `tests/issue_watch/test_module_boundaries.py` walks each module's AST and fails on any other `superclaude.*` import.

| Module | May import from the package | May import from elsewhere in `superclaude` | Third-party |
|---|---|---|---|
| `runner` | none | none | none |
| `predicates` | none | none | none |
| `audit` | none | none | none |
| `github` | `runner`, `predicates` | none | none |
| `record` | `predicates` (types only, for `Entry` fields that hold an issue number) | `superclaude.cli.swarm.atomic` | none |
| `launch` | `runner` | `superclaude.cli.install_user_setup` (`_ORCA_CLIS` only) | none |
| `cycle` | `runner`, `github`, `predicates`, `record`, `launch`, `audit` | none | none |
| `cli` | `cycle`, `record`, `audit`, `launch`, `runner` | none | `click` (already a dependency, `pyproject.toml` dependencies) |

Import cost note (verified): `superclaude.cli.swarm.atomic` itself imports only `os`, `tempfile` and `pathlib` (`swarm/atomic.py:7-11`), but importing it executes `swarm/__init__.py`, which imports `click` (line 90) and the whole `swarm.commands` tree (line 164). `install_user_setup` imports `install_hooks` (line 31), which uses only the standard library. Both costs are paid once per `once` process and are acceptable for a 5-minute batch job; the alternative (copying 25 lines of `write_prepared_bytes`) would contradict NFR-014's "reuses". `cli.py` imports the package lazily from `main.py`, so `superclaude --help` is unaffected beyond today's eager imports.

Arch lint: `src/superclaude/tools/arch_lint.py` has three rules only, constant rebinding (lines 164-186), ID-pattern literal duplication (188-209) and class shadowing (211-228), all keyed to `superclaude.contracts.__all__`. No proposed name (`CLAIM_MARKER`, `ORCA_AGENT`, `REASONS`, `Store`, `Entry`, `Lock`) is in that `__all__` (`contracts/__init__.py:302-313`), and no proposed regex literal equals an `ID_PATTERNS` body (`contracts/__init__.py:64-77`). The lint therefore passes without an `# arch-lint: allow-duplicate` marker. It enforces no import layering, which is why the boundary test above exists.
```

### src/superclaude/cli/issue_watch/record.py:1-60

```python
"""Dispatch record of the issue watcher (design section 7, ``dispatch.json``).

Times are aware UTC datetimes in memory and ``YYYY-MM-DDTHH:MM:SSZ`` strings on
disk; JSON object keys are decimal strings on disk and ``int`` in memory. This
module never reads the wall clock (every time is a ``now`` parameter), never
runs a command, and imports only the standard library and ``predicates`` at
module level.
"""

from __future__ import annotations

import json
import os
import re
import stat
from collections.abc import Callable, Iterable, Iterator, Mapping
from contextlib import AbstractContextManager, contextmanager
from dataclasses import asdict, dataclass, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Protocol

from superclaude.cli.issue_watch.predicates import (
    ApprovalResult,
    format_utc,
    parse_utc,
    valid_issue_number,
    valid_operation_id,
)

SCHEMA_VERSION = 1
"""Store schema version this module reads and writes."""

ENTRY_STATES = frozenset(
    {"pending", "launched", "unknown", "failed", "abandoned", "claimed"}
)
"""The six entry states of design section 7.3."""


class StoreError(Exception):
    """The store cannot be used; ``reason`` is a closed audit reason."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


class LockHeld(Exception):
    """Another process holds the store lock (exit 75 ``lock_held``)."""


class LockError(Exception):
    """The lock file is missing or unsafe; ``reason`` is a closed audit reason."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


class TransitionError(Exception):
```

### src/superclaude/cli/issue_watch/cli.py:1-60

```python
"""The ``superclaude issue-watch`` command group (design sections 4.1, 5.2, 10.2).

Part 1: the group, the shared ``--config`` option, ``build_deps`` and the verbs
``once``, ``status``, ``check-config`` and ``init-state``. Part 2: ``reset``
(design 4.1, DF-03, DF-04, DF-57). This module only
sequences calls into the package and maps results to exit codes; it holds no
business logic and never imports ``subprocess`` (every command runs through
``runner.SubprocessRunner``). It never catches ``SystemExit`` or
``BaseException`` around a cycle.
"""

from __future__ import annotations

import json
import shlex
import shutil
import socket
import sys
from datetime import datetime
from pathlib import Path
from typing import NoReturn
from uuid import uuid4

import click

from . import audit, cycle, record
from .launch import MAX_ISSUE_NUMBER, OrcaLauncher
from .record import FileStore, LockError, LockHeld, StoreError
from .runner import SubprocessRunner

_DEFAULT_CONFIG = "~/.config/superclaude/issue-watch.json"

# Exit codes of design 4.3 that this module returns itself.
_EXIT_UNHEALTHY = 1
_EXIT_CRASH = 1  # [PROPOSAL] C-3: an unexpected exception out of the cycle
_EXIT_CONFIG = 2
_EXIT_STORE = 6
_EXIT_LOCK_HELD = 75


def _expand_config(ctx: click.Context, param: click.Parameter, value: Path) -> Path:
    """Expand a leading ``~`` in the default and in a passed value (DF-13)."""
    try:
        return value.expanduser()
    except RuntimeError:  # no home directory can be resolved
        raise click.BadParameter("cannot expand ~: no home directory") from None


def _config_option(func):
    """The shared ``--config`` option; the file need not exist (it is exit 2)."""
    return click.option(
        "--config",
        "config_path",
        type=click.Path(path_type=Path),
        default=_DEFAULT_CONFIG,
        show_default=True,
        callback=_expand_config,
        help="Path of the JSON configuration file.",
    )(func)

```

### src/superclaude/cli/issue_watch/cli.py:100-165

```python

    Examples:

    \b
        superclaude issue-watch check-config
        superclaude issue-watch init-state
        superclaude issue-watch once --dry-run
        superclaude issue-watch status --json
    """


@issue_watch_group.command("once")
@click.option(
    "--dry-run",
    is_flag=True,
    help="Read and decide, but write no store and never call Orca.",
)
@_config_option
def once_command(dry_run: bool, config_path: Path) -> None:
    """Run one poll cycle and exit with its code (design 4.3)."""
    config = _load_config(config_path)
    try:
        result = cycle.run_cycle(build_deps(config), dry_run)
    except Exception as exc:  # never SystemExit, KeyboardInterrupt or BaseException
        # [PROPOSAL] (Gate C fix C-3, executor decision): reason cycle_crashed,
        # exit 1. The lock is already released by its context manager. Only the
        # exception class name is printed, never its message (it may hold text).
        audit.stderr_fallback("cycle_crashed", _EXIT_CRASH)
        click.echo(f"issue-watch: cycle_crashed: {type(exc).__name__}", err=True)
        sys.exit(_EXIT_CRASH)
    click.echo(f"cycle: {result.reason}")
    click.echo(f"exit: {result.exit_code}")
    if dry_run:
        if result.probe is not None:
            click.echo(f"probe: {result.probe}")
        if result.would_launch is not None:
            click.echo(f"would_launch: {result.would_launch}")
    sys.exit(result.exit_code)


def _print_status(report: dict) -> None:
    """The text form of ``status`` (design 10.2)."""
    age = report["last_completed_cycle_age_seconds"]
    click.echo(f"healthy: {'yes' if report['healthy'] else 'no'}")
    click.echo(f"last completed cycle age: {'never' if age is None else f'{age}s'}")
    click.echo(f"disabled since: {report['disabled_since'] or 'no'}")
    click.echo(f"next permitted at: {report['next_permitted_at'] or 'now'}")
    click.echo(f"day cap used: {report['day_cap_used']}")
    counts = report["counts"]
    click.echo(
        "counts: " + (", ".join(f"{k}={counts[k]}" for k in sorted(counts)) or "none")
    )
    click.echo(f"stale: {len(report['stale'])}")
    for item in report["stale"]:
        click.echo(
            f"  issue {item['issue']} {item['state']} {item['last_reason']}"
            f" updated {item['updated_at']}"
        )
    click.echo(f"retry: {len(report['retry'])}")
    for item in report["retry"]:
        click.echo(f"  issue {item['issue']}: run from {item['cwd']}")
        click.echo(f"    {shlex.join(item['argv'])}")


@issue_watch_group.command("status")
@click.option("--json", "as_json", is_flag=True, help="Print the report as JSON.")
```

### src/superclaude/cli/issue_watch/cli.py:300-348

```python
    Use `reset ISSUE --forfeit-guarantee` (only for an abandoned or unknown
    issue) or `reset --rate-limit`, never both and never neither.

    Examples:

    \b
        superclaude issue-watch reset 42 --forfeit-guarantee
        superclaude issue-watch reset --rate-limit
    """
    by_issue = issue is not None
    if by_issue == rate_limit:
        _refuse_reset("reset needs ISSUE --forfeit-guarantee or --rate-limit, not both")
    if by_issue and not forfeit_guarantee:
        _refuse_reset(f"reset {issue} needs --forfeit-guarantee")
    config = _load_config(config_path)
    store = FileStore(config.state_dir)
    log = audit.AuditLog(config.state_dir)
    now = cycle.SystemClock().now()
    stamp = {
        "ts": cycle.format_utc(now),
        "host": socket.gethostname(),
        "login": None,
        "cycle_id": uuid4().hex,
        "dry_run": False,
    }
    try:
        with store.lock():
            reason, code = _reset_locked(store, issue, now)
            _write_reset(log, stamp, issue, reason, code, rotate=True)
    except LockHeld:
        reason, code = "lock_held", _EXIT_LOCK_HELD
        _write_reset(log, stamp, issue, reason, code, rotate=False)
    except LockError as exc:
        reason, code = exc.reason, _EXIT_STORE
        _write_reset(log, stamp, issue, reason, code, rotate=False)
    if code == 0:
        if by_issue:
            click.echo(f"issue {issue} may now be launched a second time")
        else:
            click.echo("rate limit cleared")
    elif reason == "reset_refused":
        click.echo(
            f"issue-watch: reset refused: issue {issue} has no abandoned or "
            "unknown entry; nothing changed",
            err=True,
        )
    else:
        click.echo(f"issue-watch: {reason}", err=True)
    sys.exit(code)
```

### src/superclaude/cli/issue_watch/predicates.py:1-100

```python
"""Pure predicates for the issue watcher (spec Section 3 definitions).

This module performs no I/O and reads no clock: every time is a parameter.
It imports nothing from ``superclaude`` so every other module may import it.
"""

from __future__ import annotations

import re
from collections.abc import Collection, Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

CLAIM_MARKER = "<!-- sc:issue:claim -->"
"""Claim-comment marker; ``github.MARKER_JQ`` is built from this constant."""

SKEW_TOLERANCE_S = 300
"""Seconds a claim marker may precede ``pending_at`` and still count."""

MAX_ISSUE_NUMBER = 999_999_999
"""Largest issue number the watcher accepts."""

_UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
_UTC_SHAPE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")


def parse_utc(text: str) -> datetime:
    """Parse a GitHub ``YYYY-MM-DDTHH:MM:SSZ`` time into an aware UTC datetime.

    Raises ``ValueError`` for any other input (DF-35: no ``fromisoformat``). The
    shape is checked first with ASCII digits and a capital ``Z`` only, because
    ``strptime`` alone accepts unpadded fields, a lower-case ``z`` and non-ASCII
    digits.
    """
    if not isinstance(text, str):
        raise ValueError("time value is not a string")
    if _UTC_SHAPE.fullmatch(text) is None:
        raise ValueError("time value is not YYYY-MM-DDTHH:MM:SSZ")
    return datetime.strptime(text, _UTC_FORMAT).replace(tzinfo=timezone.utc)


def format_utc(value: datetime) -> str:
    """Format an aware datetime as ``YYYY-MM-DDTHH:MM:SSZ`` in UTC.

    Raises ``ValueError`` for a naive datetime, whose zone would be guessed.
    """
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("naive datetime")
    return value.astimezone(timezone.utc).strftime(_UTC_FORMAT)


def valid_issue_number(value: object) -> bool:
    """Return True for an ``int`` (never ``bool``) in 1..``MAX_ISSUE_NUMBER``."""
    return type(value) is int and 1 <= value <= MAX_ISSUE_NUMBER


OPERATION_ID_PATTERN = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
"""Operation ids that may be stored and printed in a retry command (design 9.2).

``launch.OPERATION_ID_PATTERN`` is a second copy, because ``launch`` may import
only ``runner`` (design 5.3); a test pins the two patterns equal.
"""


def valid_operation_id(value: object) -> bool:
    """Return True for a ``str`` that fully matches ``OPERATION_ID_PATTERN``."""
    return isinstance(value, str) and OPERATION_ID_PATTERN.fullmatch(value) is not None


@dataclass(frozen=True)
class Login:
    """Own login, account id and the reply's ``Date`` header (G1)."""

    login: str
    account_id: int
    server_date: datetime | None


@dataclass(frozen=True)
class DiscoveredIssue:
    """One issue from the discovery read (G2)."""

    number: int
    labels: tuple[str, ...]
    assignees: tuple[str, ...]
    state: str


@dataclass(frozen=True)
class LabelEvent:
    """One issue event; ``label`` is None for events without a label."""

    id: int
    event: str
    label: str | None
    actor_id: int | None
    actor_login: str | None
    actor_type: str | None
    created_at: datetime

```

### src/superclaude/cli/issue_watch/launch.py:22-70

```python
from superclaude.cli.install_user_setup import _ORCA_CLIS

from .runner import CommandResult, Runner

# Orca agent id from the seed brief's launch line (decision DF-11). It names the
# agent Orca starts, not a model alias, and is deliberately not configurable.
ORCA_AGENT = "claude"

MAX_ISSUE_NUMBER = 999_999_999
"""Largest issue number ``build_claim_prompt`` accepts (FR-012)."""

PROMPT_PATTERN = re.compile(r"^/sc:issue --claim [1-9][0-9]{0,8}$")
"""Every prompt ``build_claim_prompt`` can return, and nothing else."""

OPERATION_ID_PATTERN = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
"""Operation ids that may be stored and printed in a retry command (design 9.2)."""

# [PROPOSAL, UNVERIFIED] key paths of the operation id in Orca's launch reply:
# the success reply first, then the error reply (design 8.4 line 636, FU-1).
# Pinned by the two ``_assumed_shape`` fixtures until a real reply is recorded.
OPERATION_ID_PATHS: tuple[tuple[str, ...], ...] = (
    ("receipt", "operation_id"),
    ("error", "operation_id"),
)

OP_UNKNOWN_TEXT = "agent_session_operation_unknown"
"""Orca's error code for a launch whose reply was lost (C16, UNVERIFIED)."""

ORIGIN_REPO = "ironbellyorg/ironclaude"
"""The only origin ``check_origin`` accepts, compared lower-cased (FR-025)."""

ORIGIN_MISMATCH = "origin_mismatch"
"""Reason ``check_origin`` returns for every failed check."""

LaunchKind = Literal["launched", "unknown", "spawn_error"]

LAUNCH_DETAILS: frozenset[str] = frozenset(
    {
        "ok",
        "spawn_error",
        "timeout",
        "exit_nonzero",
        "non_json",
        "no_operation_id",
        "operation_id_invalid",
        "op_unknown",
    }
)
"""The fixed set of ``LaunchOutcome.detail`` values."""
```

### src/superclaude/cli/issue_watch/audit.py:20-125

```python
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

# Closed reason table: name -> (kind, exit).
REASON_TABLE: dict[str, tuple[str, int]] = {
    # Cycle reasons, exit 2.
    "config_invalid": ("cycle", 2),
    "approvers_invalid": ("cycle", 2),
    "platform_unsupported": ("cycle", 2),
    "worktree_invalid": ("cycle", 2),
    "origin_mismatch": ("cycle", 2),
    "orca_not_found": ("cycle", 2),
    "account_id_mismatch": ("cycle", 2),
    # Cycle reasons, exit 6.
    "store_invalid": ("cycle", 6),
    "store_missing": ("cycle", 6),
    "lock_missing": ("cycle", 6),
    "lock_invalid": ("cycle", 6),
    "state_dir_unwritable": ("cycle", 6),
    # Cycle reasons, exit 3.
    "login_invalid": ("cycle", 3),
    "gh_auth_failed": ("cycle", 3),
    "gh_timeout": ("cycle", 3),
    "gh_non_json": ("cycle", 3),
    "project_read_failed": ("cycle", 3),
    # Cycle reasons, exit 4.
    "truncated": ("cycle", 4),
    "discovery_duplicate": ("cycle", 4),
    # Cycle reasons, exit 5.
    "rate_limited": ("cycle", 5),
    "rate_limit_clamped": ("cycle", 5),
    # Cycle reason, exit 75.
    "lock_held": ("cycle", 75),
    # Cycle reason, exit 1. [PROPOSAL] (Gate C fix C-3, executor decision): an
    # unexpected exception out of ``run_cycle``, written by ``once`` only.
    "cycle_crashed": ("cycle", 1),
    # Cycle reasons, exit 0.
    "disabled": ("cycle", 0),
    "disabled_mid_cycle": ("cycle", 0),
    "not_enabled": ("cycle", 0),
    # [PROPOSAL] (Gate C fix C-2, executor decision): a cycle that ran to its end
    # with no stop; its cycle line names this, never a skip or entry reason.
    "cycle_complete": ("cycle", 0),
    # Skip reasons, exit 0.
    "not_approved": ("skip", 0),
    "approval_before_trigger": ("skip", 0),
    "approval_before_init": ("skip", 0),
    "events_incomplete": ("skip", 0),
    "events_unreadable": ("skip", 0),
    "edited_after_approval": ("skip", 0),
    "project_mismatch": ("skip", 0),
    "project_unreadable": ("skip", 0),
    "unassigned": ("skip", 0),
    "assigned_other": ("skip", 0),
    "already_dispatched": ("skip", 0),
    "in_backoff": ("skip", 0),
    "day_cap": ("skip", 0),
    "budget_exhausted": ("skip", 0),
    "revalidation_failed": ("skip", 0),
    "marker_unreadable": ("skip", 0),
    "edits_unreadable": ("skip", 0),
    # Entry reasons.
    "prompt_invalid": ("entry", 7),
    "revalidation_transient": ("entry", 7),
    "attempts_exhausted": ("entry", 0),
    "spawn_error": ("entry", 7),
    "launch_unknown": ("entry", 7),
    "pending_orphan": ("entry", 0),
    "claim_not_observed": ("entry", 0),
    "launched": ("entry", 0),
    "claimed": ("entry", 0),
    # Decision note, used only as the value of a ``note`` key.
    "re-approved": ("note", 0),
    # Warning reasons.
    "discovery_count": ("warning", 0),
    "clock_skew": ("warning", 0),
    "dry_run_shadow_reset": ("warning", 0),
    "reset_refused": ("warning", 2),
    # Operator reset: decision line for an entry, warning line for the rate limit.
    "operator_reset": ("skip/warning", 0),
}

REASONS = frozenset(REASON_TABLE)

ROTATE_BYTES = 5 * 1024 * 1024
_ROTATIONS = 4


def _fsync_dir(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _encode(line: dict) -> bytes:
    text = json.dumps(line, sort_keys=True, ensure_ascii=True)
    return (text + "\n").encode("ascii")


class AuditLog:
    """Append-only ``state_dir / "audit.jsonl"`` with rotations ``.1`` to ``.4``."""

```

### src/superclaude/cli/issue_watch/audit.py:381-404

```python
def stderr_fallback(
    reason: str,
    exit_code: int,
    *,
    ts: str | None = None,
    host: str | None = None,
) -> None:
    """Write one JSON line to stderr with ``kind ts host exit reason`` only.

    Used when ``audit.jsonl`` cannot be written. ``ts`` and ``host`` default to
    the current UTC time and ``socket.gethostname()`` (a stamp, not a decision).
    """
    if reason not in REASONS:
        raise ValueError(f"unknown audit reason {reason!r}")
    if ts is None:
        now = datetime.datetime.now(datetime.timezone.utc)
        ts = now.strftime(_UTC_TS_FORMAT)
    if host is None:
        host = socket.gethostname()
    for key, value in (("exit", exit_code), ("ts", ts), ("host", host)):
        _check_value(key, value)
    out = {"kind": "cycle", "ts": ts, "host": host, "exit": exit_code, "reason": reason}
    sys.stderr.write(_encode(out).decode("ascii"))
    sys.stderr.flush()
```

### src/superclaude/cli/issue_watch/cycle.py:1-80

```python
"""One poll cycle of the issue watcher (design sections 4.2, 4.3, 5.4 and 8.5).

Part 1 holds the constants, the configuration and its validators, the approvers
file check, the clock and deadline, the ``Deps`` and ``CycleResult`` records
and the exit-code rules. This module never imports ``subprocess``: every
command runs through the injected ``Runner``. Time is read only through the
``Clock``. Nothing here touches ``fcntl`` or ``/proc`` at import time.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import stat
import sys
import time
import unicodedata
from collections.abc import Callable, Iterable
from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Protocol
from uuid import uuid4

from . import audit, github, launch, predicates, record
from .launch import Launcher
from .predicates import ApprovalResult, DiscoveredIssue, format_utc, parse_utc
from .record import Entry, LockError, LockHeld, Store, StoreDoc, StoreError
from .runner import CommandResult, Runner

# Design section 14 defaults. They are module constants, not operator knobs.
MAX_CANDIDATES = 10
MAX_LAUNCHES_PER_CYCLE = 1
DAY_CAP = 6
GH_TIMEOUT_S = 20.0
PROBE_TIMEOUT_S = 10.0
GIT_TIMEOUT_S = 10.0
LAUNCH_TIMEOUT_S = 120.0
DEADLINE_TOTAL_S = 240.0
GH_FLOOR_S = 5.0
LAUNCH_CUTOFF_S = 120.0
SKEW_WARN_S = 60
HEALTH_AGE_S = 900
STALE_AGE_S = 86400
DISCOVERY_WARN = 80

# Filesystem types a state directory must not live on (design 4.2, DF-53).
NETWORK_FS_TYPES = frozenset(
    {"nfs", "nfs4", "cifs", "smb3", "sshfs", "fuse.sshfs", "9p"}
)

SCHEMA_VERSION = 1
DEFAULT_TRIGGER_LABEL = "issue-watch:trigger"
DEFAULT_APPROVAL_LABEL = "issue-watch:approved"

_TOP_KEYS = frozenset(
    {
        "schema_version",
        "enabled",
        "labels",
        "project_id",
        "owner_account_id",
        "worktree",
        "approvers_file",
        "state_dir",
    }
)
_LABEL_KEYS = frozenset({"trigger", "approval"})
_LABEL_MAX = 50
_PROJECT_ID = re.compile(r"PVT_[A-Za-z0-9_-]{1,64}")
_APPROVER_LINE = re.compile(r"[1-9][0-9]{0,19}")
_ACCOUNT_ID_MAX = 10**20 - 1
_APPROVERS_MAX_BYTES = 1024 * 1024
_UTC_TS_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
_MOUNTINFO = "/proc/self/mountinfo"
_OCTAL_ESCAPE = re.compile(r"\\(040|011|012|134)")


```

### src/superclaude/cli/issue_watch/cycle.py:361-470

```python
class Clock(Protocol):
    """Wall and monotonic time; every time read in a cycle goes through it."""

    def now(self) -> datetime:
        """Return the current time as a timezone-aware UTC datetime."""
        ...

    def monotonic(self) -> float:
        """Return a monotonic reading in seconds."""
        ...


class SystemClock:
    """The real ``Clock``."""

    def now(self) -> datetime:
        return datetime.now(timezone.utc)

    def monotonic(self) -> float:
        return time.monotonic()


class Deadline:
    """The cycle's time budget (design 8.5): 240 s, a 5 s floor, a 120 s launch cutoff."""

    def __init__(self, clock: Clock, total: float = DEADLINE_TOTAL_S) -> None:
        self._clock = clock
        self._total = float(total)
        self._start = clock.monotonic()

    def elapsed(self) -> float:
        """Seconds since the deadline was created."""
        return self._clock.monotonic() - self._start

    def remaining(self) -> float:
        """Seconds left, never below zero."""
        return max(0.0, self._total - self.elapsed())

    def timeout_for(self, configured: float) -> float | None:
        """Return the lesser of ``configured`` and the time left.

        None when fewer than ``GH_FLOOR_S`` seconds remain: the call must not
        start, and the caller must test for None before it calls a ``Runner``.
        """
        left = self.remaining()
        if left < GH_FLOOR_S:
            return None
        return min(float(configured), left)

    def launch_allowed(self) -> bool:
        """False once more than ``LAUNCH_CUTOFF_S`` seconds have elapsed."""
        return self.elapsed() <= LAUNCH_CUTOFF_S


@dataclass(frozen=True)
class Deps:
    """Everything ``run_cycle`` needs, injected (design 5.4, DF-45)."""

    runner: Runner
    store: Store
    launcher: Launcher
    clock: Clock
    audit: audit.AuditLog
    config: Config
    which: Callable[[str], str | None]
    host: str


@dataclass(frozen=True)
class CycleResult:
    """What one cycle did: the exit code, the cycle reason and the lines written."""

    exit_code: int
    reason: str
    cycle_id: str
    launched_issue: int | None = None
    would_launch: int | None = None
    probe: str | None = None
    lines: tuple[dict, ...] = ()


# Exit precedence (design 4.3, OD-10).
_PRECEDENCE = (2, 6, 7, 5, 3, 4)
_LOCK_HELD_EXIT = 75


def resolve_exit(conditions: frozenset[int]) -> int:
    """Return the exit code for a set of raised exit conditions.

    The first present of 2, 6, 7, 5, 3, 4; else 75 only when it is the sole
    condition; else 0. This is the only place conditions are combined.
    """
    for code in _PRECEDENCE:
        if code in conditions:
            return code
    if set(conditions) - {0} == {_LOCK_HELD_EXIT}:
        return _LOCK_HELD_EXIT
    return 0


def exit_for(reason: str) -> int:
    """Return the exit code of ``reason`` from ``audit.REASON_TABLE`` (DF-41)."""
    return audit.REASON_TABLE[reason][1]


# --- Part 2: the poll cycle (design section 6.2, steps 1 to 15) ---------------

_LOGIN = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}")
_RATE_CLAMP = timedelta(seconds=github.RATE_LIMIT_MAX_WAIT_S)

```

### src/superclaude/cli/issue_watch/runner.py:60-130

```python
    A character split by the byte limit is dropped (``errors="ignore"``), so the
    result never re-encodes to more than the cap.
    """
    raw = text.encode("utf-8")[:STDERR_CAP_BYTES]
    return raw.decode("utf-8", errors="ignore")


class SubprocessRunner:
    """The real ``Runner``: one ``subprocess.run`` call per command, no shell."""

    def run(
        self, argv: list[str], timeout: float, *, cwd: str | None = None
    ) -> CommandResult:
        """Run ``argv`` with ``shell=False`` and stdin closed.

        Raises ``TypeError`` when ``argv`` is a ``str``, empty or not a list of
        ``str``. A timeout gives ``timed_out=True`` and ``returncode=None``; an
        ``OSError`` at start, or a ``ValueError`` from a NUL byte in ``argv`` or
        ``cwd``, gives ``spawn_error`` set to its class name and empty output.
        Output is decoded as UTF-8 with undecodable bytes replaced, so a child
        that prints other bytes never makes this method raise.
        """
        if (
            not isinstance(argv, list)
            or not argv
            or not all(isinstance(a, str) for a in argv)
        ):
            raise TypeError("argv must be a non-empty list of str")
        argv_t = tuple(argv)
        start = time.monotonic()
        try:
            proc = subprocess.run(
                argv,
                shell=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                stdin=subprocess.DEVNULL,
                cwd=cwd,
            )
        except subprocess.TimeoutExpired as exc:
            return CommandResult(
                argv=argv_t,
                returncode=None,
                stdout=_as_text(exc.stdout),
                stderr=_cap_stderr(_as_text(exc.stderr)),
                timed_out=True,
                spawn_error=None,
                duration_s=time.monotonic() - start,
            )
        except (OSError, ValueError) as exc:
            return CommandResult(
                argv=argv_t,
                returncode=None,
                stdout="",
                stderr="",
                timed_out=False,
                spawn_error=type(exc).__name__,
                duration_s=time.monotonic() - start,
            )
        return CommandResult(
            argv=argv_t,
            returncode=proc.returncode,
            stdout=proc.stdout,
            stderr=_cap_stderr(proc.stderr),
            timed_out=False,
            spawn_error=None,
            duration_s=time.monotonic() - start,
        )
```

## Coverage slice

Rows for reviewer 3 (refactorer): non-functional requirements NFR-001..NFR-014 (lines 353-426) and the cross-task interaction findings IE-01..IE-05 with observed-not-flagged items (artifacts/interaction-effects.yaml), verbatim. The helpers that built them are NOT trusted.

```yaml
  # ---------------------------------------------------------------- NFR
  - id: NFR-001
    status: covered
    impl: ["IW/launch.py:84-92, 101-102"]
    tests: ["T/test_security_invariants.py:451,522 (hostile labels, logins, commenters never in any argv)", "T/test_launch.py:141"]
    bites: yes
  - id: NFR-002
    status: covered
    impl: ["IW/github.py:175-262 argv builders (GET on REST, graphql constants without 'mutation', no title/body)"]
    tests: ["T/test_security_invariants.py:637 (5 scenario cycles), 668,697 (every builder),864 (scan rejects forbidden argv),879 (no 'mutation' in any github.py string constant)", "T/test_no_text.py:816,856"]
    bites: yes (scan has negative self-tests, so it cannot pass vacuously)
  - id: NFR-003
    status: covered
    impl: ["IW/github.py:37 REPO, 74-103 (literal owner and name in GraphQL)", "IW/launch.py:50"]
    tests: ["T/test_security_invariants.py:668 (no SuperClaude-Org, no {owner} in any argv),897", "T/test_github.py:314", "T/test_origin_parity.py:90"]
    bites: yes
  - id: NFR-004
    status: covered
    impl: ["IW/runner.py:82-101 (TypeError on str argv; shell=False)"]
    tests: ["T/test_runner.py:57,82", "T/test_no_shell.py:150,156 plus mutation guards 229-264"]
    bites: yes
  - id: NFR-005
    status: covered
    impl: ["IW/cycle.py:1052-1062, 1079-1125", "IW/record.py:627-651 sweep"]
    tests: ["T/test_crash_injection.py:217,238,287,310,327,347 (C1-C5, 5 reruns each, launches <= 1)", "T/test_concurrency.py:146", "T/test_cycle.py:4074 (50 cycles), 2905 (other login not relaunched), 4449,4476", "T/test_cli_e2e.py:334", "T/conftest.py:103 (FakeRunner returns 99 on unexpected argv)", "T/test_no_text.py:528"]
    bites: yes
  - id: NFR-006
    status: covered
    impl: ["IW/audit.py:159-197 (closed keys, no rate_remaining), 381-404"]
    tests: ["T/test_audit.py:214-225,449,490-662", "T/test_no_text.py:528,597,912,937 (PWNED canary never in argv, audit, store, rotated files)"]
    bites: yes
  - id: NFR-007
    status: covered
    impl: ["IW/cycle.py:472-497, 817-827"]
    tests: ["T/test_cycle.py:1584 (table over login, discovery, scope, store, rate limit)", "T/test_cycle.py:1602"]
    bites: yes
  - id: NFR-008
    status: partial
    impl: ["IW/cycle.py:383-412", "IW/runner.py:102-111 (TimeoutExpired => timed_out)", "IW/github.py:352-353 (timed_out => timeout => gh_timeout)"]
    tests: ["T/test_cycle.py:1897,1907 (FakeRunner timed_out => exit 3 gh_timeout, 20 s timeout)", "T/test_runner.py:217 (a real sleeping child is cut)"]
    bites: "each half yes; no single test chains a real sleeping stub through `once`"
    note: "AUTHORIZED SPLIT (DF-55): T/test_cli_e2e.py:11-13 says the sleeping-stub case is split into a runner unit test and in-process cycle tests"
  - id: NFR-009
    status: covered
    impl: ["IW/github.py:437-463 CallBudget, 46-49"]
    tests: ["T/test_cycle.py:4214 (10 skipping candidates stop at 32+2 calls, 2 unread), 4236 (reserved 3 bring total to 35+2),1283", "T/test_github.py:1330,1338,1349,1356"]
    bites: yes
  - id: NFR-010
    status: covered
    impl: ["IW/cycle.py:903-912 (already_dispatched)"]
    tests: ["T/test_cycle.py:4177 (second once: no launch, entry byte-equal, only comments read)", "T/test_cli_e2e.py:401"]
    bites: yes
  - id: NFR-011
    status: covered
    impl: ["IW/record.py:213-280 validate/migrate, 347-378 load/save (write_prepared_bytes, chmod 0600, dir fsync), 753-802 init_state"]
    tests: ["T/test_record.py:221 (truncated),419 (bad version),447,473,528,544,613,636,649,666", "T/test_cycle.py:1545 (missing/garbage store: exit 6, bytes untouched),4578,4594"]
    bites: yes
    note: "MIGRATIONS ships empty and SCHEMA_VERSION is 1, so migration is exercised with a monkeypatched table only (T/test_record.py:473)"
  - id: NFR-012
    status: gate-only
    impl: ["no code; pyproject.toml, Makefile, .github unchanged (git diff --stat)"]
    tests: ["none in pytest (grep for pyproject/dependency in T/ finds nothing relevant)", "evidence is gate output: test-results/p9-g6-verify-deps.txt (PASS, subset of AC3 allow-list), p9-g10.txt (EXIT=0)"]
    bites: "n/a; the 'one new session per cycle' half is covered by FR-016 tests (T/test_cycle.py:3534)"
  - id: NFR-013
    status: covered
    impl: ["IW/cycle.py:1190-1191, 1322-1369 slo_numbers (pure helper; no production caller by design)"]
    tests: ["T/test_slo_helper.py:399 (four numbers from a rotated fixture log), 204,255,276,321"]
    bites: yes
  - id: NFR-014
    status: partial
    impl: ["IW package layout; Protocols Runner (runner.py:38), Store (record.py:318), Launcher (launch.py:262), Clock (cycle.py:361)", "IW/record.py:372 reuses swarm.atomic.write_prepared_bytes"]
    tests: ["T/test_module_boundaries.py:219 (exact module set),241 (import table per module),259,269 (no 'select'),276 (exactly four Protocols)", "T/test_find_orca_parity.py:145-270 (mirror of _find_orca)", "T/test_record.py:666"]
    bites: "yes for modules, imports, protocols, select, parity"
    note: "NOT TESTED: 'every time read goes through the clock'. No static scan exists. Wall-clock reads outside the Clock: IW/audit.py:396 (stderr_fallback default ts; cli.py:79,127,219 call it without ts) and IW/runner.py:89-129 (monotonic duration_s). Low risk: only stamps."

# ---- artifacts/interaction-effects.yaml (findings section) ----
findings:
  - id: IE-01
    symbol: "predicates.{format_utc, parse_utc, valid_issue_number, valid_operation_id} used by record"
    tasks: [P2 Step 2.2, P4 Step 4.1a, GB fix B-10]
    call_sites: 15   # record.py: format_utc 287,292,301,304,305,500,857,858; parse_utc 145; valid_issue_number 163,172,467; valid_operation_id 183,585,607
    severity: HIGH   # by the count rule only; the behavioural risk is low (see note)
    category: cross_task
    cited_by_task: partial   # Step 4.1a (tasklist line 332) names parse_utc, format_utc, valid_issue_number; valid_operation_id was added by B-10 and no task item names it
    evidence:
      - src/superclaude/cli/issue_watch/record.py:23-29   # imports four functions plus the ApprovalResult type
      - docs/designs/issue-watcher.md:239                # design 5.3 row for record: predicates "(types only ...)"
      - tests/issue_watch/test_module_boundaries.py:20-21,57-61   # the test rule was widened to any predicates name for record
      - .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:332,998   # Step 4.1a allows three functions; PRE-11 logs the mismatch as minor
      - .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/qa/gate-b/qa-fix-report.md:20,28   # B-10 adds valid_operation_id and calls it "within design 5.3"
    note: >
      Departure from design 5.3 ("types only") is real and widened in the test instead of the design. The design text was not
      amended and the departure is not in the deviation register (grep of phase-outputs/reports/deviation-register.md for
      "predicates" gives no match). No import cycle and no runtime break: predicates imports nothing from the package.
      B-10's claim "within design 5.3" is wrong for a function import. Tests pass (orchestrator run), so this is a design-fidelity
      finding, not a safety break.

  - id: IE-02
    symbol: "predicates.format_utc reached as cycle.format_utc from cli.reset_command"
    tasks: [P2 Step 2.2, P6 cycle, P7 cli]
    call_sites: 1    # cli.py:319
    severity: LOW
    category: cross_task
    cited_by_task: false   # no task item names cycle.format_utc for cli (grep of the tasklist: only the Phase 8 Task Log line 1046 mentions it)
    evidence:
      - src/superclaude/cli/issue_watch/cli.py:26-29,319   # cli imports audit, cycle, record, launch, runner; line 319 calls cycle.format_utc(now)
      - src/superclaude/cli/issue_watch/cycle.py:29        # cycle's from-import is the only reason cycle.format_utc exists
      - docs/designs/issue-watcher.md:242                  # design 5.3 row for cli: cycle, record, audit, launch, runner (no predicates)
      - tests/issue_watch/test_module_boundaries.py:72-75  # the walker checks import statements only, so attribute access passes
      - .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:1046   # executor noted it in the Phase 8 log, item (3)/(4)
    note: >
      cli reaches a predicates helper through cycle's namespace, which skips the boundary table without breaking its letter.
      It works only while cycle keeps `from .predicates import format_utc` (cycle uses it at 555, 623, 1268, 1292, 1293, so
      an unused-import cleanup would not remove it today). The reset tests in test_cli.py exercise the line.

  - id: IE-03
    symbol: "OPERATION_ID_PATTERN (predicates.py:57 and launch.py:36) with valid_operation_id"
    tasks: [P2 Step 2.2, P5 launch, GB fix B-10]
    call_sites: 3    # launch.py:127, launch.py:274 (launch copy); predicates.py:67 (predicates copy, which record calls at 183, 585, 607)
    severity: MEDIUM
    category: cross_task
    cited_by_task: false   # grep of the tasklist for OPERATION_ID_PATTERN / valid_operation_id: no match; the pair exists only because of fix B-10
    evidence:
      - src/superclaude/cli/issue_watch/predicates.py:57-67
      - src/superclaude/cli/issue_watch/launch.py:36,127,272-274
      - tests/issue_watch/test_launch.py:198-200            # parity test: pattern and flags equal
      - .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/qa/gate-b/qa-fix-report.md:20   # why the copy exists (launch may import only runner)
    note: >
      Two copies of the regex that keeps a hostile operation id out of a saved store and out of a printed retry command.
      Mitigated: a test pins the two patterns and flags equal. The gate is also enforced a third time in
      launch.LaunchOutcome.__post_init__ (launch.py:256-259) before cycle calls record.mark_launched/mark_unknown, so a
      divergence would fail closed (ValueError), not open.

  - id: IE-04
    symbol: "issue-number bound 999_999_999 (predicates.MAX_ISSUE_NUMBER, launch.MAX_ISSUE_NUMBER, audit._MAX_ISSUE)"
    tasks: [P2 Steps 2.2/2.3, P5 launch, P7 cli]
    call_sites: 3    # predicates.py:54, launch.py:90 (also cli.py:283 reads launch's copy for the click range), audit.py:236
    severity: MEDIUM
    category: cross_task
    cited_by_task: false
    evidence:
      - src/superclaude/cli/issue_watch/predicates.py:20,54
      - src/superclaude/cli/issue_watch/launch.py:30,90
      - src/superclaude/cli/issue_watch/audit.py:203,236
      - src/superclaude/cli/issue_watch/cli.py:27,283
      - tests/issue_watch/test_audit.py:484                # audit copy pinned equal to predicates
    note: >
      No test pins launch.MAX_ISSUE_NUMBER equal to predicates.MAX_ISSUE_NUMBER. Boundary values are tested separately in
      each module (test_launch.py:46,64; test_predicates.py:651-663), so a drift would fail one of those tests. The
      build_claim_prompt bound is the one that decides what text reaches `orca`.

  - id: IE-05
    symbol: "audit.REASON_TABLE grew from 57 to 59 names (cycle_complete, cycle_crashed) while the task text still pins 57"
    tasks: [P2 Steps 2.3/2.8, GC fixes C-2/C-3, P7 cli, P9 runbook]
    call_sites: 2    # production uses of the two new names: cycle.py:1137 (cycle_complete), cli.py:127-129 (cycle_crashed)
    severity: MEDIUM
    category: cross_task
    cited_by_task: partial   # Task Log line 1050 (Phase 9) says OQ-2/OQ-49 and the 57 count are stale; no step item was corrected
    evidence:
      - src/superclaude/cli/issue_watch/audit.py:57,64
      - tests/issue_watch/test_audit.py:3-6,38,215-219,125-129   # code and tests consistently pin 59, literal list
      - docs/designs/issue-watcher-setup.md:344                  # runbook says 59 and marks the two names [PROPOSAL]
      - .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:199,214,287,417,686,759,923,975   # stale "57" in step items and open questions
      - .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/phase-outputs/reports/deviation-register.md:61
      - .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/phase-outputs/reports/final-change-set.md:218
    note: >
      Nothing in src/, tests/ or docs/ still says 57: the pin test, the table and the runbook agree on 59. The stale 57 sits
      only in the executor's own task file and two delivered reports (10 lines). Risk: a resumed or re-run Step 2.3/2.8 would
      write or assert a 57-name table and fail the 59-name pin. docs/designs/issue-watcher.md has no count and does not list
      the two new names (grep: no match), so the design and the code differ on the reason set; the runbook is the only doc that names them.

observed_not_flagged:
  - id: ON-01
    what: "Gate C deadline fix (C-1 then C2-1): a launch must not start after the 120 s cut-off"
    why_not_flagged: "Both tasks and the fix reports cite each other; the current code holds both checks."
    evidence:
      - src/superclaude/cli/issue_watch/cycle.py:1039-1049    # launch_allowed() before the origin call and again right after it
      - src/superclaude/cli/issue_watch/cycle.py:410-412,697-702,1017-1019
      - tests/issue_watch/test_cycle.py:4352                   # test for the clock crossing the cut-off inside the origin call
      - .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/qa/gate-c/qa-fix-report-cycle2.md:11,16   # fix and mutant check
    residual: >
      After the second check the cycle runs record.mark_pending and a durable store save (cycle.py:1060-1061) before
      launcher.launch (1062); there is no third check, so a very slow disk write could cross the cut-off. The launch itself
      takes a fixed 120 s (LAUNCH_TIMEOUT_S), not the time left. Not a defect against design 647, only a limit.
  - id: ON-02
    what: "cli exit constants (cli.py:34-38) duplicate REASON_TABLE exits; cycle uses exit_for(table)"
    why_not_flagged: "Phase 7 item text names audit.stderr_fallback(reason, 2) and the exit table; per-path tests pin each exit."
    evidence:
      - src/superclaude/cli/issue_watch/cli.py:34-38,79,127,177,210,219,248,252,330
      - src/superclaude/cli/issue_watch/audit.py:393-401      # stderr_fallback checks reason membership only, not that exit equals the table exit
      - tests/issue_watch/test_audit.py:843, tests/issue_watch/test_cli.py:681
    call_sites: 14
  - id: ON-03
    what: "M4 fix M-1 (cycle line carries clock_skew_s every cycle with a known Date)"
    why_not_flagged: "Fix report lists every touched test; audit accepts 0; slo_numbers does not read the key."
    evidence:
      - src/superclaude/cli/issue_watch/cycle.py:751-756,1154
      - .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/qa/m4/qa-fidelity-fix-report.md:16-23
  - id: ON-04
    what: "operation_id passed from cycle._launch to record.mark_launched/mark_unknown after B-10/B-11 made them raise on a bad id"
    why_not_flagged: "LaunchOutcome.__post_init__ rejects a bad id and a launched outcome without one, so cycle cannot pass an invalid id."
    evidence:
      - src/superclaude/cli/issue_watch/launch.py:251-259
      - src/superclaude/cli/issue_watch/cycle.py:1064-1072
      - src/superclaude/cli/issue_watch/record.py:585-586,607-608
  - id: ON-05
    what: "UTC format string repeated in predicates.py:23, audit.py:200, cycle.py:76"
    why_not_flagged: "cycle's copy only formats an approvers-file mtime (cycle.py:349); audit's is pinned by its own tests. Cosmetic if they drift."

counts:
  findings: 5
  by_severity: {HIGH: 1, MEDIUM: 3, LOW: 1}
  observed_not_flagged: 5

limits:
  - "Tasks come from tasklist text and qa fix reports, not from per-task diffs (one commit)."
  - "Overlap graph was built on the 30 mapped symbols plus the import and constant duplicates found by Grep; the other ~370 new symbols were not checked pairwise."
```
