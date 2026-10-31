"""Static checks for the routing-refresh fixture (fixtures/routing_refresh_cases.json).

The fixture defines the S01-S29 recommendation-generation cases, the T01-T76
traceability map and the 47-command dispositions from the approved spec. These
tests are static: they validate the fixture against the repository's current
guide, commands and skills. They run no model, execute no recommended command
and touch nothing outside pytest's tmp paths. Observed generation results are
recorded separately by plan Task 8.
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

import pytest

from superclaude.cli.recommend.prompts import CLASSIFICATION_KEYS

_REPO = Path(__file__).resolve().parents[2]
_FIXTURE = Path(__file__).parent / "fixtures/routing_refresh_cases.json"
_GUIDE = _REPO / "src/superclaude/core/HOW-WE-WORK.md"
_SKILL = _REPO / "src/superclaude/skills/sc-recommend/SKILL.md"
_COMMANDS = _REPO / "src/superclaude/commands"
_SKILLS = _REPO / "src/superclaude/skills"
_PACKAGE = "TASK-RESEARCH-recommend-refresh-20261024-044336"
# Commands shipped after the frozen routing-refresh research package was written:
# issue #323 (codegraph adoption, Phase 3) adds /sc:graph. The package is frozen,
# so the shipped set is compared minus these additions.
_POST_REFRESH_ADDITIONS = {"graph"}

_TOKEN_RE = re.compile(r"`/([a-z][a-z0-9:-]*)")
_FLAG_RE = re.compile(r"--[a-z][a-z0-9-]*")
_FIXTURE_REF_RE = re.compile(r"\{fixture:([a-z0-9-]+)\}")
_ACTIVATION_RE = re.compile(
    r"^## (?:Activation|Skill Invocation)\n(.*?)(?=^## |\Z)", re.M | re.S
)
_AUTHORITIES = {
    "read-only",
    "report-only",
    "artifact-only",
    "documents-only",
    "plan-only",
    "mutating-with-approval",
    "memory-write",
}
_CASE_KEYS = {
    "id",
    "request",
    "environment",
    "guide_route",
    "targets",
    "mode_flags",
    "retained_inputs",
    "stop",
    "authority",
    "side_effects",
    "guide_phrases",
    "negative",
    "activation",
    "repeats",
    "variants",
}
_RETIRED = {"estimate", "sc", "select-tool", "task-mcp"}


def _data() -> dict:
    return json.loads(_FIXTURE.read_text(encoding="utf-8"))


_CASES = _data()["cases"]


def _primitive(token: str) -> Path | None:
    """Return the source file for /sc:<command>, /<skill> or a skill directory name."""
    if token.startswith("sc:") and not token.endswith("-protocol"):
        path = _COMMANDS / f"{token[3:]}.md"
    else:
        path = _SKILLS / token.replace(":", "-") / "SKILL.md"
    return path if path.is_file() else None


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _block(begin: str, end: str) -> str:
    text = _GUIDE.read_text(encoding="utf-8")
    start = text.index(begin) + len(begin)
    return text[start : text.index(end, start)]


def _route(route: dict) -> tuple[str, str]:
    """Return (steps, steps + notes) for a routing row or an Other-commands line."""
    if route["block"] == "routing":
        cells = _routing_rows()[route["row"]]
        return cells[3], f"{cells[3]} {cells[7]}"
    block = _block("<!-- other-commands:v1 -->", "<!-- /other-commands -->")
    line = next(
        ln for ln in block.splitlines() if ln.startswith(f"| `/{route['command']}`")
    )
    return line, line


_LEADING_GUARD_RE = re.compile(r"^\s*\d+[a-z]?\. only (?:for|when|if) ")
_TRAILING_GUARD_RE = re.compile(r"`[^`]*`[^`]*\(only (?:if|for) [^)]+\)")


def _conditional_step(step: str) -> bool:
    """True when the step opens with an "only for/when/if" guard or carries one in
    parentheses right after its command; a stray "only " elsewhere does not count."""
    return bool(_LEADING_GUARD_RE.match(step) or _TRAILING_GUARD_RE.search(step))


def _spec_path() -> Path:
    found = sorted(_REPO.glob(f".dev/tasks/*/{_PACKAGE}/SPEC-sc-recommend-refresh.md"))
    assert len(found) == 1, found
    return found[0]


def _section(text: str, start: str, end: str) -> str:
    begin = text.index(start)
    return text[begin : text.index(end, begin + len(start))]


def test_fixture_schema_and_completeness():
    data = _data()
    assert data["schema"] == "routing-refresh-cases/1"
    assert data["evidence_class"].startswith("static definitions")
    assert "Task 8" in data["evidence_class"]
    ids = [case["id"] for case in data["cases"]]
    assert ids == [f"S{n:02d}" for n in range(1, 30)]
    assert list(data["checks"]) == [f"T{n:02d}" for n in range(1, 77)]
    assert len(data["commands"]) == 47
    defined = set(data["fixture_inputs"])
    for case in data["cases"]:
        assert _CASE_KEYS <= set(case), (case["id"], _CASE_KEYS - set(case))
        assert case["request"].strip() and case["stop"].strip(), case["id"]
        assert case["environment"] in data["environments"], case["id"]
        assert case["authority"] in _AUTHORITIES, case["id"]
        assert case["targets"] and case["negative"]["competitors"], case["id"]
        assert case["negative"]["must_not"].strip(), case["id"]
        assert set(case["variants"]) == {"unavailable_plugin", "seeded_wrong_cache"}
        for variant in case["variants"].values():
            assert variant["environment"] in data["environments"], case["id"]
            assert variant["expected"].strip(), case["id"]
        used = set(_FIXTURE_REF_RE.findall(json.dumps(case)))
        assert used <= defined, (case["id"], used - defined)
    for check, entry in data["checks"].items():
        assert entry["static"] or entry.get("behavioral") == "Task8", check
        assert entry.get("behavioral") in (None, "Task8"), check


def test_every_mapped_test_function_exists():
    """Each T-check names real test functions, so the map cannot rot silently."""
    for check, entry in _data()["checks"].items():
        for ref in entry["static"]:
            rel, *names = ref.split("::")
            path = _REPO / rel
            assert path.is_file(), (check, rel)
            scope = ast.parse(path.read_text(encoding="utf-8")).body
            for name in names:
                node = next(
                    (
                        n
                        for n in scope
                        if isinstance(n, (ast.FunctionDef, ast.ClassDef))
                        and n.name == name
                    ),
                    None,
                )
                assert node is not None, (check, ref)
                scope = node.body
            assert names[-1].startswith("test_"), (check, ref)


@pytest.mark.parametrize("case", _CASES, ids=[case["id"] for case in _CASES])
def test_case_targets_and_competitors_are_current_primitives(case):
    tokens = list(case["targets"]) + list(case["negative"]["competitors"])
    for repeat in case["repeats"]:
        tokens += repeat["targets"]
    for token in tokens:
        assert _primitive(token) is not None, (case["id"], token)
        assert token.removeprefix("sc:") not in _RETIRED, (case["id"], token)
    competitors = set(case["negative"]["competitors"])
    assert not competitors & set(case["targets"]), case["id"]


@pytest.mark.parametrize("case", _CASES, ids=[case["id"] for case in _CASES])
def test_case_guide_route_supports_expected_target(case):
    """The canonical guide names the target, the phrases and not the competitor."""
    routes = [(case["guide_route"], case["targets"], case["guide_phrases"])]
    for repeat in case["repeats"]:
        if "guide_route" in repeat:
            routes.append(
                (repeat["guide_route"], repeat["targets"], repeat["guide_phrases"])
            )
    competitors = set(case["negative"]["competitors"])
    for index, (route, targets, phrases) in enumerate(routes):
        steps, text = _route(route)
        named = set(_TOKEN_RE.findall(steps))
        assert set(targets) <= named, (case["id"], set(targets) - named)
        for phrase in phrases:
            assert phrase in text, (case["id"], phrase)
        if index and route != case["guide_route"]:
            # A repeat on its own route must not name the case's competitors either,
            # unless the repeat deliberately selects that primitive.
            clash = (competitors - set(targets)) & named
            assert not clash, (case["id"], "repeat", clash)
    steps, _ = _route(case["guide_route"])
    if case["negative"].get("absent_from_route", True):
        clash = competitors & set(_TOKEN_RE.findall(steps))
        assert not clash, (case["id"], clash)
    else:
        # Shared rows may name a competitor, but only inside an explicitly
        # conditional step, never as an unconditional default.
        for step in steps.split("<br>"):
            present = competitors & set(_TOKEN_RE.findall(step))
            if present:
                assert _conditional_step(step), (case["id"], present, step)
    for forbidden in case.get("forbidden_step_text", []):
        assert forbidden not in steps, (case["id"], forbidden)
    if case["guide_route"]["block"] == "routing" and case["authority"] in {
        "read-only",
        "report-only",
    }:
        row = case["guide_route"]["row"]
        block = _block("<!-- routing-table:v1 -->", "<!-- /routing-table -->")
        line = next(ln for ln in block.splitlines() if ln.startswith(f"| {row} |"))
        assert _cells(line)[5] != "yes", (case["id"], row)


_EXAMPLES_RE = re.compile(r"^## Examples\n.*?(?=^## |\Z)", re.M | re.S)
_USAGE_RE = re.compile(r"^## Usage\n(.*?)(?=^## |\Z)", re.M | re.S)
_HINT_RE = re.compile(r"^argument-hint:\s*(.+)$", re.M)
_ENUM_RE = re.compile(
    r"(--[a-z][a-z0-9-]*)[ =]([a-z][a-z0-9_-]*(?:[|/][a-z][a-z0-9_-]*)+)(?=[\]\s)`]|$)"
)
_TABLE_PAIR_RE = re.compile(r"`(--[a-z][a-z0-9-]*) ([a-z][a-z0-9_-]*)`")


def _declared(source: str) -> tuple[str, dict[str, set[str]]]:
    """Declared interface text and flag -> enumerated values, taken only from the
    Usage block, argument-hint front matter and option-table first cells (T40/T44).
    Examples never count. A flag with an empty value set takes a placeholder."""
    body = _EXAMPLES_RE.sub("", source)
    firsts = [
        _cells(ln)[0] for ln in body.splitlines() if re.match(r"\|\s*`(--|<)", ln)
    ]
    text = "\n".join(_HINT_RE.findall(body) + _USAGE_RE.findall(body) + firsts)
    values: dict[str, set[str]] = {flag: set() for flag in _FLAG_RE.findall(text)}
    for flag, enum in _ENUM_RE.findall(text):
        values[flag] |= set(re.split(r"[|/]", enum))
    for cell in firsts:
        pair = _TABLE_PAIR_RE.fullmatch(cell)
        if pair:
            values[pair.group(1)].add(pair.group(2))
    return text, values


def _mode_declared(mode: str, source: str) -> bool:
    """`--flag`, `--flag value` or a keyword mode (`create`, `mode=quick`) is declared."""
    text, values = _declared(source)
    flag, _, value = mode.partition(" ")
    if not flag.startswith("--"):
        return re.search(rf"(?<![\w=-]){re.escape(flag)}(?![\w=-])", text) is not None
    if flag not in values:
        return False
    return not value or not values[flag] or value in values[flag]


@pytest.mark.parametrize("case", _CASES, ids=[case["id"] for case in _CASES])
def test_case_mode_flags_are_declared_by_their_target(case):
    """Every flag, flag value or keyword mode the fixture expects is declared by its
    target's Usage, argument hint or option table, never only by an example."""
    entries = [(case.get("flag_target", case["targets"][0]), case["mode_flags"])]
    entries += [(r["targets"][0], r["mode_flags"]) for r in case["repeats"]]
    for target, flags in entries:
        path = _primitive(target)
        assert path is not None, (case["id"], target)
        source = path.read_text(encoding="utf-8")
        for flag in flags:
            assert _mode_declared(flag, source), (case["id"], target, flag)


