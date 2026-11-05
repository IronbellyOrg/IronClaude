"""Static tests for the three tier-pinned /sc:issue worker agents.

Enforcement type: STATIC (agent file text). Design section 6 (pinning),
section 13 (repository and GitHub call rules), default D27 (no Edit tool) and
coordinator constraint C1 (no read-only permission mode: the workers must be
able to write their files under .dev/issues/).

``gh_lines_missing_repo`` is the one fork-safety scan for /sc:issue; the skill
package test (test_issue_protocol.py) imports it.
"""

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
AGENTS = ROOT / "src/superclaude/agents"
MODELS = ROOT / "src/superclaude/skills/ccsession-tag/ccsession-models.json"
WORKERS = {
    "issue-worker-t3": ("claude-gw-tier3", "tier3"),
    "issue-worker-t2": ("claude-gw-tier2", "tier2"),
    "issue-worker-t1": ("claude-gw-tier1a", "tier1a"),
}

_GH_WRITE_FAMILY = re.compile(r"\bgh\s+(issue|pr|label)\b")
_CODE_SPAN = re.compile(r"`([^`\n]+)`")


def gh_lines_missing_repo(text: str) -> list[str]:
    """Return every gh issue/pr/label mention that does not carry ``--repo``.

    A mention is a backtick code span whose text contains ``gh issue``,
    ``gh pr`` or ``gh label``, or, outside code spans, a line of text (fenced
    code included) that contains one. Prohibitions count too: a "never run"
    line is written with ``--repo <R>`` like any other.
    """
    missing = []
    for line in text.splitlines():
        spans = _CODE_SPAN.findall(line)
        for span in spans:
            if _GH_WRITE_FAMILY.search(span) and "--repo" not in span:
                missing.append(span)
        rest = _CODE_SPAN.sub("", line)
        if _GH_WRITE_FAMILY.search(rest) and "--repo" not in rest:
            missing.append(line.strip())
    return missing


def split_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), path
    head, body = text[4:].split("\n---\n", 1)
    fields = {}
    for line in head.splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields, body


@pytest.mark.parametrize("name", sorted(WORKERS))
def test_worker_file_exists_with_pinned_picker_id(name):
    fields, _ = split_frontmatter(AGENTS / f"{name}.md")
    assert fields["name"] == name
    assert fields["model"] == WORKERS[name][0]
    assert "[1m]" not in fields["model"]
    assert fields["description"]


@pytest.mark.parametrize("name", sorted(WORKERS))
def test_picker_tier_exists_in_ccsession_models(name):
    tiers = json.loads(MODELS.read_text(encoding="utf-8"))["tiers"]
    assert WORKERS[name][1] in tiers


@pytest.mark.parametrize("name", sorted(WORKERS))
def test_tools_exclude_edit(name):
    fields, _ = split_frontmatter(AGENTS / f"{name}.md")
    tools = [t.strip() for t in fields["tools"].split(",")]
    assert tools == ["Read", "Grep", "Glob", "Write", "Bash"]
    assert "Edit" not in tools


@pytest.mark.parametrize("name", sorted(WORKERS))
def test_no_permission_mode(name):
    """Coordinator constraint C1: a read-only mode would block every write."""
    fields, _ = split_frontmatter(AGENTS / f"{name}.md")
    assert "permissionMode" not in fields
    assert "permissionMode" not in (AGENTS / f"{name}.md").read_text(encoding="utf-8")


@pytest.mark.parametrize("name", sorted(WORKERS))
def test_body_states_github_git_and_write_rules(name):
    _, body = split_frontmatter(AGENTS / f"{name}.md")
    assert "Read-only GitHub access" in body
    assert "read-only `gh` calls only" in body
    assert "never write to GitHub or ClickUp" in body
    assert "Your only git write is `git fetch origin`" in body
    assert "never add, fetch from or push to any other remote" in body
    assert "write files only inside" in body and "under `.dev/issues/`" in body
    assert "never edit source code" in body
    assert "~/.claude/skills/sc-issue-protocol/templates/" in body
    assert "~/.claude/commands/sc/analyze.md" in body
    assert "Return only the path" in body


