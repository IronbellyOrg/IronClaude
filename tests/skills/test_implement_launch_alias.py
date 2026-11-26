"""Launch alias of the retry-ladder advisers of sc-implement-protocol (issue 393).

Enforcement type: STATIC. The Agent call's `model` takes only an alias, never a model id,
so every adviser launch value must be an alias. This file pins the prose of
`refs/retry.md` that states that rule (`PINS`, each also run against five in-memory
mutations of the text) and checks a pure reference resolver, `plan`, over hermetic
environments given as plain dicts (the file never reads the process environment).

Known limit: the resolver reads the ladder prose as a reference model, not the prose
itself, so a wrong sentence outside the pins is caught only by a reviewer. A controlled
launch per alias stays a follow-up.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import TypedDict

import pytest

_ROOT = Path(__file__).resolve().parents[2]
_RETRY = (
    _ROOT / "src/superclaude/skills/sc-implement-protocol/refs/retry.md"
).read_text(encoding="utf-8")
_ALIAS_DOC = (_ROOT / "docs/reference/model-aliases.md").read_text(encoding="utf-8")

# Hard-coded on purpose: do not reuse `ALIASES` of test_model_alias_policy.py, which
# includes `inherit` (not allowed on the Agent call) and lacks `fable`.
AGENT_ALIASES = frozenset({"opus", "sonnet", "haiku", "fable"})

TAKES_ONLY = "takes only `opus`, `sonnet`, `haiku` or `fable`"
RULE_PHRASE = "is `opus` for every adviser"
HEADER_FORM = "model: <id> family: <claude|gpt> rung: <T1|top> launch: <alias>"
T3_SENTENCE = (
    "Every adviser on the primary ladder is launched on `opus`, and a pick whose id "
    "does not start with `claude-` carries `family-fallback`."
)
ANCHOR_START = "**Escalation rule.**"
ANCHOR_END = "Worked example with the fallback ladder:"
STALE = (
    "an executor on `T2Model02` or `T2Model01` gets adviser A on `T1Model02`",
    "adviser A is the GPT T1 model (`T1Model01` when the executor is not already on it",
)
RUNG_NAMES = ("T2bModel01", "T2Model02", "T1Model02", "T1Model01")
MODEL_ID = re.compile(r"\b(?:gpt|glm)-\d|claude-[a-z]+-\d")


def _between(text: str, start: str, end: str, include_end: bool = False) -> str:
    i = text.find(start)
    if i < 0:
        return ""
    j = text.find(end, i + len(start))
    if j < 0:
        return ""
    return text[i : j + len(end)] if include_end else text[i:j]


def _section(text: str) -> str:
    return _between(text, "### Model ladder", "### Cost and caps")


def _launch(text: str) -> str:
    """The Launch alias paragraphs: the label must start a line inside the section."""
    sec = _section(text)
    m = re.search(r"^\*\*Launch alias\.\*\*", sec, re.MULTILINE)
    return sec[m.start() :] if m else ""


def _region(text: str) -> str:
    """Escalation rule to the worked-example lead-in; empty unless each anchor occurs once."""
    if text.count(ANCHOR_START) != 1 or text.count(ANCHOR_END) != 1:
        return ""
    return _between(text, ANCHOR_START, ANCHOR_END, include_end=True)


def _table_ok(text: str) -> bool:
    i = text.find(ANCHOR_END)
    if i < 0:
        return False
    rows: list[str] = []
    for ln in text[i + len(ANCHOR_END) :].splitlines():
        if ln.startswith("|"):
            rows.append(ln)
        elif rows:
            break
    body = rows[2:]  # drop the header and the separator
    if len(body) != 4:
        return False
    for row in body:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        for cell in cells[1:4]:
            m = re.match(r"^\d+× `(\w+)`(?: \(([^)]*)\))?$", cell)
            if m is None or m.group(1) not in AGENT_ALIASES:
                return False
            if "launchable" in (m.group(2) or "") and "family-fallback" not in cell:
                return False
            if re.search(r"\b(?:gpt|glm|claude)-", cell):
                return False
    return True


def _line_resolving_b(text: str) -> str:
    return next(
        (ln for ln in text.splitlines() if ln.startswith("**Resolving adviser B.**")),
        "",
    )


def _count(word: str, text: str) -> int:
    return len(re.findall(rf"\b{word}\b", text))


def _alias_count_ok(p: str) -> bool:
    inside = p.count(TAKES_ONLY)
    return bool(p) and all(
        _count(w, p) == _count(w, TAKES_ONLY) * inside
        for w in ("sonnet", "haiku", "fable")
    )


PINS: dict[str, Callable[[str], bool]] = {
    "launch-rule": lambda t: RULE_PHRASE in _launch(t),
    "takes-only": lambda t: TAKES_ONLY in _launch(t),
    "never-full-id": lambda t: "never a full model id" in _launch(t),
    "family-fallback-token": lambda t: "`family-fallback: <reason>`" in _launch(t),
    "launch-header": lambda t: HEADER_FORM in _launch(t),
    "no-spawn-line": lambda t: (
        bool(_launch(t))
        and not any(ln.startswith("GPT spawn path: ") for ln in _launch(t).splitlines())
    ),
    "alias-count": lambda t: _alias_count_ok(_launch(t)),
    "region-sentence": lambda t: _region(t).count(T3_SENTENCE) == 1,
    "no-model-ids": lambda t: (
        bool(_launch(t))
        and bool(_region(t))
        and not MODEL_ID.search(_launch(t))
        and not MODEL_ID.search(_region(t))
    ),
    "line-181": lambda t: (
        bool(_line_resolving_b(t))
        and "strongest reachable model" not in _line_resolving_b(t)
        and "`opus`" in _line_resolving_b(t)
        and "the header form given under Launch alias below" in _line_resolving_b(t)
    ),
    "stale-absent": lambda t: (
        bool(_section(t))
        and not any(s in _section(t) for s in STALE)
        and all(n in _section(t) for n in RUNG_NAMES)
    ),
    "table": _table_ok,
}


def failed_pins(text: str) -> list[str]:
    return [name for name, check in PINS.items() if not check(text)]


def _mutate(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, f"mutation anchor not unique: {old!r}"
    return text.replace(old, new)


# (label, old, new, the pins the change must fail, and only those)
MUTATIONS: list[tuple[str, str, str, frozenset[str]]] = [
    (
        "rule opus to sonnet",
        RULE_PHRASE,
        "is `sonnet` for every adviser",
        frozenset({"launch-rule", "alias-count"}),
    ),
    (
        "sentence opus to sonnet",
        "is launched on `opus`, and a pick whose id",
        "is launched on `sonnet`, and a pick whose id",
        frozenset({"region-sentence"}),
    ),
    (
        "except adviser B",
        "Every adviser on the primary ladder is launched",
        "Every adviser on the primary ladder, except adviser B, is launched",
        frozenset({"region-sentence"}),
    ),
    (
        "gpt spawn sentence",
        " " + ANCHOR_END,
        " Adviser B is spawned on `gpt-6.1-sol`. " + ANCHOR_END,
        frozenset({"no-model-ids"}),
    ),
    (
        "strongest reachable model",
        "and writes it on line 1",
        "and writes the strongest reachable model on line 1",
        frozenset({"line-181"}),
    ),
]


def test_alias_set_matches_doc() -> None:
    lines = [ln for ln in _ALIAS_DOC.splitlines() if "takes the aliases" in ln]
    assert len(lines) == 1
    words = set(re.findall(r"`([^`]+)`", lines[0])) - {"model", "inherit"}
    assert words == AGENT_ALIASES


def test_every_pin_passes_on_the_changed_text() -> None:
    assert failed_pins(_RETRY) == []


@pytest.mark.parametrize("m", MUTATIONS, ids=[m[0] for m in MUTATIONS])
def test_mutation_fails_exactly_its_pins(
    m: tuple[str, str, str, frozenset[str]],
) -> None:
    label, old, new, expected = m
    failed = set(failed_pins(_mutate(_RETRY, old, new)))
    assert failed == expected, (
        f"{label}: expected pins {sorted(expected)}, got {sorted(failed)}"
    )


# ---------------------------------------------------------------- resolver


class Pick(TypedDict):
    id: str
    source: str  # the variable or alias the pick came from, or "unreachable"
    rung: str  # "T1", "top" or "other"
    launch: str
    family_fallback: bool


Env = Mapping[str, str]
Planner = Callable[[str, Env], dict[str, Pick]]

PRIMARY = RUNG_NAMES
FALLBACK = ("haiku", "sonnet", "opus")
T1_VARS = ("T1Model01", "T1Model02")
ROLES = ("esc1_a", "esc1_b", "critique", "esc2_1", "esc2_2")
_ALIAS_VAR = {
    "haiku": "ANTHROPIC_DEFAULT_HAIKU_MODEL",
    "sonnet": "ANTHROPIC_DEFAULT_SONNET_MODEL",
    "opus": "ANTHROPIC_DEFAULT_OPUS_MODEL",
}


def _strip(model_id: str) -> str:
    return model_id.split("[", 1)[0]


def _family(model_id: str) -> str | None:
    m = _strip(model_id)
    return (
        "claude" if m.startswith("claude-") else "gpt" if m.startswith("gpt-") else None
    )


def ladder(env: Env) -> tuple[str, tuple[str, ...]]:
    """The primary ladder only when all four rung variables are set and non-empty."""
    if all(env.get(v) for v in PRIMARY):
        return "primary", PRIMARY
    return "fallback", FALLBACK


def plan(executor_tier: str, env: Env) -> dict[str, Pick]:
    kind, rungs = ladder(env)
    top = rungs[-1]
    idx = rungs.index(executor_tier) if executor_tier in rungs else None
    ids = {
        r: _strip(env[r])
        if kind == "primary"
        else _strip(env.get(_ALIAS_VAR[r]) or f"claude-{r}-5-5")
        for r in rungs
    }

    def make(name: str | None) -> Pick:
        if name is None:  # no model of the wanted family can be reached
            return Pick(
                id="",
                source="unreachable",
                rung="T1",
                launch="opus",
                family_fallback=True,
            )
        rung = "top" if name == top else "T1" if name in T1_VARS else "other"
        if kind == "primary":
            return Pick(
                id=ids[name],
                source=name,
                rung=rung,
                launch="opus",
                family_fallback=_family(ids[name]) != "claude",
            )
        return Pick(
            id=ids[name], source=name, rung=rung, launch=name, family_fallback=False
        )

    def gpt_t1(own: str | None) -> str | None:
        cands = [v for v in T1_VARS if _family(ids[v]) == "gpt"]
        others = [v for v in cands if ids[v] != own]
        return next(iter(others or cands), None)

    def claude_top() -> str | None:
        return next((r for r in reversed(rungs) if _family(ids[r]) == "claude"), None)

    if kind == "fallback":  # Claude rungs only; a GPT T1 model is not launchable
        a: str | None = top if idx is None else rungs[min(idx + 1, len(rungs) - 1)]
        b: str | None = None
    else:
        fam = _family(ids[rungs[idx]]) if idx is not None else None
        if idx is None:
            a = top
        elif fam == "gpt":
            a = gpt_t1(ids[rungs[idx]])
        elif fam == "claude":
            a = (
                top
                if idx == len(rungs) - 1
                else next(
                    (r for r in rungs[idx + 1 :] if _family(ids[r]) == "claude"), top
                )
            )
        else:
            a = top
        afam = _family(ids[a]) if a else None
        if fam == "claude":
            b = gpt_t1(None)
        elif fam == "gpt":
            b = claude_top()
        else:
            b = gpt_t1(None) if afam == "claude" else claude_top()
    return {
        "esc1_a": make(a),
        "esc1_b": make(b),
        "critique": make(a),
        "esc2_1": make(top),
        "esc2_2": make(top),
    }


# ------------------------------------------------------------ environments

_OBSERVED = {
    "T2bModel01": "gpt-6.1-terra",
    "T2Model02": "glm-5.3",
    "T1Model02": "gpt-6.1-sol",
    "T1Model01": "claude-opus-5-5",
    "T2Model01": "gpt-6.1-sol",
}
ENVS: dict[str, dict[str, str]] = {
    "observed": dict(_OBSERVED),
    "swapped": {
        **_OBSERVED,
        "T1Model01": "gpt-6.1-sol",
        "T1Model02": "claude-opus-5-5",
    },
    "all-claude": {
        "T2bModel01": "claude-haiku-5-5",
        "T2Model02": "claude-sonnet-5-5",
        "T1Model02": "claude-opus-5-5",
        "T1Model01": "claude-fable-5-2",
    },
    "suffixed": {k: v + "[1m]" for k, v in _OBSERVED.items()},
    "partial": {**_OBSERVED, "T1Model01": ""},
    "fallback-tier-ids": {
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "gpt-6.1-sol[1m]",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-5.3",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "gpt-6.1-terra",
    },
}


def violations(name: str, env: Env, tier: str, recs: Mapping[str, Pick]) -> list[str]:
    kind, _ = ladder(env)
    out: list[str] = []
    for role in ROLES:
        r = recs[role]
        where = f"{name}/{tier}/{role}"
        if r["launch"] not in AGENT_ALIASES or "[" in r["launch"]:
            out.append(f"{where}: launch {r['launch']!r} is not a bare alias")
        if r["source"] == "T2Model01":
            out.append(f"{where}: picked T2Model01, which is never an adviser")
        if kind == "primary":
            if r["launch"] != "opus":
                out.append(
                    f"{where}: primary ladder launch is {r['launch']!r}, not opus"
                )
            if _family(r["id"]) != "claude" and not r["family_fallback"]:
                out.append(
                    f"{where}: non-claude pick {r['id']!r} lacks family-fallback"
                )
        elif r["source"] != "unreachable" and r["launch"] != r["source"]:
            out.append(
                f"{where}: fallback launch {r['launch']!r} is not its rung alias"
            )
    return out


def sweep(planner: Planner) -> list[str]:
    out: list[str] = []
    for name, env in ENVS.items():
        _, rungs = ladder(env)
        for tier in (*rungs, "unknown"):
            recs = planner(tier, env)
            assert set(recs) == set(ROLES)
            out += violations(name, env, tier, recs)
    return out


def test_sweep_is_clean_and_covers_both_ladders() -> None:
    assert sweep(plan) == []
    kinds = {ladder(env)[0] for env in ENVS.values()}
    assert kinds == {"primary", "fallback"}
    assert len(ENVS) == 6


def _header(r: Pick) -> str:
    fam = _family(r["id"]) or ""
    line = f"model: {r['id']} family: {fam} rung: {r['rung']} launch: {r['launch']}"
    return line + " family-fallback: no claude id" if r["family_fallback"] else line


def test_header_never_states_a_served_family() -> None:
    checked = 0
    for name, env in ENVS.items():
        _, rungs = ladder(env)
        for tier in (*rungs, "unknown"):
            for role, r in plan(tier, env).items():
                if not r["id"] or r["rung"] not in ("T1", "top"):
                    continue
                if _family(r["id"]) is None:
                    continue
                m = re.match(
                    r"^model: (\S+) family: (claude|gpt) rung: (T1|top) launch: (\w+)"
                    r"(?: family-fallback: .+)?$",
                    _header(r),
                )
                assert m is not None, (name, tier, role)
                assert m.group(2) == _family(
                    r["id"]
                )  # the pick's family, never launch's
                assert "served" not in _header(r)
                checked += 1
    assert checked > 0


def _raw_id_launch(tier: str, env: Env) -> dict[str, Pick]:
    return {k: {**v, "launch": v["id"]} for k, v in plan(tier, env).items()}


def _never_family_fallback(tier: str, env: Env) -> dict[str, Pick]:
    return {k: {**v, "family_fallback": False} for k, v in plan(tier, env).items()}


def _t2model01_one_rung_up(tier: str, env: Env) -> dict[str, Pick]:
    recs = plan(tier, env)
    if tier == "T2Model02" and env.get("T2Model01"):
        recs["esc1_a"] = Pick(
            id=_strip(env["T2Model01"]),
            source="T2Model01",
            rung="other",
            launch="opus",
            family_fallback=True,
        )
    return recs


@pytest.mark.parametrize(
    "planner",
    [_raw_id_launch, _never_family_fallback, _t2model01_one_rung_up],
    ids=["raw-id", "no-family-fallback", "t2model01-one-rung-up"],
)
def test_negative_control_is_flagged(planner: Planner) -> None:
    assert sweep(planner), "the checks missed a deliberately wrong resolver"
