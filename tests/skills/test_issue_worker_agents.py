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


# Live acceptance of #365: Claude Code's Write tool refuses any subagent write
# of a `.md` file whose name starts with REPORT, SUMMARY, FINDINGS or ANALYSIS
# ("Subagents should return findings as text, not write report files."), so
# issue-worker-t2's Write of `.dev/issues/365/summary.md` was refused. The
# claim summary is therefore `issue-summary.md`. The worker files are tool
# inputs, so each agent file states that early and in its Rules section, and
# SKILL.md's spawn rule tells the orchestrator to restate it in every spawn
# prompt.
SKILL = ROOT / "src/superclaude/skills/sc-issue-protocol/SKILL.md"
_TOOL_INPUT_HEADING = "## Your files are tool inputs, not reports"
_TOOL_INPUT_PARAGRAPH = (
    "The files you write under `.dev/issues/` (`scout.md`, `accuracy-check.md`, "
    "`issue-summary.md`, the reports under `analysis/` such as "
    "`analysis/analyze-<scope>.md`, `flags.md`, `flags-t1.md`, `issue-body.md`, "
    "`draft-notes.md`) are input files for the orchestrator's next tool calls "
    "(`gh --body-file` posts and `/sc:recommend`), not report files. Claude Code "
    "refuses a subagent's Write of any `.md` file whose name starts with REPORT, "
    "SUMMARY, FINDINGS or ANALYSIS (in any letter case), which is why none of "
    "these names starts with those words. Writing every file your job names with "
    "the Write tool is mandatory; returning its content as text instead is a "
    "failure (`E-WORKER-NO-OUTPUT`)."
)
_TOOL_INPUT_RULES_BULLET = (
    "- **Write your files.** Every file your job names is a tool input, not a "
    'report (see "Your files are tool inputs, not reports" above): write it with '
    "the Write tool and never return its content as text."
)
_SPAWN_PROMPT_LINE = (
    "Every spawn prompt names each exact path the job must write under "
    "`.dev/issues/` and states that these are input files for the orchestrator's "
    "next tool calls, not report files: the worker writes them with the Write "
    "tool, and returning their content as text counts as no output "
    "(`E-WORKER-NO-OUTPUT`)."
)
_WORKER_FILES = (
    "scout.md",
    "accuracy-check.md",
    "issue-summary.md",
    "analysis/analyze-<scope>.md",
    "flags.md",
    "flags-t1.md",
    "issue-body.md",
    "draft-notes.md",
)


def section_lines(lines: list[str], heading: str) -> list[str]:
    """Return the lines after ``heading`` up to the next ``## `` heading."""
    if heading not in lines:
        return []
    rest = lines[lines.index(heading) + 1 :]
    end = next((i for i, line in enumerate(rest) if line.startswith("## ")), len(rest))
    return rest[:end]


def tool_input_rule_problems(text: str) -> list[str]:
    """Return what is missing from an agent file's tool-input rule."""
    lines = text.splitlines()
    if _TOOL_INPUT_HEADING not in lines:
        return ["tool-input heading missing"]
    problems = []
    heading = lines.index(_TOOL_INPUT_HEADING)
    jobs = "## Jobs for this tier"
    if jobs not in lines or heading > lines.index(jobs):
        problems.append("tool-input heading is not before the jobs section")
    if lines.count(_TOOL_INPUT_PARAGRAPH) != 1:
        problems.append("tool-input paragraph does not appear exactly once")
    if lines[heading + 1 : heading + 3] != ["", _TOOL_INPUT_PARAGRAPH]:
        problems.append("tool-input paragraph is not directly under its heading")
    section = "\n".join(section_lines(lines, _TOOL_INPUT_HEADING))
    problems.extend(
        f"worker file {name} not named" for name in _WORKER_FILES if name not in section
    )
    if section_lines(lines, "## Rules").count(_TOOL_INPUT_RULES_BULLET) != 1:
        problems.append("Rules bullet does not appear exactly once in ## Rules")
    return problems


def spawn_rule_lines(text: str) -> list[str]:
    return section_lines(text.splitlines(), "## Workers and the spawn rule")


@pytest.mark.parametrize("name", sorted(WORKERS))
def test_worker_states_its_files_are_tool_inputs(name):
    text = (AGENTS / f"{name}.md").read_text(encoding="utf-8")
    assert tool_input_rule_problems(text) == []


