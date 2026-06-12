"""E1 differential runner -- OLD=MISS: local-path `--file`; NEW=CATCH: H1 runtime-entrypoint proxy.

OLD=MISS (real-git replay at pre-fix parent 94d5baa0, CI-skip-guarded): the pre-fix
`PrdClaudeProcess._build_file_args` (a `@staticmethod(config, step_id)` at the parent, REMOVED by
fix 7601ad25) emits `--file <local_path>` argv for `scope-discovery` -- a local filesystem path
handed to the cloud-only `claude --file` flag, which the pre-fix argv-only review accepted as clean.
NEW=CATCH (skip-guarded until impl lands): the H1 `runtime-entrypoint-verification.md` ref documents
the negative-witness (fix-reverted -> FAIL) catch. Maps 1:1 to RELEASE-SPEC §8.3 "E1 backtest".
"""

from __future__ import annotations

import pytest

from tests.troubleshoot.backtest._impl_guard import HARDENING_REFS, requires_impl_ref
from tests.troubleshoot.backtest.catch_rate import VERDICT_MISS, EscapeResult
from tests.troubleshoot.backtest.git_replay import (
    escape_by_id,
    is_git_worktree,
    missing_replay_commits,
)
from tests.troubleshoot.backtest.replay_executor import run_prefix_replay_snippet

_E1 = escape_by_id("E1")

pytestmark = pytest.mark.skipif(
    (not is_git_worktree()) or bool(missing_replay_commits([_E1.prefix_parent_sha])),
    reason=(
        f"E1 OLD=MISS real-git replay needs pre-fix parent {_E1.prefix_parent_sha} "
        "(absent on a shallow CI clone, actions/checkout@v4 default fetch-depth: 1; set "
        "fetch-depth: 0 to enable)."
    ),
)

# Replayed in a fresh subprocess whose sys.path is rooted at the parent tree's src/ (see
# run_prefix_replay_snippet). Invokes the pre-fix _build_file_args after reading its real signature.
_E1_SNIPPET = """
import inspect, tempfile, os
from types import SimpleNamespace
from pathlib import Path
from superclaude.cli.prd import process as P
_tmp = tempfile.mkdtemp()
_spec = os.path.join(_tmp, "local-spec.md")
with open(_spec, "w") as _fh:
    _fh.write("# local spec")
_bfa = inspect.getattr_static(P.PrdClaudeProcess, "_build_file_args")
_fn = getattr(_bfa, "__func__", _bfa)  # unwrap @staticmethod to the underlying function
_cfg = SimpleNamespace(spec_files=[_spec], skill_refs_dir=Path(_tmp))
_argv = _fn(_cfg, "scope-discovery")
print(json.dumps({
    "signature": str(inspect.signature(_fn)),
    "argv": _argv,
    "emits_local_file": ("--file" in _argv and _spec in _argv),
}))
"""


def test_backtest_e1_old_protocol_misses_local_path_file() -> None:
    """Pre-fix `_build_file_args` emits `--file <local_path>` -- a genuine OLD=MISS negative witness."""
    observed = run_prefix_replay_snippet(_E1.prefix_parent_sha, _E1_SNIPPET)
    argv = observed["argv"]
    assert observed["emits_local_file"] is True, (
        f"expected pre-fix _build_file_args to emit a local-path --file (the escape), got argv={argv}"
    )
    assert "--file" in argv, f"OLD=MISS negative witness absent -- argv={argv}"
    # The un-hardened argv-only review accepts this malformed cloud-flag argv as clean -> the MISS.
    result = EscapeResult(
        escape_id="E1",
        wave="H1",
        verdict=VERDICT_MISS,
        negative_witness=True,
        card_path=None,
        detail=f"pre-fix _build_file_args({observed['signature']}) emitted {argv!r}",
    )
    assert result.verdict == VERDICT_MISS and result.negative_witness is True


@requires_impl_ref("runtime-entrypoint-verification.md")
def test_backtest_e1_new_gate_catches_via_h1_ref() -> None:
    """NEW=CATCH proxy: the H1 ref documents the negative-witness (fix-reverted -> FAIL) catch."""
    text = (HARDENING_REFS / "runtime-entrypoint-verification.md").read_text(
        encoding="utf-8"
    )
    low = text.lower()
    assert "negative witness" in low, (
        "H1 ref must document the negative-witness requirement"
    )
    assert "--file" in text or "runtime" in low or "entrypoint" in low, (
        "H1 ref must document the runtime-entrypoint / local-path-as-cloud-file catch mechanism"
    )
