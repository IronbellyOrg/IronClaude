"""T19 menu equality — surviving identities and value coverage, not token counts."""

from pathlib import Path

import pytest

from tests.troubleshoot._procedures import (
    enumerate_producers,
    menu_equal,
    write_producers_md,
)


@pytest.mark.parametrize(
    "change,expected",
    [
        ("full", True),
        ("wrong-id", False),
        ("wrong-file", False),
        ("missing-shared-value", False),
        ("missing-value", False),
        ("excluded-omitted", True),
        ("excluded-restored", False),
        ("missing-id", False),
        ("malformed", False),
        ("tokens-only", False),
    ],
)
def test_menu_equality(change: str, expected: bool, tmp_path: Path) -> None:
    p = enumerate_producers(
        {
            "io.sh": "rc=runner-unavailable\nrc=runner-unavailable\nrc=DEAD_LETTER\nrc=excluded"
        },
        "runner-unavailable",
        "rc",
    )
    p.rows[-1]["surviving"] = "no"
    md = write_producers_md(p, tmp_path / "producers.md")
    prompt = md
    if change == "wrong-id":
        prompt = md.replace("| P1 |", "| P99 |")
    elif change == "wrong-file":
        prompt = md.replace("io.sh:1", "other.sh:1")
    elif change in {"missing-shared-value", "excluded-omitted"}:
        identity = "P2" if change == "missing-shared-value" else "P4"
        prompt = "\n".join(
            line for line in md.splitlines() if not line.startswith(f"| {identity} |")
        )
    elif change == "missing-value":
        prompt = md.replace("rc=DEAD_LETTER", "rc=OTHER")
    elif change == "excluded-restored":
        prompt = md.replace("| no |", "| yes |")
    elif change == "missing-id":
        prompt = md.replace("| P1 |", "| |")
    elif change == "malformed":
        prompt = md.replace("| P1 |", "| P1 | extra |")
    elif change == "tokens-only":
        prompt = "`one-x` `two-x` `three-x`"
    assert menu_equal(prompt, md) is expected


@pytest.mark.parametrize(
    "md",
    [
        "",
        "## Producers\n",
        "| id | line | statement | surviving |\n|---|---|---|---|",
        "| id | line | statement | surviving |\n|---|---|---|---|\n| P1 | bad:0 | rc=OK | yes |",
    ],
)
def test_missing_or_malformed_menus_do_not_pass(md: str) -> None:
    assert not menu_equal(md, md)
