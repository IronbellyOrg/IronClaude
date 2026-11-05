# Wave 1.5 Branch B (architectural-doc lookup) — returned by troubleshoot-analyst, currency finalized by parent

```json
[
  {
    "doc_path": "/home/coder/workspaces/IronClaude/.dev/worktrees/ccsession-proxy-stall/src/superclaude/skills/ccsession-tag/README.md",
    "summary": "Only doc that describes the shim lifecycle. ccsession starts the shim (README.md:503-504); one shim is shared by every session on its port and is meant to outlive the session that started it: 'a shim still used by older sessions keeps running until you stop it' (README.md:416-418) and 'ccsession never stops a running shim by itself, because other sessions may be using it' (README.md:504-505). Stopping is manual (README.md:481-502). No log location is documented; the restart recipe discards output (README.md:494-495). It promises no time limit once a model starts answering (README.md:332-335).",
    "currency_verdict": "current",
    "reason": "no header markers; parent-collected mtime: doc and code are in the same directory and committed together (git log), so Step 1 fresh + Step 2 no markers => current"
  },
  {
    "doc_path": "/home/coder/workspaces/IronClaude/.dev/worktrees/ccsession-proxy-stall/src/superclaude/skills/ccsession-tag/SKILL.md",
    "summary": "Weak hit: says the folder holds the gateway model shim (SKILL.md:10-11) and points to README.md (SKILL.md:25-26). No lifecycle content.",
    "currency_verdict": "current",
    "reason": "no header markers; same directory as the code, same commits"
  }
]
```
degraded: true (Grep/Read only)

Gaps no document covers (returned by the worker): whether the shim must survive its launching terminal / Orca tab closing (only implied by "keeps running until you stop it"); where the shim logs; any supervisor or restart for a dead shim.
