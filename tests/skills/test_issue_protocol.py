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

import ast
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


# --- the Orca worktree step (design pipeline-flag, ST-5 and ST-6) ----------------


def _wave(text: str, number: int) -> str:
    """The text of `## Wave <number>` up to the next `## ` heading."""
    match = re.search(rf"^## Wave {number}\b.*?(?=^## |\Z)", text, re.M | re.S)
    assert match, f"refs/claim.md has no Wave {number}"
    return match.group(0)


def test_st5_orca_script_is_named_in_the_files_table_and_exists():
    rows = [ln for ln in _text(SKILL).splitlines() if ln.startswith("| `scripts/")]
    assert any(ln.startswith("| `scripts/orca_worktree.py` |") for ln in rows)
    assert (SKILL_DIR / "scripts/orca_worktree.py").is_file()
    assert len(list(REFS.glob("*.md"))) == 5


def test_st6_preflight_is_in_wave_0_and_worktree_is_wave_7_after_the_posts():
    claim = _text(REFS / "claim.md")
    wave0 = _wave(claim, 0)
    assert 'orca_worktree.py" preflight' in wave0
    assert "E-ORCA-REQUIRED" in wave0
    assert wave0.index("gh auth status") < wave0.index("preflight")
    assert wave0.index("preflight") < wave0.index("default branch")
    assert claim.index("## Wave 0") < claim.index("## Wave 1")
    assert claim.index("## Wave 6") < claim.index("## Wave 7")
    wave6, wave7 = _wave(claim, 6), _wave(claim, 7)
    assert "After both comments are posted, run Wave 7" in wave6
    assert (
        'orca_worktree.py" worktree --repo <R> --number <N> --base origin/<B>' in wave7
    )
    assert "--source <D>" in wave7
    assert "never a STOP" in wave7
    for code in (
        "W-ORCA-LIST-FAILED",
        "W-ORIGIN-BASE-MISSING",
        "W-ORIGIN-BASE-STALE",
        "W-WORKTREE-CREATE-FAILED",
        "W-WORKTREE-AMBIGUOUS",
        "W-WORKTREE-STALE",
        "W-WORKTREE-COPY-FAILED",
    ):
        assert code in wave7 and code in _text(SKILL)


LAUNCH_TEMPLATE = TEMPLATES / "launch-prompt.md"
_BLOCK_MARKER = re.compile(r"^<!-- block:([a-z]+) -->[ \t]*$", re.M)


def _launch_blocks() -> dict[str, str]:
    parts = _BLOCK_MARKER.split(_text(LAUNCH_TEMPLATE))
    return dict(zip(parts[1::2], parts[2::2]))


def test_st5_launch_prompt_template_is_in_the_files_table_and_exists():
    rows = [ln for ln in _text(SKILL).splitlines() if ln.startswith("| `templates/")]
    assert any(ln.startswith("| `templates/launch-prompt.md` |") for ln in rows)
    assert LAUNCH_TEMPLATE.is_file()
    assert len(list(REFS.glob("*.md"))) == 5


def test_st8_launch_prompt_has_exactly_the_four_blocks():
    assert list(_launch_blocks()) == ["common", "worktree", "full", "submit"]
    assert len(_BLOCK_MARKER.findall(_text(LAUNCH_TEMPLATE))) == 4


def test_st8_pr_tokens_live_only_in_the_submit_block_and_the_worktree_prohibition():
    blocks = _launch_blocks()
    holders = {
        token: {name for name, body in blocks.items() if token in body}
        for token in ("/sc:pr-submit", "git push", "git commit", "--monitor")
    }
    assert holders["--monitor"] == {"submit"}
    for token in ("/sc:pr-submit", "git push", "git commit"):
        assert holders[token] == {"worktree", "submit"}, token
    assert "/sc:pr-submit --monitor 3" in blocks["submit"]
    assert "conventional-commit" in blocks["submit"]
    assert "conventional-commit" not in "".join(
        body for name, body in blocks.items() if name != "submit"
    )
    prohibition = "Do not run `/sc:implement`, `/task`, `git commit`, `git push` or `/sc:pr-submit`."
    assert prohibition in blocks["worktree"]
    for name in ("common", "full"):
        assert not any(t in blocks[name] for t in holders), name


