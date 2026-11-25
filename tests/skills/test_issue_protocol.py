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

from tests.skills.test_issue_worker_agents import (
    PLAN_SECTIONS_RULE,
    gh_lines_missing_repo,
)

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

# The three required plan sections (issue 651): the last three headings of every
# issue-body template, in this order, before the closing marker line.
PLAN_SECTIONS = ["Priority", "Fix approach", "Test plan"]

_BUG_SIMPLE_BODY = [
    "Bug Summary",
    "Environment (OS, version)",
    "Current Behavior",
    "Expected Behavior",
    "Steps to Reproduce",
    "Impact Assessment (Severity, Blast Radius)",
    "Error Messages",
    "Codebase Context (from `/sc:analyze`)",
    "Related Issues",
]
BUG_SIMPLE = _BUG_SIMPLE_BODY + PLAN_SECTIONS
BUG_COMPLEX = (
    _BUG_SIMPLE_BODY
    + [
        "Frequency",
        "User Impact",
        "Business Impact",
        "Cascading Effects",
        "Logs and Stack Trace",
        "Attempted Solutions",
        "Proposed Solution",
        "For Development Team (Root Cause Analysis)",
    ]
    + PLAN_SECTIONS
)
_FEATURE_SIMPLE_BODY = [
    "Feature Summary",
    "Problem Statement",
    "User Story",
    "Proposed Solution",
    "Acceptance Criteria",
    "Out of Scope",
    "Components Affected (from `/sc:analyze`)",
    "Related Issues/PRs",
]
FEATURE_SIMPLE = _FEATURE_SIMPLE_BODY + PLAN_SECTIONS
FEATURE_COMPLEX = (
    _FEATURE_SIMPLE_BODY
    + [
        "Success Metrics",
        "Architecture Impact",
        "Dependencies",
        "Documentation Needs",
        "Alternatives Considered",
        "Impact Analysis (Blast Radius, Integration Impact)",
        "Risks & Mitigation",
        "Effort Estimate (hours) and Complexity",
    ]
    + PLAN_SECTIONS
)
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


LAUNCH_BLOCKS = [
    "common",
    "worktree",
    "full",
    "submit",
    "research",
    "spec",
    "plan",
    "debugworktree",
    "debugfull",
    "result",
]


def test_st8_launch_prompt_has_exactly_the_ten_blocks():
    assert list(_launch_blocks()) == LAUNCH_BLOCKS
    assert len(_BLOCK_MARKER.findall(_text(LAUNCH_TEMPLATE))) == len(LAUNCH_BLOCKS)


