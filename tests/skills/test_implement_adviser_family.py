"""Escalation-1 adviser family choice of sc-implement-protocol (SPEC FR-034, FR-035).

Enforcement type: STATIC - a pure-function reference of the FR-034 choice
(SPEC AC-18) and the pinned GPT spawn path (SPEC AC-19, V1 F-10).
"""

from pathlib import Path

_RETRY = (
    Path(__file__).resolve().parents[2]
    / "src/superclaude/skills/sc-implement-protocol/refs/retry.md"
).read_text(encoding="utf-8")

# Verified on 2026-10-25 (package artifacts/t10-spawn-path.md): no GPT alias, no full-id path.
GPT_SPAWN_PATH = "none verified; family-fallback applies"

CLAUDE_TOP = "claude-opus-5-5"
GPT_T1 = "gpt-6.1-sol"


def _family(model_id):
    m = (model_id or "").split("[", 1)[0]
    return (
        "claude" if m.startswith("claude-") else "gpt" if m.startswith("gpt-") else None
    )


def escalation_1(executor, gpt_t1=GPT_T1, claude_top=CLAUDE_TOP):
    """Return [adviser A, adviser B] as header dicts, per FR-034/FR-035."""
    fam = _family(executor)
    if fam == "gpt":
        a = {"model": gpt_t1, "family": "gpt", "rung": "T1"}
        want_b = "claude"
    else:  # Claude, neither family or unknown: adviser A is the Claude top rung
        a = {"model": claude_top, "family": "claude", "rung": "top"}
        want_b = "gpt"
    if want_b == "claude":
        b = {"model": claude_top, "family": "claude", "rung": "top"}
    elif gpt_t1 and _family(gpt_t1) == "gpt":
        b = {"model": gpt_t1, "family": "gpt", "rung": "T1"}
    else:
        b = {
            "model": claude_top,
            "family": "claude",
            "rung": "top",
            "family-fallback": "no reachable GPT T1 model",
        }
    return [a, b]


def header(b):
    line = f"model: {b['model']} family: {b['family']} rung: {b['rung']}"
    if "family-fallback" in b:
        line += f" family-fallback: {b['family-fallback']}"
    return line


def test_ac18_two_families_and_gpt_is_t1():
    for ex in (
        "claude-sonnet-5-5",
        "claude-opus-5-5",
        GPT_T1 + "[1m]",
        "grok-4.7",
        None,
    ):
        a, b = escalation_1(ex)
        assert a["family"] != b["family"], ex
        for adv in (a, b):
            if adv["family"] == "gpt":
                assert adv["rung"] == "T1", ex


def test_ac19_spawn_path_pinned():
    lines = [ln for ln in _RETRY.splitlines() if ln.startswith("GPT spawn path: ")]
    assert lines == ["GPT spawn path: " + GPT_SPAWN_PATH]


def test_ac19_no_gpt_reachable_gives_fallback_header_and_no_stop():
    assert GPT_SPAWN_PATH == "none verified; family-fallback applies"
    assert "`family-fallback: <reason>`" in _RETRY
    assert "never STOPs and never prompts the user" in _RETRY
    _, b = escalation_1("claude-opus-5-5", gpt_t1=None)
    h = header(b)
    assert h.startswith("model: ") and "family-fallback: " in h
    assert "STOP" not in h