def test_st8_common_block_carries_the_required_statements():
    common = _launch_blocks()["common"]
    for text in (
        ".dev/issues/<N>/issue-summary.md",
        ".dev/issues/<N>/next-steps.md",
        "through the Skill tool in this session",
        "never run a step inside a subagent",
        "model tier",
        "Never merge anything",
    ):
        assert text in common, text


def test_st12_launch_prompt_gh_calls_name_the_fork():
    text = _text(LAUNCH_TEMPLATE)
    assert gh_lines_missing_repo(text) == []
    assert "gh pr list --repo <R> --head <branch> --state all" in text
    assert "IronbellyOrg" not in text  # the repository comes from origin, rendered


def test_st6_skill_steps_name_the_orca_check_and_the_worktree_step():
    skill = _text(SKILL)
    claim_mode = skill.split("## Claim mode", 1)[1].split("## Create mode", 1)[0]
    assert "E-ORCA-REQUIRED" in claim_mode and "preflight" in claim_mode
    assert claim_mode.index("preflight") < claim_mode.index("**Wave 1, lookup.**")
    assert "**Wave 7, worktree.**" in claim_mode
    assert "Print the `next-steps.md` path and STOP" not in skill
    assert "E-ORCA-REQUIRED" in skill.split("## Error handling", 1)[1]


def test_every_worktree_warning_code_is_listed_with_a_remedy_line():
    """Each code the script can print is named in SKILL.md and in the Wave 7 table."""
    script = _text(SKILL_DIR / "scripts/orca_worktree.py")
    block = script.split("WARNING_ORDER = [", 1)[1].split("]", 1)[0]
    codes = re.findall(r'"(W-[A-Z-]+)"', block)
    assert "W-FIRST-TAB-LEFT" in codes
    skill = _text(SKILL).split("## Error handling", 1)[1]
    wave7 = _text(REFS / "claim.md").split("## Wave 7", 1)[1].split("## Wave 8", 1)[0]
    for code in codes:
        assert f"`{code}`" in skill, code
        assert f"| `{code}` |" in wave7, code
    assert "| `W-FIRST-TAB-LEFT` | close the plain tab in Orca by hand |" in wave7


# --- the launch step (design pipeline-flag, ST-4, ST-7, ST-9, ST-10, ST-11) -------

ORCA_SCRIPT = SKILL_DIR / "scripts/orca_worktree.py"
# Orca link flags and agent flags that only `orca agent launch` may carry.
LINK_FLAGS = {"--issue", "--pr", "--linear-issue"}
LINK_PREFIXES = ("--reference", "--gitlab")
NEVER_FLAGS = {
    "--model",
    "--effort",
    "--setup",
    "--branch",
    "--activate",
    "--run-hooks",
}
LAUNCH_ONLY_FLAGS = {"--agent", "--prompt", "--surface"}
_WHOLE_FLAG = re.compile(r"(?<![\w-])--[a-z][a-z0-9-]*")
_ORCA_COMMAND_LINE = re.compile(r"\borca (?:status|worktree|agent|terminal|repo)\b")


def _forbidden(flag: str) -> bool:
    return flag in LINK_FLAGS | NEVER_FLAGS or flag.startswith(LINK_PREFIXES)


def test_st4_script_has_no_forbidden_orca_flag_and_launch_flags_only_in_launch():
    tree = ast.parse(_text(ORCA_SCRIPT))
    flags = {
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and re.fullmatch(r"--[a-z][a-z0-9-]*", node.value)
    }
    assert sorted(f for f in flags if _forbidden(f)) == []
    assert LAUNCH_ONLY_FLAGS <= flags
    (launch,) = [
        n
        for n in ast.walk(tree)
        if isinstance(n, ast.FunctionDef) and n.name == "cmd_launch"
    ]
    inside = {
        n.value
        for n in ast.walk(launch)
        if isinstance(n, ast.Constant) and isinstance(n.value, str)
    }
    assert LAUNCH_ONLY_FLAGS <= inside
    for other in (n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)):
        if other.name == "cmd_launch":
            continue
        used = {
            n.value
            for n in ast.walk(other)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)
        }
        assert not (used & LAUNCH_ONLY_FLAGS), other.name