def test_flag_value_check_rejects_undeclared_enumerated_value():
    explain = (_COMMANDS / "explain.md").read_text(encoding="utf-8")
    improve = (_COMMANDS / "improve.md").read_text(encoding="utf-8")
    assert _mode_declared("--level basic", explain)
    assert not _mode_declared("--level beginner", explain)
    # improve --preview appears only in an example, so it is not declared.
    assert "--preview" in improve
    assert not _mode_declared("--preview", improve)
    index_repo = (_COMMANDS / "index-repo.md").read_text(encoding="utf-8")
    assert _mode_declared("mode=quick", index_repo)
    assert not _mode_declared("mode=full", index_repo)


def _entries(case: dict):
    """The case and each repeat with its effective guide route (repeats inherit)."""
    yield case, case["guide_route"]
    for repeat in case["repeats"]:
        yield repeat, repeat.get("guide_route", case["guide_route"])


def _routing_rows() -> dict[str, list[str]]:
    block = _block("<!-- routing-table:v1 -->", "<!-- /routing-table -->")
    lines = [ln for ln in block.splitlines() if ln.startswith("|")][2:]
    return {_cells(ln)[0]: _cells(ln) for ln in lines}


def _route_problems(entry: dict, route: dict) -> list:
    """SKILL.md Step 0: Other commands apply only on no_match, so an "other" route is
    wrong for any target that a routing row names in its steps."""
    if route["block"] != "other":
        return []
    routed = {
        t for cells in _routing_rows().values() for t in _TOKEN_RE.findall(cells[3])
    }
    return sorted(set(entry["targets"]) & routed)


