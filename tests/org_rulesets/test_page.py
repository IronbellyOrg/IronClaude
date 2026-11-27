"""The operator page docs/developer-guide/branch-protection-multi-repo.md."""

from __future__ import annotations

import re
import shlex
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "docs" / "developer-guide" / "branch-protection-multi-repo.md"
SUMMARY = ROOT / ".dev" / "issues" / "838" / "issue-summary.md"


@pytest.fixture(scope="module")
def page():
    return PAGE.read_text(encoding="utf-8")


def test_the_page_defines_the_variables(page):
    assert re.search(r"^OWNER=", page, re.M) and re.search(r"^REPO=", page, re.M)
    assert re.search(r"^OUT=", page, re.M)


def test_every_gh_api_command_uses_the_variables_or_a_placeholder(page):
    commands = [ln for ln in page.splitlines() if "gh api" in ln]
    assert len(commands) >= 5
    for line in commands:
        assert "$OWNER" in line or "<org>" in line, line
        if "repos/" in line:
            assert "$REPO" in line or "<repo>" in line, line


def test_the_page_says_what_the_operator_needs(page):
    lowered = page.lower()
    for needle in (
        "--apply",
        "--confirm",
        "dry run",
        "-before.json",
        "90-day",
        "blocks moving and deleting",
        "canary",
        "exit status",
        'never "0"',
    ):
        assert needle in lowered, needle


def test_the_canary_must_show_complete_activity_coverage(page):
    flat = " ".join(page.split())
    assert "complete activity coverage before other repos rely on it" in flat


def test_the_script_commands_on_the_page_parse(orr, page):
    """Every command line that runs the script uses real options."""
    lines = [ln.strip() for ln in page.splitlines() if "apply_org_rulesets.py" in ln]
    commands = [ln for ln in lines if ln.startswith("uv run python scripts/")]
    assert len(commands) == 2
    values = {"$OWNER": "acme", "$REPO": "acme-one", "$OUT": "/tmp/out"}
    for line in commands:
        words = shlex.split(line)[4:]
        words = [values.get(w, w) for w in words]
        words = ["0" * 64 if w == "<digest>" else w for w in words]
        args = orr.parse_args(words)
        assert (args.org, args.repo) == ("acme", "acme-one")


def script_messages(orr):
    """The refusal, failure and usage texts of the script, as written in its source."""
    source = Path(orr.__file__).read_text(encoding="utf-8")
    found = re.findall(
        r'(?:problems\.append|stop|fail|UsageError)\(\s*f?"([^"]+)"', source
    )
    found += re.findall(r'return None, f"([^"]+)"', source)
    found += list(orr._REFUSAL_TEXT.values())
    return found


def test_every_refusal_and_failure_text_of_the_script_is_on_the_page(orr, page):
    flat = " ".join(page.split())
    messages = script_messages(orr)
    assert len(messages) >= 20
    for message in messages:
        parts = re.split(r"\{[^}]*\}", message.strip())
        pattern = ".+?".join(re.escape(part) for part in parts)
        assert re.search(pattern, flat), message


def test_the_fixed_output_lines_of_the_script_are_on_the_page(page):
    flat = " ".join(page.split())
    for text in (
        "no plan: the repo could not be planned",
        "would refuse --apply:",
        "refused:",
        "failed:",
        "usage error:",
        "skipped, already present:",
        "before state saved:",
        "created:",
        "comment for issue 838",
        "rollback by hand",
    ):
        assert text in flat, text


def test_every_text_quoted_in_the_message_lists_is_in_the_script(orr, page):
    """The other direction: the first span of each table row and bullet between
    'Refusals and failures' and 'Roll back by hand' is a script string once the
    placeholders in angle brackets are cut out."""
    start = page.index("## Refusals and failures")
    end = page.index("## Roll back by hand")
    source = Path(orr.__file__).read_text(encoding="utf-8")
    spans = []
    for line in page[start:end].splitlines():
        found = re.match(r"^(?:\| |- )`([^`]+)`", line)
        if found and found.group(1) != "Text":
            spans.append(found.group(1))
    assert len(spans) >= 20
    for span in spans:
        for piece in re.split(r"<[^>]*>", span):
            piece = piece.strip()
            if len(piece) > 2:
                assert piece in source, (
                    f"{piece!r} (from {span!r}) is not in the script"
                )


def private_repo_names():
    text = SUMMARY.read_text(encoding="utf-8")
    start = text.index("Clay's answer for this story")
    found = re.search(r"all with Clay admin: (.+?)\. That list", text[start:])
    return [name.strip() for name in found.group(1).split(",")]


@pytest.mark.skipif(
    not SUMMARY.exists(), reason="the untracked issue summary is absent"
)
def test_no_real_private_repo_name_is_written_in_a_tracked_file():
    names = private_repo_names()
    assert len(names) == 17
    files = [PAGE, ROOT / "scripts" / "apply_org_rulesets.py"]
    files += sorted(
        p for p in (ROOT / "tests" / "org_rulesets").iterdir() if p.is_file()
    )
    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for name in names:
            assert name.lower() not in text, f"{name} in {path.name}"


GUIDE = ROOT / "docs" / "developer-guide" / "branch-protection.md"
INDEX = ROOT / "docs" / "developer-guide" / "documentation-index.md"
LINK = "(branch-protection-multi-repo.md)"


def test_the_guide_links_to_the_page_once_and_keeps_its_commands():
    text = GUIDE.read_text(encoding="utf-8")
    assert text.count("branch-protection-multi-repo.md") == 1
    assert f"[Branch Protection for Other Repos]{LINK}" in text
    for fragment in (
        "gh api --method POST repos/",
        "/rulesets --input .github/rulesets/protect-release-tags.json",
        "/rules/branches/master --jq '.[].type'",
        "/rulesets/<id> -f enforcement=disabled",
        "gh api --method DELETE repos/",
    ):
        assert fragment in text, fragment


def test_the_index_links_to_the_page_twice_and_keeps_its_entries():
    text = INDEX.read_text(encoding="utf-8")
    assert text.count("branch-protection-multi-repo.md") == 2
    assert text.count(f"[Branch Protection for Other Repos]{LINK}") == 2
    assert "### 🔒 [Branch Protection](branch-protection.md)" in text
    assert (
        "- [Branch Protection](branch-protection.md) - Rulesets for `master`, "
        "`integration` and `v*` tags; apply, check, break glass"
    ) in text
