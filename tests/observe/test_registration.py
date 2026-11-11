"""``superclaude observe`` is registered in the shipped CLI (AD-2; release-gates.md reading 1)."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

from click.testing import CliRunner

from superclaude.cli.main import main
from superclaude.cli.observe.commands import observe_group


def test_the_group_lists_observe_among_its_commands():
    assert main.commands["observe"] is observe_group
    result = CliRunner().invoke(main, ["--help"])
    assert result.exit_code == 0
    assert re.search(r"^\s+observe\s", result.output, re.M)


def test_observe_help_lists_every_option():
    result = CliRunner().invoke(main, ["observe", "--help"])
    assert result.exit_code == 0
    for option in ("--once", "--width", "--ascii", "--fixture", "--run", "--snapshot"):
        assert option in result.output


def test_once_fixture_base_prints_a_record_with_the_synthetic_banner_first():
    result = CliRunner().invoke(main, ["observe", "--once", "--fixture", "base"])
    assert result.exit_code == 0
    first = result.output.splitlines()[0]
    assert "SYNTHETIC FIXTURE base, not Orca data" in first
    assert "\x1b" not in result.output


def test_main_py_registers_observe_with_one_deferred_block_in_the_house_form():
    spec = importlib.util.find_spec(
        "superclaude.cli.main"
    )  # the package attribute `main` is the group
    text = Path(spec.origin).read_text(encoding="utf-8")
    block = (
        "from superclaude.cli.observe.commands import observe_group  # noqa: E402,I001  "
        "# intentional: deferred subcommand registration to avoid circular imports\n"
        "\n"
        'main.add_command(observe_group, name="observe")\n'
    )
    assert text.count(block) == 1
    assert text.index(block) < text.index('if __name__ == "__main__":')