@pytest.mark.parametrize("name", sorted(WORKERS))
def test_tool_input_check_fails_on_pre_fix_text(name, tmp_path):
    """Negative case: a temporary copy without the section and bullet fails."""
    text = (AGENTS / f"{name}.md").read_text(encoding="utf-8")
    block = f"{_TOOL_INPUT_HEADING}\n\n{_TOOL_INPUT_PARAGRAPH}\n\n"
    assert text.count(block) == 1
    assert text.count(_TOOL_INPUT_RULES_BULLET + "\n") == 1
    old = tmp_path / f"{name}.md"
    old.write_text(
        text.replace(block, "").replace(_TOOL_INPUT_RULES_BULLET + "\n", ""),
        encoding="utf-8",
    )
    assert tool_input_rule_problems(old.read_text(encoding="utf-8")) != []


def test_spawn_rule_restates_tool_inputs():
    lines = spawn_rule_lines(SKILL.read_text(encoding="utf-8"))
    assert lines.count(_SPAWN_PROMPT_LINE) == 1


def test_spawn_rule_check_fails_without_the_line(tmp_path):
    """Negative case: a temporary SKILL.md copy without the line fails."""
    text = SKILL.read_text(encoding="utf-8")
    assert text.count(_SPAWN_PROMPT_LINE + "\n\n") == 1
    old = tmp_path / "SKILL.md"
    old.write_text(text.replace(_SPAWN_PROMPT_LINE + "\n\n", ""), encoding="utf-8")
    assert _SPAWN_PROMPT_LINE not in spawn_rule_lines(old.read_text(encoding="utf-8"))


# The harness rule behind the rename: Claude Code's Write tool refuses a
# subagent write whose file basename matches this pattern (error "Subagents
# should return findings as text, not write report files."). A probe subagent
# on 2026-11-04 confirmed it: summary.md, findings.md and report.md were
# refused; the "allowed" names below were written. Every file name a worker is
# told to write must avoid it.
_HARNESS_REPORT_NAME = re.compile(
    r"^(REPORT|SUMMARY|FINDINGS|ANALYSIS).*\.md$", re.IGNORECASE
)
SKILL_DIR = SKILL.parent
COMMAND = ROOT / "src/superclaude/commands/issue.md"
_ANALYSIS_NAME = "analysis/analyze-<scope>.md"
_OLD_SUMMARY_REFS = (
    "<D>/summary.md",
    ".dev/issues/<N>/summary.md",
    "templates/summary.md",
    "`summary.md`",
)
# Pre-fix texts (fix 2), kept only for the negative test below.
_OLD_TOOL_INPUT_PARAGRAPH = (
    "The files you write under `.dev/issues/` (`scout.md`, `accuracy-check.md`, "
    "`summary.md`, the reports under `analysis/`, `flags.md`, `flags-t1.md`, "
    "`issue-body.md`, `draft-notes.md`) are input files for the orchestrator's "
    "next tool calls (`gh --body-file` posts and `/sc:recommend`), not report "
    "files, so a general instruction against writing report or summary `.md` "
    "files does not apply to them. Writing every file your job names with the "
    "Write tool is mandatory; returning its content as text instead is a failure "
    "(`E-WORKER-NO-OUTPUT`)."
)
_OLD_WAVE_4_LINE = (
    "5. **Wave 4, accuracy check and summary.** Spawn `issue-worker-t2`, or "
    "`issue-worker-t1` when `scout.md` says `complex`; it writes "
    "`<D>/accuracy-check.md`, `<D>/summary.md` (effort in hours) and, when out "
    "of date, `<D>/analysis/`."
)


def written_md_names(text: str) -> set[str]:
    """Return the basename of every ``.md`` token inside a backtick code span.

    A token is a whitespace-separated word of a span that ends in ``.md``. A
    leading ``@`` is stripped and the basename is the text after the last
    ``/``. Placeholder brackets are kept: ``<REPORT.md`` in ``refs/chains.md``
    names a file ``/sc:troubleshoot`` prints, not one a worker writes.
    """
    names = set()
    for span in _CODE_SPAN.findall(text):
        for token in span.split():
            if token.endswith(".md"):
                names.add(token.removeprefix("@").rsplit("/", 1)[-1])
    return names


def blocked_names(text: str) -> list[str]:
    """Return the collected file names the harness rule would refuse."""
    return sorted(n for n in written_md_names(text) if _HARNESS_REPORT_NAME.match(n))


