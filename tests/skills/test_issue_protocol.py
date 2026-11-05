"""Static tests for the sc-issue-protocol skill package (design section 16).

Enforcement type: STATIC (skill package text). Pins the SKILL.md frontmatter
and size, the two-way inventory of refs/templates/scripts, the spawn rule,
the posted-template markers, the issue-template headings, the next-step chain
flags and the fork-safety rule of design section 13.

Flag check source: every ``/sc:*`` flag in ``refs/chains.md`` is checked only
against the source command file ``src/superclaude/commands/<name>.md`` (and
``/task`` against ``src/superclaude/skills/task/SKILL.md``), the same source
``_command_text`` in tests/core/test_how_we_work_routing_table.py reads. This
deliberately narrows design section 16's "installed-or-source" wording so the
test never depends on the machine's ``~/.claude`` install.

The fork-safety scan is the one shared helper ``gh_lines_missing_repo`` from
test_issue_worker_agents.py.
"""

import re
from pathlib import Path

import pytest

from tests.skills.test_issue_worker_agents import gh_lines_missing_repo

ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT / "src/superclaude/skills/sc-issue-protocol"
SKILL = SKILL_DIR / "SKILL.md"
REFS = SKILL_DIR / "refs"
TEMPLATES = SKILL_DIR / "templates"
COMMANDS = ROOT / "src/superclaude/commands"
TASK_SKILL = ROOT / "src/superclaude/skills/task/SKILL.md"
AGENTS = [ROOT / f"src/superclaude/agents/issue-worker-t{n}.md" for n in (3, 2, 1)]

SPAWN_RULE = "never pass the `model` parameter"
ALLOWED_TOOLS = "Read, Glob, Grep, Write, Edit, Bash, Task, Skill, AskUserQuestion"

BUG_SIMPLE = [
    "Bug Summary",
    "Environment (OS, version)",
    "Current Behavior",
    "Expected Behavior",
    "Steps to Reproduce",
    "Impact Assessment (Severity, Blast Radius)",
    "Error Messages",
    "Codebase Context (from `/sc:analyze`)",
    "Related Issues",
    "Testing Notes",
]
BUG_COMPLEX = BUG_SIMPLE + [
    "Frequency",
    "User Impact",
    "Business Impact",
    "Cascading Effects",
    "Logs and Stack Trace",
    "Attempted Solutions",
    "Proposed Solution",
    "For Development Team (Root Cause Analysis, Fix Approach, Verification Plan)",
]
FEATURE_SIMPLE = [
    "Feature Summary",
    "Problem Statement",
    "User Story",
    "Proposed Solution",
    "Acceptance Criteria",
    "Out of Scope",
    "Components Affected (from `/sc:analyze`)",
    "Related Issues/PRs",
]
FEATURE_COMPLEX = FEATURE_SIMPLE + [
    "Success Metrics",
    "Architecture Impact",
    "Dependencies",
    "Testing Strategy",
    "Documentation Needs",
    "Alternatives Considered",
    "Impact Analysis (Blast Radius, Integration Impact)",
    "Risks & Mitigation",
    "Effort Estimate (hours) and Complexity",
]
ISSUE_TEMPLATES = {
    "issue-bug-simple": BUG_SIMPLE,
    "issue-bug-complex": BUG_COMPLEX,
    "issue-feature-simple": FEATURE_SIMPLE,
    "issue-feature-complex": FEATURE_COMPLEX,
}
POSTED_MARKERS = {
    "accuracy-check-comment": "<!-- sc:issue:accuracy-check -->",
    "claim-comment": "<!-- sc:issue:claim -->",
    "create-review-comment": "<!-- sc:issue:create-review -->",
    **{stem: f"<!-- sc:issue:create template={stem} -->" for stem in ISSUE_TEMPLATES},
}

_SKILL_PATH = re.compile(r"(?:refs|templates|scripts)/[A-Za-z0-9_.-]+\.(?:md|py)")
_COMMAND_SPAN = re.compile(r"`(/(?:sc:[a-z][a-z0-9-]*|task)\b[^`]*)`")
_FLAG = re.compile(r"--[a-z][a-z0-9-]*")


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def last_nonempty_line(text: str) -> str:
    return [line for line in text.splitlines() if line.strip()][-1].strip()


