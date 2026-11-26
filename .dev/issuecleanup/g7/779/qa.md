VERDICT: PASS

# QA of findings.md for issue 779

Checked against live sources on 2026-11-25.

## Blocking defects
None.

## What I verified
- Issue 779 (gh issue view --json): OPEN, label `bug`, 0 comments, created 2026-11-24T19:13:58Z. The body says the frame source "was NOT found", Related Issues "None found", severity medium, and Steps 1-9 as quoted (Step 9 adds a flag in `runtime.sh`). Verdict "still-relevant" holds.
- `/opt/aidev/orca/runtime.mjs`: `serveEnv` is lines 61-83 and sets no Chromium/Electron variable. The `spawn(binary, ['serve','--bind','127.0.0.1','--port','6768','--pairing-address',base,'--json'])` call is at lines 667-668. Both are accurate. The `.mjs` is 700 lines.
- `/opt/aidev/orca/runtime.sh` is root-owned and only takes a lock, builds a clean env and runs `runtime.mjs`. The "no flag hook exists, so Step 9 is a new change outside this repo" claim holds.
- Grep of the repo for `runtime.sh`, excluding `.dev/` and `.git`: no hits. Confirmed.
- `gh issue list` and `gh pr list` searches (orca CPU idle, Xvfb, compositing, gpu-process): only 779 itself plus unrelated 765, 323 and 764. Related PRs "None found" holds. 757 and 766 exist and are open, and the findings hedge them as search-only relations.
- All seven headings are present in the required order (lines 5, 16, 20, 24, 32, 36, 40). No placeholders or TODO/TBD.
- Complexity (complex), size (M), priority (P2), the next steps and the dependencies are consistent with the issue text and the verified facts. The restart safety note (use `runtime.sh stop` and `start`) matches the issue.

## Notes (non-blocking)
- findings.md says `runtime.sh` is "63 lines". `wc -l` gives 49 lines, so the figure is wrong. It does not affect any conclusion. The analyze report has the same error.
- I could not re-run the 3 s `top` sample (4.3% CPU), and the process-list facts are point-in-time. Both are stated as observations and marked UNVERIFIED in the findings, which is acceptable.
