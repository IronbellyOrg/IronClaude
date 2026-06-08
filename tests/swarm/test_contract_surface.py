"""T07.15 -- NFR-016 contract-surface non-precluding grep audit.

Roadmap row R-130 / NFR-016 ratifies the Phase-2 caller-agnosticism
audit at the Phase-7 STRICT tier and EXTENDS it along two axes the
earlier ``test_no_claude_isms.py`` (AC-013) deliberately stops short
of:

* **Call-form Claude-tool invocations.** Phase 2 catches bare tokens
  via word boundaries (``\bRead\b``).  A future contributor smuggling
  in ``Read(file_path=...)`` as a literal *method-call* expression on
  a placeholder ``self.Read`` attribute would slip past the word-
  boundary scan because the call site reads identically to the tool
  invocation.  Phase 7 closes that hole by adding a second,
  independent scan keyed on the *call form* ``Tool(`` with a negative
  lookbehind that excludes ``.read(`` (legitimate file/stdin method
  calls) and ``xRead(`` (identifier suffixes).

* **Vendor strings.** ``claude.ai`` (the host-vendor web origin) and
  the bare ``anthropic`` token (vendor name in any case) are added to
  the forbidden set.  The Phase-3 audit
  (``test_no_anthropic_routing.py``) already enforces this inside the
  *transports* tree; T07.15 raises the same bar for the broader
  contract surface (schema / models / commands / __init__ / state /
  logging_ / reduce) so a vendor string smuggled into the job spec
  or the result contract is caught even if transports/ stays clean.

The Phase-2 audit and this Phase-7 audit are deliberately kept as
*independent test modules* (per the docstring in
``test_no_claude_isms.py``).  Two separate failure surfaces mean a
regression that breaks one scanner cannot silently mask a breach
caught by the other.

Detached-survival check
-----------------------

The acceptance criteria for T07.15 also bind the detached-mode
guarantee: a detached job (T07.11 / FR-014) MUST survive a forced
SIGKILL of the launching process, not merely a clean exit.  The
companion T07.02 test ``test_detached_session_survives_caller_exit``
verifies the *clean-exit* form (subprocess returns normally, session
remains).  Here we strengthen that to a forced kill -- the launcher
is started, given a moment to spawn the tmux session, then SIGKILL'd
mid-flight.  If the detached session were merely a foreground child
of the launcher Python process, the kernel would tear it down with
the parent; the tmux daemon-spawned session must remain alive.

The detached check is gated on ``shutil.which('tmux')``.  When tmux
is absent the test is skipped cleanly per the task verification
clause ("passes or skips cleanly").

Mutation guarantee
------------------

Every forbidden shape is exercised against a synthetic source to
prove the scanner actually flags it.  Without this, a regression
emptying the pattern table or breaking the regex would let every
surface scan pass vacuously.
"""

from __future__ import annotations

import os
import re
import shutil
import signal
import subprocess
import sys
import time
import uuid
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SWARM_DIR = REPO_ROOT / "src" / "superclaude" / "cli" / "swarm"

# Contract surfaces per NFR-016.  Mirrors the Phase-2 AC-013 surface
# set with the addition of reduce.py -- the result-contract + done-
# sentinel emitter is also a caller-visible artifact and must not
# leak Claude-isms or vendor strings.
#
# Each entry is (relative path, role) so the failure message can name
# what category of contract surface was breached.
#   * job-spec        -- DM-001 JSON schema + JobSpec dataclasses
#   * result-contract -- DM-012 ResultContract + DM-017 DoneSentinel
#   * CLI             -- Click group + subcommands (operator surface)
#   * monitoring      -- DM-014 SwarmState + DM-015 EventRecord
CONTRACT_SURFACE_FILES: tuple[tuple[str, str], ...] = (
    ("schema.py", "job-spec"),
    ("models.py", "job-spec/result-contract"),
    ("commands.py", "CLI"),
    ("__init__.py", "CLI"),
    ("state.py", "monitoring"),
    ("logging_.py", "monitoring"),
    ("reduce.py", "result-contract"),
)

# Claude-tool *call-form* tokens.  These match a CapitalCase
# identifier followed immediately by ``(`` -- the way a Claude tool
# is actually invoked at the call site.  The negative lookbehind
# excludes the form ``.read(`` (legitimate file/stdin method) and
# ``xRead(`` (an identifier suffix) without losing the bare ``Read(``
# Claude tool invocation.
#
# Listed verbatim so the audit is auditable; do not collapse into a
# single literal -- the per-token parametrization is what proves
# each token is actually checked.
FORBIDDEN_CALL_TOKENS: tuple[str, ...] = (
    "Read",
    "Edit",
    "Bash",
    "Tool",
    "Glob",
    "Grep",
    "Skill",
    "Task",
    "WebFetch",
    "WebSearch",
    "NotebookEdit",
    "TodoWrite",
    "ExitPlanMode",
    "EnterPlanMode",
)