@pytest.mark.parametrize("case", _CASES, ids=[case["id"] for case in _CASES])
def test_other_command_routes_are_not_named_by_a_routing_row(case):
    for entry, route in _entries(case):
        assert not _route_problems(entry, route), (case["id"], entry["request"])


def test_route_check_rejects_other_route_for_a_routed_command():
    old = {
        "request": "Generate coordinated project documentation.",
        "targets": ["sc:index"],
    }
    assert _route_problems(old, {"block": "other", "command": "sc:index"}) == [
        "sc:index"
    ]
    fixed = {"block": "routing", "row": "document-built"}
    assert _route_problems(old, fixed) == []


def _required_positionals(source: str) -> set[str]:
    """`<name>` rows that an option table marks Required: Yes (Examples excluded)."""
    required: set[str] = set()
    header: list[str] | None = None
    for line in _EXAMPLES_RE.sub("", source).splitlines():
        if not line.startswith("|"):
            header = None
            continue
        cells = _cells(line)
        if header is None:
            header = cells
        elif "Required" in header and len(cells) == len(header):
            name = re.fullmatch(r"`(<[^>]+>)`", cells[0])
            if name and cells[header.index("Required")].lower().startswith("yes"):
                required.add(name.group(1))
    return required


def _positional_problems(entry: dict) -> list:
    """Each Required positional is bound to a retained input the request supplies,
    or the entry expects a clarification question for it."""
    required: set[str] = set()
    for target in entry["targets"]:
        required |= _required_positionals(_primitive(target).read_text("utf-8"))
    bound = entry.get("positionals", {})
    asked = set(entry.get("clarify", []))
    problems = []
    if set(bound) | asked != required or set(bound) & asked:
        problems.append(("positionals", sorted(required), sorted(bound), sorted(asked)))
    for name, value in bound.items():
        if (
            value not in entry.get("retained_inputs", [])
            or value not in entry["request"]
        ):
            problems.append(("unretained", name, value))
    if asked and "clarification" not in entry.get("expected", ""):
        problems.append(("no clarification", sorted(asked)))
    return problems


