"""Hook-update tests (spec FR-7.1).

T-701 a successful `gh pr create` → hook stdout contains BOTH `/sc:auggie-review`
AND `/sc:pr-submit --monitor`; T-702 a non-matching command → exit 0; T-703 a failed
`gh pr create` (tool_response.error non-empty) → exit 0. The hook is resolved under
the `src/` source-of-truth (NEVER `.claude/`).
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HOOK = REPO_ROOT / "src" / "superclaude" / "hooks" / "scripts" / "offer-pr-review.sh"


def _run_hook(payload: dict) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(HOOK)],
        input=json.dumps(payload).encode(),
        capture_output=True,
        timeout=5,
    )