def _orca_module(name: str):
    import importlib.util
    import sys

    spec = importlib.util.spec_from_file_location(name, ORCA_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses need it
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(spec.name, None)
    return module


def _render(level: str, stage: str | None, submit: bool = False) -> str:
    return _orca_module("orca_worktree_t10").render_prompt(
        _text(LAUNCH_TEMPLATE), level, submit, 12, "owner/repo", stage
    )


CASES = [
    ("worktree", False),
    ("full", False),
    ("full", True),
]


@pytest.mark.parametrize("stage", [None, "research", "spec", "plan", "debug"])
@pytest.mark.parametrize(("level", "submit"), CASES)
def test_r23_launch_prompt_ends_with_the_result_step_and_makes_no_github_write(
    level, submit, stage
):
    text = _render(level, stage, submit)
    assert "Last step" in text and ".dev/issues/12/result.md" in text
    assert text.strip().endswith("does everything on GitHub itself.")
    result = text.split("Last step", 1)[1]  # nothing follows the result step
    assert "outcome: succeeded" in result and "pull_request:" in result
    assert "artifacts:" in result
    assert "Only the coordinator writes to an issue, a label or a Project" in text
    for forbidden in ("issue-pipeline", "gh issue", "gh label", "gh project", "gh api"):
        assert forbidden not in text, forbidden
    if stage != "debug":
        assert "--fix" not in text


@pytest.mark.parametrize(("level", "submit"), CASES)
def test_r23_troubleshoot_is_limited_at_worktree_and_carries_fix_at_full(level, submit):
    text = _render(level, "debug", submit)
    stage = text.split("Stage: debug.", 1)[1].split("\n\n", 1)[0]
    assert "/sc:troubleshoot" in stage
    if level == "worktree":
        assert "without `--fix`" in stage
        assert "with `--fix`" not in stage
    else:
        assert "with `--fix`" in stage
        assert "without `--fix`" not in stage


@pytest.mark.parametrize(
    ("stage", "command"),
    [
        ("research", "/sc:research"),
        ("spec", "/sc:design"),
        ("plan", "/sc:workflow"),
    ],
)
def test_r23_each_stage_names_its_command_in_the_launch_prompt(stage, command):
    text = _render("worktree", stage)
    assert f"Stage: {stage}." in text and command in text
    assert "/sc:implement" not in text.split("Stage:", 1)[1].split("\n\n", 1)[0] or (
        stage == "plan"
    )


def test_r23_the_prompt_command_takes_a_stage_and_refuses_an_unknown_one():
    module = _orca_module("orca_worktree_t10b")
    with pytest.raises(ValueError):
        module.render_prompt(_text(LAUNCH_TEMPLATE), "full", False, 12, "o/r", "ready")
    with pytest.raises(SystemExit):
        module.main(["prompt", "--stage", "ready"])


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


def test_st9_launch_result_file_is_documented_for_launched_and_failed():
    for path in (REFS / "claim.md", SKILL):
        lines = [ln for ln in _text(path).splitlines() if "launch-result.json" in ln]
        assert lines, path
        # the Wave 7 line only says the file is not copied; one line must say what it holds
        assert any("`launched`" in ln and "`failed`" in ln for ln in lines), path


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
    assert len(blocks) == 3
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
    assert _yaml_keys(blocks[2]) == [
        "issue_type",
        "complexity_field",
        "classification_missing",
    ]
    assert "create mode prints none of them" in section
    assert "Create mode adds these three fields after the claim block" in section


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


def plan_section_problems(text: str) -> list[str]:
    """Return one message per problem with the three required plan sections.

    Each of ``## Priority``, ``## Fix approach`` and ``## Test plan`` must appear
    exactly once with a non-empty body that does not say "Not known yet", and the
    three must be the last three headings, in that order (issue 651).
    """
    lines = text.splitlines()
    problems = []
    for name in PLAN_SECTIONS:
        heading = f"## {name}"
        count = lines.count(heading)
        if count != 1:
            problems.append(f"{heading} appears {count} times, expected 1")
            continue
        start = lines.index(heading) + 1
        end = next(
            (
                i
                for i in range(start, len(lines))
                if lines[i].startswith(("## ", "<!-- sc:issue:create"))
            ),
            len(lines),
        )
        body = "\n".join(lines[start:end]).strip()
        if not body:
            problems.append(f"{heading} has an empty body")
        elif "Not known yet" in body:
            problems.append(f'{heading} says "Not known yet"')
    if headings(text)[-len(PLAN_SECTIONS) :] != PLAN_SECTIONS:
        problems.append("the plan sections are not the last three headings, in order")
    return problems


def _mutated_template(stem: str, tmp_path: Path, lines: list[str]) -> str:
    copy = tmp_path / f"{stem}.md"
    copy.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return copy.read_text(encoding="utf-8")


@pytest.mark.parametrize("stem", sorted(ISSUE_TEMPLATES))
def test_issue_template_has_required_plan_sections(stem):
    assert plan_section_problems(_text(TEMPLATES / f"{stem}.md")) == []


@pytest.mark.parametrize("stem", sorted(ISSUE_TEMPLATES))
def test_plan_section_check_fails_when_a_heading_is_removed(stem, tmp_path):
    lines = _text(TEMPLATES / f"{stem}.md").splitlines()
    kept = [line for line in lines if line != "## Fix approach"]
    assert len(kept) == len(lines) - 1
    problems = plan_section_problems(_mutated_template(stem, tmp_path, kept))
    assert "## Fix approach appears 0 times, expected 1" in problems


@pytest.mark.parametrize("stem", sorted(ISSUE_TEMPLATES))
def test_plan_section_check_fails_when_a_body_is_emptied(stem, tmp_path):
    lines = _text(TEMPLATES / f"{stem}.md").splitlines()
    lines[lines.index("## Priority") + 1 : lines.index("## Fix approach")] = [""]
    problems = plan_section_problems(_mutated_template(stem, tmp_path, lines))
    assert problems == ["## Priority has an empty body"]


@pytest.mark.parametrize("stem", sorted(ISSUE_TEMPLATES))
def test_plan_section_check_fails_when_a_body_says_not_known_yet(stem, tmp_path):
    lines = _text(TEMPLATES / f"{stem}.md").splitlines()
    lines.insert(lines.index("## Test plan") + 1, "Not known yet")
    problems = plan_section_problems(_mutated_template(stem, tmp_path, lines))
    assert problems == ['## Test plan says "Not known yet"']


def test_create_ref_defines_priority_rule_set_and_required_sections():
    text = _text(REFS / "create.md")
    assert PLAN_SECTIONS_RULE in text
    rows = re.findall(r"(?m)^\| (Urgent|High|Medium|Low) \| (.+) \|$", text)
    assert [level for level, _ in rows] == ["Urgent", "High", "Medium", "Low"]
    assert all(trigger.strip() for _, trigger in rows)


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
    assert len(steps) == 2
    for step in steps:
        assert "--handoff tasklist" not in step and "--handoff design" not in step
        assert "--models" not in step
    text = _text(REFS / "chains.md")
    assert "--handoff tasklist" not in text and "--handoff design" not in text


def test_feature_simple_row_plans_directly_from_the_summary():
    row = next(
        r
        for r in chain_rows(_text(REFS / "chains.md"))
        if r.startswith("| Feature, simple |")
    )
    assert "/sc:brainstorm" not in row
    assert "`/sc:workflow <S> --depth quick --handoff none`" in row
    assert "`/sc:implement <plan path printed by step 1>`" in row


def test_default_level_is_full_and_only_worktree_waits_for_a_person():
    skill = _text(SKILL)
    assert "`full` also implements without a commit or a push" in skill
    assert "`full` (default)" not in skill
    claim = _text(REFS / "claim.md")
    wave5 = _wave(claim, 5)
    assert "(explicit)" in wave5 and "(default: " in wave5 and "16 hours" in wave5
    assert "`<L>` is the same level as in Wave 5." in _wave(claim, 8)
    next_steps = _text(TEMPLATES / "next-steps.md")
    assert "at level `full`" in next_steps and "default level `full`" not in next_steps
    launched = next(ln for ln in claim.splitlines() if "- `launched`:" in ln)
    before, rest = launched.split("For `worktree`:", 1)
    worktree, full = rest.split("For `full`:", 1)
    assert "run the printed implement command" in worktree
    assert "run the printed implement command" not in before + full


def test_default_level_rule_is_bug_full_complex_feature_worktree():
    claim = _text(REFS / "claim.md")
    wave5 = _wave(claim, 5)
    next_steps = wave5.index("Write `<D>/next-steps.md`")
    start = wave5.index("Resolve the level `<L>`")
    boundary = wave5.index("Set the plan boundary")
    assert next_steps < start < boundary
    rule = wave5[start:boundary]
    for token in ("`Type`", "`Complexity`", "`Effort estimate`", "issue-summary.md"):
        assert token in rule
    assert rule.index("cannot be read") < rule.index("`full` for a bug")
    assert "`<L>` is `worktree` and no other check runs" in rule
    assert "also gets `worktree`" in rule
    assert (
        "`full` for a feature whose complexity is `simple` or `medium` and whose "
        "effort is 16 hours or less"
    ) in rule
    assert (
        "`worktree` for a feature whose complexity is `complex` or whose effort "
        "is over 16 hours"
    ) in rule
    assert "an explicit value always wins" in rule
    # Wave 5 only holds the Level line; the Final output prints it (once).
    assert "Hold one line and print nothing yet" in rule
    assert "Print one line" not in rule
    lines = claim.splitlines()
    launched = next(ln for ln in lines if "- `launched`:" in ln)
    assert "Print the `Level:` line of Wave 5 with this result." in launched
    already = next(ln for ln in lines if "- `already_launched`:" in ln)
    assert "`Level: <stored level> (stored)`" in already
    assert "the stored level wins" in already
    failed = next(ln for ln in lines if ln.lstrip().startswith("- Failed worktree"))
    assert "print no `Level:` line" in failed


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


# --- issue type and Complexity field (issue 438) -------------------------------------

AGENT_T3 = AGENTS[0]
_ALLOWED_ORGS = re.compile(r"orgs/<owner(?: of R)?>/issue-fields")
_ANY_ORGS_PATH = re.compile(r"orgs/[A-Za-z0-9_<{.-][^\s`]*")


def _skill_and_agent_texts() -> dict[str, str]:
    """Every markdown file of the skill package and the three worker files."""
    paths = [*sorted(SKILL_DIR.rglob("*.md")), *AGENTS]
    return {p.name: _text(p) for p in paths if "__pycache__" not in p.parts}


def orgs_paths_other_than_allowed(text: str) -> list[str]:
    """Return every ``orgs/...`` path that is not the one allowed lookup.

    A bare ``orgs/`` token (prose such as "no other `orgs/` path") is not a path.
    """
    return _ANY_ORGS_PATH.findall(_ALLOWED_ORGS.sub("", text))


def test_orgs_path_is_the_single_allowed_read_and_sits_in_three_files():
    holders = set()
    for name, text in _skill_and_agent_texts().items():
        assert orgs_paths_other_than_allowed(text) == [], name
        if _ALLOWED_ORGS.search(text):
            holders.add(name)
    assert holders == {"SKILL.md", "create.md", "issue-worker-t3.md"}


def test_orgs_scanner_reports_a_second_path_and_ignores_prose():
    text = (
        "read `orgs/<owner of R>/issue-fields` only; no other `orgs/` path is allowed.\n"
        "Never read orgs/other/issue-fields."
    )
    assert orgs_paths_other_than_allowed(text) == ["orgs/other/issue-fields."]


def test_labels_md_has_no_area_or_complexity_label_and_creates_only_the_mode_labels():
    text = _text(REFS / "labels.md")
    assert not re.search(r"`(?:type|complexity): [a-z]+`", text)
    assert re.findall(r'gh label create "([^"]+)"', text) == ["bug", "enhancement"]


def test_field_value_write_is_a_post_and_no_file_uses_a_put():
    post = "gh api -X POST repos/<R>/issues/<N>/issue-field-values --input"
    for path in (SKILL, REFS / "create.md", REFS / "labels.md"):
        assert post in _text(path), path.name
    for name, text in _skill_and_agent_texts().items():
        assert "-X PUT" not in text, name


def test_field_readback_uses_the_field_id_and_option_name_not_numeric_value():
    text = _text(REFS / "labels.md")
    assert "`issue_field_id` equals the field id" in text
    assert "compare `single_select_option.name`" in text
    assert "Do not compare the numeric `value` directly" in text
    assert "failed or unparseable read-back does not prove success" in text


OUTPUT_LINES = [
    "not applied: label missing in repo: <name>",
    "not set: issue type <name>: <type missing in repo | lookup failed | not applied after create>",
    "not set: field Complexity <value>: <field not found in org | option not found | lookup failed | write failed (<error>) | not applied after create>",
]


def test_labels_md_carries_the_three_output_lines_exactly():
    lines = _text(REFS / "labels.md").splitlines()
    for line in OUTPUT_LINES:
        assert line in lines


def test_create_md_uses_the_output_line_prefixes_and_the_type_and_field_reasons():
    text = _text(REFS / "create.md")
    for needle in (
        "not applied: label missing in repo",
        "not set: issue type <name>: type missing in repo",
        "not set: issue type <name>: not applied after create",
        "not set: field Complexity <value>: write failed (",
        "not set: field Complexity <value>: not applied after create",
        "not set: field Complexity <value>: field not found in org",
    ):
        assert needle in text, needle


def test_t3_lookup_scout_template_and_flags_cover_issue_types_and_the_complexity_field():
    t3 = _text(AGENT_T3)
    assert "issue-types" in t3 and "issue-fields" in t3
    scout = _text(TEMPLATES / "scout-report.md")
    assert "### Repo issue types" in scout and "### Complexity field" in scout
    flags = _text(TEMPLATES / "flags-decision.md")
    assert "| Issue type | <Feature | Bug | Test> |" in flags
    assert "<Simple | Medium | Complex>" in flags
    assert "not reclassified" in _text(TEMPLATES / "create-review-comment.md")


@pytest.mark.parametrize(
    "row",
    [
        "| bug | any | Bug |",
        "| feature | tests | Test |",
        "| feature | any other area | Feature |",
        "| quick | Simple |",
        "| standard | Medium |",
        "| deep | Complex |",
    ],
)
def test_labels_md_states_the_issue_type_and_complexity_rules(row):
    assert row in _text(REFS / "labels.md").splitlines()


def test_skill_md_states_the_create_rules_of_the_issue_type_and_field():
    skill = _text(SKILL)
    for needle in (
        "create mode adds `--type <name>`",
        "gh api -X POST repos/<R>/issues/<N>/issue-field-values --input <file>",
        "Write any issue field other than Complexity.",
        "The wanted issue type is missing in the repo",
        "The Complexity field or its option is missing",
    ):
        assert needle in skill, needle
    assert "fixed set" not in skill


def test_command_and_skill_agree_on_the_new_create_boundaries():
    command = _text(COMMANDS / "issue.md")
    skill = _text(SKILL)
    assert "Write any issue field other than Complexity." in command
    assert "Write any issue field other than Complexity." in skill
    assert "issue types, issue fields" in command
    assert "an issue type, an issue field" in skill
    assert "fixed set" not in command


HANDOFF_START = "Coordinator handoff for `--pipeline none`:"


def _handoff_paragraph(path: Path) -> str:
    paragraphs = [p for p in _text(path).split("\n\n") if p.startswith(HANDOFF_START)]
    assert len(paragraphs) == 1, f"{path.name}: expected one handoff paragraph"
    return paragraphs[0]


HANDOFF_FILES = [COMMANDS / "issue.md", SKILL, REFS / "claim.md"]


def test_the_coordinator_handoff_is_the_same_paragraph_in_all_three_files():
    paragraphs = {_handoff_paragraph(path) for path in HANDOFF_FILES}
    assert len(paragraphs) == 1


@pytest.mark.parametrize(
    "needle",
    [
        "the claim leaves its files in the checkout that ran it",
        "it runs the `worktree` step of `orca_worktree.py` (the repository, the issue number, the base branch and that folder as its arguments)",
        "worker-start --worktree path:<the printed path>",
        "The script creates the worktree with no agent",
        "it must copy `.dev/issues/<N>/` into the worktree before any agent starts",
        "the coordinator must run `worker-start` straight after it",
        "the worktree stays empty, with no agent and no terminal",
        "adoption row still `reserved`: a start may or may not have happened, so it never starts again by itself",
        "a worker in that worktree settles the row as `started` with its Dispatch id",
        "reuses the existing worktree through the script's reuse lookup (marker, record, basename, branch)",
        "orca worktree ps",
    ],
)
def test_the_coordinator_handoff_paragraph_states(needle):
    assert needle in _handoff_paragraph(COMMANDS / "issue.md")


def test_the_claim_still_writes_no_worktree_record_for_pipeline_none():
    assert "no `<D>/worktree.json` is written" in _text(REFS / "claim.md")


def test_stage_claim_skips_recommend_and_plain_claim_keeps_it():
    claim = _text(REFS / "claim.md")
    step1 = claim.split("1. Without `--stage`: invoke `Skill sc-recommend`", 1)[
        1
    ].split("\n2.", 1)[0]
    # plain claim: the recommend step is unchanged
    assert (
        "Save its output verbatim to `<D>/recommend.md`"
        in step1.split("With `--stage <stage>`", 1)[0]
    )
    # --stage claim: no Skill call, one skip line, no "Default row not used"
    stage = step1.split("With `--stage <stage>`", 1)[1]
    assert "do not invoke `Skill sc-recommend`" in stage
    assert (
        "Skipped: --stage <stage> sets step 1 (the Project Status names the starting command)."
        in stage
    )
    assert "`Default row not used` line is not written" in claim
    assert "a `--stage` claim never calls it" in claim


# --- create decision rule: ask only for a contradiction (issue 834) -------------------

CONFLICT_CATEGORIES = [
    "reversed choice",
    "dropped requirement",
    "changed flag",
    "contradicted by verified code",
]
# The old broad trigger and the old first choice are built from fragments, so no
# whole copy of either sits in tests/ (a search of tests/ for them finds nothing).
OLD_TRIGGER = "new" + " material" + " or a" + " contradiction"
OLD_KEEP_ALL = '"keep' + ' all"'


def prompt_rule_section(text: str) -> str:
    """The body of the Contradiction prompt rule section of refs/create.md."""
    start = text.index("### Contradiction prompt rule")
    return text[start : text.index("\n## ", start)]


def line_starting(text: str, prefix: str) -> str:
    return next((ln for ln in text.splitlines() if ln.startswith(prefix)), "")


def _mutated(tmp_path: Path, name: str, text: str) -> str:
    copy = tmp_path / name
    copy.write_text(text, encoding="utf-8")
    return copy.read_text(encoding="utf-8")


def create_question_problems(ref: str, skill: str) -> list[str]:
    """Problems with the rule that create asks only for a supported contradiction."""
    section = prompt_rule_section(ref)
    problems = [
        f"prompt rule section lacks the category {name!r}"
        for name in CONFLICT_CATEGORIES
        if name not in section
    ]
    for needle in ("exactly one", "before Wave 5", "zero questions"):
        if needle not in section:
            problems.append(f"prompt rule section lacks {needle!r}")
    for where, text in (("refs/create.md", ref), ("SKILL.md", skill)):
        if OLD_TRIGGER in text:
            problems.append(f"{where} still carries the old broad trigger")
    if OLD_KEEP_ALL in ref:
        problems.append("refs/create.md still offers the old keep-all choice")
    return problems


def draft_notes_problems(text: str) -> list[str]:
    """Problems with the two lists and their different consequences."""
    problems = []
    if headings(text) != ["New material", "Contradictions"]:
        problems.append("the two headings are not exactly New material, Contradictions")
    if text.count("\n- None") != 2:
        problems.append("each list must keep a '- None' empty marker")
    for needle in ("no question", "one question"):
        if needle not in text:
            problems.append(f"the template does not say {needle!r}")
    return problems


def additions_report_problems(ref: str, skill: str) -> list[str]:
    """Problems with the retained-additions line and the no-approval promise."""
    problems = []
    step8 = line_starting(ref, "8. Print the issue URL")
    step6 = line_starting(skill, "6. **Wave 5, post.**")
    if "kept without approval:" not in step8:
        problems.append(
            "refs/create.md Wave 5 step 8 lacks the retained-additions line"
        )
    if "kept without approval:" not in step6:
        problems.append("SKILL.md create step 6 lacks the retained-additions line")
    if "never shown for approval" not in prompt_rule_section(ref):
        problems.append(
            "the prompt rule section no longer says the body is never shown"
        )
    if "never shown for approval" not in line_starting(skill, "- Posts go up directly"):
        problems.append("SKILL.md 'Posts go up directly' no longer says it")
    return problems


def evidence_rule_problems(ref: str, template: str) -> list[str]:
    """Problems with the three-part contradiction rule and the flag carve-out."""
    problems = []
    for where, text in (("refs/create.md", ref), ("draft-notes template", template)):
        for needle in (
            "user's own words",
            "conflicting evidence",
            "missing any of the three",
            "disagreement with a",
            "not a contradiction",
        ):
            if needle not in text:
                problems.append(f"{where} lacks {needle!r}")
    return problems


def test_create_questions_only_for_contradictions():
    ref, skill = _text(REFS / "create.md"), _text(SKILL)
    assert create_question_problems(ref, skill) == []


def test_create_question_check_fails_when_the_old_trigger_returns(tmp_path):
    ref, skill = _text(REFS / "create.md"), _text(SKILL)
    back = ref + "\nAsk when `draft-notes.md` lists " + OLD_TRIGGER + ".\n"
    problems = create_question_problems(_mutated(tmp_path, "create.md", back), skill)
    assert problems == ["refs/create.md still carries the old broad trigger"]


@pytest.mark.parametrize("name", CONFLICT_CATEGORIES)
def test_create_question_check_fails_when_a_category_is_deleted(name, tmp_path):
    ref, skill = _text(REFS / "create.md"), _text(SKILL)
    section = prompt_rule_section(ref)
    cut = ref.replace(section, section.replace(name, "removed"))
    problems = create_question_problems(_mutated(tmp_path, "create.md", cut), skill)
    assert problems == [f"prompt rule section lacks the category {name!r}"]


def test_create_question_check_fails_when_the_keep_all_choice_returns(tmp_path):
    ref, skill = _text(REFS / "create.md"), _text(SKILL)
    back = ref + "\nChoices: " + OLD_KEEP_ALL + ".\n"
    problems = create_question_problems(_mutated(tmp_path, "create.md", back), skill)
    assert problems == ["refs/create.md still offers the old keep-all choice"]


def test_draft_notes_separates_additions_and_contradictions():
    assert draft_notes_problems(_text(TEMPLATES / "draft-notes.md")) == []


def test_draft_notes_check_fails_when_the_none_marker_is_deleted(tmp_path):
    text = _text(TEMPLATES / "draft-notes.md")
    cut = text.replace("\n- None", "\n- ", 1)
    problems = draft_notes_problems(_mutated(tmp_path, "draft-notes.md", cut))
    assert problems == ["each list must keep a '- None' empty marker"]


def test_draft_notes_check_fails_when_the_consequences_are_deleted(tmp_path):
    text = _text(TEMPLATES / "draft-notes.md")
    cut = text.replace("cause no question", "cause nothing").replace(
        "exactly one question", "a prompt"
    )
    problems = draft_notes_problems(_mutated(tmp_path, "draft-notes.md", cut))
    assert problems == [
        "the template does not say 'no question'",
        "the template does not say 'one question'",
    ]


def test_create_reports_additions_without_approval():
    assert additions_report_problems(_text(REFS / "create.md"), _text(SKILL)) == []


def test_additions_report_check_fails_when_the_literal_is_removed(tmp_path):
    ref, skill = _text(REFS / "create.md"), _text(SKILL)
    cut = skill.replace("kept without approval:", "kept")
    problems = additions_report_problems(ref, _mutated(tmp_path, "SKILL.md", cut))
    assert problems == ["SKILL.md create step 6 lacks the retained-additions line"]


def test_additions_report_check_fails_when_the_promise_is_removed(tmp_path):
    ref, skill = _text(REFS / "create.md"), _text(SKILL)
    section = prompt_rule_section(ref)
    cut = ref.replace(section, section.replace("never shown for approval", "shown"))
    problems = additions_report_problems(_mutated(tmp_path, "create.md", cut), skill)
    assert problems == [
        "the prompt rule section no longer says the body is never shown"
    ]


def test_contradiction_categories_require_user_evidence():
    ref, template = _text(REFS / "create.md"), _text(TEMPLATES / "draft-notes.md")
    assert evidence_rule_problems(ref, template) == []


@pytest.mark.parametrize(
    "needle",
    ["conflicting evidence", "missing any of the three", "disagreement with a"],
)
def test_evidence_rule_check_fails_when_a_requirement_is_deleted(needle, tmp_path):
    ref, template = _text(REFS / "create.md"), _text(TEMPLATES / "draft-notes.md")
    cut = template.replace(needle, "removed")
    problems = evidence_rule_problems(ref, _mutated(tmp_path, "draft-notes.md", cut))
    assert problems == [f"draft-notes template lacks {needle!r}"]


def credential_check_problems(ref: str) -> list[str]:
    """Problems with the no-question credential check that runs before the post."""
    problems = []
    check = line_starting(ref, "Credential check")
    if not check:
        return ["refs/create.md has no 'Credential check' paragraph"]
    for needle in (
        "with no question",
        "prints nothing",
        "run a scanner",
        "<REDACTED>",
        "kept without approval",
    ):
        if needle not in check:
            problems.append(f"the credential check lacks {needle!r}")
    if "safety-scan" in check:
        # that command prints the whole matching row, which would copy the value
        problems.append("the credential check runs a scanner that prints body rows")
    if ref.index(check) > ref.index("3. `gh issue create"):
        problems.append("the credential check does not come before the create command")
    if "`redacted:` line" not in line_starting(ref, "8. Print the issue URL"):
        problems.append("Wave 5 step 8 does not print the redacted lines")
    return problems


def test_create_redacts_credentials_before_posting_without_a_question():
    assert credential_check_problems(_text(REFS / "create.md")) == []


@pytest.mark.parametrize(
    "needle", ["with no question", "<REDACTED>", "prints nothing", "run a scanner"]
)
def test_credential_check_fails_when_a_requirement_is_deleted(needle, tmp_path):
    ref = _text(REFS / "create.md")
    check = line_starting(ref, "Credential check")
    cut = ref.replace(check, check.replace(needle, "removed"))
    problems = credential_check_problems(_mutated(tmp_path, "create.md", cut))
    assert problems == [f"the credential check lacks {needle!r}"]