def headings(text: str) -> list[str]:
    return [line[3:].strip() for line in text.splitlines() if line.startswith("## ")]


def chain_rows(text: str) -> list[str]:
    """The data rows of the chain table (one row per type and complexity)."""
    return [
        line for line in text.splitlines() if re.match(r"^\| (Feature|Bug), ", line)
    ]


# --- SKILL.md frontmatter, size and inventory ------------------------------------


def test_skill_frontmatter_and_size():
    text = _text(SKILL)
    head = text.split("\n---\n", 1)[0]
    assert head.startswith("---\n")
    assert "\nname: sc:issue-protocol\n" in head + "\n"
    assert f"\nallowed-tools: {ALLOWED_TOOLS}" in head
    assert "\ndescription: " in head
    assert len(text.splitlines()) < 500


def test_every_named_path_exists_and_every_file_is_named():
    text = _text(SKILL)
    named = set(_SKILL_PATH.findall(text))
    on_disk = {
        str(p.relative_to(SKILL_DIR))
        for pattern in ("refs/*.md", "templates/*.md", "scripts/*.py")
        for p in SKILL_DIR.glob(pattern)
    }
    assert on_disk, "the skill package has files"
    assert sorted(n for n in named if not (SKILL_DIR / n).is_file()) == []
    assert sorted(on_disk - named) == []


@pytest.mark.parametrize(
    "path", [SKILL, *sorted(REFS.glob("*.md"))], ids=lambda p: p.name
)
def test_spawn_rule_text_present(path):
    assert SPAWN_RULE in _text(path)


ANALYZE_INSTALLED = "`~/.claude/commands/sc/analyze.md`"
ANALYZE_PROJECT = "(project `.claude/commands/sc/analyze.md` in a checkout)"


@pytest.mark.parametrize(
    "path", [SKILL, *sorted(REFS.glob("*.md"))], ids=lambda p: p.name
)
def test_analyze_lookup_names_both_copies(path):
    """CLAUDE.md dual-surface rule: a lookup of the installed analyze command
    also names the project copy that `make sync-dev` creates (PR #373 review)."""
    lines = [line for line in _text(path).splitlines() if ANALYZE_INSTALLED in line]
    assert [line for line in lines if ANALYZE_PROJECT not in line] == []


# --- create-mode slug (PR #373 review, augment comment 4472776355) ---------------

SLUG_PATTERN = "^[a-z0-9]+(-[a-z0-9]+)*$"


def reference_slug(description: str) -> str:
    """The slug rule of refs/create.md, written out so its examples can be run."""
    slug = re.sub(r"[^a-z0-9]+", "-", description.lower()).strip("-")
    slug = slug[:40].rstrip("-")
    return slug or "untitled"


def test_create_slug_rule_keeps_only_safe_characters():
    text = _text(REFS / "create.md")
    assert (
        "replace every run of characters other than `a-z` and `0-9` with one `-`"
        in text
    )
    assert "use `untitled` when nothing is left" in text
    assert f"`<slug>` matches `{SLUG_PATTERN}`" in text


@pytest.mark.parametrize(
    "description",
    [
        "Fix /../../etc/passwd handling",
        "../../.git/hooks",
        "a/b\\c d.e",
        "...",
        "",
        "Ünïcode only: ★★★",
        "x" * 60,
        "word " * 20,
    ],
)
def test_reference_slug_never_leaves_the_issues_directory(description):
    slug = reference_slug(description)
    assert re.fullmatch(SLUG_PATTERN, slug)
    assert len(slug) <= 40
    draft = Path(".dev/issues") / f"draft-20261104-000000-{slug}"
    assert draft.parent == Path(".dev/issues") and ".." not in draft.parts