@pytest.mark.parametrize("name", sorted(WORKERS))
def test_every_gh_issue_pr_label_mention_carries_repo(name):
    text = (AGENTS / f"{name}.md").read_text(encoding="utf-8")
    assert _GH_WRITE_FAMILY.search(text), "the body names its gh reads"
    assert gh_lines_missing_repo(text) == []


@pytest.mark.parametrize("name", sorted(WORKERS))
def test_no_source_tree_path_or_brace_placeholder(name):
    text = (AGENTS / f"{name}.md").read_text(encoding="utf-8")
    assert "src/superclaude/" not in text
    assert "{owner}/{repo}" not in text


_INSTALLED_SKILLS = "~/.claude/skills/"
_PROJECT_SKILLS = re.compile(r"(?<!~/)\.claude/skills/")
# Line 11 of each worker says which skill spawns it (provenance, not a read
# instruction), so it is exempt from the dual-surface check.
_PROVENANCE_PREFIX = "Spawned only by the `sc:issue-protocol` skill"
_OLD_RUBRIC = "the rubric in `~/.claude/skills/sc-issue-protocol/refs/claim.md`,"
_NEW_RUBRIC = (
    "the rubric in `~/.claude/skills/sc-issue-protocol/refs/claim.md` "
    "(the in-checkout copy is the project "
    "`.claude/skills/sc-issue-protocol/refs/claim.md`; read the installed copy first),"
)


def skills_lookups_missing_project_copy(text: str) -> list[str]:
    """Return every line naming ``~/.claude/skills/`` without the project copy.

    Project CLAUDE.md dual-surface rule: a lookup of another installed skill
    file also names the project ``.claude/skills/`` copy, on the same line.
    The provenance line (who spawns the worker) is exempt.
    """
    return [
        line.strip()
        for line in text.splitlines()
        if _INSTALLED_SKILLS in line
        and not line.startswith(_PROVENANCE_PREFIX)
        and not _PROJECT_SKILLS.search(line)
    ]


@pytest.mark.parametrize("name", sorted(WORKERS))
def test_every_skills_lookup_names_both_copies(name):
    """Verification finding B1: the effort-rubric lookup named only ~/.claude/."""
    text = (AGENTS / f"{name}.md").read_text(encoding="utf-8")
    assert _INSTALLED_SKILLS in text
    assert skills_lookups_missing_project_copy(text) == []


@pytest.mark.parametrize("name", ["issue-worker-t1", "issue-worker-t2"])
def test_skills_lookup_check_fails_on_old_rubric_line(name, tmp_path):
    """Negative case: a temporary copy restored to the pre-fix line 17 text fails."""
    text = (AGENTS / f"{name}.md").read_text(encoding="utf-8")
    assert text.count(_NEW_RUBRIC) == 1
    old = tmp_path / f"{name}.md"
    old.write_text(text.replace(_NEW_RUBRIC, _OLD_RUBRIC), encoding="utf-8")
    missing = skills_lookups_missing_project_copy(old.read_text(encoding="utf-8"))
    assert len(missing) == 1
    assert missing[0].startswith("1. **Accuracy check and summary")
    assert _OLD_RUBRIC in missing[0]


@pytest.mark.parametrize(
    ("text", "missing"),
    [
        ("Read `~/.claude/skills/x/refs/a.md`.", ["Read `~/.claude/skills/x/refs/a.md`."]),
        ("Read `~/.claude/skills/x/a.md` (project `.claude/skills/x/a.md`).", []),
        ("Spawned only by the `sc:issue-protocol` skill (`~/.claude/skills/s/SKILL.md`).", []),
        ("Run `~/.claude/commands/sc/analyze.md`.", []),
    ],
)
def test_skills_lookup_helper(text, missing):
    assert skills_lookups_missing_project_copy(text) == missing


@pytest.mark.parametrize(
    ("text", "missing"),
    [
        ("Run `gh issue view 3 --repo <R> --json body`.", []),
        ("Run `gh issue view 3 --json body`.", ["gh issue view 3 --json body"]),
        ("never gh label create x", ["never gh label create x"]),
        ("```\ngh pr list --state merged\n```", ["gh pr list --state merged"]),
        ("`gh api user -q .login`", []),
    ],
)
def test_scan_helper_flags_mentions_without_repo(text, missing):
    assert gh_lines_missing_repo(text) == missing