@pytest.mark.parametrize("case", _CASES, ids=[case["id"] for case in _CASES])
def test_required_positionals_are_retained_or_clarified(case):
    for entry, _ in _entries(case):
        assert not _positional_problems(entry), (case["id"], entry["request"])


def test_positional_check_rejects_a_dropped_required_spec_path():
    old = {
        "request": "Continue the release split from {fixture:validated-proposal}.",
        "targets": ["sc:release-split"],
        "expected": "validated-proposal continuation retained",
    }
    assert _required_positionals(
        (_COMMANDS / "release-split.md").read_text("utf-8")
    ) == {"<spec-file-path>"}
    assert _positional_problems(old)
    unretained = dict(old, positionals={"<spec-file-path>": "{fixture:release-spec}"})
    assert _positional_problems(unretained)


def _labelled_steps(steps: str) -> dict[str, str]:
    labelled = {}
    for step in steps.split("<br>"):
        label = re.match(r"\s*(\d+[a-z]?)\. ", step)
        if label:
            labelled[label.group(1)] = step
    return labelled


def _mandatory_problems(entry: dict, route: dict) -> list:
    """The entry lists exactly the guide row's mandatory_flags entries for the steps
    that name one of its targets, and each listed flag is declared by that command."""
    listed = entry.get("mandatory_flags", [])
    if route["block"] != "routing":
        return [("non-routing mandatory_flags", listed)] if listed else []
    cells = _routing_rows()[route["row"]]
    steps = _labelled_steps(cells[3])
    cell = {}
    if cells[4] != "-":
        for item in cells[4].split(";"):
            cell[item.partition(":")[0].strip()] = item.strip()
    used = {
        label
        for label, step in steps.items()
        if set(_TOKEN_RE.findall(step)) & set(entry["targets"])
    }
    expected = [item for label, item in cell.items() if label in used]
    problems = [] if listed == expected else [("mandatory_flags", listed, expected)]
    for item in expected:
        label, _, flags = item.partition(":")
        command = _TOKEN_RE.findall(steps[label])[0]
        source = _primitive(command).read_text("utf-8")
        for mode in re.findall(r"--[a-z][a-z0-9-]*(?:\s+(?!--)[^\s`]+)?", flags):
            if not _mode_declared(mode, source):
                problems.append(("undeclared", command, mode))
    return problems


