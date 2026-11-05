"""Write the four self-test prompts for prompt-check.py into this folder.

Run from the repository root:
    PYTHONDONTWRITEBYTECODE=1 uv run python -I <this file>
"""

from __future__ import annotations

from pathlib import Path

HERE = Path(".dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts")
QA = Path("src/superclaude/skills/sc-implement-protocol/refs/qa.md")
T1 = Path(".dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T1/prompt-1-1.md")
SHA = "0123456789abcdef0123456789abcdef01234567"


def template() -> list[str]:
    lines = QA.read_text(encoding="utf-8").splitlines()
    h = lines.index("## Subagent prompt (when not inline)")
    f = [i for i in range(h + 1, len(lines)) if lines[i].startswith("```")]
    return lines[f[0] + 1 : f[1]]


SLOTS = {
    "{task_brief}": "T1 (AC ids: T1.AC1)\n## Task 1: synthetic\n\nAcceptance criteria:\n- synthetic",
    "{global_constraints}": "(synthetic)\n- a synthetic constraint",
    "{start_sha}": SHA,
    "{diff}": "(synthetic diff)\n+added line\n\n+another added line",
    "{delta_diff}": "",
    "{prior_findings}": "",
    "{recheck_list}": "",
}


def exact() -> str:
    out: list[str] = []
    for line in template():
        for key, value in SLOTS.items():
            if key in line:
                line = line.replace(key, value)
        out.append(line)
    return SHA + "\n" + "\n".join(out) + "\n"


def main() -> None:
    body = exact()
    (HERE / "selftest-1-exact.md").write_text(body, encoding="utf-8")

    closing = "Do not trust the implementer's report."
    lines = body.split("\n")
    i = lines.index(closing)
    assert lines[i - 1] == ""
    (HERE / "selftest-2-blank-line-removed.md").write_text("\n".join(lines[: i - 1] + lines[i:]), encoding="utf-8")

    t1 = T1.read_text(encoding="utf-8")
    old = "Anchor rule: cite exactly one anchor per yes."
    assert t1.count(old) == 1
    (HERE / "selftest-3-changed-line.md").write_text(t1.replace(old, "Anchor rule: cite one anchor per yes."), encoding="utf-8")

    rest = t1.split("\n", 1)[1]
    (HERE / "selftest-4-no-sha-line.md").write_text("this is not a start sha\n" + rest, encoding="utf-8")


if __name__ == "__main__":
    main()