def old_summary_refs(text: str) -> list[str]:
    """Return every pre-rename summary reference present in ``text``."""
    return [ref for ref in _OLD_SUMMARY_REFS if ref in text]


def worker_instruction_texts() -> dict[str, str]:
    """Every text that tells a worker which files to write, by label.

    The three agent files, SKILL.md, every ref of the skill, and the rows of
    the command's Outputs table.
    """
    texts = {
        f"{name}.md": (AGENTS / f"{name}.md").read_text(encoding="utf-8")
        for name in sorted(WORKERS)
    }
    texts["SKILL.md"] = SKILL.read_text(encoding="utf-8")
    for ref in sorted((SKILL_DIR / "refs").glob("*.md")):
        texts[f"refs/{ref.name}"] = ref.read_text(encoding="utf-8")
    outputs = section_lines(
        COMMAND.read_text(encoding="utf-8").splitlines(), "## Outputs"
    )
    texts["issue.md Outputs"] = "\n".join(
        line for line in outputs if line.startswith("|")
    )
    return texts


@pytest.mark.parametrize(
    ("name", "refused"),
    [
        ("summary.md", True),
        ("findings.md", True),
        ("report.md", True),
        ("SUMMARY.md", True),
        ("Analysis-notes.md", True),
        ("scout.md", False),
        ("accuracy-check.md", False),
        ("flags.md", False),
        ("flags-t1.md", False),
        ("issue-body.md", False),
        ("draft-notes.md", False),
        ("issue-summary.md", False),
        ("cheatsheet.md", False),
        ("analyze-report.md", False),
        ("notes.md", False),
        ("analyze-<scope>.md", False),
        ("<REPORT.md", False),
    ],
)
def test_harness_regex_matches_probe(name, refused):
    assert bool(_HARNESS_REPORT_NAME.match(name)) is refused


@pytest.mark.parametrize(
    ("text", "names"),
    [
        ("`analysis/analyze-report.md`", {"analyze-report.md"}),
        ("`analysis/notes.md`", {"notes.md"}),
        ("`@.dev/issues/<N>/issue-summary.md`", {"issue-summary.md"}),
        ("`-F body=@<D>/claim-comment.md`", {"claim-comment.md"}),
        ("`/sc:implement <REPORT.md path printed by step 1>`", {"<REPORT.md"}),
        ("summary.md outside a code span", set()),
    ],
)
def test_written_md_names_takes_basenames(text, names):
    assert written_md_names(text) == names


def test_worker_written_names_avoid_harness_block():
    texts = worker_instruction_texts()
    refused = {label: blocked_names(text) for label, text in texts.items()}
    assert {label: names for label, names in refused.items() if names} == {}
    collected = set().union(*(written_md_names(text) for text in texts.values()))
    assert {
        "scout.md",
        "accuracy-check.md",
        "issue-summary.md",
        "analyze-<scope>.md",
        "issue-body.md",
        "draft-notes.md",
    } <= collected
    assert written_md_names(texts["issue.md Outputs"]), "Outputs table not scanned"
    for label in (
        "SKILL.md",
        "refs/claim.md",
        "issue-worker-t1.md",
        "issue-worker-t2.md",
    ):
        assert _ANALYSIS_NAME in texts[label], label


def test_old_summary_path_is_gone():
    texts = worker_instruction_texts()
    texts["issue.md"] = COMMAND.read_text(encoding="utf-8")
    for template in sorted((SKILL_DIR / "templates").glob("*.md")):
        texts[f"templates/{template.name}"] = template.read_text(encoding="utf-8")
    found = {label: old_summary_refs(text) for label, text in texts.items()}
    assert {label: refs for label, refs in found.items() if refs} == {}
    assert (SKILL_DIR / "templates/issue-summary.md").is_file()
    assert not (SKILL_DIR / "templates/summary.md").exists()


def test_checks_flag_pre_fix_text(tmp_path):
    """Negative case: the pre-fix paragraph and Wave 4 line fail both checks."""
    old = tmp_path / "pre-fix.md"
    old.write_text(
        f"{_OLD_TOOL_INPUT_PARAGRAPH}\n\n{_OLD_WAVE_4_LINE}\n", encoding="utf-8"
    )
    text = old.read_text(encoding="utf-8")
    assert blocked_names(text) == ["summary.md"]
    assert old_summary_refs(text) == ["<D>/summary.md", "`summary.md`"]