@pytest.mark.parametrize("case", _CASES, ids=[case["id"] for case in _CASES])
def test_case_mandatory_flags_match_the_guide_row(case):
    for entry, route in _entries(case):
        assert not _mandatory_problems(entry, route), (case["id"], entry["request"])


def test_mandatory_flag_check_rejects_omitted_or_altered_entries():
    s19 = next(case for case in _CASES if case["id"] == "S19")
    route = s19["guide_route"]
    assert s19["mandatory_flags"] == [
        "3: `--mode critique --focus requirements`",
        "5: `--mode critique --focus architecture,testing`",
    ]
    assert not _mandatory_problems(s19, route)
    assert _mandatory_problems({**s19, "mandatory_flags": []}, route)
    altered = ["3: `--mode discussion --focus requirements`", s19["mandatory_flags"][1]]
    assert _mandatory_problems({**s19, "mandatory_flags": altered}, route)


@pytest.mark.parametrize("case", _CASES, ids=[case["id"] for case in _CASES])
def test_case_activation_matches_command_source(case):
    """T41-T43: self-contained commands have no activation; others name a real skill."""
    for command, expected in case["activation"].items():
        path = _primitive(command)
        assert path is not None and path.parent == _COMMANDS, (case["id"], command)
        sections = _ACTIVATION_RE.findall(path.read_text(encoding="utf-8"))
        if expected == "self-contained":
            assert not sections, (case["id"], command)
            continue
        assert len(sections) == 1, (case["id"], command)
        refs = re.findall(r"^> Skill (\S+)$", sections[0], re.M)
        assert refs == [expected], (case["id"], command, refs)
        skill = _primitive(expected)
        assert skill is not None, (case["id"], expected)


def test_tdd_activation_uses_the_tdd_skill_not_a_guessed_protocol():
    """T43: the differently headed directive resolves to skills/tdd, not sc-tdd-protocol."""
    source = (_COMMANDS / "tdd.md").read_text(encoding="utf-8")
    assert "## Activation" not in source
    assert re.findall(r"^> Skill (\S+)$", source, re.M) == ["tdd"]
    assert (_SKILLS / "tdd/SKILL.md").is_file()
    assert not (_SKILLS / "sc-tdd-protocol").exists()


