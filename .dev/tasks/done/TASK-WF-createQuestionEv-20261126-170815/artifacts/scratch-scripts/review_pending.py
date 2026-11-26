"""Between runs: read every unattributed fork item (GET only) and clear the pending hold when none relates to the run.

Usage: review_pending.py <run name>. Prints each item with its first words; exit 0 = cleared, 1 = a keyword hit (matrix stays held).
The orchestrator reads the printed list afterwards (the cleared log is /tmp/createQuestionEv-scratch/pending-cleared.log).
"""

import json
import subprocess
import sys
from pathlib import Path

SC = Path("/tmp/createQuestionEv-scratch")
PENDING = SC / "PENDING-REVIEW"
FORK = "IronbellyOrg/IronClaude"
KEYWORDS = ["superclaude install", "create_issue", "issue_logger", "keep my wording", "qev-", "synthetic run marker",
            "how many skills it copied", "990001", "sc:issue --create` crashes"]
GH = subprocess.run(["bash", "-lc", "command -v gh"], capture_output=True, text=True).stdout.strip() or "/home/coder/.local/bin/gh"


def get(path: str) -> dict:
    done = subprocess.run([GH, "api", path], capture_output=True, text=True, timeout=60)
    return json.loads(done.stdout) if done.returncode == 0 else {}


if not PENDING.exists():
    print("nothing pending")
    sys.exit(0)
data = json.loads(PENDING.read_text())
hits, lines = [], []
for item in data.get("unattributed", []):
    if item["kind"] == "issue":
        full = get(f"repos/{FORK}/issues/{item['number']}")
        text = (full.get("title") or "") + "\n" + (full.get("body") or "")
        label = f"issue {item['number']} by {item.get('author')} ({item['created_at']}): {(full.get('title') or '')[:70]}"
    elif item["kind"] == "comment":
        full = get(f"repos/{FORK}/issues/comments/{item['id']}")
        text = full.get("body") or ""
        label = f"comment {item['id']} by {item.get('author')} ({item['created_at']}): {(text.strip().splitlines() or [''])[0][:70]}"
    else:
        text, label = item.get("name", ""), f"branch {item.get('name')}"
    found = [k for k in KEYWORDS if k.lower() in text.lower()]
    lines.append(label + (f"  KEYWORD HIT {found}" if found else ""))
    if found:
        hits.append(label)
print("\n".join(lines))
if hits:
    print("HELD: an unattributed item matches the run; the orchestrator must read it")
    sys.exit(1)
note = f"after run {data.get('run')}: no unattributed item matches the run's keywords or marker; items: " + " | ".join(lines)
done = subprocess.run(
    ["uv", "run", "--no-project", "python",
     "/home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/harness/run_create.py",
     "clear-pending", "--note", note[:3000]], capture_output=True, text=True)
print("cleared" if done.returncode == 0 else "clear failed: " + done.stderr)
sys.exit(done.returncode)
