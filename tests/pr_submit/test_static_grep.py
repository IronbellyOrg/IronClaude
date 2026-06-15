"""Static-grep / core-purity tests (spec FR-1.3 / AC-9, §6.3).

T-104: every `gh` command in the skill sources + the hook is fork-scoped — `gh pr`/
`gh repo` pin `--repo IronbellyOrg/IronClaude`; `gh api` paths are
`repos/IronbellyOrg/IronClaude/...` (gh api takes no --repo flag). T-N50: the
core-pure file set (state-machine.md, severity-routing.md, loop-guard.md AND
fsm.py/severity_router.py/loop_guard.py) contains ZERO `gh`/`git` tokens. T-N40: no
`--depth quick --fix` conflict is ever emitted. T-N41: the deterministic core never
imports the anthropic SDK (FR-G1 ban).
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "src" / "superclaude" / "skills" / "sc-pr-submit-protocol"
HOOK = REPO_ROOT / "src" / "superclaude" / "hooks" / "scripts" / "offer-pr-review.sh"
PR_SUBMIT_PKG = REPO_ROOT / "src" / "superclaude" / "pr_submit"

FORK = "IronbellyOrg/IronClaude"

# Real gh command invocations (not the substring "gh" in prose like "through").
_GH_CMD = re.compile(r"\bgh\s+(pr|api|repo|release|run|auth|search|workflow)\b")
# The T-N50 core-pure file set.
CORE_PURE_FILES = [
    SKILL_DIR / "refs" / "state-machine.md",
    SKILL_DIR / "refs" / "severity-routing.md",
    SKILL_DIR / "refs" / "loop-guard.md",
    # V1.1: the auggie-fallback ref carries NO gh token (it documents the
    # `> Skill sc:auggie-review-protocol` invocation + a flag table, not a gh api call),
    # so it joins the zero-token set. The gh-BEARING review-retrigger.md + retrigger-review.sh
    # are DELIBERATELY excluded (covered by the T-104 / T-1101 fork-pin path instead) —
    # mirroring how thread-reply.md / augment-poll.md are excluded for the same reason.
    SKILL_DIR / "refs" / "auggie-fallback.md",
    PR_SUBMIT_PKG / "fsm.py",
    PR_SUBMIT_PKG / "severity_router.py",
    PR_SUBMIT_PKG / "loop_guard.py",
]

AUGGIE_REVIEW_CMD = REPO_ROOT / "src" / "superclaude" / "commands" / "auggie-review.md"
RETRIGGER_SCRIPT = SKILL_DIR / "scripts" / "retrigger-review.sh"
REVIEW_RETRIGGER_REF = SKILL_DIR / "refs" / "review-retrigger.md"
AUGGIE_FALLBACK_REF = SKILL_DIR / "refs" / "auggie-fallback.md"


def _skill_and_hook_files() -> list[Path]:
    files = [HOOK]
    files += [
        p for p in SKILL_DIR.rglob("*") if p.is_file() and p.suffix in (".md", ".sh")
    ]
    return files


def _command_lines(path: Path):
    """Yield (lineno, logical_line) for ACTUAL command lines (not prose / comments).

    - `.sh`: skip comment lines (leading `#`); join backslash line-continuations so a
      multi-line `gh api ... \\` command is checked as one logical line.
    - `.md`: only lines INSIDE fenced ``` code blocks (real command examples), never
      prose mentions of `gh` in backticks.
    """
    raw = path.read_text(encoding="utf-8").splitlines()
    if path.suffix == ".sh":
        out, buf, start = [], "", 0
        for i, line in enumerate(raw, 1):
            stripped = line.strip()
            if not buf and stripped.startswith("#"):
                continue
            if not buf:
                start = i
            if line.rstrip().endswith("\\"):
                buf += line.rstrip()[:-1] + " "
                continue
            out.append((start, buf + line))
            buf = ""
        if buf:
            out.append((start, buf))
        return out
    # .md — only fenced code blocks
    out, in_fence = [], False
    for i, line in enumerate(raw, 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            out.append((i, line))
    return out


def _fork_scoped(line: str) -> bool:
    """A gh command line is fork-scoped if it names the fork, pins --repo, or is graphql."""
    return FORK in line or "--repo" in line or "graphql" in line


def test_t104_every_gh_call_is_fork_scoped():
    """T-104: every ACTUAL gh command in the skill sources + hook is scoped to the fork."""
    offenders: list[str] = []
    for path in _skill_and_hook_files():
        for lineno, line in _command_lines(path):
            if _GH_CMD.search(line) and not _fork_scoped(line):
                offenders.append(
                    f"{path.relative_to(REPO_ROOT)}:{lineno}: {line.strip()}"
                )
    assert not offenders, "Unscoped gh commands:\n" + "\n".join(offenders)


def test_tn50_core_pure_no_gh_git_tokens():
    """T-N50: the core-pure file set contains ZERO `gh`/`git` tokens (NFR-6 / AC-9)."""
    token = re.compile(r"\bgh\b|\bgit\b")
    offenders: list[str] = []
    for path in CORE_PURE_FILES:
        assert path.exists(), f"core-pure file missing: {path}"
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if token.search(line):
                offenders.append(
                    f"{path.relative_to(REPO_ROOT)}:{lineno}: {line.strip()}"
                )
    assert not offenders, "gh/git tokens in core-pure files:\n" + "\n".join(offenders)


def test_tn40_no_depth_quick_fix_anywhere():
    """T-N40: the `--depth quick --fix` conflict is never emitted by any skill source."""
    offenders: list[str] = []
    for path in _skill_and_hook_files():
        text = path.read_text(encoding="utf-8")
        # Allow the explicit STOP-warnings that NAME the forbidden form to forbid it.
        for lineno, line in enumerate(text.splitlines(), 1):
            if (
                "--depth quick --fix" in line
                and "never" not in line.lower()
                and "stop" not in line.lower()
            ):
                offenders.append(
                    f"{path.relative_to(REPO_ROOT)}:{lineno}: {line.strip()}"
                )
    assert not offenders, "emitted --depth quick --fix:\n" + "\n".join(offenders)


def test_tn41_core_never_imports_anthropic():
    """T-N41: the deterministic core never imports the anthropic SDK (FR-G1 ban)."""
    offenders: list[str] = []
    for path in PR_SUBMIT_PKG.glob("*.py"):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if re.search(r"^\s*(import|from)\s+anthropic\b", line):
                offenders.append(
                    f"{path.relative_to(REPO_ROOT)}:{lineno}: {line.strip()}"
                )
    assert not offenders, "anthropic import in core:\n" + "\n".join(offenders)


POLL_SCRIPT = (
    REPO_ROOT
    / "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh"
)


def test_t105_runtime_repo_pin():
    """T-105 (FR-1.3 / AC-7): the poll script's RUNTIME gh commands pin the fork.

    The runtime complement to T-104's static grep: T-104 proves no UNSCOPED gh
    command exists anywhere in the skill sources; T-105 asserts the ACTUAL gh
    invocations the poll script will run at runtime carry the fork pin —
    every `gh pr` line includes `--repo IronbellyOrg/IronClaude`, and every
    `gh api` line targets `repos/IronbellyOrg/IronClaude/...` or `graphql`
    (`gh api` takes no `--repo` flag). This guards FM-11 / the PR-target fork
    discipline at the level of the commands actually executed, not just prose.
    """
    assert POLL_SCRIPT.exists(), f"poll script missing: {POLL_SCRIPT}"
    pr_lines: list[str] = []
    api_lines: list[str] = []
    for _lineno, line in _command_lines(POLL_SCRIPT):
        if re.search(r"\bgh\s+pr\b", line):
            pr_lines.append(line)
        if re.search(r"\bgh\s+api\b", line):
            api_lines.append(line)

    # The script MUST issue at least one gh pr and one gh api call at runtime.
    assert pr_lines, "no runtime `gh pr` command found in the poll script"
    assert api_lines, "no runtime `gh api` command found in the poll script"

    pr_offenders = [line.strip() for line in pr_lines if f"--repo {FORK}" not in line]
    assert not pr_offenders, (
        "runtime `gh pr` lines missing `--repo IronbellyOrg/IronClaude`:\n"
        + "\n".join(pr_offenders)
    )

    api_offenders = [
        line.strip()
        for line in api_lines
        if f"repos/{FORK}" not in line and "graphql" not in line
    ]
    assert not api_offenders, (
        "runtime `gh api` lines not pinned to repos/IronbellyOrg/IronClaude or graphql:\n"
        + "\n".join(api_offenders)
    )


def test_tn51_run_log_redacts_credentials_static():
    """T-N51 (NFR-7, static): run_log.py defines redaction patterns for token/credential scrubbing."""
    text = (PR_SUBMIT_PKG / "run_log.py").read_text(encoding="utf-8")
    assert "_REDACTION_PATTERNS" in text
    assert "[REDACTED]" in text


# --- V1.1 static gates (FR-8/FR-9, addendum §6.5) ----------------------------


def test_t1101_retrigger_gh_is_fork_scoped():
    """T-1101 (FR-8): every gh command in the gh-BEARING re-trigger surfaces
    (review-retrigger.md + retrigger-review.sh) is FORK-PINNED to
    repos/IronbellyOrg/IronClaude (NOT bare gh api, NOT upstream).

    These two files carry a gh token by design (the issue-comment POST surface), so they
    live on the T-104 fork-pin path, NOT the zero-token T-N50 set. (The broad
    test_t104 already scans them via SKILL_DIR.rglob; this is the tighter dedicated assert.)
    """
    offenders: list[str] = []
    for path in (REVIEW_RETRIGGER_REF, RETRIGGER_SCRIPT):
        assert path.exists(), f"re-trigger surface missing: {path}"
        for lineno, line in _command_lines(path):
            if _GH_CMD.search(line) and not _fork_scoped(line):
                offenders.append(
                    f"{path.relative_to(REPO_ROOT)}:{lineno}: {line.strip()}"
                )
    assert not offenders, "Unscoped gh in re-trigger surfaces:\n" + "\n".join(offenders)


def test_t1105_retrigger_token_in_script_not_core():
    """T-1105 (FR-8): the `auggie review` POST token lives in the bash script, while the
    FSM (the posting-decision core) holds NO hard-coded trigger literal — the FSM decides
    WHETHER/WHEN to re-trigger via the `do_retrigger` seam; the script carries the token.

    NOTE: `detection.py`'s `accepted_trigger_phrases` legitimately contains the phrases for
    DETECTION (recognizing an operator/App trigger), which is the contract's RECOGNITION
    side — distinct from the POSTING side this test guards. So this test scopes to fsm.py.
    """
    script = RETRIGGER_SCRIPT.read_text(encoding="utf-8")
    assert "auggie review" in script  # the script emits the trigger token
    # The FSM must NOT hard-code the POSTED trigger literal.
    fsm_src = (PR_SUBMIT_PKG / "fsm.py").read_text(encoding="utf-8").lower()
    assert "auggie review" not in fsm_src, "hard-coded trigger literal in fsm.py"


def test_t1115_auggie_fallback_flag_parity():
    """T-1115 (FR-9.3): the auggie-fallback ref's invocation flag string matches the
    flags the auggie-review command actually defines (no drift)."""
    fallback = AUGGIE_FALLBACK_REF.read_text(encoding="utf-8")
    cmd = AUGGIE_REVIEW_CMD.read_text(encoding="utf-8")
    flag_string = "--depth quick --remediation-offer --auggie-model claude-sonnet-4-6"
    # The byte-exact fallback invocation string is present in the ref.
    assert flag_string in fallback
    # Each flag the ref uses is a REAL option defined in auggie-review.md's option TABLE
    # (binding, not loose substring): every flag appears as a `| `--flag`` ...` table row.
    for flag in ("--depth", "--remediation-offer", "--auggie-model"):
        assert f"| `{flag}`" in cmd, (
            f"fallback flag {flag!r} is not a defined option row in auggie-review.md"
        )
    # `--depth quick`: `quick` must be an accepted VALUE on the --depth option row.
    depth_row = next(
        (ln for ln in cmd.splitlines() if ln.strip().startswith("| `--depth`")), ""
    )
    assert "quick" in depth_row, "`quick` is not an accepted value on the --depth row"
    # `--auggie-model claude-sonnet-4-6`: the model is the documented --auggie-model example.
    model_row = next(
        (ln for ln in cmd.splitlines() if ln.strip().startswith("| `--auggie-model`")),
        "",
    )
    assert "claude-sonnet-4-6" in model_row, (
        "claude-sonnet-4-6 is not the documented --auggie-model example"
    )
    # The INVOCATION line itself must NOT pass --no-post-pr (post-pr defaults true for a
    # PR target). The ref may MENTION --no-post-pr in prose ("must NOT be passed"); guard
    # the actual `> Skill ...` invocation line, not the whole document.
    invocation_lines = [
        ln for ln in fallback.splitlines() if "sc:auggie-review-protocol" in ln
    ]
    assert invocation_lines, "no fallback invocation line found in auggie-fallback.md"
    for ln in invocation_lines:
        assert "--no-post-pr" not in ln, f"invocation passes --no-post-pr: {ln}"