@pytest.mark.parametrize("case", _CASES, ids=[case["id"] for case in _CASES])
def test_variants_name_real_primitives_and_wrong_cache_rows(case):
    """Spec 8.2: unavailable plugin capability and a seeded wrong cache row."""
    unavailable = case["variants"]["unavailable_plugin"]
    assert unavailable["environment"] == "plugin-only"
    missing = unavailable["missing"]
    assert _primitive(missing) is not None, (case["id"], missing)
    skills = {s.replace(":", "-") for s in case["activation"].values()}
    assert missing in set(case["targets"]) | skills | set(case["activation"]), case[
        "id"
    ]
    assert f"not installed: {missing}" in unavailable["expected"], case["id"]
    wrong = case["variants"]["seeded_wrong_cache"]
    assert wrong["environment"] == "checkout-seeded-wrong-cache"
    row = wrong["cache_row"]
    assert row["key"] in CLASSIFICATION_KEYS, (case["id"], row["key"])
    candidate = row["candidate"].removeprefix("/")
    assert _primitive(candidate) is not None, (case["id"], candidate)
    assert candidate not in case["targets"], case["id"]
    assert row["candidate"] in row["envelope"], case["id"]
    if case["guide_route"]["block"] == "routing":
        # A matched routing row skips the cache entirely.
        assert "cache not consulted" in wrong["expected"], case["id"]
    else:
        assert _unmatched_cache_expectation_ok(
            wrong["expected"], row["key"], case["targets"][0]
        ), case["id"]
    assert f"cached {row['candidate']} never emitted" in wrong["expected"]


def _unmatched_cache_expectation_ok(expected: str, key: str, target: str) -> bool:
    """Unmatched requests reach the cache only if the classifier returns the seeded
    key, so the expectation must cover both the hit and the no_key/miss outcome."""
    required = (
        f"if dispatch hits {key}",
        "rejected",
        "on a miss",
        "no_key",
        f"selects /{target}",
        "no hit telemetry",
    )
    return (
        all(phrase in expected for phrase in required)
        and "cache not consulted" not in expected
    )


def test_unmatched_cache_expectation_rejects_unconditional_wording():
    old = (
        "no routing row matched; cache hint consulted; cached /sc:pm rejected by "
        "current verification and request binding; live discovery selects /sc:git "
        "from Other commands; no hit telemetry; cached /sc:pm never emitted"
    )
    assert not _unmatched_cache_expectation_ok(old, "parallel-agent-fanout", "sc:git")


def test_conditional_step_guard_rejects_incidental_only():
    assert _conditional_step("7b. only for explicit composer selection: `/roadmap x`")
    assert _conditional_step('1. `/sc:brainstorm "<idea>"` (only if vague)')
    assert not _conditional_step("7b. `/roadmap x`, then read only the outputs")
    assert not _conditional_step("3. run `/roadmap x` always; only one pass")


def test_cache_expectation_follows_the_guide_block():
    """Matched rows claim a bypass; Other-commands (no_match) cases never do."""
    for case in _CASES:
        expected = case["variants"]["seeded_wrong_cache"]["expected"]
        matched = case["guide_route"]["block"] == "routing"
        assert ("cache not consulted" in expected) == matched, case["id"]
        for repeat in case["repeats"]:
            route = repeat.get("guide_route", case["guide_route"])
            if route["block"] == case["guide_route"]["block"]:
                continue
            # A repeat on the other block cannot inherit the case's cache outcome.
            cached = repeat["cache_expected"]
            routed = route["block"] == "routing"
            assert ("cache not consulted" in cached) == routed, case["id"]


def test_matched_routes_bypass_cache_so_seeded_rows_cannot_win():
    skill = _SKILL.read_text(encoding="utf-8")
    step0 = _section(skill, "## Step 0", "## Hot-Path Cache Lookup")
    assert "Skip the Hot-Path Cache Lookup and the Cold-Path Write-Back" in step0
    assert "Use it only when no routing row matches (`no_match`)" in step0
    assert "continue with the Hot-Path Cache Lookup" in step0


def test_unmatched_cache_hints_are_consulted_then_rejected():
    hot = _section(
        _SKILL.read_text(encoding="utf-8"), "## Hot-Path Cache Lookup", "## Phase 0"
    )
    assert "a hit is only a hint" in hot
    assert "reject it and use live Phase 0-2 discovery" in hot
    assert "Do not log a hit for a rejected hint" in hot


