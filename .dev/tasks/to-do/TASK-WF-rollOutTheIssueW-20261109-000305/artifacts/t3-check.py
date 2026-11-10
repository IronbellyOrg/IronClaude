"""Offline checks for the capture sheet; never execute documented commands."""
from pathlib import Path
import json
import re
import shlex
import subprocess

from superclaude.cli.issue_watch import github, launch

PACKAGE = Path(__file__).resolve().parent.parent
START = "03e5816196f4b9ac896c1f0d644304966686cd21"
FILE = "docs/designs/issue-watcher-setup.md"
text = Path(FILE).read_text()
before = subprocess.check_output(["git", "show", f"{START}:{FILE}"], text=True)
section = text.split("#### 14.1.1 Capture sheet\n", 1)[1].split("### 14.2", 1)[0]
rows = [line for line in section.splitlines() if line.startswith("| `")]
fixtures = sorted(Path("tests/issue_watch/fixtures/_assumed_shape").glob("*.json"))
assert len(rows) == len(fixtures) == 19
by_name = {row.split("`")[1]: row for row in rows}
assert set(by_name) == {path.name for path in fixtures}
replacements = {
    "<test issue>": "1", "<page>": "1", "<owner login>": "test-login",
    "<trigger label>": "trigger-label", "<worktree>": "/test/worktree",
    "<orca>": "/test/orca",
    **{f"<{name}>": getattr(github, name) for name in (
        "EDITS_QUERY", "PROJECT_ITEMS_QUERY", "EVENTS_JQ", "MARKER_JQ", "REREAD_JQ"
    )},
}
expected = {
    "gh_issue_list.json": ("github.argv_discover", github.argv_discover("trigger-label", "test-login")),
    "gh_issue_reread.json": ("github.argv_reread", github.argv_reread(1)),
    "rest_events_page.json": ("github.argv_events", github.argv_events(1, 1)),
    "rest_comments_marker.json": ("github.argv_comments", github.argv_comments(1, 1)),
    "graphql_edits.json": ("github.argv_edits", github.argv_edits(1)),
    "gh_stderr_http_502.json": ("github.argv_events", github.argv_events(1, 1)),
}
for path in fixtures:
    row = by_name[path.name]
    result = subprocess.run(["grep", "-c", "-F", path.name], input=section, text=True, capture_output=True)
    assert result.returncode == 0 and result.stdout.strip() == "1", path.name
    command = next(code for code in re.findall(r"`([^`]+)`", row.split("|")[3]) if code.startswith(("gh ", "<orca> ")))
    argv = shlex.split(command)
    for i, token in enumerate(argv):
        for placeholder, value in replacements.items():
            token = token.replace(placeholder, value)
        argv[i] = token
    builder, want = expected.get(path.name, ("github.argv_user", github.argv_user()))
    if path.name.startswith("orca_"):
        builder, want = "launch.launch_argv", launch.launch_argv("/test/orca", "/test/worktree", launch.build_claim_prompt(1))
    elif path.name in ("graphql_project_items.json", "gh_graphql_rate_limited.json", "gh_graphql_insufficient_scopes.json", "gh_stderr_scope_read_project.json"):
        builder, want = "github.argv_project_items", github.argv_project_items(1)
    assert argv == want, (path.name, argv, want)
    data = json.loads(path.read_text())
    print(f"{path.name}: grep_count=1 builder={builder} argv=PASS")
    print("  fixture meaning source=" + data["source"] + " note=" + data.get("note", "(absent)"))
    assert "<test issue>" in command or command == "gh api user --include" or path.name == "gh_issue_list.json"
    assert not re.search(r"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_", row)
original_section = before.split("### 14.1 The live test", 1)[1].split("### 14.2", 1)[0]
for line in original_section.splitlines():
    if line.startswith(("- ", "You commit the record")):
        assert line in text.splitlines(), line
insertion = text.split("#### 14.1.1 Capture sheet", 1)[1].split("You commit the record", 1)[0]
assert text.replace("#### 14.1.1 Capture sheet" + insertion, "", 1) == before
assert "placeholder values of the same type" in section
assert "List every fixture that was not captured" in section
print("19 fixture rows, 19 builder argv comparisons, placeholder-only variable arguments: PASS")
print("Original four bullets and following paragraph byte-identical; all other text unchanged: PASS")
print("$ git diff " + START + " -- " + FILE)
print(subprocess.check_output(["git", "diff", START, "--", FILE], text=True))