def test_all_five_refs_exist():
    assert sorted(p.name for p in REFS.glob("*.md")) == [
        "chains.md",
        "claim.md",
        "create.md",
        "labels.md",
        "tiers.md",
    ]


# --- templates ------------------------------------------------------------------


@pytest.mark.parametrize(("stem", "marker"), sorted(POSTED_MARKERS.items()))
def test_posted_template_ends_with_marker(stem, marker):
    assert last_nonempty_line(_text(TEMPLATES / f"{stem}.md")) == marker


def test_marker_check_fails_when_marker_is_removed(tmp_path):
    copy = tmp_path / "claim-comment.md"
    lines = _text(TEMPLATES / "claim-comment.md").splitlines()
    copy.write_text(
        "\n".join(line for line in lines if "sc:issue:claim" not in line) + "\n"
    )
    assert last_nonempty_line(copy.read_text()) != POSTED_MARKERS["claim-comment"]


@pytest.mark.parametrize(("stem", "expected"), sorted(ISSUE_TEMPLATES.items()))
def test_issue_template_headings_in_order(stem, expected):
    assert headings(_text(TEMPLATES / f"{stem}.md")) == expected


@pytest.mark.parametrize("stem", sorted(ISSUE_TEMPLATES))
def test_issue_template_has_no_clickup_text(stem):
    assert "clickup" not in _text(TEMPLATES / f"{stem}.md").lower()


# --- next-step chains -------------------------------------------------------------


def _command_source(token: str) -> str:
    if token == "task":
        return _text(TASK_SKILL)
    return _text(COMMANDS / f"{token[3:]}.md")


def test_every_chain_flag_exists_in_its_command():
    spans = _COMMAND_SPAN.findall(_text(REFS / "chains.md"))
    assert spans, "chains.md names commands in code spans"
    missing = []
    for span in spans:
        flags = _FLAG.findall(span)
        if not flags:  # a bare command name, e.g. the `/sc:issue` mention
            continue
        token = span[1:].split()[0]
        source = _command_source(token)
        missing.extend(f"{token} {flag}" for flag in flags if flag not in source)
    assert missing == []


def test_brainstorm_steps_have_no_handoff_and_use_default_models():
    rows = chain_rows(_text(REFS / "chains.md"))
    assert len(rows) == 6
    steps = [
        s
        for row in rows
        for s in _COMMAND_SPAN.findall(row)
        if s.startswith("/sc:brainstorm")
    ]
    assert len(steps) == 3
    for step in steps:
        assert "--handoff tasklist" not in step and "--handoff design" not in step
        assert "--models" not in step
    text = _text(REFS / "chains.md")
    assert "--handoff tasklist" not in text and "--handoff design" not in text


# --- fork safety (design section 13, section 20 item 4) ---------------------------


_FORK_FILES = [SKILL, *sorted(REFS.glob("*.md")), *AGENTS]


@pytest.mark.parametrize("path", _FORK_FILES, ids=lambda p: p.name)
def test_every_gh_issue_pr_label_mention_carries_repo(path):
    assert gh_lines_missing_repo(_text(path)) == []


@pytest.mark.parametrize(
    "path",
    [
        *sorted(
            p
            for p in SKILL_DIR.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts
        ),
        *AGENTS,
    ],
    ids=lambda p: p.name,
)
def test_no_brace_placeholder(path):
    try:
        text = _text(path)
    except UnicodeDecodeError:
        pytest.skip("not UTF-8 text")
    assert "{owner}/{repo}" not in text


def test_fork_safety_scan_fails_on_a_ref_without_repo(tmp_path):
    ref = tmp_path / "claim.md"
    ref.write_text(
        _text(REFS / "claim.md") + "\nRun `gh issue view 302 --json state`.\n"
    )
    assert gh_lines_missing_repo(ref.read_text()) == ["gh issue view 302 --json state"]


# --- installed-path rule ------------------------------------------------------------


def test_no_source_tree_path_in_skill_files():
    hits = []
    for path in sorted(SKILL_DIR.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if "src/superclaude/" in text:
            hits.append(str(path.relative_to(ROOT)))
    assert hits == []