def test_example_only_flags_are_not_declared_or_routed():
    """T44: build --validate and cleanup --preview are examples; design has no --output."""
    for name, flag in (("build", "--validate"), ("cleanup", "--preview")):
        source = (_COMMANDS / f"{name}.md").read_text(encoding="utf-8")
        usage = _section(source, "## Usage", "\n## ")
        examples = _section(source, "## Examples", "\n## ")
        assert flag not in usage and flag in examples, name
    assert "--output" not in (_COMMANDS / "design.md").read_text(encoding="utf-8")
    for route, flag in (
        ({"block": "other", "command": "sc:build"}, "--validate"),
        ({"block": "routing", "row": "cleanup"}, "--preview"),
        ({"block": "routing", "row": "focused-design"}, "--output"),
    ):
        assert flag not in _FLAG_RE.findall(_route(route)[1]), (route, flag)
    assert "/sc:tasklist --source" not in _GUIDE.read_text(encoding="utf-8")


def test_retired_identities_have_no_shipped_command():
    """T46: the four retired identities ship no command file and are never routed."""
    data = _data()
    retired = {
        c["name"] for c in data["commands"] if c["history"].startswith("Retired")
    }
    assert retired == _RETIRED
    for name in retired:
        assert not (_COMMANDS / f"{name}.md").exists(), name
        assert not (_REPO / "plugins/superclaude/commands" / f"{name}.md").exists()
    tokens = set(_TOKEN_RE.findall(_GUIDE.read_text(encoding="utf-8")))
    assert not {f"sc:{name}" for name in retired} & tokens


def test_command_dispositions_trace_appendix_c_and_inventory():
    """T75: fixture, Appendix C, inventory and live commands agree on 47 (43 + 4)."""
    spec = _spec_path()
    appendix = _section(
        spec.read_text(encoding="utf-8"),
        "## Appendix C",
        "## Appendix D",
    )
    rows = []
    for line in appendix.splitlines():
        cells = _cells(line)
        if len(cells) == 6 and line.startswith("| ") and cells[0] != "Command":
            report = re.search(r"\(([^)]*)\)", cells[5]).group(1)
            rows.append(
                {
                    "name": cells[0],
                    "history": cells[1],
                    "disposition": cells[2],
                    "requirements_tests": cells[4],
                    "report": "analyses/" + report.rsplit("/", 1)[1],
                }
            )
    commands = _data()["commands"]
    assert commands == rows
    inventory = json.loads((spec.parent / "inventory.json").read_text("utf-8"))
    names = {c["name"] for c in commands}
    assert names == set(inventory["commands"])
    assert set(inventory["retired_commands"]) == _RETIRED
    active = {c["name"] for c in commands if c["history"].startswith("Active")}
    assert (len(active), len(names - active)) == (43, 4)
    shipped = {p.stem for p in _COMMANDS.glob("*.md") if p.name != "README.md"}
    assert shipped - _POST_REFRESH_ADDITIONS == active
    for command in commands:
        if command["name"] in _RETIRED:
            assert "R" in command["history"].split("; ", 1)[1].split("+")
            assert "NO CHANGE retirement" in command["disposition"]
    formatting_only = sorted(c["name"] for c in commands if c["history"] == "Active; F")
    assert formatting_only == [
        "agent",
        "analyze",
        "build",
        "design",
        "document",
        "git",
        "index-repo",
        "load",
        "save",
        "test",
    ]


def test_analyst_reports_and_disposition_appendix_are_retained():
    """T76: every command keeps its analyst report and Appendix D stays present."""
    spec = _spec_path()
    for command in _data()["commands"]:
        report = spec.parent / command["report"]
        text = report.read_text(encoding="utf-8")
        for heading in ("## Findings", "## Gaps", "## Key Takeaways"):
            assert heading in text, (command["name"], heading)
    body = spec.read_text(encoding="utf-8")
    dispositions = _section(body, "## Appendix D", "## Appendix E")
    headings = (
        "### Accepted consolidated groups",
        "### Rejected or refined proposals",
        "### Deferred source-contract and operational findings",
    )
    for heading, following in zip(headings, (*headings[1:], None)):
        assert heading in dispositions
        part = dispositions.split(heading, 1)[1]
        if following:
            part = part.split(following, 1)[0]
        rows = [ln for ln in part.splitlines() if ln.startswith("|")][2:]
        # Each disposition class keeps concrete recorded entries, not just a heading.
        assert rows and all(len(_cells(r)) >= 3 and _cells(r)[1] for r in rows), heading