def test_st4_markdown_orca_command_lines_have_no_forbidden_flag():
    files = [SKILL, *sorted(REFS.glob("*.md")), *sorted(TEMPLATES.glob("*.md"))]
    files.append(COMMANDS / "issue.md")
    seen = 0
    for path in files:
        for line in _text(path).splitlines():
            if not _ORCA_COMMAND_LINE.search(line):
                continue
            seen += 1
            flags = _WHOLE_FLAG.findall(line)
            assert [f for f in flags if _forbidden(f)] == [], (path.name, line)
            if "orca agent launch" not in line:
                assert not set(flags) & LAUNCH_ONLY_FLAGS, (path.name, line)
    assert seen, "the scan matched no orca command line"


def test_st4_flag_matcher_uses_whole_tokens():
    # "--prompt" must not trip the "--pr" link flag, and "--issue-url" is another flag.
    assert not _forbidden("--prompt") and not _forbidden("--issue-url")
    assert (
        _forbidden("--pr")
        and _forbidden("--reference-url")
        and _forbidden("--gitlab-mr")
    )


def test_st7_plan_boundary_line_and_the_k_rule():
    assert "Plan boundary: after step <K>" in _text(TEMPLATES / "next-steps.md")
    claim = _text(REFS / "claim.md")
    wave5 = _wave(claim, 5)
    assert (
        "`<K>` is the number of the last step before the first step whose command is"
        in wave5
    )
    assert "`/sc:implement` or `/task`" in wave5
    assert "Plan boundary: before step 1" in wave5
    assert "`--pipeline full` ignores the line" in wave5
    assert _text(TEMPLATES / "next-steps.md").splitlines()[0].startswith("/model ")


def test_st9_prompt_is_written_before_wave_7_and_wave_8_skips_none():
    claim = _text(REFS / "claim.md")
    wave5, wave8 = _wave(claim, 5), _wave(claim, 8)
    assert (
        'orca_worktree.py" prompt --template "<skill base>/templates/launch-prompt.md"'
        in wave5
    )
    assert '--out "<D>/launch-prompt.md"' in wave5
    assert "not `none`" in wave5 and "written before Wave 7" in wave5
    assert (
        claim.index("## Wave 5") < claim.index("## Wave 7") < claim.index("## Wave 8")
    )
    assert "Runs only when `--pipeline` is not `none`" in wave8
    assert "`created` or `reused`" in wave8
    assert "never attempted for a `failed` worktree" in wave8
    assert 'orca_worktree.py" launch --number <N> --source <D> --level <L>' in wave8
    assert "never a STOP" in wave8 or "never a STOP" in claim.split("## Wave 8", 1)[1]


def test_st9_a_reclaim_does_not_rewrite_the_prompt_of_a_running_agent():
    wave5 = _wave(_text(REFS / "claim.md"), 5)
    assert '--source "<D>"' in wave5
    assert "`status: kept`" in wave5
    assert "worktree still exists" in wave5


def test_st9_final_output_lists_the_launch_results_and_every_launch_code():
    claim = _text(REFS / "claim.md")
    final = claim.split("## Final output", 1)[1]
    for text in (
        "`launched`",
        "`already_launched`",
        "`--pipeline none`",
        "never merges",
    ):
        assert text in final, text
    for code in (
        "W-LAUNCH-FAILED",
        "W-LAUNCH-NOT-CCSESSION",
        "W-ENFORCEMENT-ABSENT",
        "W-L2-ABSENT",
    ):
        assert code in claim and code in _text(SKILL), code


def test_st9_final_output_prints_the_hand_command_the_remedy_line_promises():
    claim = _text(REFS / "claim.md")
    assert "the hand command is printed" in claim.split("## Wave 8", 1)[1]
    warnings_item = next(
        ln
        for ln in claim.split("## Final output", 1)[1].splitlines()
        if "Every warning" in ln
    )
    assert "`hand_command`" in warnings_item and "`W-LAUNCH-FAILED`" in warnings_item
    assert "not governed by the enforcement hook" in warnings_item


