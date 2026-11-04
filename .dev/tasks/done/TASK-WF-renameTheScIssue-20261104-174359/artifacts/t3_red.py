"""Run the new T3 checks on the pre-fix copies; exit 1 when they flag the old text."""

import importlib.util
import sys
from pathlib import Path

root, pre = Path(sys.argv[1]), Path(sys.argv[2])
spec = importlib.util.spec_from_file_location(
    "issue_worker_tests", root / "tests/skills/test_issue_worker_agents.py"
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

flagged = 0
for path in sorted(pre.glob("*.md")):
    text = path.read_text(encoding="utf-8")
    blocked = mod.blocked_names(text)
    refs = mod.old_summary_refs(text)
    flagged += bool(blocked or refs)
    print(f"{path.name}: blocked_names={blocked} old_summary_refs={refs}")

agent = (pre / "issue-worker-t1.md").read_text(encoding="utf-8")
skill = (pre / "SKILL.md").read_text(encoding="utf-8")
print("old paragraph literal byte-present in pre issue-worker-t1.md:",
      mod._OLD_TOOL_INPUT_PARAGRAPH in agent)
print("old Wave 4 literal byte-present in pre SKILL.md:", mod._OLD_WAVE_4_LINE in skill)
print(f"pre-fix files flagged: {flagged}")
sys.exit(1 if flagged else 0)