# Negative lookbehind ``(?<![.\w])`` -- the previous character must
# be neither ``.`` (method access) nor an identifier character
# (suffix of a larger word).  Whitespace, ``(``, ``=``, ``,``,
# line start, etc. all permit the match.
_CALL_FORM_RE: re.Pattern[str] = re.compile(
    r"(?<![.\w])(" + "|".join(re.escape(tok) for tok in FORBIDDEN_CALL_TOKENS) + r")\("
)

# Vendor strings.  Case-insensitive because the AC forbids the
# vendor token in any case (``Anthropic``, ``ANTHROPIC``,
# ``anthropic``).  The bare ``\banthropic\b`` is wide enough to
# catch alternate hosts (``anthropic.com``), envelope headers
# (``Anthropic-Version``), and aspirational comments; there is no
# legitimate use of that token in the contract surface.
FORBIDDEN_VENDOR_PATTERNS: tuple[tuple[str, str], ...] = (
    ("claude.ai host", r"claude\.ai"),
    ("anthropic vendor token", r"\banthropic\b"),
)

_VENDOR_RE: re.Pattern[str] = re.compile(
    "|".join(f"(?:{pattern})" for _, pattern in FORBIDDEN_VENDOR_PATTERNS),
    re.IGNORECASE,
)


def _scan_call_form(text: str) -> list[tuple[int, str, str]]:
    """Return (lineno, token, stripped-line) for each call-form hit."""
    hits: list[tuple[int, str, str]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for match in _CALL_FORM_RE.finditer(line):
            hits.append((lineno, match.group(1), line.strip()))
    return hits


def _scan_vendor(text: str) -> list[tuple[int, str, str]]:
    """Return (lineno, matched_token, stripped-line) for each vendor hit."""
    hits: list[tuple[int, str, str]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for match in _VENDOR_RE.finditer(line):
            hits.append((lineno, match.group(0), line.strip()))
    return hits


# ---------------------------------------------------------------------------
# Static audit -- every contract-surface file must be clean.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "rel_path,role",
    CONTRACT_SURFACE_FILES,
    ids=[f"{role}:{rel}" for rel, role in CONTRACT_SURFACE_FILES],
)
def test_contract_surface_has_no_claude_tool_call_form(
    rel_path: str, role: str
) -> None:
    """NFR-016: zero ``Tool(`` call-form references in contract surfaces.

    Each surface category (job spec / result contract / CLI / monitor)
    is scanned in its own parametrization so a failure message names
    the role that broke caller-agnosticism.
    """
    source = SWARM_DIR / rel_path
    assert source.exists(), (
        f"Contract surface file missing: {source.relative_to(REPO_ROOT)} "
        f"(role={role}). NFR-016 audit cannot run without it."
    )
    hits = _scan_call_form(source.read_text(encoding="utf-8"))
    assert not hits, (
        f"NFR-016 violation in {role} surface "
        f"({source.relative_to(REPO_ROOT)}): Claude tool call-form leaked.\n"
        + "\n".join(f"  line {ln}: '{tok}(' -> {body}" for ln, tok, body in hits)
    )


@pytest.mark.parametrize(
    "rel_path,role",
    CONTRACT_SURFACE_FILES,
    ids=[f"{role}:{rel}" for rel, role in CONTRACT_SURFACE_FILES],
)
def test_contract_surface_has_no_vendor_strings(
    rel_path: str, role: str
) -> None:
    """NFR-016: zero ``claude.ai`` / ``anthropic`` vendor strings.

    Per-file parametrization mirrors the call-form audit so a
    regression in (e.g.) the result-contract surface points
    immediately at ``models.py`` / ``reduce.py`` rather than a
    pooled failure message.
    """
    source = SWARM_DIR / rel_path
    assert source.exists(), (
        f"Contract surface file missing: {source.relative_to(REPO_ROOT)} "
        f"(role={role}). NFR-016 audit cannot run without it."
    )
    hits = _scan_vendor(source.read_text(encoding="utf-8"))
    assert not hits, (
        f"NFR-016 violation in {role} surface "
        f"({source.relative_to(REPO_ROOT)}): vendor string leaked.\n"
        + "\n".join(f"  line {ln}: '{tok}' -> {body}" for ln, tok, body in hits)
    )


def test_contract_surface_set_covers_acceptance_roles() -> None:
    """T07.15 names four surface categories; the file table must cover them."""
    roles = {role for _, role in CONTRACT_SURFACE_FILES}
    required = {"job-spec", "result-contract", "CLI", "monitoring"}
    covered = {r for role in roles for r in role.split("/")}
    missing = required - covered
    assert not missing, f"NFR-016 surface roles missing coverage: {missing}"


def test_forbidden_call_token_set_is_nonempty() -> None:
    """Empty FORBIDDEN_CALL_TOKENS would silently green every surface scan."""
    assert FORBIDDEN_CALL_TOKENS, (
        "FORBIDDEN_CALL_TOKENS must enumerate Claude-tool surface; "
        "an empty tuple would render NFR-016 audit a no-op."
    )
    assert _CALL_FORM_RE.pattern, (
        "_CALL_FORM_RE.pattern is empty; the call-form audit would pass vacuously."
    )


def test_forbidden_vendor_pattern_set_is_nonempty() -> None:
    """Empty FORBIDDEN_VENDOR_PATTERNS would silently green vendor scans."""
    assert FORBIDDEN_VENDOR_PATTERNS, (
        "FORBIDDEN_VENDOR_PATTERNS must enumerate vendor surface; "
        "an empty tuple would render NFR-016 vendor audit a no-op."
    )
    assert _VENDOR_RE.pattern, (
        "_VENDOR_RE.pattern is empty; the vendor audit would pass vacuously."
    )


# ---------------------------------------------------------------------------
# Mutation guards -- prove the detectors actually flag each shape.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("token", FORBIDDEN_CALL_TOKENS)
def test_audit_detects_call_form_mutation(token: str) -> None:
    """Scanner must flag every Claude-tool call-form on a synthetic source.

    Without this guard, a regression in ``_scan_call_form`` (regex
    typo, broken negative lookbehind, empty token list) would let the
    surface scan pass vacuously on a real breach.
    """
    synthetic = f"def handler():\n    return {token}(arg=1)\n"
    hits = _scan_call_form(synthetic)
    assert any(tok == token for _, tok, _ in hits), (
        f"Scanner failed to detect injected call-form '{token}(' -- "
        "NFR-016 audit would silently pass on a real regression."
    )


def test_audit_excludes_method_call_form() -> None:
    """Negative: ``.read(`` / ``.edit(`` method calls must NOT be flagged.

    File-handle and stdin reads (``fh.read()``, ``sys.stdin.read()``)
    appear all over ``commands.py`` and must remain valid.  The
    negative-lookbehind anchor is what keeps the scan narrow; if it
    breaks, the audit will start screaming about legitimate I/O.
    """
    for synthetic in (
        "chunk = fh.read()\n",
        "raw = sys.stdin.read()\n",
        "buf = path.read_text()\n",
        "self.edit(value)\n",
        "config.bash(cmd)\n",
    ):
        hits = _scan_call_form(synthetic)
        assert not hits, (
            f"Scanner falsely flagged method-call form in {synthetic!r}: "
            f"{hits!r}. NFR-016 audit must stay narrow on call-form."
        )


def test_audit_excludes_identifier_suffix_form() -> None:
    """Negative: identifier suffixes like ``Reader(`` must NOT be flagged.

    A future contributor adding ``BashOperator``, ``Reader``, or
    ``EditableConfig`` must not trip the audit -- the AC targets the
    bare Claude tool surface, not every word with a shared prefix.
    """
    for synthetic in (
        "rdr = Reader(path)\n",
        "op = BashOperator(cmd)\n",
        "cfg = EditableConfig()\n",
        "g = GlobMatcher(pat)\n",
        "t = Taskbar()\n",
    ):
        hits = _scan_call_form(synthetic)
        assert not hits, (
            f"Scanner falsely flagged identifier suffix in {synthetic!r}: "
            f"{hits!r}. NFR-016 audit must not trip on prefix-shared names."
        )


def test_audit_detects_vendor_mutation_claude_ai() -> None:
    """Scanner flags ``claude.ai`` host URL in any case."""
    for synthetic in (
        "# see https://claude.ai/docs\n",
        "ORIGIN = 'https://Claude.AI/v1'\n",
        "url = 'CLAUDE.AI'\n",
    ):
        hits = _scan_vendor(synthetic)
        assert any("claude.ai" in tok.lower() for _, tok, _ in hits), (
            f"Scanner missed synthetic claude.ai mention in {synthetic!r}; "
            "NFR-016 vendor audit would silently pass on a real regression."
        )


def test_audit_detects_vendor_mutation_anthropic() -> None:
    """Scanner flags bare ``anthropic`` token in any case."""
    for synthetic in (
        "# upstream provider: anthropic\n",
        "VENDOR = 'Anthropic'\n",
        "HEADER = 'ANTHROPIC-Version: 2023-06-01'\n",
    ):
        hits = _scan_vendor(synthetic)
        assert any(tok.lower() == "anthropic" for _, tok, _ in hits), (
            f"Scanner missed synthetic anthropic token in {synthetic!r}; "
            "NFR-016 vendor audit must be case-insensitive."
        )


def test_audit_vendor_does_not_flag_unrelated_substrings() -> None:
    """Negative: ``anthropomorphic`` / ``anthropic_test`` must NOT trip.

    The ``\\banthropic\\b`` word boundary keeps the scan from noise on
    morphologically-related English words.  Without this guard, a
    future scan that drops the boundary anchor would generate
    false positives on unrelated identifiers.
    """
    for synthetic in (
        "# anthropomorphic interface\n",
        "VAR = 'anthropicism'\n",
    ):
        hits = _scan_vendor(synthetic)
        flagged_anthropic = [
            tok for _, tok, _ in hits if tok.lower() == "anthropic"
        ]
        assert not flagged_anthropic, (
            f"Scanner falsely flagged morpheme-related token in {synthetic!r}: "
            f"{hits!r}. NFR-016 vendor audit must use word boundaries."
        )


# ---------------------------------------------------------------------------
# Detached-survival check -- detached job must outlive SIGKILL of caller.
# ---------------------------------------------------------------------------


TMUX_PRESENT = shutil.which("tmux") is not None
NOT_NESTED = "TMUX" not in os.environ

requires_tmux = pytest.mark.skipif(
    not (TMUX_PRESENT and NOT_NESTED),
    reason="tmux binary absent or running inside tmux; detached survival "
    "check requires a clean tmux host",
)


@requires_tmux
def test_detached_job_survives_caller_sigkill() -> None:
    """T07.15 / FR-014 -- detached job survives a forced SIGKILL of caller.

    Companion to T07.02's clean-exit survival test.  Here we spawn a
    launcher subprocess that calls ``launch_detached`` then idles
    (so we can observe its PID), SIGKILL the launcher mid-flight, and
    confirm the tmux session remains live.  If the session were a
    foreground child of the launcher Python process, the kernel
    would tear it down with the parent on SIGKILL; the tmux
    daemon-spawned session survives because it is reparented to the
    tmux server.
    """
    from superclaude.cli.swarm import tmux as swarm_tmux

    job_id = f"t715-{uuid.uuid4().hex[:10]}"

    # Launcher: spawn detached session, then idle so we can SIGKILL it
    # mid-flight (otherwise it would exit cleanly and the test would
    # degenerate into the T07.02 clean-exit form).
    launcher_script = (
        "import sys, time;"
        "from superclaude.cli.swarm import tmux as t;"
        f"print(t.launch_detached({job_id!r}, ['sleep', '60']));"
        "sys.stdout.flush();"
        "time.sleep(30)"
    )
    launcher = subprocess.Popen(
        [sys.executable, "-c", launcher_script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        # Wait for the launcher to print the session name -- proof the
        # detached launch returned before we kill it.
        deadline = time.time() + 10.0
        session_name: str | None = None
        while time.time() < deadline:
            assert launcher.stdout is not None
            line = launcher.stdout.readline()
            if line:
                session_name = line.strip()
                break
            if launcher.poll() is not None:
                break
            time.sleep(0.05)
        assert session_name == f"swarm-{job_id}", (
            f"launcher did not emit expected session name in 10s; "
            f"got {session_name!r}, launcher.poll()={launcher.poll()}"
        )

        # SIGKILL the launcher -- no clean-up handlers run.
        launcher.send_signal(signal.SIGKILL)
        launcher.wait(timeout=5.0)
        assert launcher.returncode is not None, (
            "launcher did not terminate after SIGKILL"
        )

        # Detached tmux session must remain alive.  Poll briefly to
        # accommodate any propagation latency in the tmux server.
        deadline = time.time() + 5.0
        while time.time() < deadline:
            if swarm_tmux.has_session(job_id):
                break
            time.sleep(0.05)
        assert swarm_tmux.has_session(job_id) is True, (
            f"detached tmux session {session_name!r} did not survive "
            "SIGKILL of the launching process; FR-014 detached-mode "
            "guarantee broken."
        )
    finally:
        # Best-effort cleanup.  If the launcher is still somehow live,
        # reap it; then tear down the tmux session.
        if launcher.poll() is None:
            launcher.kill()
            launcher.wait(timeout=5.0)
        if TMUX_PRESENT and swarm_tmux.has_session(job_id):
            swarm_tmux.kill(job_id)
