"""Wave 1C evidence: simulate Task 1 in memory and test the plan's acceptance checks.

Read-only on the repo. Prints facts only; writes nothing.
Run: uv run python edit_simulation.py
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path

REPO = Path("/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel")
SPEC = REPO / ".dev/tasks/to-do/TASK-WF-stage3CRequest-20261119-143901/source.md"
AGENT = REPO / "src/superclaude/agents/reflect-reviewer.md"
VARIANT = REPO / ".dev/stage3c-variants/brainstorm/reflect-reviewer.md"
TESTMOD = REPO / "tests/skills/test_review_severity_rule.py"

ANCHOR = "a HIGH that is only wording is a Note."
NEXT = " When no consumer can be established"


def grep_c(text: str, pattern: str) -> int:
    """grep -c with a BRE pattern that has no BRE specials except '.' (any char)."""
    rx = re.compile(re.escape(pattern).replace(r"\.", "."))
    return sum(1 for line in text.splitlines() if rx.search(line))


spec_lines = SPEC.read_text(encoding="utf-8").splitlines()
fence = [i for i, l in enumerate(spec_lines) if l.startswith("```")]
passage = "\n".join(spec_lines[fence[0] + 1 : fence[1]])
print("fenced block lines:", fence[0] + 1, "-", fence[1] + 1, "| passage lines:", passage.count("\n") + 1)

agent = AGENT.read_text(encoding="utf-8")
print("agent anchor+next occurrences:", agent.count(ANCHOR + NEXT))
edited = agent.replace(ANCHOR + NEXT, ANCHOR + " " + passage + NEXT, 1)

variant_bytes = VARIANT.read_bytes()
print("variant sha256:", hashlib.sha256(variant_bytes).hexdigest())
print("simulated edit == variant bytes:", edited.encode("utf-8") == variant_bytes)

a_lines, e_lines = agent.splitlines(), edited.splitlines()
changed = [i + 1 for i, (x, y) in enumerate(zip(a_lines, e_lines)) if x != y]
print("line count before/after:", len(a_lines), len(e_lines), "| changed lines:", changed)

for pat in (
    "Before you write `Medium:`",
    "A behaviour that would happen anyway (for example exit 0 on success) is not that.",
    "a HIGH that is only wording is a Note. Before you write",
):
    print(f"grep -c before={grep_c(agent, pat)} after={grep_c(edited, pat)} :: {pat}")

# Load the test module (constants and pure helpers only; no git calls).
spec_ = importlib.util.spec_from_file_location("trs", TESTMOD)
trs = importlib.util.module_from_spec(spec_)
spec_.loader.exec_module(trs)

flat = trs._flat(edited)
for needle in (
    "Before you write `Medium:`, ask whether someone following the text as written could produce behaviour the spec forbids",
    "A behaviour that would happen anyway (for example exit 0 on success) is not that.",
):
    print("needle in edited:", trs._flat(needle) in flat, "| in current:", trs._flat(needle) in trs._flat(agent))

print("banned severity phrases in passage:", trs._phrase_hits(passage, trs.BANNED_SEVERITY_PHRASES))
print("banned severity phrases in edited agent:", trs._scan_phrases({"agent": edited}, trs.BANNED_SEVERITY_PHRASES))
print("sweep hits on edited line 122:", trs._sweep_hits(e_lines[121]))
print("zero-tolerance unqualified on line 122:", trs._zero_tolerance_unqualified(e_lines[121]))
print("cap regression on line 122:", bool(trs.CAP_REGRESSION.search(e_lines[121])))
s1, s2, s3, _s4, _s5 = trs.canonical_rule_bullets()
print("S1-S3 still present in edited agent:", all(trs._rule_body(b) in flat for b in (s1, s2, s3)))
print("(S[1-5]) label in edited agent:", bool(re.search(r"\(S[1-5]\)", edited)))
print("'Before you write' lines in current agent:", grep_c(agent, "Before you write"))