def test_pipeline_none_creates_no_worktree_and_wave_7_skips_it():
    claim = _text(REFS / "claim.md")
    wave7, wave6 = _wave(claim, 7), _wave(claim, 6)
    assert "Does not run for `--pipeline none`" in wave7
    assert "Runs for every `--pipeline` value" not in claim
    assert "unless `--pipeline` is `none`" in wave6
    assert "no Wave 7 and no Wave 8" in wave6
    assert "no `<D>/worktree.json` is written" in wave6
    # Orca stays a dependency of every claim, so the Wave 0 check still runs for none.
    wave0 = claim.split("## Wave 0", 1)[1].split("## Wave 1", 1)[0]
    assert "It also runs for `--pipeline none`" in wave0
    skill = _text(SKILL).split("## Claim mode", 1)[1].split("## Create mode", 1)[0]
    assert "**Wave 7, worktree.** Not for `--pipeline none`." in skill
    assert "except for `--pipeline none`, which ends the claim here" in skill


def test_pipeline_none_final_output_has_no_worktree_line_and_names_this_checkout():
    final = _text(REFS / "claim.md").split("## Final output", 1)[1]
    item1 = next(ln for ln in final.splitlines() if ln.startswith("1. "))
    assert "For `--pipeline none` print no `Worktree:` line" in item1
    none_line = next(ln for ln in final.splitlines() if "`--pipeline none`:" in ln)
    assert "No worktree created and no agent launched" in none_line
    assert "in this checkout" in none_line and "<wt>" not in none_line


def test_pipeline_none_return_contract_has_null_worktree_fields():
    section = (
        _text(SKILL).split("## Return contract", 1)[1].split("## Error handling", 1)[0]
    )
    assert "worktree_status: created | reused | failed | not_requested" in section
    assert (
        "`worktree_status` is `not_requested` and `worktree_path`, `worktree_branch`, "
        "`worktree_match_key` and `worktree_warning` are `null`"
    ) in section
    command = _text(COMMANDS / "issue.md")
    assert "Every value creates the worktree" not in command
    assert "`none` creates no worktree and launches no agent" in command


def _yaml_keys(block: str) -> list[str]:
    return re.findall(r"^([a-z_]+):", block, re.M)


def test_st10_claim_return_contract_has_the_ten_fields_and_keeps_the_old_ones():
    skill = _text(SKILL)
    section = skill.split("## Return contract", 1)[1].split("## Error handling", 1)[0]
    blocks = re.findall(r"```yaml\n(.*?)```", section, re.S)
    assert len(blocks) == 2
    assert _yaml_keys(blocks[0]) == [
        "status",
        "mode",
        "issue_number",
        "issue_url",
        "dir",
        "clickup_status",
        "labels_applied",
        "labels_missing",
        "next_steps_path",
    ]
    assert _yaml_keys(blocks[1]) == [
        "pipeline_level",
        "submit",
        "worktree_status",
        "worktree_path",
        "worktree_branch",
        "worktree_match_key",
        "worktree_warning",
        "launch_status",
        "launch_warning",
        "enforcement_hook",
    ]
    assert "create mode prints none of them" in section


def test_st11_no_source_tree_path_in_the_command_file():
    assert "src/superclaude/" not in _text(COMMANDS / "issue.md")


def test_skill_will_and_will_not_match_the_command_file():
    skill = _text(SKILL)
    will_not = skill.split("## Will Not", 1)[1]
    for token in (
        "`/sc:implement`",
        "`/task`",
        "a commit",
        "a push",
        "`/sc:pr-submit`",
    ):
        assert token in will_not, token
    assert "Merge anything." in will_not and "Pass an Orca link flag" in will_not
    assert "Run any next-step command" not in skill
    assert "Stop a claim after writing `next-steps.md`" not in skill
    assert "launch one agent" in skill.split("## Will Not", 1)[0].split("## Will", 1)[1]


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
