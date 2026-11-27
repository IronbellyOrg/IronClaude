import contextlib
import io
import re
import subprocess
import sys

import pytest
from harness import events, gate, loader, runner, scorer

EXP = loader.EXPERIMENT
REPO = EXP.parents[2]
README = (EXP / "README.md").read_text(encoding="utf-8")
PROCEDURE = (EXP / "table" / "table-procedure.md").read_text(encoding="utf-8")
SCRIPTS = {"gate": gate, "events": events, "runner": runner, "scorer": scorer}
READING = "owner-input --evidence .dev/research/jev-vs-keyword-table-611/questions.py"


def subcommands(module):
    """The subcommand names, read from the module's own argument parser through its ``--help`` output."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out), pytest.raises(SystemExit):
        module.main(["--help"])
    found = re.search(r"\{([a-z0-9,-]+)\}", out.getvalue())
    assert found, f"{module.__name__} shows no subcommand list"
    return found.group(1).split(",")


def order_of_work():
    section = README.split("## Order of work")[1].split("## How to rescore")[0]
    return re.split(r"(?m)^(?=\d+\. )", section)[1:]


@pytest.mark.parametrize("script", sorted(SCRIPTS))
def test_every_subcommand_is_named_in_the_readme_next_to_its_script(script):
    names = subcommands(SCRIPTS[script])
    assert names
    for sub in names:
        assert f"{script}.py {sub}" in README, f"{script}.py {sub} is not in the README"


def test_the_readme_has_the_exact_test_command():
    assert "uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests -v" in README


def test_the_live_run_steps_are_in_the_order_the_story_names():
    expected = ["decision-rule.md", READING, "gate.py freeze-corpus", "gate.py gate1", "gate.py freeze-table",
                "owner-input --evidence .dev/research/jev-vs-keyword-table-611/decision-rule.md", "gate.py freeze-rule",
                "events.py price", "gate.py record-tests", "events.py go", "gate.py gate2", "runner.py rehearse", "runner.py run",
                "scorer.py score"]
    steps = order_of_work()
    assert len(steps) == len(expected)
    for number, (step, token) in enumerate(zip(steps, expected), 1):
        assert token in step, f"step {number} does not hold {token}"
    assert "keyscan.py" in steps[12]


def test_the_reading_step_comes_right_before_freeze_corpus_in_the_readme_and_the_procedure():
    steps = order_of_work()
    assert READING in steps[1] and "six definitions" in steps[1] and "immediately before `gate.py freeze-corpus`" in steps[1]
    assert "gate.py freeze-corpus" in steps[2] and READING not in steps[2]
    assert "Reading step, before `gate.py freeze-corpus`" in PROCEDURE and READING in PROCEDURE
    assert PROCEDURE.index("Reading step") < PROCEDURE.index("Gate 1 first")


def test_the_keyscan_step_maps_the_key_inside_the_same_single_subshell_command():
    block = next(b for b in re.findall(r"```bash\n(.*?)```", README, re.S) if "keyscan.py" in b)
    assert block.count("bash -c") == 1 and 'export JEV_API_KEY="$TYPESAFE_API_KEY"' in block
    assert block.index("bash -c") < block.index("export JEV_API_KEY") < block.index("keyscan.py")
    assert not re.search(r"JEV_API_KEY=[^\"$ ]", README)


def test_the_readme_has_the_rescore_section_the_delivery_status_and_every_open_item():
    assert "## How to rescore" in README and "scorer.py score --run-id ID --rescore NAME --rule PATH" in README
    status = README.split("## Delivery status")[1]
    assert "`Refs #611`" in status
    for part in ("B.", "C.", "D.", "E."):
        assert re.search(rf"\| {re.escape(part)} .*\| No, left", status), part
    for item in ("noul_low_operator", "noul_high_operator", "unresolved_failure_invalid_count", "Who labels", "Who applies the table",
                 "JEV_API_URL", "jev-litellm-gateway-operational-guide.md", "price to re-confirm", "Where the prompts come from"):
        assert item in README, item
    assert "never calls the live API" in README


def test_the_procedure_quotes_the_table_exactly_as_the_skill_file_has_it():
    skill = (REPO / "src" / "superclaude" / "skills" / "sc-troubleshoot-protocol" / "SKILL.md").read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(skill) if line.startswith("   - Stack trace, exception name"))
    quoted = "\n".join(skill[start:start + 7])                     # the six cue rows and the ambiguity rule
    assert skill[start + 6].lstrip().startswith("- On ambiguity")
    assert quoted in PROCEDURE


@pytest.mark.parametrize("script", sorted(SCRIPTS))
def test_each_command_line_module_starts_as_a_script_from_an_unrelated_folder(script, tmp_path):
    path = EXP / "harness" / f"{script}.py"
    res = subprocess.run([sys.executable, "-I", str(path), "--help"], cwd=tmp_path, capture_output=True, text=True,
                         env={"PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1"})
    assert res.returncode == 0 and "usage:" in res.stdout, res.stderr


def test_no_readme_or_template_holds_a_vendor_url_or_a_key_shaped_string():
    for f in [EXP / "README.md", *sorted((EXP / "table").glob("*.md")), *sorted((EXP / "corpus").glob("*.md"))]:
        t = f.read_text(encoding="utf-8")
        assert "api.typesafe.ai" not in t and "sk-" not in t, f
        prose = re.sub(r"`[^`]*`", " ", re.sub(r"```.*?```", " ", t, flags=re.S))      # a long word outside code spans looks like a key
        assert not re.search(r"\b[A-Za-z0-9_-]{32,}\b", prose), f
