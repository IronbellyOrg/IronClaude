"""Static-grep / core-purity tests (spec FR-1.3 / AC-9, §6.3).

T-104: every `gh` command in the skill sources + the hook is REPO-scoped to the
resolved origin repo — `gh pr`/`gh repo` pin `--repo <owner/repo>` (or ARE the
`gh repo view` resolution idiom that reads origin's `owner/repo`); `gh api` paths are
`repos/<owner/repo>/...` (gh api takes no --repo flag); `graphql` calls carry the repo
in their query vars. The repo is RESOLVED at runtime (origin's `nameWithOwner`,
fallback the origin remote URL), never a hardcoded fork — a BARE `gh pr`/`gh api` that
would silently default onto an upstream parent is the defect this greps for. T-N50: the
core-pure file set (state-machine.md, severity-routing.md, loop-guard.md AND
fsm.py/severity_router.py/loop_guard.py) contains ZERO `gh`/`git` tokens. T-N40: no
`--depth quick --fix` conflict is ever emitted. T-N41: the deterministic core never
imports the anthropic SDK (FR-G1 ban).
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "src" / "superclaude" / "skills" / "sc-pr-submit-protocol"
HOOK = REPO_ROOT / "src" / "superclaude" / "hooks" / "scripts" / "offer-pr-review.sh"
PR_SUBMIT_PKG = REPO_ROOT / "src" / "superclaude" / "pr_submit"

# Real gh command invocations (not the substring "gh" in prose like "through").
_GH_CMD = re.compile(r"\bgh\s+(pr|api|repo|release|run|auth|search|workflow)\b")
# The `gh repo view` resolution idiom — the de-hardcoding primitive. It reads the
# CURRENT checkout's `owner/repo` (so downstream calls can pin `--repo "$REPO"`); it
# has no target to misroute, so it counts as repo-scoped on its own.
_REPO_RESOLVE = re.compile(r"\bgh\s+repo\s+view\b")
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
AUGGIE_REVIEW_SKILL = (
    REPO_ROOT
    / "src"
    / "superclaude"
    / "skills"
    / "sc-auggie-review-protocol"
    / "SKILL.md"
)
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


def _repo_scoped(line: str) -> bool:
    """A gh command line is repo-scoped if it pins a whole-token ``--repo``, is a
    ``gh api`` call carrying a ``repos/<owner/repo>/`` path or ``graphql``, or IS the
    ``gh repo view`` resolution idiom.

    This is the generalized safety property: the prior implementation required the
    literal fork slug, but the repo is now RESOLVED at runtime — so "scoped" means the
    call carries an explicit repo reference (computed, not bare), never a hardcoded
    owner/repo. A bare `gh pr`/`gh api` with none of these would silently default onto
    an upstream parent → the defect.

    The match is structure-anchored, NOT a loose substring (D3 hardening): a trailing
    ``#`` comment is stripped first (so ``gh pr create … # see repos/docs`` does NOT
    pass), ``--repo`` is matched as a whole token (so ``--reposcope`` does NOT pass), and
    ``repos/``/``graphql`` only count when they ride on an actual ``gh api`` command (so
    an incidental ``# graphql`` mention does NOT pass). These three holes were real
    bypasses of the prior unanchored ``in``-substring predicate.
    """
    code = re.sub(r"\s+#.*$", "", line)  # strip a trailing shell / markdown comment
    if re.search(r"--repo\b", code):  # whole-token --repo (gh pr / gh repo)
        return True
    if _REPO_RESOLVE.search(code) is not None:  # the `gh repo view` resolution idiom
        return True
    # repos/ path or graphql must be on an actual `gh api` invocation, not anywhere.
    if re.search(r"\bgh\s+api\b", code) and ("repos/" in code or "graphql" in code):
        return True
    return False


def test_t104_every_gh_call_is_repo_scoped():
    """T-104: every ACTUAL gh command in the skill sources + hook is scoped to the resolved repo."""
    offenders: list[str] = []
    for path in _skill_and_hook_files():
        for lineno, line in _command_lines(path):
            if _GH_CMD.search(line) and not _repo_scoped(line):
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
    """T-105 (FR-1.3 / AC-7): the poll script's RUNTIME gh commands pin the RESOLVED repo.

    The runtime complement to T-104's static grep: T-104 proves no UNSCOPED gh
    command exists anywhere in the skill sources; T-105 asserts the ACTUAL gh
    invocations the poll script will run at runtime carry a COMPUTED repo pin —
    every `gh pr` line includes `--repo` (the resolved `$REPO`, never bare), and every
    `gh api` line targets a `repos/.../` path or `graphql` (`gh api` takes no `--repo`
    flag). The de-hardcoding generalizes the prior literal-fork pin to a resolved pin:
    the script first RESOLVES the repo (origin's `nameWithOwner`, fallback the origin
    remote) and threads it through every call. This guards FM-11 / the PR-target
    discipline at the level of the commands actually executed, not just prose.
    """
    assert POLL_SCRIPT.exists(), f"poll script missing: {POLL_SCRIPT}"
    # The script MUST resolve the target repo at runtime (the de-hardcoding mechanism) —
    # never assume a literal owner/repo.
    script_text = POLL_SCRIPT.read_text(encoding="utf-8")
    assert "nameWithOwner" in script_text, (
        "poll script does not resolve the target repo (expected `gh repo view --json nameWithOwner`)"
    )

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

    pr_offenders = [line.strip() for line in pr_lines if "--repo" not in line]
    assert not pr_offenders, (
        "runtime `gh pr` lines missing a `--repo <resolved>` pin (bare → upstream-default risk):\n"
        + "\n".join(pr_offenders)
    )

    api_offenders = [
        line.strip()
        for line in api_lines
        if "repos/" not in line and "graphql" not in line
    ]
    assert not api_offenders, (
        "runtime `gh api` lines not pinned to a repos/<owner/repo>/ path or graphql:\n"
        + "\n".join(api_offenders)
    )


def test_tn51_run_log_redacts_credentials_static():
    """T-N51 (NFR-7, static): run_log.py defines redaction patterns for token/credential scrubbing."""
    text = (PR_SUBMIT_PKG / "run_log.py").read_text(encoding="utf-8")
    assert "_REDACTION_PATTERNS" in text
    assert "[REDACTED]" in text


# --- V1.1 static gates (FR-8/FR-9, addendum §6.5) ----------------------------


def test_t1101_retrigger_gh_is_repo_scoped():
    """T-1101 (FR-8): every gh command in the gh-BEARING re-trigger surfaces
    (review-retrigger.md + retrigger-review.sh) is REPO-PINNED to the resolved
    `repos/<owner/repo>/...` (NOT bare gh api, NOT an upstream parent).

    These two files carry a gh token by design (the issue-comment POST surface), so they
    live on the T-104 repo-pin path, NOT the zero-token T-N50 set. (The broad
    test_t104 already scans them via SKILL_DIR.rglob; this is the tighter dedicated assert.)
    """
    offenders: list[str] = []
    for path in (REVIEW_RETRIGGER_REF, RETRIGGER_SCRIPT):
        assert path.exists(), f"re-trigger surface missing: {path}"
        for lineno, line in _command_lines(path):
            if _GH_CMD.search(line) and not _repo_scoped(line):
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
    pr_submit_skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    cmd = AUGGIE_REVIEW_CMD.read_text(encoding="utf-8")
    flag_string = "--depth quick --remediation-offer"
    # The byte-exact fallback invocation string is present in the ref and the canonical
    # Wave 6b skill text.
    assert flag_string in fallback
    assert flag_string in pr_submit_skill
    # Each flag the ref uses is a REAL option defined in auggie-review.md's option TABLE
    # (binding, not loose substring): every flag appears as a `| `--flag`` ...` table row.
    for flag in ("--depth", "--remediation-offer"):
        assert f"| `{flag}`" in cmd, (
            f"fallback flag {flag!r} is not a defined option row in auggie-review.md"
        )
    # `--depth quick`: `quick` must be an accepted VALUE on the --depth option row.
    depth_row = next(
        (ln for ln in cmd.splitlines() if ln.strip().startswith("| `--depth`")), ""
    )
    assert "quick" in depth_row, "`quick` is not an accepted value on the --depth row"
    # The command's documented default model must match the protocol default.
    model_row = next(
        (ln for ln in cmd.splitlines() if ln.strip().startswith("| `--auggie-model`")),
        "",
    )
    assert "`prism-b`" in model_row, (
        "prism-b is not the documented --auggie-model default"
    )
    # The INVOCATION line itself must NOT pass --no-post-pr (post-pr defaults true for a
    # PR target) and must NOT pass --auggie-model (fallback inherits /sc:auggie-review's
    # default model). The ref may MENTION either flag in prose; guard the actual
    # `> Skill ...` invocation line, not the whole document.
    invocation_lines = [
        ln
        for source in (fallback, pr_submit_skill)
        for ln in source.splitlines()
        if "sc:auggie-review-protocol" in ln
    ]
    assert invocation_lines, (
        "no fallback invocation line found in fallback docs or skill"
    )
    for ln in invocation_lines:
        assert "--no-post-pr" not in ln, f"invocation passes --no-post-pr: {ln}"
        assert "--auggie-model" not in ln, f"invocation passes --auggie-model: {ln}"


def test_auggie_review_protocol_defaults_to_prism_b():
    """The primary /sc:auggie-review Auggie invocation defaults to prism-b."""
    skill = AUGGIE_REVIEW_SKILL.read_text(encoding="utf-8")
    assert '--model "${AUGGIE_MODEL:-prism-b}"' in skill
    assert '${AUGGIE_MODEL:+--model "$AUGGIE_MODEL"}' not in skill


# --- D2: $REPO origin-URL resolution fallback (sed) -------------------------

_RESOLUTION_SCRIPTS = (
    SKILL_DIR / "scripts" / "poll-augment-review.sh",
    SKILL_DIR / "scripts" / "retrigger-review.sh",
    SKILL_DIR / "scripts" / "reply-resolve-thread.sh",
)

# Every remote-URL shape `git remote get-url origin` can emit, → the expected owner/repo.
_REMOTE_URL_FORMS = {
    "https://github.com/acme/widgets.git": "acme/widgets",
    "https://github.com/acme/widgets": "acme/widgets",
    "git@github.com:acme/widgets.git": "acme/widgets",  # scp-style ssh
    "ssh://git@github.com/acme/widgets.git": "acme/widgets",  # url-style ssh (D2 fix)
    "git@gitlab.com:acme/widgets.git": "acme/widgets",  # non-github host
}


def test_repo_resolution_sed_handles_all_url_forms():
    """D2: the $REPO origin-URL fallback `sed` program in each script must resolve EVERY
    remote-URL shape to a clean `owner/repo` — including url-style ssh (`ssh://…`), which
    the pre-D2 sed left as a malformed non-empty value that slipped past the empty-guard.

    The sed program is EXTRACTED from each script (not hardcoded here) so the test tracks
    the real resolution logic and cannot silently drift from it.
    """
    sed_re = re.compile(r"sed -E '([^']*)'")
    for script in _RESOLUTION_SCRIPTS:
        assert script.exists(), f"resolution script missing: {script}"
        match = next(
            (
                sed_re.search(line)
                for line in script.read_text(encoding="utf-8").splitlines()
                if "git remote get-url origin" in line and sed_re.search(line)
            ),
            None,
        )
        assert match, f"no `sed -E '…'` origin-URL fallback found in {script.name}"
        program = match.group(1)
        for url, expected in _REMOTE_URL_FORMS.items():
            result = subprocess.run(
                ["sed", "-E", program],
                input=url,
                text=True,
                capture_output=True,
                timeout=5,
            )
            got = result.stdout.strip()
            assert got == expected, (
                f"{script.name}: sed resolved {url!r} → {got!r}, expected {expected!r}"
            )


# --- D3: _repo_scoped is structure-anchored, not a loose substring ----------


def test_repo_scoped_rejects_bare_gh_bypasses():
    """D3: the tightened `_repo_scoped` must REJECT bare/upstream-defaulting gh lines that
    the prior unanchored `in`-substring predicate let through, while still ACCEPTING every
    genuinely repo-scoped form."""
    # Bare gh defects that MUST NOT be classified as scoped (these were real bypasses):
    bypasses = [
        "gh pr create --base x --head y  # see repos/docs",  # trailing-comment repos/
        "gh pr create --reposcope foo",  # --repo as a substring of --reposcope
        "gh pr merge 42 --merge  # graphql endpoint",  # incidental graphql in a comment
        "gh pr create --title t --body b",  # genuinely bare (no scope at all)
    ]
    for line in bypasses:
        assert _repo_scoped(line) is False, f"bare gh line wrongly scoped: {line!r}"
    # Genuinely scoped forms that MUST still pass:
    scoped = [
        'gh pr view "$PR" --repo "$REPO" --json number',
        "gh pr view <N> --repo <owner/repo> --json number",
        'gh api "repos/${REPO}/pulls/${PR}/comments"',
        "gh api repos/<owner/repo>/pulls/<N>/reviews",
        "gh api graphql -f query='...'",
        'REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"',
    ]
    for line in scoped:
        assert _repo_scoped(line) is True, f"scoped gh line wrongly rejected: {line!r}"
