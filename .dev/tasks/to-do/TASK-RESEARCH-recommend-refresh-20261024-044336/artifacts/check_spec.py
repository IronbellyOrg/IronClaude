"""Check research completeness and reference integrity, not recommendation behavior.

Run from this worktree with: uv run python <package>/artifacts/check_spec.py
The acceptance tests described by the specification remain proposed.
"""
import hashlib
import json
import re
import subprocess
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[3]
SPEC = PACKAGE / "SPEC-sc-recommend-refresh.md"


def main():
    inventory = json.loads((PACKAGE / "inventory.json").read_text())
    spec = SPEC.read_text()
    expected = set(inventory["commands"])
    history = subprocess.check_output(
        [
            "git", "log", f"--since={inventory['window_start']}",
            f"--until={inventory['window_end']}", "--format=", "--name-only",
            "--", "src/superclaude/commands/",
        ], cwd=ROOT, text=True,
    )
    selected = {
        Path(path).stem for path in history.splitlines()
        if path.endswith(".md") and Path(path).name != "README.md"
    }
    assert selected == expected, (selected - expected, expected - selected)
    assert len(expected) == 47
    report_names = {path.stem for path in (PACKAGE / "analyses").glob("*.md")}
    assert report_names == expected
    for name in sorted(expected):
        text = (PACKAGE / "analyses" / f"{name}.md").read_text()
        for heading in ("Findings", "Gaps", "Key Takeaways"):
            assert f"## {heading}" in text, (name, heading)
        assert "{{RF_PLACEHOLDER:" not in text, name
    active = {name for name in expected if (ROOT / "src/superclaude/commands" / f"{name}.md").is_file()}
    assert len(active) == 43
    assert expected - active == set(inventory["retired_commands"])
    appendix = spec.split("## Appendix C:", 1)[1].split("## Appendix D:", 1)[0]
    rows = [line for line in appendix.splitlines() if line.startswith("| ") and line.split("|")[1].strip() in expected]
    names = [line.split("|")[1].strip() for line in rows]
    assert len(names) == len(set(names)) == 47
    assert set(names) == expected
    definitions = re.findall(r"^\| ([TS]\d{2}) \|", spec, re.M)
    assert len(definitions) == len(set(definitions)), "Duplicate case definition"
    expected_cases = {f"T{i:02}" for i in range(1, 77)} | {f"S{i:02}" for i in range(1, 30)}
    assert set(definitions) == expected_cases
    for row in rows:
        refs = re.findall(r"\b[TS]\d{2}\b", row)
        assert refs and set(refs) <= expected_cases, row
    required_cases = {
        "help": {"S01"}, "design": {"S02"}, "tdd": {"S03"},
        "cleanup-audit": {"S04"}, "improve": {"S05"},
        "auggie-review": {"S06"}, "review-translation": {"S07"},
        "init-lite": {"S08"}, "cli-eval": {"S09", "S10"},
        "cli-portify": {"S11"}, "release-split": {"S12"},
        "post-release": {"S13"}, "roadmap": {"S14"},
        "tasklist": {"S15"}, "validate-roadmap": {"S16"},
        "validate-tests": {"S17"}, "swarm-wizard": {"S21"},
    }
    by_name = dict(zip(names, rows))
    for name, cases in required_cases.items():
        assert cases <= set(re.findall(r"\bS\d{2}\b", by_name[name])), name
    for token in ("{{RF_PLACEHOLDER:", "{{SC_PLACEHOLDER:", "<!-- TODO -->"):
        assert token not in spec
    assert "status: scaffold" not in spec
    for target in re.findall(r"\]\(([^)]+)\)", spec):
        if target.startswith(("https:", "http:", "#")):
            continue
        path = Path(target.split("#", 1)[0])
        assert (path if path.is_absolute() else PACKAGE / path).exists(), target
    implementation_diff = subprocess.check_output(
        ["git", "diff", "HEAD", "--name-only", "--", "src", "plugins", "tests"],
        cwd=ROOT, text=True,
    )
    assert not implementation_diff.strip(), implementation_diff
    result = {
        "check": "research-artifact-integrity",
        "result": "PASS",
        "historical_commands": len(selected), "analyst_reports": len(report_names),
        "coverage_rows": len(rows), "active_commands": len(active),
        "retired_commands": len(expected - active),
        "contract_cases_defined": 76, "behavioral_cases_defined": 29,
        "implementation_files_changed": 0,
        "spec_sha256": hashlib.sha256(spec.encode()).hexdigest(),
        "limitation": "Structural integrity only. Does not execute proposed recommendation cases or verify all semantic claims.",
    }
    output = PACKAGE / "artifacts/spec-validation.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
