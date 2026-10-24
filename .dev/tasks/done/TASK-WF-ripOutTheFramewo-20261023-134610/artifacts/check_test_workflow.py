"""Check the approved upload-only deletion against the recorded starting commit."""

import subprocess
from pathlib import Path

import yaml

root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
baseline_file = Path(__file__).resolve().parent / "t1-baseline.txt"
baseline = baseline_file.read_text().splitlines()[0].removeprefix("head=")
assert len(baseline) == 40 and all(c in "0123456789abcdef" for c in baseline)


def at_baseline(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{baseline}:{path}"], cwd=root)


upload_step = b"""      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
          token: ${{ secrets.CODECOV_TOKEN }}
          flags: unittests
          name: codecov-umbrella
          fail_ci_if_error: false

"""
path = ".github/workflows/test.yml"
original = at_baseline(path)
current = (root / path).read_bytes()
assert original.count(upload_step) == 1, "Starting workflow upload step changed"
assert current == original.replace(upload_step, b"", 1), "Unexpected workflow changes"
assert b"codecov" not in current.lower(), "Upload references remain"
print("PASS: workflow differs only by the complete approved upload-step deletion")

before = yaml.safe_load(original)
after = yaml.safe_load(current)
steps = before["jobs"]["test"]["steps"]
steps[:] = [step for step in steps if step.get("name") != "Upload coverage to Codecov"]
assert before == after, "Unrelated YAML settings changed"
coverage = [step for step in after["jobs"]["test"]["steps"] if step.get("name") == "Run tests with coverage"]
assert len(coverage) == 1, "Coverage step is missing or duplicated"
assert coverage[0]["run"] == "pytest -v --tb=short --color=yes --cov=superclaude --cov-report=xml --cov-report=term\n"
print("PASS: YAML parses; coverage step, XML and terminal reports, jobs and settings preserved")

for protected in ("pyproject.toml", "src/superclaude/templates/documents/readme_template.md"):
    assert (root / protected).read_bytes() == at_baseline(protected), protected
    print(f"PASS: unchanged {protected}")
